# Frame that encloses the product
demo_crop = {
    'start': (460, 680),
    'finish': (3400, 2100),
}

demo_pin_mask = {
    'top_right_soc': {
        # Rectangle that encloses pin R2
        'pin_0': {
            'start': (1180, 1040),
            'finish': (1220, 1100),
        },

        # Rectangle that encloses pin R1
        'pin_1': {
            'start': (1180, 1300),
            'finish': (1220, 1360),
        },
    },

    'top_left_soc': {
        # Rectangle that encloses pin L1
        'pin_2': {
            'start': (220, 980),
            'finish': (270, 1030),
        },
        # Rectangle that encloses pin L2N
        'pin_3': {
            'start': (220, 1120),
            'finish': (270, 1160),
        },
        # Rectangle that encloses pin L3
        'pin_4': {
            'start': (220, 1250),
            'finish': (270, 1300),
        },
        # Rectangle that encloses pin GROUND
        'pin_5': {
            'start': (210, 1520),
            'finish': (260, 1570),
        },
    }
}

# Rectangle that encloses the calibration reference corners
demo_calibration_rect = {
    'x_range_left': (400, 430),
    'x_range_right': (1010, 1040),
    'y_range_top': (350, 380),
    'y_range_bot': (610, 640),
}

demo_scale_const = {
    'col': 33,
    'row': 14,
}
