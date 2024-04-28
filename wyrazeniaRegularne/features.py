import datetime
import math
import random

from wyrazeniaRegularne import ssh_log_reader


def get_user_logs(logs):
    users = dict()

    for log in logs:
        user = ssh_log_reader.get_user_from_log(log)
        if user:
            if user in users.keys():
                users[user].append(log)
            else:
                users[user] = [log]

    return users


def random_entries(logs, n):
    users = get_user_logs(logs)
    if not users:
        return []

    random_user = random.choice(list(users))
    random_user_entries = users[random_user]
    if n > len(random_user_entries):
        final_random_entries = random.sample(random_user_entries, len(random_user_entries))
    else:
        final_random_entries = random.sample(random_user_entries, n)

    return final_random_entries


def calc_time(arg_logs, is_global=False):
    users = get_user_logs(arg_logs)
    global_sum = 0.0
    global_squares_sum = 0.0
    global_count = 0
    users_times = {}
    for user, logs in users.items():
        user_sum = 0.0
        user_count = 0
        user_times = []
        started_sessions = []
        last_date = datetime.timedelta()
        sorted_logs = sorted(logs, key=lambda x: x['timestamp'])
        for log in sorted_logs:
            last_date = log['timestamp']
            msg_type = ssh_log_reader.get_message_type(log['msg'])
            if msg_type == 'session opened':
                started_sessions.append([log['sshd'], log['timestamp']])
            if msg_type == 'session closed':
                for session in started_sessions:
                    if log['sshd'] == session[0]:
                        user_count += 1
                        time_diff = (log['timestamp'] - session[1]).total_seconds()
                        user_times.append(time_diff)
                        user_sum += time_diff
                        started_sessions.remove(session)

        while len(started_sessions) != 0: #niezakonczone sesje
            user_count += 1
            time_diff = (last_date - started_sessions[0][1]).total_seconds()
            user_times.append(time_diff)
            user_sum += time_diff
            started_sessions.remove(started_sessions[0])

        if user_count > 0:
            user_average = user_sum / user_count
            user_squares_sum = sum((x - user_average) ** 2 for x in user_times)
            user_deviation = round(math.sqrt(user_squares_sum / user_count), 3)
            users_times[user] = [round(user_average, 3), user_deviation]
            global_sum += user_sum
            global_squares_sum += user_squares_sum
            global_count += user_count

    global_average = round(global_sum / global_count, 3)
    global_deviation = round(math.sqrt(global_squares_sum / global_count), 3)

    if is_global:
        return {'.GLOBAL': [global_average, global_deviation]}

    return users_times


def count_logins(arg_logs):
    users = get_user_logs(arg_logs)
    most_logged_val = 0
    most_logged_user = None
    least_logged_val = None
    least_logged_user = None
    for user, logs in users.items():
        user_log_val = 0
        for log in logs:
            msg_type = ssh_log_reader.get_message_type(log['msg'])
            if msg_type == "failed login" or msg_type == "successful login":
                user_log_val += 1

        if user_log_val > most_logged_val:
            most_logged_user = user
            most_logged_val = user_log_val
        if least_logged_val is None or least_logged_val > user_log_val:
            least_logged_val = user_log_val
            least_logged_user = user

    return {most_logged_user: f" logged {most_logged_val} times", least_logged_user: f" logged {least_logged_val} times"}

