import requests
import threading
import time


def send_notification(payload, recipients):
    for recipient in recipients:
        message = payload
        message["to"] = recipient.expo_token
        requests.post('https://exp.host/--/api/v2/push/send', json = message)


def send(payload, recipients):
    notification_thread = threading.Thread(target=send_notification, args=(payload, recipients))
    notification_thread.start()
    time.sleep(1)

def send_fingerprint_status(status, recipients):
    payload = {
        'title': 'Smart Society',
        'body': 'Fingerprint registration status updated',
        'data': {
            'notification_type': 'update_status',
            'payload': {
                'type': "fingerprint",
                'status': status,
            }
        }
    }
    notification_thread = threading.Thread(target=send_notification, args=(payload, recipients))
    notification_thread.start()
    time.sleep(1)