# coding=utf-8


class ExxAPIException(Exception):
    """Exception class to handle general API Exceptions

        `code` values

        `message` format

    """
    def __init__(self, response):
        self.code = ''
        self.message = 'Unknown Error'
        try:
            json_res = response.json()
        except ValueError:
            self.message = response.content
        else:
            if 'error' in json_res:
                self.message = json_res['error']
            if 'code' in json_res:
                self.code = ' {}'.format(json_res['code'])
                self.message = json_res['message']

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return 'ExxAPIException{}: {}'.format(self.code, self.message)


class ExxRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'ExxRequestException: {}'.format(self.message)
