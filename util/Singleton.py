class Singleton:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if not Singleton.__instance:
            Singleton()
        return Singleton.__instance

    @classmethod
    def __init__(cls):
        """ Virtually private constructor. """
        if Singleton.__instance:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = cls
