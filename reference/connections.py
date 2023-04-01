from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

MQTTClient = AWSIoTMQTTClient("SmartSocietyRPI") # random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
MQTTClient.configureEndpoint("a3tsmej2y71ety-ats.iot.ap-south-1.amazonaws.com", 8883)
MQTTClient.configureCredentials("./certs/root-ca.crt", "./certs/private.key", "./certs/certificate.pem")
MQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
MQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
MQTTClient.configureConnectDisconnectTimeout(20) # 10 sec
MQTTClient.configureMQTTOperationTimeout(5) # 5 sec
