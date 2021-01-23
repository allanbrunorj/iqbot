from iqoptionapi.stable_api import IQ_Option

class IQUser:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.API = IQ_Option(self.email, self.password)
        self.API.connect()
        self.login_success = self.API.check_connect()

        # API.change_balance('PRACTICE') # PRACTICE / REAL

    def close(self):
        self.API.close_connection()



