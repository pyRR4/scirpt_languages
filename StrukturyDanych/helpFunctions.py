def get_sorted_dates(logs_dict):
    dates = []
    for log in logs_dict:
        dates.append(log["date"])

    return sorted(dates)


def get_code_ratio(logs_dict, code):
    code_logs = 0
    for log in logs_dict:
        if log["code"] == code:
            code_logs += 1

    return code_logs


def domain_to_string(logs_dict, code):
    to_string_list = []
    for key, log in logs_dict.items():
        ip = "IP: " + str(key) + " || "
        num_of_requests = "Num of requests: " + str(len(log)) + " || "
        log_dates = get_sorted_dates(log)
        first_request = "First request: " + str(log_dates[0]) + " || "
        last_request = "Last request: " + str(log_dates[-1]) + " || "
        code_ratio = "Code " + str(code) + " ratio: " + str(get_code_ratio(log, code))
        to_string_list.append(ip + num_of_requests + first_request + last_request + code_ratio)

    return to_string_list

