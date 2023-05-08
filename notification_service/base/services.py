import requests


def send_message_to_external_server(message_id: int, phone: int, text: str, token: str) -> requests.Response:
    """ Send message to external server
    :param message_id: message id
    :param phone: phone number
    :param text: message text
    :param token: JWT token
    :return: response from external server
    """
    headers = {'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json',
               'accept': 'application/json'}
    data = {
        "id": message_id,
        "phone": phone,
        "text": text
    }
    return requests.post(f'https://probe.fbrq.cloud/v1/send/{message_id}', json=data, headers=headers)
