light_config_list = [
    # Garden area
    {
        'light_id': 1,
        'ldr_pin': 3,
        'output_pin': 11,
        'threshold': 10000,
    },

    # Tower A
    {
        'light_id': 2,
        'ldr_pin': 5,
        'output_pin': 13,
        'threshold': 12000,
    },

    # Tower B
    {
        'light_id': 3,
        'ldr_pin': 7,
        'output_pin': 15,
        'threshold': 20000,
    },
]

plant_config_list = [
    # {
    #     'plant_id': 1,
    #     'sms_pin': 33,
    #     'output_pin': 29,
    # },
    # {
    #     'plant_id': 2,
    #     'sms_pin': 35,
    #     'output_pin': 31,
    # },
]

gate_config_list = {
    # Pedestrian gate
    1: {
        'gate_id': 1,
        'servo_pin': 16,
        'green_led_pin': 32,
        'red_led_pin': 36,
        'angle1': 90,
        'angle2': 0,
    },
    # Vehicle gate
    2: {
        'gate_id': 2,
        'servo_pin': 18,
        'green_led_pin': 38,
        'red_led_pin': 40,
        'angle1': 0,
        'angle2': 90,
    }
}
