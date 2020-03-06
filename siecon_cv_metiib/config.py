# Frame that encloses the product
demo_crop = {
    'START': (460, 680),
    'FINISH': (3400, 2100),
}

demo_pin_mask = {
    'top_right_soc': {
        # Rectangle that encloses pin R2
        'pin_0': {
            'START': (1180, 1040),
            'FINISH': (1220, 1100),
        },

        # Rectangle that encloses pin R1
        'pin_1': {
            'START': (1180, 1300),
            'FINISH': (1220, 1360),
        },
    },

    'top_left_soc': {
        # Rectangle that encloses pin L1
        'pin_2': {
            'START': (220, 980),
            'FINISH': (270, 1030),
        },
        # Rectangle that encloses pin L2N
        'pin_3': {
            'START': (220, 1120),
            'FINISH': (270, 1160),
        },
        # Rectangle that encloses pin L3
        'pin_4': {
            'START': (220, 1250),
            'FINISH': (270, 1300),
        },
        # Rectangle that encloses pin GROUND
        'pin_5': {
            'START': (210, 1520),
            'FINISH': (260, 1570),
        },
    }
}

# Rectangle that encloses the calibration reference corners
demo_calibration_rect = {
    'X_RANGE_LEFT': (400, 430),
    'X_RANGE_RIGHT': (1010, 1040),
    'Y_RANGE_TOP': (350, 380),
    'Y_RANGE_BOT': (610, 640),
}

demo_scale_const = {
    'col': 33,
    'row': 14,
}

demo_soc = 'top_left_soc'

demo_pins = ['pin_2', 'pin_3', 'pin_4', 'pin_5']
