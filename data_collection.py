'''
Data collection and labeling for acoustic silentspeech
2/18/2022, Ruidong Zhang, rz379@cornell.edu
'''

import os
import re
from tkinter import Frame
import cv2
import math
import time
import random
import serial
import argparse
import numpy as np
from datetime import datetime

from commands import load_cmds, generate_connected_isolated_digits

def get_serial_port():
    all_dev = os.listdir('/dev')
    serial_ports = ['/dev/' + x for x in all_dev if x[:6] == 'cu.usb']
    if len(serial_ports) == 0:
        raise RuntimeError('No serial port found')
    selected = 0
    if len(serial_ports) > 1:
        print('Multiple serial ports found, choose which one to use (0-%d)' % (len(serial_ports) - 1))
        for n, p in enumerate(serial_ports):
            print('%d: /dev/%s' % (n, p))
        selected = int(input())
    return serial_ports[selected]

def data_record(path_prefix, output_path, cmd_set, duration, folds, n_reps_per_fold, noserial, count_down):
    if not os.path.exists(os.path.join(path_prefix, output_path)):
        print('Creating path', os.path.join(path_prefix, output_path))
        os.mkdir(os.path.join(path_prefix, output_path))
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    frame_size = (1280, 720)

    n_frames = 0
    # next_display = 5
    t0 = 0

    # cmds_1, imgs = load_cmds('music', folds, n_reps_per_fold)
    # cmds_t, imgs = load_cmds('int', folds, n_reps_per_fold)
    # cmds_2 = []
    # for cmd in cmds_t:
    #     cmds_2 += [(cmd[0] + 8, cmd[1], cmd[2])]
    # cmds = cmds_1 + cmds_2
    # cmds, imgs = generate_connected_isolated_digits()
    cmds, imgs, uses_vid, record_frame = load_cmds(cmd_set, folds, n_reps_per_fold)
    ts = []
    if record_frame:
        ts_with_frame = []
    rcds = []

    save_pos = datetime.now().strftime('record_%Y%m%d_%H%M%S_%f')
    vid = cv2.VideoWriter(os.path.join(path_prefix, output_path, save_pos + '.mp4'), cv2.VideoWriter_fourcc('a', 'v', 'c', '1'), 30, frame_size)

    if not noserial:
        serial_port = get_serial_port()
        ser = serial.Serial(serial_port, 115200)
        print('Listening on', serial_port)
        time.sleep(1)
        ser.write(b's')
        print('Start signal sent')
        ser.read(1)

    syncing_frame = 0
    syncing_ts = 0

    cmd_idx = 0
    last_cmd_display_time = 0

    frame = -1 # Records the current frame of the playing video
    try:
    # if True:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            if t0 == 0:
                t0 = time.time()
            n_frames += 1
            frame_ts = time.time()
            
            if not noserial and ser.inWaiting():
                in_bytes = ser.readline()
                if in_bytes == b'000\n':
                    syncing_frame = n_frames
                    syncing_ts = frame_ts
                    print('Received syncing signal, frame # %d, ts %.3f' % (syncing_frame, syncing_ts))
                    
            image = cv2.flip(image, 1)
            time_from_start = time.time() - t0
            info_text = 'Frame # %06d, ts: %.6f' % (n_frames, frame_ts)
            if time_from_start >= count_down:
                info_text += ', %s' % cmds[cmd_idx][1]
            cv2.putText(image, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
            vid.write(image)
            if time_from_start < count_down:
                cv2.putText(image, 'Please knock', (300, 380), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), thickness=3)
                cv2.putText(image, 'Session starting in %d s...' % math.ceil(count_down - time_from_start), (250, 480), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), thickness=2)
            else:
                if len(cmds[cmd_idx]) == 4:
                    duration = cmds[cmd_idx][3]
                image[:] = 255
                # cv2.putText(image, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
                estimated_time_left = 0
                for i in range(cmd_idx, len(cmds)):
                    if len(cmds[cmd_idx]) == 4:
                        estimated_time_left += cmds[i][3]
                    else:
                        estimated_time_left += duration
                progress_text = 'Session progress: %.1f%%, estimated time left: %d s' % (cmd_idx / len(cmds) * 100, estimated_time_left)
                cv2.putText(image, progress_text, (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)

                if time.time() - last_cmd_display_time > duration:
                    # display command
                    # print('Please touch area %s' % cmds[cmd_idx])
                    # cmd_idx += 1
                    if last_cmd_display_time > 0 and not bad_sample:
                        rcds += ['%s,%f,%f,%s\n' % (str(cmds[cmd_idx][0]), cmd_start_time, time.time(), cmds[cmd_idx][1])]
                        cmd_idx += 1
                    last_cmd_display_time = time.time()
                    cmd_start_time = time.time()
                    bad_sample = False
                    # image[-200:, -300:, 0:2] = 0 ## Bottom-right square to red
                    if cmds[cmd_idx][2] is not None and uses_vid:    # Initialize the video
                        inst_vid = imgs[cmds[cmd_idx][2]]
                        inst_vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        frame = -1      # Current frame is blank; so no video is playing
                elif last_cmd_display_time > 0:
                    cmd_progress = (time.time() - last_cmd_display_time) / duration
                    image[370:372, 0: round(cmd_progress * image.shape[1])] = 0
                    if cmds[cmd_idx][2] is not None:
                        if uses_vid:
                            inst_vid = imgs[cmds[cmd_idx][2]]
                            grabbed, img_cache = inst_vid.read()
                            frame += 1
                            if grabbed:
                                img = img_cache
                            image[-img.shape[0]:, -img.shape[1]:, :] = img
                        else:
                            inst_img = imgs[cmds[cmd_idx][2]]
                            image[-inst_img.shape[0]:, -inst_img.shape[1]:, :] = inst_img

                    text_progress = np.clip((cmd_progress - 0.2) / 0.2, 0, 1)
                    cv2.putText(image, '%s' % cmds[cmd_idx][1], (450, 345), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 0), thickness=2)
                    # Karaoke effect for words
                    (w, h), bs = cv2.getTextSize('%s' % cmds[cmd_idx][1], cv2.FONT_HERSHEY_SIMPLEX, 2.5, thickness=2)
                    word_img = np.ones((h+2*bs,w,3),np.uint8) * 255
                    cv2.putText(word_img, '%s' % cmds[cmd_idx][1], (0, h+bs), cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), thickness=2)
                    image[345-h-bs:345+bs, 450:450+round(w*text_progress), :] = word_img[:, :round(w*text_progress), :]
                        
            if record_frame:
                ts_with_frame += [np.array([frame_ts, getXpos(cmds[cmd_idx][1], frame), getYpos(cmds[cmd_idx][1], frame)])]
                # ts += ['%f,%f,%f\n' % (frame_ts, getXpos(cmds[cmd_idx][1], frame), getYpos(cmds[cmd_idx][1], frame))]
            # else:
            ts += ['%f\n' % frame_ts]
            if cmd_idx == len(cmds):
                break
            # if target_time > 0 and time_from_start > target_time:
            #     break
            # if time_from_start >= next_display:
            #     fps = n_frames / time_from_start
            #     # print('Time: %.1fs, frames: %d, fps: %.1f' % (time_from_start, n_frames, fps))
            #     next_display += 5

            # if n_frames % 30 == 0:
            cv2.imshow('Data Collection', image)
            pressed_key = cv2.waitKey(1) & 0xFF
            if pressed_key == 27:
                break
            if pressed_key == ord('x'):
                bad_sample = True
                last_cmd_display_time = time.time() - duration
                print('Bad:', frame_ts)
            if pressed_key == ord(' ') and time.time() - last_cmd_display_time > 0.6:
                last_cmd_display_time = min(last_cmd_display_time, time.time() - duration + 0.2)
    except:
        pass
    time.sleep(duration)
    if not noserial:
        ser.write(b'e')
    cap.release()
    vid.release()
    with open(os.path.join(path_prefix, output_path, save_pos + '_records.txt'), 'wt') as f:
        for r in rcds:
            f.write(r)
    with open(os.path.join(path_prefix, output_path, save_pos + '_frame_time.txt'), 'wt') as f:
        for t in ts:
            f.write(t)
    if record_frame:
        np.save(os.path.join(path_prefix, output_path, save_pos + '_tongue_continuous.npy'), ts_with_frame)
    with open(os.path.join(path_prefix, output_path, 'CIR_syncing_frame.txt'), 'wt') as f:
        f.write('1,%d,%d\n' % (syncing_frame, int(syncing_ts)))
    if not noserial:
        print(ser.readline().decode())
        if ser.inWaiting():
            print(ser.readline().decode())

def getXpos(cmd, frame):
    if cmd == 'left' or cmd == 'upleft':
        if frame < 15 or frame > 100:
            return 50
        elif frame < 45:
            return (45 - frame) * 50 / 30
        elif frame < 70:
            return 0
        else:
            return (frame - 70) * 50 / 30
    elif cmd == 'right' or cmd == 'upright':
        if frame < 15 or frame > 100:
            return 50
        elif frame < 45:
            return (frame - 15) * 50 / 30 + 50
        elif frame < 70:
            return 100
        else:
            return (100 - frame) * 50 / 30 + 50
    else:
        return 50

def getYpos(cmd, frame):
    if cmd == 'upleft' or cmd == 'upright' or cmd == 'up':
        if frame < 15 or frame > 100:
            return 0
        elif frame < 45:
            return (frame - 15) * 100 / 30
        elif frame < 70:
            return 100
        else:
            return (100 - frame) * 100 / 30
    else:
        return 0

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path-prefix', help='dataset parent folder', default='/Users/zrd/research_projects/echowrist/pilot_study')
    parser.add_argument('-o', '--output', help='output dir name')
    parser.add_argument('-c', '--commandsets', help='command set name, comma separated if multiple', default='15')
    parser.add_argument('-t', '--time', help='duration of each command/gesture', type=float, default=3)
    parser.add_argument('-f', '--folds', help='how many folds', type=int, default=1)
    parser.add_argument('-r', '--reps_per_fold', help='how many repetitiions per gesture for a fold', type=int, default=3)
    parser.add_argument('-cd', '--count_down', help='count down time (s) before start', type=int, default=3)
    parser.add_argument('--noserial', help='do not listen on serial', action='store_true')

    args = parser.parse_args()
    data_record(args.path_prefix, args.output, args.commandsets, args.time, args.folds, args.reps_per_fold, args.noserial, args.count_down)
