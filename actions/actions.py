from abc import ABC, abstractmethod


class Action(ABC):

    '''
    Абстрактный класс для всех действий на карте
    '''

    def __init__(self):
        super().__init__()

    @abstractmethod
    def __call__(self, *args, **kwds):
        pass
