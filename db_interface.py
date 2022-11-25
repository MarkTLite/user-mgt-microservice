import abc

class DatabaseInterface(metaclass=abc.ABCMeta):
    """ The Database Interface Methods"""
    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass
    
    @abc.abstractmethod
    def create(self):
        pass

    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass
