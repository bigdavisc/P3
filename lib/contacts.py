class ContactsManager:
    '''
    ContactsManager

    This class is used to manage the file that retains contact information
    '''

    ''' Internal '''
    # Create contacts file if it doesn't exist, otherwise load into memory
    def __init__(self):
        import os
        self.__contacts_file__ = "C://ProgramData/P3Data/contacts.txt"
        self.__err_queue__ = []
        self.__err_limit__ = 10
        self.__err_size__ = 50
        self.__delimiter__ = "/"
        self.__directory__ = {}  # nickname/ip/port
        if not os.path.isfile(self.__contacts_file__):
            self.__create_file__()
        else:
            self.__load_dir__()
    def __create_file__(self):
        import os
        import re
        DIR_PAT = "^(.*)(?:\/(.*).txt)$"
        re_match = re.match(DIR_PAT, self.__contacts_file__)
        try:
            os.makedirs(re_match.group(1))
        except FileExistsError:
            self.__push_err__("[CREATE FILE] Folder already exists; cannot create")
        try:
            f = open(self.__contacts_file__, "x")
        except FileExistsError:
            self.__push_err__("[CREATE FILE] File already exists; cannot create")
    def __load_dir__(self):
        f = open(self.__contacts_file__, "r")
        for contact in f.readlines():
            l = contact.split(self.__delimiter__)
            self.__directory__[l[0]] = {"ip": l[1], "port": l[2]}
        f.close()
    def __save_dir__(self):
        d = []
        for key in list(self.__directory__.keys()):
            d.append(key+self.__delimiter__+self.__directory__[key]["ip"]+self.__delimiter__+self.__directory__[key]["port"]+"\n")
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
        #Change __contacts_file__ to new_path
        #If create is True and new_path isn't a valid file,
            #Create directories and file to satisfy
        return True # True indicates a valid file at new_path exists by func end
    def add_contact(self, nickname, ip, port):
        try:
            self.__directory__[nickname]
        except KeyError:
            self.__directory__[nickname] = {"ip": ip, "port": port}
            self.__save_dir__()
            return True
        self.__push_err__("[ADD CONTACT] Contact already exists")
        return False
    def update_contact(self, nickname, ip, port):
        return True
    def remove_contact(self, nickname):
        return True

    ''' Status funcs '''
    def list_contacts(self):
        return self.__directory__
    def pop_err(self):
        try:
            return self.__err_queue__.pop(0)
        except IndexError:
            return ""
