'''
Command sets
2/18/2021, Ruidong Zhang, rz379@cornell.edu
'''

import cv2
import math
import random
import numpy as np

cmd_digits = {
    'cmds': [
        'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
    ],
    'instruction_imgs': ['asl0.png', 'asl1.png', 'asl2.png', 'asl3.png', 'asl4.png', 'asl5.png', 'asl6.png', 'asl7.png', 'asl8.png', 'asl9.png'],
    'use_vid': False
}


cmd_touch = {
    'cmds': [
        '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_5fingers = {
    'cmds': [
        'No', '1', '2', '3', '4', '5',
    ],
    'instruction_imgs': [
        'ft0.png', 'ft1.png', 'ft2.png', 'ft3.png', 'ft4.png', 'ft5.png'
    ],
    'use_vid': False
}

cmd_ftfingers = {
    'cmds': [
        'No', '1', '2', '3', '4', '5',
        '12', '23', '34', '45',
        '123', '234', '345',
        '1234', '2345', '12345',
    ],
    'instruction_imgs': [
        'ft0.png', 'ft1.png', 'ft2.png', 'ft3.png', 'ft4.png', 'ft5.png',
        'ft12.png', 'ft23.png', 'ft34.png', 'ft45.png',
        'ft123.png', 'ft234.png', 'ft345.png',
        'ft1234.png', 'ft2345.png', 'ft12345.png',
    ],
    'use_vid': False
}

cmd_asldigits = {
    'cmds': [
        'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
    ],
    'instruction_imgs': [
        'asl0.png', 'asl1.png', 'asl2.png', 'asl3.png', 'asl4.png', 'asl5.png', 'asl6.png', 'asl7.png', 'asl8.png', 'asl9.png',
    ],
    'use_vid': False
}

cmd_43 = {
    'cmds': [
        'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
        'Weather', 'News', 'Alarm', 'Time', 'Traffic', 'Camera',
        'Previous', 'Next', 'Pause', 'Resume', 'Stop', 'Volume', 'Up', 'Down',
        'Message', 'Send', 'Hang up',
        'Answer', 'Call', 'Check', 'Copy', 'Cut', 'Help', 'Home', 'Mute',
        'Paste', 'Play', 'Redial', 'Screenshot', 'Search', 'Skip', 'Skype', 'Undo',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_music = {
    'cmds': [
        'Previous', 'Next', 'Pause', 'Resume', 'Stop', 'Volume up', 'Volume down', 'Play',
        # 'What\'s the weather', 'Latest news', 'Set an alarm', 'What time is it', 'How\'s the traffic', 'Open camera', 'Hang up',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_int = {
    'cmds': [
        'What\'s the weather', 'Latest news', 'Set an alarm', 'What time is it', 'How\'s the traffic', 'Open camera', 'Hang up',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_speechin = {
    'cmds': [
        'Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
        'Answer', 'Call', 'Camera', 'Check', 'Copy', 'Cut', 'Hang up', 'Help', 'Home', 'Mute',
        'Paste', 'Pause', 'Play', 'Previous', 'Redial', 'Screenshot', 'Search', 'Skip', 'Skype', 'Undo',
        'Volume', 'Share', 'Next', 'Open', 'Close', 'Keyboard',
        'OK Google', 'Hey Siri', 'Alexa',
        'Question mark', 'Exclamation point', 'Comma', 'Dot', 'Semicolon', 'Colon', 'Quotation mark',
        'Parentheses', 'Dash', 'Slash', 'Underscore',
        'Left', 'Right', 'Up', 'Down',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# b d g word initial with a i u
cmd_bdg_wi = {
    'cmds': [
        'ba', 'da', 'ga', 'bi', 'di', 'gi', 'bu', 'du', 'gu',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# b d g word final with a i u
cmd_bdg_wf = {
    'cmds': [
        'ab', 'ad', 'ag', 'ib', 'id', 'ig', 'ub', 'ud', 'ug',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# b d g intervocalic with a i u
cmd_bdg_iv = {
    'cmds': [
        'aba', 'ada', 'aga', 'ibi', 'idi', 'igi', 'ubu', 'udu', 'ugu',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# b d g intervocalic with a i u
cmd_mnng_iv = {
    'cmds': [
        'ama', 'ana', 'anga', 'imi', 'ini', 'ingi', 'umu', 'unu', 'ungu',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# speechin phonemes
cmd_speechin_phonemes = {
    'cmds': [
        'p', 'b', 'm', 'f', 'v', 'w', 'r', 'sh', 'th', 't', 'd', 's', 'z', 'n', 'l', 
        'k', 'g', 'y', 'i', 'u', 'ei', 'oh',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# seven alveolar tongue gestures
cmd_tongue_alveolar = {
    'cmds': [
        'l', 'll', 'l-hold', 'l-left', 'l-right', 'l-forward', 'l-backwards',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# four tongue touch point gestures (alveolar, palate, right top molar, left top molar)
# followed by same three gestures for bottom teeth
cmd_tongue6 = {
    'cmds': [
        '^>', '<^', '^', '_>', '<_', '_',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# 1) top left to top center, 2) top right to top center, 3) top center to top left 
# 4) top center to top right, 5) bottom left to bottom center, 6) bottom right to bottom center,
# 7) bottom center to bottom left, 8) bottom center to bottom right
cmd_tongue_swipe8 = {
    'cmds': [
        'up |--.->|', 'up |<-.--|', 'up |->.--|', 'up |--.<-|',
        'down |--.->|', 'down |<-.--|', 'down |->.--|', 'down |--.<-|',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# swipe left alveolar (however feels natural), swipe right alveolar, swipe back alveolar,
# swipe forward alveolar, tap alveolar, double tap alveolar
cmd_tongue_alveo6 = {
    'cmds': [
        'swipe left', 'swipe right', 'swipe back', 'swipe forward', 'tap', 'double tap',
    ],
    'instruction_imgs': ['t6left.mp4', 't6right.mp4', 't6back.mp4', 't6forward.mp4', 't6l.mp4', 't6ll.mp4'],
    'use_vid': True
}

# Continuous tongue tracking
cmd_tongue_cont6 = {
    'cmds': [
        'left', 'right', 'up', 'upleft', 'upright', 'upback',
    ],
    'instruction_imgs': ['c-left.mp4', 'c-right.mp4', 'c-up.mp4', 'c-upleft.mp4', 'c-upright.mp4', 'c-upback.mp4'],
    'use_vid': True
}

cmd_words1 = {
    'cmds': [
        'measure', 'watch', 'think tank', 'judicial', 'bazooka', 'how','sniff','offset','hole',
        'throughout',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_words2 = {
    'cmds': [
        'echo', 'Newfoundland', 'sing', 'lake', 'amazing', 'alligator','bedding','homemade',
        'afternoon','Manitoba','shy',
    ],
    'instruction_imgs': [],
    'use_vid': False
}


# similar to AVletters databse
cmd_alphabet = {
        'cmds': [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_tongueinput_positions = {
            'cmds': [
        'up-left', 'up-right', 'up', 'back',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_fourcorners = {
    'cmds': [
        'bottom-left', 'bottom-right', 'top-left', 'top-right',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# FOR USER STUDY
cmd_words21 = {
        'cmds': [
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'oh',
        'add', 'subtract', 'multiply', 'divide', 'percent', 'AM', 'PM', 'hours', 'minutes', 'seconds',
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_hidden = {
    'cmds': [
        'kings', 'steak', 'lane', 'nothing', 'think', 'tin', 'young', 'hint', 'healing', 'kit'
    ],
    'instruction_imgs': [],
    'use_vid': False
}

# FOR USER STUDY
cmd_consonants = {
    'cmds': [
        'awa', 'ara', 'asha','apa','ama','afa', 'ata', 'atha', 'asa', 'ana', 'ala',
        'aka', 'anga', 'aya', 'aha', 'a-a', 
    ],
    'instruction_imgs': [],
    'use_vid': False
}

cmd_vowels = {
    'cmds': [
        'beat', 'bit', 'bait', 'boat', 'bet', 'bat', 'bought', 'boot', 'but', 'bite', 
        'bout', 'put'
    ],
    'instruction_imgs': [],
    'use_vid': False
}



def generate_discrete(cmds, folds, reps_per_fold):

    original_cmd_list = []
    img_list = {}
    for i, cmd in enumerate(cmds['cmds']):
        if len(cmds['instruction_imgs']) == 0:
            original_cmd_list += [(i, cmd, None)]
        elif cmds['use_vid']:             # Uses videos instead of images
            original_cmd_list += [(i, cmd, cmds['instruction_imgs'][i])]
            img_list[cmds['instruction_imgs'][i]] = cv2.VideoCapture('img/%s' % cmds['instruction_imgs'][i])
        else:
            original_cmd_list += [(i, cmd, cmds['instruction_imgs'][i])]
            img_list[cmds['instruction_imgs'][i]] = cv2.resize(cv2.imread('img/%s' % cmds['instruction_imgs'][i]), (331, 400))

    cmd_list = []
    cmds_repped = original_cmd_list * reps_per_fold
    for _ in range(folds):
        random.shuffle(cmds_repped)
        cmd_list += cmds_repped

    return cmd_list, img_list, cmds['use_vid'], cmds == cmd_tongue_cont6

def generate_connected_digits(folds, reps_per_fold, len_range=(3, 6)):
    # base_cmds = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    base_cmds = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']

    cmd_list = []
    img_list = {}

    for _ in range(folds):
        len_seq = list(range(len_range[0], len_range[1] + 1))
        len_seq *= math.ceil(reps_per_fold / len(len_seq))
        random.shuffle(len_seq)
        len_seq = len_seq[:reps_per_fold]

        fold_digits_seq = list(range(len(base_cmds))) * math.ceil(np.sum(len_seq) / len(base_cmds))
        random.shuffle(fold_digits_seq)

        digit_pos = 0
        for l in len_seq:
            this_cmd_index = fold_digits_seq[digit_pos: digit_pos + l]
            this_cmd_label = ' '.join([str(x) for x in this_cmd_index])
            this_cmd_text = ' '.join([base_cmds[x] for x in this_cmd_index])
            cmd_list += [(this_cmd_label, this_cmd_text, None)]
            digit_pos += l
    return cmd_list, img_list

def generate_connected_isolated_digits(n_connected_digits=60, n_isolated_digits=81, t_cd=4, t_id=2):
    cds, _ = generate_connected_digits(1, n_connected_digits)
    ids = []
    # ids, _ = generate_discrete(cmd_27, 1, n_isolated_digits // 27)

    c_i_ds = [(x[0], x[1], x[2], t_cd) for x in cds] + [(x[0], x[1], x[2], t_id) for x in ids]
    # random.shuffle(c_i_ds)

    return c_i_ds, {}

# def generate_grid(folds, reps_per_fold):
#     base_words = [
#         ['Bin', 'Lay', 'Place', 'Set'],
#         ['blue', 'green', 'red', 'white'],
#         ['at', 'by', 'in', 'with'],
#         ['A', 'B', 'C', 'D'],
#         ['1', '2', '3', '4'],
#         ['again', 'now', 'please', 'soon']
#     ]

#     n_groups = len(base_words)

#     assert(reps_per_fold % 4 == 0)  # saves the trouble :)
#     reps_each_word = reps_per_fold // 4
#     base_words_labels = list(range(sum([len(x) for x in base_words])))

#     generated_rand_groups = [[] for _ in range(n_groups)]

#     for i in range(n_groups):
        

def load_cmds(cmd_set, folds, reps_per_fold):

    original_cmd_list = []
    img_list = {}
    cs = cmd_set.lower().replace('_', '')
    if cs == 'digits':
        cmds = cmd_digits
    elif cs == 'speechin':
        cmds = cmd_speechin
    elif cs == 'speechin-phonemes':
        cmds = cmd_speechin_phonemes
    elif cs == 'tongue-alveolar':
        cmds = cmd_tongue_alveolar
    elif cs == 'tongue6':
        cmds = cmd_tongue6
    elif cs == 'tongue-swipe8':
        cmds = cmd_tongue_swipe8
    elif cs == 'tongue-cont6':
        cmds = cmd_tongue_cont6
    elif cs == 'tongue-alveo6':
        cmds = cmd_tongue_alveo6
    elif cs == 'consonants':
        cmds = cmd_consonants
    elif cs == 'vowels':
        cmds = cmd_vowels
    elif cs == 'words1':
        cmds = cmd_words1
    elif cs == 'words2':
        cmds = cmd_words2
    elif cs == 'alphabet':
        cmds = cmd_alphabet
    elif cs == 'tongueinput-positions':
        cmds = cmd_tongueinput_positions
    elif cs == 'fourcorners':
        cmds = cmd_fourcorners
    elif cs == 'words21':
        cmds = cmd_words21
    elif cs == 'hidden':
        cmds = cmd_hidden
    elif cs == 'bdg-wi':
        cmds = cmd_bdg_wi
    elif cs == 'bdg-wf':
        cmds = cmd_bdg_wf
    elif cs == 'bdg-iv':
        cmds = cmd_bdg_iv
    elif cs == 'mnng-iv':
        cmds = cmd_mnng_iv
    elif cs == '43':
        cmds = cmd_43
    # elif cs == '15':
    #     cmds = cmd_15
    elif cs == 'music':
        cmds = cmd_music
    elif cs == 'int':
        cmds = cmd_int
    elif cs == 'touch':
        cmds = cmd_touch
    elif cs == '5fingers':
        cmds = cmd_5fingers
    elif cs == 'ftfingers':
        cmds = cmd_ftfingers
    elif cs == 'asldigits':
        cmds = cmd_asldigits
    elif cs not in ['connecteddigits', 'grid']:
        raise ValueError('Command set with name %s not found' % cmd_set)
    
    if cs == 'connecteddigits':
        return generate_connected_digits(folds, reps_per_fold, len_range=(3, 6)), False
    else:
        return generate_discrete(cmds, folds, reps_per_fold)
