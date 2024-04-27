import datetime
import ipaddress
import re
import abc


class ValueNotFound(Exception):
    pass


class SSHLogEntry(metaclass=abc.ABCMeta):
    def __init__(self, log):
        pattern = r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}) (LabSZ) sshd\[(\d+)\]: (.*)$'

        match = re.match(pattern, log)
        if match:
            date = datetime.datetime.strptime(match.group(1), "%b %d %H:%M:%S")
            if date.month == 1:
                date.replace(year=2024)
            else:
                date = date.replace(year=2023)
            hostname = match.group(2)
            sshd = match.group(3)
            msg = match.group(4)

            self.date = date
            self.msg = msg
            self.pid_number = sshd
            self.hostname = hostname
            self._raw_log = log
        else:
            raise ValueError

    def __str__(self):
        return (f'Data: {self.date} | Numer PID: {self.pid_number} | Wiadomość: {self.msg} '
                f'| Nazwa hosta: {self.hostname}')

    def __repr__(self):
        return (f"{type(self).__name__}(date={self.date}, msg='{self.msg}', "
                f"pid_number={self.pid_number}, hostname='{self.hostname}', "
                f"has_ip='{self.has_ip}', )")

    def __eq__(self, other):
        if isinstance(other, SSHLogEntry):
            return self._raw_log == other.get_raw_log()
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, SSHLogEntry):
            return self.date < other.date
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, SSHLogEntry):
            return self.date > other.date
        return NotImplemented

    @property
    def has_ip(self):
        try:
            self.get_ipv4s()
        except ValueNotFound:
            return False
        return True

    @abc.abstractmethod
    def validate(self):
        pass

    def get_ipv4s(self):
        ipv4 = self.get_ipv4s_from_log(self.msg)
        if ipv4 is not None:
            return ipaddress.IPv4Address(str(ipv4.group(1)))
        else:
            raise ValueNotFound

    def get_raw_log(self):
        return self._raw_log

    @classmethod
    def get_log_type(cls, msg):
        if re.search("Failed password", msg):
            return IncorrectPasswordEntry
        elif re.search("Accepted password", msg):
            return CorrectPasswordEntry
        elif re.search("error", msg):
            return ErrorEntry
        else:
            return OtherEntry

    @classmethod
    def get_ipv4s_from_log(cls, log):
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', log)
        if not match:
            return None
        return match

    @classmethod
    def get_message_type(cls, msg):
        if re.search("Failed password", msg):
            return "failed login"
        elif re.search("Accepted password", msg):
            return "successful login"
        elif re.search("error", msg):
            return "error"
        else:
            return "different"


class IncorrectPasswordEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)

    def validate(self):
        return super().get_message_type(self.msg) == "failed login"


class CorrectPasswordEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)

    def validate(self):
        return super().get_message_type(self.msg) == "successful login"


class ErrorEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)

    def validate(self):
        return super().get_message_type(self.msg) == "error"


class OtherEntry(SSHLogEntry):
    def __init__(self, log):
        super().__init__(log)

    def validate(self):
        return True


if __name__ == '__main__':
    log_instance = SSHLogEntry("Dec 10 23:04:09 LabSZ sshd[20032]: "
                               "Failed password for root from 123.235.32.19 port 33548 ssh2")
    print(log_instance)
    print(log_instance.get_ipv4s())
