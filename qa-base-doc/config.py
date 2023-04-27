import configparser

class Config:
    config = configparser.ConfigParser()
    path = ''

    @classmethod
    def loadINI(cls, path):
        cls.path = path
        cls.config.read(path)

    @classmethod
    def get(cls, key, section='default'):
        return cls.config.get(section, key)
    
    @classmethod
    def set(cls, key, val, section='default'):
        cls.config.set(section, key, val)

    @classmethod
    def save(cls):
        with open(cls.path, 'w') as configfile:
            cls.config.write(configfile)

