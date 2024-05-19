import datetime
import ipaddress
from typing import List, Union, Iterator, Any

from pytests.TypedEntry import SSHLogEntry, ValueNotFound


class SSHLogJournal:
    def __init__(self) -> None:
        self.entries_list: List[SSHLogEntry] = []

    def append(self, log: str) -> None:
        entry: SSHLogEntry = SSHLogEntry.get_log_type(log)(log)
        if entry.validate():
            self.entries_list.append(entry)
        else:
            raise ValueError

    def __len__(self) -> int:
        return len(self.entries_list)

    def __iter__(self) -> Iterator[SSHLogEntry]:
        return iter(self.entries_list)

    def __contains__(self, item: SSHLogEntry) -> bool:
        return item in self.entries_list

    def __getattr__(self, item: Any) -> Any:
        if isinstance(item, datetime.datetime):
            attr_list_date: List[datetime.datetime] = []
            for entry in self.entries_list:
                date: datetime.datetime = entry.__getattr__('date')
                if date == item:
                    attr_list_date.append(date)
            return attr_list_date
        elif isinstance(item, int):
            return self.entries_list[item]
        elif isinstance(item, ipaddress.IPv4Address):
            attr_list_entry: List[SSHLogEntry] = []
            for entry in self.entries_list:
                try:
                    ip = entry.get_ipv4s()
                    if ip == item:
                        attr_list_entry.append(entry)
                except ValueNotFound:
                    pass
            return attr_list_entry
        else:
            raise AttributeError(f"{self.__class__.__name__} nie pozwala na pozyskanie atrybutów po {item}")

    def __getitem__(self, key: Union[int, slice]) -> Union[SSHLogEntry, List[SSHLogEntry]]:
        if isinstance(key, slice):
            start = key.start if key.start is not None else 0
            stop = key.stop if key.stop is not None else 0
            step = key.step if key.step is not None else 1
            return self.entries_list[start:stop:step]
        else:
            return self.entries_list[key]

