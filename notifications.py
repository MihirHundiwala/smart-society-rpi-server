import requests
import threading
import time


def send_notification(payload, recipients):
    print(payload, recipients)
    for recipient in recipients:
        message = payload
        message["to"] = recipient
        requests.post('https://exp.host/--/api/v2/push/send', json = message)


def send_fingerprint_status(status, recipients):
    payload = {
        'title': 'Smart Society',
        'body': 'Fingerprint registration status updated',
        'data': {
            'notification_type': 'update_status',
            'payload': {
                'type': "update_fingerprint_status",
                'data': status,
            }
        }
    }
    send_notification(payload, recipients)


def send_gate_open_notification(data, recipients):
    print("Here 1")
    payload = {
        'title': 'Smart Society',
        'body': 'Gate was opened',
        'data': {
            'notification_type': 'update_status',
            'payload': {
                'type': 'update_gate_entry',
                'data': data,
            },
        }
    }
    send_notification(payload, recipients)
