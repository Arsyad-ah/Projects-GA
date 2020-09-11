import os

# TODO to create SQL class for reading and writing to DB. move to utils.py?
class Database:
    def __init__(self, db_path, db_name):
        self._db_path = db_path
        self._db_name = db_name
    
    def write_data(self, table_name, data, append_data=True):
        pass

    def read_data(self, table_name):
        pass

    def remove_table(self, table_name):
        pass

    def remove_db(self, db_name):
        pass


def create_folder(path):
    """Create folder if does not exist"""
    # TODO change print to log
    if not os.path.isdir(path):
        os.mkdir(path)
        print ('path created: %s' % path)
    else:
        print ('path exists')

def check_file(path_to_file):
    """Check if file exists"""
    return os.path.exists(path_to_file)