class DataManager:
    '''
    DataManager

    This class is the baseline data retention class via file management
    '''

    ''' Internal '''
    # These are core mechanics of this library for downstream use.
    def __init__(self, filepath, fields):
        import os
        import copy
        # Where the data is stored
        self.__data_file__ = filepath
        # What fields the data is organized in
        self.__data_fields__ = copy.deepcopy(fields) # First field is always the key
        self.__data_fields__.append("updated")
        # What errors have occurred; how many to save; how long the text can be
        self.__err_queue__ = []
        self.__err_limit__ = 10
        self.__err_size__ = 200
        # What delimits the data
        self.__delimiter__ = "/"
        # The memory object that stores data for access
        self.__directory__ = {}
        # The key for the header row; contains audit info
        self.__context_key__ = "[DATA]"
        # Create the file if it doesn't exist, then load the file
        if not os.path.isfile(self.__data_file__):
            self.__create_file__()
        self.__load_dir__()
    def __create_file__(self, path=""):
        import os
        import re
        DIR_PAT = "^(.*)(?:\/(.*).txt)$"
        # If no path is specified, use the default
        if not path:
            path = self.__data_file__
        re_match = re.match(DIR_PAT, path)
        # Create folders, file as necessary
        try:
            os.makedirs(re_match.group(1))
        except FileExistsError:
            self.__push_err__("[CREATE FILE] Folder already exists; cannot create")
        try:
            f = open(path, "x")
        except FileExistsError:
            self.__push_err__("[CREATE FILE] File already exists; cannot create")
    def __load_dir__(self):
        import datetime
        import copy
        # Empty memory, set up audit context
        self.__directory__.clear()
        self.__directory__[self.__context_key__] = {"LOADED": str(datetime.datetime.now()), "FILE": self.__data_file__}
        f = open(self.__data_file__, "r")
        # Begin reading file
        for contact in f.readlines():
            if contact.startswith(self.__context_key__):
                continue
            l = contact.split(self.__delimiter__)
            row = {}
            # Load each data field into an object indexed by the first data piece; the key
            for i in range(1, len(self.__data_fields__)):
                row[self.__data_fields__[i]] = l[i]
            row["updated"] = row["updated"].replace("\n","")
            self.__directory__[l[0]] = copy.deepcopy(row)
        f.close()
    def __save_dir__(self):
        # Write the audit line
        d = [self.__context_key__+": Last load["+self.__directory__[self.__context_key__]["LOADED"]+"] File loaded["+self.__directory__[self.__context_key__]["FILE"]+"]\n"]
        # Begin writing data key by key
        for key in list(self.__directory__.keys()):
            if key == self.__context_key__:
                continue
            line = key
            for i in range(1, len(self.__data_fields__)):
                line += self.__delimiter__ + self.__directory__[key][self.__data_fields__[i]]
            line += "\n"
            d.append(line)
        f = open(self.__data_file__, "w")
        f.writelines(d)
        f.close()
    def __push_err__(self, msg):
        # Add message to error queue; push the oldest if queue full
        self.__err_queue__.append(msg[:self.__err_size__])
        if len(self.__err_queue__) > self.__err_limit__:
            self.__err_queue__.pop(0)

    ''' Management funcs '''
    # These will return True when the action is successful, False when not.
    # Whenever False is returned, an error will be pushed to __err_queue__
    def change_file_path(self, new_path, create=False):
        import os
        if os.path.isfile(new_path):
            # TODO add some validation here; create a .p3c extension. Encryption?
            self.__data_file__ = new_path
            self.__load_dir__()
            return True
        elif create:
            self.__create_file__(new_path)
            self.__data_file__ = new_path
            self.__load_dir__()
            return True
        else:
            self.__push_err__(f"[CHANGE FILE PATH] File '{new_path}' doesn't exist, and 'create' was set to False")
            return False
    def refresh(self):
        self.__load_dir__()

    ''' Status funcs '''
    # These will only be used to return data and not process anything.
    def list_data(self):
        import copy
        a = copy.deepcopy(self.__directory__)
        del(a[self.__context_key__])
        return a
    def get_data(self, key):
        try:
            return self.__directory__[key]
        except KeyError:
            return {}
    def get_file_path(self):
        return self.__data_file__
    def pop_err(self):
        try:
            return self.__err_queue__.pop(0)
        except IndexError:
            return ""

class ContactsManager(DataManager):
    '''
    ContactsManager

    This class is used to manage the file that retains contact information
    '''
    def __init__(self):
        DataManager.__init__(self, "C://ProgramData/P3Data/contacts.txt", ["nickname", "ip", "port"])
    def update_contact(self, nickname, ip, port):
        import datetime
        # Validations
        if nickname == self.__context_key__:
            self.__push_err__(f"[ADD CONTACT] Nickname '{self.__context_key__}' not allowed")
            return False
        if self.__delimiter__ in nickname:
            self.__push_err__(f"[ADD CONTACT] Character '{self.__delimiter}' not allowed")
            return False
        # TODO add validation to confirm ip and port structures
        # Load new contact into memory, save to file
        self.__directory__[nickname] = {"ip": str(ip), "port": str(port), "updated": str(datetime.datetime.now())}
        self.__save_dir__()
        return True
    def remove_contact(self, nickname):
        try:
            # Delete contact from memory, save to file
            del(self.__directory__[nickname])
            self.__save_dir__()
            return True
        except KeyError:
            self.__push_err__(f"[REMOVE CONTACT] Contact '{nickname}' doesn't exist; cannot delete")
            return False
    def list_contacts(self):
        return self.list_data()
    def get_contact(self, nickname):
        return self.get_data(nickname)

class GroupsManager(DataManager):
    '''
    GroupsManager

    This class is used to manage collections of contacts
    '''
    def __init__(self):
        DataManager.__init__(self, "C://ProgramData/P3Data/groups.txt", ["groupname", "nicknames"])
        self.__group_delimiter__ = ":"
    def update_group(self, groupname, nicknames):
        import datetime
        # Validations
        if groupname == self.__context_key__:
            self.__push_err__(f"[ADD GROUP] Nickname '{self.__context_key__}' not allowed")
            return False
        if self.__delimiter__ in groupname:
            self.__push_err__(f"[ADD GROUP] Character '{self.__delimiter__}' not allowed")
            return False
        if self.__delimiter__ in nicknames:
            self.__push_err__(f"[ADD GROUP] Character '{self.__delimiter__}' not allowed")
            return False
        # TODO validate nicknames structure
        # Load group to memory, save to file
        self.__directory__[groupname] = {"nicknames": nicknames, "updated": str(datetime.datetime.now())}
        self.__save_dir__()
        return True
    def remove_group(self, groupname):
        try:
            # Delete group from memory, save to file
            del(self.__directory__[groupname])
            self.__save_dir__()
            return True
        except KeyError:
            self.__push_err(f"[REMOVE GROUP] Group '{groupname}' doesn't exist; cannot delete")
            return False
    def get_group_members(self, groupname):
        try:
            return self.__directory__[groupname]["nicknames"].split(self.__group_delimiter__)
        except KeyError:
            return []
