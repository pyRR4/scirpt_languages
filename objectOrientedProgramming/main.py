import datetime
import ipaddress

from objectOrientedProgramming.SSHLogEntry import SSHLogEntry, OtherEntry, IncorrectPasswordEntry, CorrectPasswordEntry, ErrorEntry
from objectOrientedProgramming.SSHLogJournal import SSHLogJournal
from objectOrientedProgramming.SSHUser import SSHUser
from wyrazeniaRegularne.ssh_log_reader import read_logs
from wyrazeniaRegularne.features import get_user_logs


if __name__ == '__main__':

    #ssh_user
    logs = read_logs("C:/Users/igopo/OneDrive/Pulpit/Wszystko i nic/IST 22-27/IV sem/JS/Labs/scirpt_languages/"
                     "wyrazeniaRegularne/SSH.log", False)
    users = get_user_logs(logs)
    validate_list = []
    for key, val in users.items():
        sorted_val = sorted(val, key=lambda x: x['timestamp'], reverse=True)
        val = sorted_val
        ssh_user = SSHUser(key, val[0])
        validate_list.append(ssh_user)

    #journal creating
    journal = SSHLogJournal()

    with open("C:/Users/igopo/OneDrive/Pulpit/Wszystko i nic/IST 22-27/IV sem/JS/Labs/scirpt_languages/"
              "wyrazeniaRegularne/SSH.log", 'r') as lines:
        for line in lines:
            journal.append(line) #journal append

    print("\n\n=================Długość dziennika:===================")
    print(len(journal)) #__len__

    print("\n\n=================Adresy IP wypisywane iteratorem, przy użyciu has_ip:===================")
    iterator = iter(journal)
    for element in iterator:
        if element.has_ip:
            print(element.get_ipv4s())

    #print("\n\n=================__contains__:===================")
    #print(journal.__contains__("jakis log"))
    #log_msg = "Dec 10 17:00:39 LabSZ sshd[17923]: Received disconnect from 183.62.140.253: 11: Bye Bye [preauth]\n"
    #existing_log = SSHLogEntry.get_log_type(log_msg)(log_msg)
    #print(journal.__contains__(existing_log)) #contains

    print("\n\n=================Kacze typowanie, przy pomocy slicingu:===================")
    helper_list = validate_list[:10] + journal[5:15:2]

    for el in helper_list: #duck_typing
        if el.validate():
            print(f"{el} validated correctly")
        else:
            print(f"{el} validated incorrectly") #FILTER username is incorrect

    print("\n\n=================__getattr__ - IP:===================")
    ip_journal = journal.__getattr__(ipaddress.IPv4Address("183.62.140.253"))
    for elem in ip_journal[:10]:
        print(elem)

    print("\n\n=================__getattr__ - date:===================")
    date_test = datetime.datetime.strptime("Dec 10 17:00:39", "%b %d %H:%M:%S")
    date_test = date_test.replace(year=2023)
    date_journal = journal.__getattr__(date_test)
    for elem in date_journal[:10]:
        print(elem)

    print("\n\n=================__getattr__ - index:===================")
    print(journal.__getattr__(2))

    # print("\n\n=================__repr__ - IP:===================")
    # for elem in journal[:10]:
    #     print(elem.__repr__)
    #
    # print("\n\n=================__lt__/__gt__ - IP:===================")
    # jrn0 = journal[0]
    # jrn1 = journal[1]
    # print(f"journal[0] - {jrn0}")
    # print(f"journal[1] - {jrn1}")
    # if jrn0.__lt__(jrn1):
    #     print("journal[0] < journal[1]")
    # elif jrn1.__lt__(jrn0):
    #     print("journal[1] < journal[0]")
    # else:
    #     print("journal[1] == journal[0]")
    #
    # if jrn0.__gt__(jrn1):
    #     print("journal[1] < journal[0]")
    # elif jrn1.__gt__(jrn0):
    #     print("journal[0] < journal[1]")
    # else:
    #     print("journal[1] == journal[0]")
