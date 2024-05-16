import datetime
import ipaddress

from objectOrientedProgramming.SSHLogEntry import SSHLogEntry, ValueNotFound


class SSHLogJournal:
    def __init__(self):
        self.entries_list = []

    def append(self, log):
        entry = SSHLogEntry.get_log_type(log)(log)
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
                try:
                    ip = entry.get_ipv4s()
                    if ip == item:
                        attr_list.append(entry)
                except ValueNotFound:
                    pass
            return attr_list
        else:
            raise AttributeError(f"{self.__class__.__name__} nie pozwala na pozyskanie atrybutów po {item}")

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else 0
            step = key.step if key.step is not None else 1
            return self.entries_list[start:stop:step]
        else:
            return self.entries_list[key]

