import re


class SSHUser:
    def __init__(self, username, date):
        self.user_name = username
        self.date = date

    def __str__(self):
        return self.user_name

    def validate(self):
        if re.fullmatch(r'^[a-z_][a-z0-9_-]{0,31}$', self.user_name):
            return True
        return False

