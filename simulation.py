import time
from Map.renderer import ConsoleRenderer
from Map.map import Map
from actions.spawn import SpawnEntity, RespawnEntity
from actions.movement import MoveAction
from config import BASE_ENTITIES, RESPAWN_RULES, setup_logging


class Simulation:

    '''
    Главный класс Симуляции.
    В нем прописана основная логика существования мира.
    
    args:   map_size - int, длина каждой стороны карты (квадрата)

    Param:  turns_count - количество ходов с начала симуляции,
            running - статус симуляции,
            map - карта симуляции, класс Map,
            renderer - рендерер карты, класс Renderer,
            base_entities - базовый набор сущностей, создаваемых на старте симуляции
            (можно задать вручную в качестве аргумента к методу start_simulation())

    Methods: 
            - start_simulation() - Старт симуляции, меняет статус симуляции на running=True
            и запускает стартовые действия действия (init_actions)
            - next_turn() - запускает регулярные действия, плюсует счетчик ходов
            - pause_simulation() - ставит симуляцию на паузу через смену статуса running=False

    '''

    def __init__(self, map_size):
        setup_logging()
        self.turns_count = 0
        self.running = False
        self.map = Map(map_size)
        self.renderer = ConsoleRenderer(self.map)
        self.init_actions = [
            SpawnEntity()
        ]
        self.turn_actions = [
            MoveAction(),
            *[RespawnEntity(**rule) for rule in RESPAWN_RULES]
        ]
        self.base_entities = BASE_ENTITIES

    def next_turn(self):
        '''
        Метод, определяющий логику смены хода.
        Запускает регулярные действия симуляции, 
        а также плюсует счетчик ходов.
        '''
        self.turns_count += 1
        for action in self.turn_actions:
            action(self)
        self.renderer.render_map()
        print(f"Ход {self.turns_count}")

    def start_simulation(self, *args):
        import logging
        '''
        Метод, запускающий симуляцию и начальные действия.
        В качестве аргументов передается список кортежей, 
        содержащих тип сущности и количество сущностей этого типа, 
        которое нужно создать. По умолчанию принимает данные из параметра
        base_entities
        '''
        self.running = True
        if not args:
            args = self.base_entities
        for entity_type, quantity in args:
            self.init_actions[0](self, entity_type, quantity)
        logging.info(f'Starting a new Simulation')
        while self.running:
            self.next_turn()
            time.sleep(0.5)

    def pause_simulation(self):
        '''
        Метод, ставящий симуляцию на паузу
        '''
        self.running = False


def main():
    sim = Simulation(10)
    try:
        sim.start_simulation()
    except KeyboardInterrupt:
        sim.pause_simulation()
        print("Симуляция приостановлена")
