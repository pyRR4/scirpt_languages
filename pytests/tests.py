from ipaddress import IPv4Address, AddressValueError

import pytest

from pytests.TypedEntry import SSHLogEntry, ValueNotFound, IncorrectPasswordEntry, CorrectPasswordEntry, ErrorEntry, \
    OtherEntry
from pytests.TypedJournal import SSHLogJournal


def test_date():
    log = ("Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port "
           "38926 ssh2")
    entry = SSHLogEntry.get_log_type(log)(log)
    assert entry.date.strftime("%Y-%m-%d %H:%M:%S") == "2023-12-10 06:55:48"


def test_correct_ip():
    log = "Dec 10 10:14:10 LabSZ sshd[24833]: Failed password for invalid user admin from 119.4.203.64 port 2191 ssh2"
    expected_ip = IPv4Address("119.4.203.64")
    entry = SSHLogEntry.get_log_type(log)(log)
    assert entry.get_ipv4s() == expected_ip


def test_incorrect_ip():
    log = "Dec 10 10:14:10 LabSZ sshd[24833]: Failed password for invalid user admin from 666.777.888.999 port 2191 ssh2"
    entry = SSHLogEntry.get_log_type(log)(log)
    with pytest.raises(AddressValueError):
        entry.get_ipv4s()


def test_no_ip():
    log = "Dec 10 10:14:10 LabSZ sshd[24833]: pam_unix(sshd:auth): check pass; user unknown"
    entry = SSHLogEntry.get_log_type(log)(log)
    with pytest.raises(ValueNotFound):
        entry.get_ipv4s()


entry_classes = {
    "IncorrectPasswordEntry": IncorrectPasswordEntry,
    "CorrectPasswordEntry": CorrectPasswordEntry,
    "ErrorEntry": ErrorEntry,
    "OtherEntry": OtherEntry
}


@pytest.mark.parametrize("log, expected_class", [
    ("Jan  4 04:00:49 LabSZ sshd[16122]: Failed password for root from 182.100.67.52 port 9186 ssh2"
     , IncorrectPasswordEntry),
    ("Jan  4 09:44:53 LabSZ sshd[26266]: Accepted password for hxu from 111.222.107.90 port 61761 ssh2"
     , CorrectPasswordEntry),
    ("Jan  4 12:33:56 LabSZ sshd[30963]: error: Received disconnect from 103.79.141.133: 3: "
     "com.jcraft.jsch.JSchException: Auth fail [preauth]", ErrorEntry),
    ("Jan  4 12:33:56 LabSZ sshd[30960]: Disconnecting: Too many authentication failures for root "
     "[preauth]", OtherEntry)
])
def test_append(log, expected_class):
    journal = SSHLogJournal()
    journal.append(log)
    assert isinstance(journal[-1], expected_class)
