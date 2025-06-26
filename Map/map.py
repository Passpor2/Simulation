from entities.entities import Grass, Herbivore, Predator, Rock, Tree

class Map:

    '''
    Класс, представляющий карту Симуляции

    Args:   size - размер карты (длина стороны, т.к. карта квадратная)

    Param:
            - size - размер карты (длина стороны)
            - map_rows - хранилище клеток карты в виде словаря
            - entities - список сущностей и их координат на карте
    '''

    def __init__(self, size: int):
        self.size = size
        self.map_rows = {key: [None for _ in range(self.size)] for key in range(size)}
        self.entities = {
            Grass: [], 
            Herbivore: [], 
            Predator: [], 
            Rock: [], 
            Tree: []
        }

    def add_entity(self, entity, location):
        y, x = location
        if 0 <= y < self.size and 0 <= x < self.size and self.map_rows[y][x] is None:
            self.map_rows[y][x] = entity
            if self.entities.get(type(entity)):
                self.entities[type(entity)].append(location)
            else:
                self.entities[type(entity)] = [location]
            return True
        return False
    
    def remove_entity(self, entity):
        y, x = entity.location
        if self.map_rows[y][x] == entity and (y, x) in self.entities[type(entity)]:
            self.map_rows[y][x] = None
            self.entities[type(entity)].remove((y, x))

    def move_entity(self, entity, new_loc):
        new_y, new_x = new_loc
        if 0 <= new_y < self.size and 0 <= new_x < self.size and self.map_rows[new_y][new_x] is None:
            old_y, old_x = entity.location
            self.map_rows[old_y][old_x] = None
            self.map_rows[new_y][new_x] = entity
            self.entities[type(entity)].remove((old_y, old_x))
            self.entities[type(entity)].append(new_loc)
            entity.location = new_loc
            return True
        return False

    def get_adjacent_positions(self, y, x, speed=1):
        directions = [(0, speed), (0, -speed), (speed, 0), (-speed, 0)]
        next_positions = []
        for dy, dx in directions:
            new_y, new_x = y + dy, x + dx
            if 0 <= new_y < self.size and 0 <= new_x < self.size:
                if self.map_rows[new_y][new_x] is None:
                    next_positions.append((new_y, new_x))
        return next_positions
    
    def count_entities(self, entity_type):
        return len(self.entities.get(entity_type, []))
