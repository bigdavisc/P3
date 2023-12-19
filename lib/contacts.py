
class ContactsManager:
    '''
    ContactsManager

    This class is used to manage the file that retains contact information
    '''

    ''' Internal '''
    def __init__(self):
        import os
        self.__contacts_file__ = "C://ProgramData/P3Data/contacts.txt"
        self.__err_queue__ = []
        self.__err_limit__ = 10
        self.__err_size__ = 50
        if not os.path.isfile(self.__contacts_file__):
            self.__create_file__()
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
        return True
    def update_contact(self, nickname, ip, port):
        return True
    def remove_contact(self, nickname):
        return True

    ''' Status funcs '''
    def list_contacts(self):
        return []
    def pop_err(self):
        return self.__err_queue__.pop(0)
