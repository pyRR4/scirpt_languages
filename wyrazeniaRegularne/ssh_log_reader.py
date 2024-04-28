import datetime
import logging
import re
import sys


def read_logs(logs_path, do_logging=True, logger_level=logging.DEBUG):
    logs_list = []

    with open(logs_path, 'r') as logs:
        logger = setup_logger(logger_level)
        for line in logs:
            log = match_log(line)
            if log is not None:
                logs_list.append(log)
                if do_logging:
                    message_logging(log['msg'], line, logger)

    return logs_list


def match_log(log):
    pattern = r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}) LabSZ sshd\[(\d+)\]: (.*)$'

    match = re.match(pattern, log)
    if not match:
        return None
    if not match.group(1):
        return None

    date = datetime.datetime.strptime(match.group(1), "%b %d %H:%M:%S")
    if date.month == 1:
        date = date.replace(year=2024)
    else:
        date = date.replace(year=2023)
    timestamp = date
    sshd = match.group(2)
    msg = match.group(3)

    log_to_dict = {
        'timestamp': timestamp,
        'sshd': sshd,
        'msg': msg
    }

    return log_to_dict


def message_logging(msg, line, msg_logger):
    msg_logger.debug(f"Przeczytano {len(line.encode())} bajtów")
    msg_type = get_message_type(msg)
    if msg_type == "connection closed" or msg_type == "successful login":
        msg_logger.info(msg_type)
    elif msg_type == "failed login":
        msg_logger.warning(msg_type)
    elif msg_type == "invalid user":
        msg_logger.error(msg_type)
    elif msg_type == 'break-in':
        msg_logger.critical(msg_type)


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.WARNING


def setup_logger(level):
    new_logger = logging.getLogger()
    new_logger.setLevel(level)

    error_stream_handler = logging.StreamHandler(sys.stderr)
    error_stream_handler.setLevel(logging.ERROR)

    info_stream_handler = logging.StreamHandler(sys.stdout)
    info_stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    error_stream_handler.setFormatter(formatter)
    info_stream_handler.setFormatter(formatter)

    info_stream_handler.addFilter(InfoFilter())

    new_logger.addHandler(error_stream_handler)
    new_logger.addHandler(info_stream_handler)

    return new_logger


def get_ipv4s_from_log(log):
    match = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', log["msg"])
    if not match:
        return None
    return match


def get_ip_set(logs):
    ips = set()
    for log in logs:
        ip = get_ipv4s_from_log(log)
        if ip:
            for el in ip:
                ips.add(el)
    return ips


def get_user_from_log(log):
    match = (re
             .search(r'(?:user\s|for invalid user\s|for user\s|for\s| user=)(?!request|\d{1,3}|invalid user)(\w+)',
                     log['msg']))
    if not match or log['msg'] == 'pam_unix(sshd:auth): check pass; user unknown':
        return None
    return match.group(1)


def get_user_set(logs):
    users = set()
    for log in logs:
        user = get_user_from_log(log)
        if user:
            users.add(user)
    return users


def get_message_type(log):
    if re.search("Failed password", log):
        return "failed login"
    elif re.search("Accepted password", log):
        return "successful login"
    elif re.search("Connection closed", log):
        return "connection closed"
    elif re.search("Invalid user", log):
        return "invalid user"
    elif re.search("POSSIBLE BREAK-IN ATTEMPT", log):
        return "break-in"
    elif re.search("session closed for", log):
        return "session closed"
    elif re.search("session opened for", log):
        return "session opened"
    else:
        return "different"


def get_messages(logs):
    messages = []
    for log in logs:
        msg_type = get_message_type(log['msg'])
        messages.append({msg_type: log['msg']})
    return messages
