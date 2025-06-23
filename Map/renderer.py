from abc import ABC, abstractmethod

class Renderer(ABC):

    def __init__(self, sim_map):
        super().__init__()
        self.map = sim_map

    @abstractmethod
    def render_map(self):
        pass


class ConsoleRenderer(Renderer):

    '''
    Класс, который прорисовывает карту симуляции в консоли

    Args:       - sim_map - карта симуляции

    Param:      - map - карта симуляции

    Methods:    - render_map - печатает карту в консоли
    '''

    def __init__(self, sim_map):
        super().__init__(sim_map)

    def render_map(self):
        import os

        os.system('cls' if os.name == 'nt' else 'clear')
        print('┌' + '─' * (self.map.size * 2 + 1) + '┐')
        for row in range(self.map.size):
            print('│ ' + ' '.join(str(cell) if cell else ' ' for cell in self.map.map_rows[row]) + ' │')
        print('└' + '─' * (self.map.size * 2 + 1) + '┘')
