light_config_list = [
    # {
    #     'light_id': 1,
    #     'ldr_pin': '',
    #     'output_pin': '',
    # },
    # {
    #     'light_id': 2,
    #     'ldr_pin': '',
    #     'output_pin': '',
    # },
]

plant_config_list = [
    # {
    #     'plant_id': 1,
    #     'sms_pin': 8,
    #     'output_pin': 10,
    # }
]

gate_config_list = {
    # Pedestrian gate
    1 : {
        'gate_id': 1,
        'servo_pin': 16,
        'green_led_pin': 35,
        'red_led_pin': 37,
        'angle1': 90,
        'angle2': 0,
    },
    # Vehicle gate
    # 2 : {
    #     'gate_id': 2,
    #     'servo_pin': 18,
    #     'green_led_pin': 36,
    #     'red_led_pin': 38,
    #     'angle1': 0,
    #     'angle2': 90,
    # }
}
