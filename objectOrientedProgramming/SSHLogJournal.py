import datetime
import ipaddress

import SSHLogEntry


class SSHLogJournal:
    def __init__(self):
        self.entries_list = []

    def append(self, log):
        entry = SSHLogEntry.SSHLogEntry.get_log_type(log)(log)
        if entry.validate():
            self.entries_list.append(entry)
        else:
            raise ValueError

    def __len__(self):
        return len(self.entries_list)

    def __iter__(self):
        return iter(self.entries_list)

    def __contains__(self, item):
        return item in self.entries_list

    def __getattr__(self, item):
        if isinstance(item, datetime.datetime):
            attr_list = []
            for entry in self.entries_list:
                date = entry.__getattr__('date')
                if date == item:
                    attr_list.append(date)
                return attr_list
        elif isinstance(item, int):
            return self.entries_list[item]
        elif isinstance(item, ipaddress.IPv4Address):
            attr_list = []
            for entry in self.entries_list:
                ip = entry.get_ipv4s()
                if ip == item:
                    attr_list.append(item)
                return attr_list
        else:
            raise AttributeError(f"{self.__class__.__name__} nie pozwala na pozyskanie atrybutów po {item}")

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.entries_list[key.start:key.stop:key.step]
        else:
            return self.entries_list[key]

