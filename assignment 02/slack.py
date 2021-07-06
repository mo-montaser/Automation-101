import requests


class SendMessage():
    def __init__(self, url, message):
        self.url = url
        self.message = message

    def send(self):
        data = {"text": self.message}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, json=data, headers=headers)
        if response.text == "ok":
            print('Password sent successfully')
