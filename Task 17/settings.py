import os

class Settings:
    __settings_path_key = "settings_path"

    def __init__(self, path=None):
        if path is not None:
            Settings.set_path(path)
        self.__parse()


    @classmethod
    def set_path(cls, path):
        os.environ[cls.__settings_path_key] = path


    @classmethod
    def get_path(cls):
        return os.environ[cls.__settings_path_key]


    def __parse_value(self, value):
        if value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            try:
                return float(value)
            except ValueError as e:
                return value # not boolean, not float, must be a string


    def __parse_line(self, line):
        setting_string = line.split("#")[0] # remove the comment
        if len(setting_string.strip()) == 0: # this is nothing but a comment
            return

        setting_string_split = setting_string.split("=")

        key   = setting_string_split[0].strip()
        value = self.__parse_value(setting_string_split[1].strip())

        setattr(self, key, value)


    def __parse(self):
        with open(self.get_path(), "r") as f:
            for line in f:
                self.__parse_line(line)


    def __exit__(self):
        del os.environ[Settings.__settings_path_key]
    
