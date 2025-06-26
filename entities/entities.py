from abc import ABC, abstractmethod
from actions.interactions import FindPath, Eat, Attack
import logging


class Entity(ABC):

    '''
    Абстрактный базовый класс для всех сущностей в симуляции

    Args:   - location - текущее местоположение сущности на карте
    '''

    def __init__(self, location):
        super().__init__()
        self.location = location

    @abstractmethod
    def __str__(self):
        return super().__str__()


class Grass(Entity):

    '''
    Сущность - трава
    '''

    def __init__(self, location):
        super().__init__(location)

    def __str__(self):
        return '*'


class Rock(Entity):

    '''
    Сущность - камень
    '''

    def __init__(self, location):
        super().__init__(location)

    def __str__(self):
        return 'o'


class Tree(Entity):

    '''
    Сущность - дерево
    '''

    def __init__(self, location):
        super().__init__(location)

    def __str__(self):
        return 'T'


class Creature(Entity, ABC):

    '''
    Абстрактный базовый класс для всех живых существ в симуляции

    Args:   - location - текущее местоположение существа на карте
            - max_hp - максимальное здоровье существа
            - speed - скорость передвижения существа

    Param:  - location - текущее местоположение существа на карте
            - max_hp - максимальное здоровье существа
            - speed - скорость передвижения существа
            - hp - текущие очки здоровья
            - target - цель, к которой существо движется или которую
            атакует/ест
    '''

    def __init__(self, location, max_hp=100, speed=1):
        super().__init__(location)
        self.max_hp = max_hp
        self.speed = speed
        self.hp = max_hp
        self.target = None

    @abstractmethod
    def make_move(self):
        pass


class Herbivore(Creature):

    '''
    Класс, описывающий растительноядных существ в симуляции
    '''

    def __init__(self, location, max_hp=100, speed=1):
        super().__init__(location, max_hp, speed)

    def __str__(self):
        return 'h'

    def make_move(self, simulation):
        find_path = FindPath()
        eat = Eat()
        logging.debug(f"Herbivore at {self.location} (HP: {self.hp}, Speed: {self.speed}) searching for Grass")
        for _ in range(self.speed):
            next_pos = find_path(simulation, self, Grass)
            if next_pos:
                target = simulation.map.map_rows[next_pos[0]][next_pos[1]]
                if target and isinstance(target, Grass) and next_pos == target.location:
                    logging.info(f"Herbivore at {self.location} eats Grass at {next_pos}")
                    eat(simulation, self, target)
                    break
                else:
                    logging.info(f"Herbivore at {self.location} moves to {next_pos}")
                    simulation.map.move_entity(self, *next_pos)
            else:
                directions = simulation.map.get_adjacent_positions(*self.location)
                import random
                random.shuffle(directions)
                for new_y, new_x in directions:
                    if simulation.map.move_entity(self, (new_y, new_x)):
                        logging.info(f"Herbivore at {self.location} moves randomly to {(new_y, new_x)}")
                        break
                else:
                    logging.warning(f"Herbivore at {self.location} cannot move: no free cells")
                    break


class Predator(Creature):

    '''
    Класс, описывающий хищников в симуляции

    Args:   - attack - определяет атаку, по умолчанию равен 10

    Param:  - attack - параметр атаки существа
    '''

    def __init__(self, location, max_hp=100, speed=2, attack=30):
        super().__init__(location, max_hp, speed)
        self.attack = attack

    def __str__(self):
        return 'X'

    def make_move(self, simulation):
        find_path = FindPath()
        attack = Attack()
        eat = Eat()
        logging.debug(f"Predator at {self.location} (HP: {self.hp}, Speed: {self.speed}) searching for Herbivore")
        for _ in range(self.speed):
            next_pos = find_path(simulation, self, Herbivore)
            if next_pos:
                target = simulation.map.map_rows[next_pos[0]][next_pos[1]]
                if target and isinstance(target, Herbivore) and next_pos == target.location:
                    logging.info(f"Predator at {self.location} attacks Herbivore at {next_pos} (HP: {target.hp})")
                    attack(simulation, self, target)
                    if target.hp <= 0:
                        logging.info(f"Predator at {self.location} eats Herbivore at {next_pos}")
                        eat(simulation, self, target)
                    break
                else:
                    logging.info(f"Predator at {self.location} moves to {next_pos}")
                    simulation.map.move_entity(self, *next_pos)
            else:
                directions = simulation.map.get_adjacent_positions(*self.location)
                import random
                random.shuffle(directions)
                for new_y, new_x in directions:
                    if simulation.map.move_entity(self, (new_y, new_x)):
                        logging.info(f"Predator at {self.location} moves randomly to {(new_y, new_x)}")
                        break
                else:
                    logging.warning(f"Predator at {self.location} cannot move: no free cells")
                    break
