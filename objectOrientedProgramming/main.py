from objectOrientedProgramming.SSHLogEntry import SSHLogEntry
from objectOrientedProgramming.SSHLogJournal import SSHLogJournal
from objectOrientedProgramming.SSHUser import SSHUser
from wyrazeniaRegularne.ssh_log_reader import read_logs
from wyrazeniaRegularne.features import get_user_logs

if __name__ == '__main__':
    logs = read_logs("C:/Users/igopo/OneDrive/Pulpit/Wszystko i nic/IST 22-27/IV sem/JS/Labs/scirpt_languages/"
                     "wyrazeniaRegularne/SSH.log", False)
    users = get_user_logs(logs)
    validate_list = []
    for key, val in users.items():
        sorted_val = sorted(val, key=lambda x: x['timestamp'], reverse=True)
        val = sorted_val
        ssh_user = SSHUser(key, val[0])
        validate_list.append(ssh_user)

    journal = SSHLogJournal()

    with open("C:/Users/igopo/OneDrive/Pulpit/Wszystko i nic/IST 22-27/IV sem/JS/Labs/scirpt_languages/"
              "wyrazeniaRegularne/SSH.log", 'r') as lines:
        for line in lines:
            journal.append(line)

    validate_list += journal[5:15:2]

    for el in validate_list:
        if el.validate():
            print("git")
        else:
            print("nie git")
