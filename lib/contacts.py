class ContactsManager:
    '''
    ContactsManager

    This class is used to manage the file that retains contact information
    '''

    ''' Internal '''
    # These are core mechanics of this library for downstream use.
    def __init__(self):
        import os
        self.__contacts_file__ = "C://ProgramData/P3Data/contacts.txt"
        self.__err_queue__ = []
        self.__err_limit__ = 10
        self.__err_size__ = 200
        self.__delimiter__ = "/"
        self.__directory__ = {}  # Entries look like nickname/ip/port
        if not os.path.isfile(self.__contacts_file__):
            self.__create_file__()
        else:
            self.__load_dir__()
    def __create_file__(self, path=""):
        import os
        import re
        DIR_PAT = "^(.*)(?:\/(.*).txt)$"
        if not path:
            path = self.__contacts_file__
        re_match = re.match(DIR_PAT, path)
        try:
            os.makedirs(re_match.group(1))
        except FileExistsError:
            self.__push_err__("[CREATE FILE] Folder already exists; cannot create")
        try:
            f = open(path, "x")
        except FileExistsError:
            self.__push_err__("[CREATE FILE] File already exists; cannot create")
    def __load_dir__(self):
        self.__directory__.clear()
        f = open(self.__contacts_file__, "r")
        for contact in f.readlines():
            l = contact.split(self.__delimiter__)
            self.__directory__[l[0]] = {"ip": l[1], "port": l[2], "updated": l[3].replace("\n","")}
        f.close()
    def __save_dir__(self):
        d = []
        for key in list(self.__directory__.keys()):
            d.append(key+self.__delimiter__+self.__directory__[key]["ip"]+self.__delimiter__+self.__directory__[key]["port"]+self.__delimiter__+self.__directory__[key]["updated"]+"\n")
        f = open(self.__contacts_file__, "w")
        f.writelines(d)
        f.close()
    def __push_err__(self, msg):
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
            self.__contacts_file__ = new_path
            self.__load_dir__()
            return True
        elif create:
            self.__create_file__(new_path)
            self.__contacts_file__ = new_path
            self.__load_dir__()
            return True
        else:
            self.__push_err__(f"[CHANGE FILE PATH] File '{new_path}' doesn't exist, and 'create' was set to False")
            return False
    def update_contact(self, nickname, ip, port, add=True):
        import datetime
        if not add:
            try:
                self.__directory__[nickname]
            except KeyError:
                self.__push_err__(f"[ADD CONTACT] Contact '{nickname}' doesn't exist, and 'add' was set to False")
                return False
        self.__directory__[nickname] = {"ip": ip, "port": port, "updated": str(datetime.datetime.now())}
        self.__save_dir__()
        return True
    def remove_contact(self, nickname):
        try:
            del(self.__directory__[nickname])
            return True
        except KeyError:
            self.__push_err__(f"[REMOVE CONTACT] Contact '{nickname}' doesn't exist; cannot delete")
            return False

    ''' Status funcs '''
    # These will only be used to return data and not process anything.
    def list_contacts(self):
        return self.__directory__
    def get_file_path(self):
        return self.__contacts_file__
    def pop_err(self):
        try:
            return self.__err_queue__.pop(0)
        except IndexError:
            return ""
