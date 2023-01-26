from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

MQTTClient = AWSIoTMQTTClient("SmartSocietyRPI") # random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
MQTTClient.configureEndpoint("a3tsmej2y71ety-ats.iot.ap-south-1.amazonaws.com", 8883)
MQTTClient.configureCredentials("/home/pi/AWSIoTCore/root-ca.crt", "/home/pi/AWSIoTCore/private.key", "/home/pi/AWSIoTCore/certificate.pem")
MQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
MQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
MQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
MQTTClient.configureMQTTOperationTimeout(5) # 5 sec
