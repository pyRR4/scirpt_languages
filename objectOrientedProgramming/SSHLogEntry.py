import datetime
import ipaddress
import re


class SSHLogEntry:
    def __init__(self, log):
        pattern = r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}) (LabSZ) sshd\[(\d+)\]: (.*)$'

        match = re.match(pattern, log)
        if match:
            date = datetime.datetime.strptime(match.group(1), "%b %d %H:%M:%S")
            if date.month == 1:
                date.replace(year=2024)
            else:
                date = date.replace(year=2023)
            timestamp = date
            hostname = match.group(2)
            sshd = match.group(3)
            msg = match.group(4)

            self.date = date
            self.msg = msg
            self.pid_number = sshd
            self.hostname = hostname

    def __str__(self):
        return (f'Data: {self.date} | Numer PID: {self.pid_number} | Wiadomość: {self.msg} '
                f'| Nazwa hosta: {self.hostname}')

    def get_ipv4s(self):
        return ipaddress.IPv4Address(str(get_ipv4s_from_log(self.msg).group(1)))


def get_ipv4s_from_log(log):
    match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', log)
    if not match:
        return None
    return match


if __name__ == '__main__':
    date = datetime.datetime.strptime('1920 Jan 12 15:15:15', "%Y %b %d %H:%M:%S")
    log_instance = SSHLogEntry("Dec 10 23:04:09 LabSZ sshd[20032]: "
                               "Failed password for root from 123.235.32.19 port 33548 ssh2")
    print(log_instance)
    print(log_instance.get_ipv4s())

