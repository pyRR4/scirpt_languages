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

