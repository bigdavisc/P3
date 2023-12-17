class ContactsManager:
'''
ContactsManager

This class is used to manage the file that retains contact information
'''
    __contacts_file__ = "C://ProgramData/P3Data"
    __err_queue__ = []
    __err_limit__ = 10
    __err_size__ = 50
    ''' Internal '''
    def __init__(self):
        #Check if contacts file exists
        #If not, create
        pass
    def __push_err__(self, msg):
        __err_queue__.append(msg[:__err_size__])
        if len(__err_queue__) > __err_limit__:
            __err_queue__.pop(0)

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
        return __err_queue__.pop(0)
