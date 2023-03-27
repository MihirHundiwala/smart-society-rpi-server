def iot_publish(MQTTClient, topic, payload):
    try:
        MQTTClient.publish(topic = topic, QoS=1, payload=payload)
    except:
        MQTTClient.disconnect()
        MQTTClient.connect()
        MQTTClient.publish(topic = topic, QoS=1, payload=payload)
    return