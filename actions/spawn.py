from actions.actions import Action
from random import shuffle
import logging


class SpawnEntity(Action):
    
    '''
    Callable класс, создающий сущности заданного типа в заданном 
    количестве в рандомных свободных клетках

    Args:   - simulation - экземпляр карты класса Map,
            - entity - тип сущности, которую необходимо создать,
            - quantity - количество сущностей, которые необходимо создать

    '''

    def __init__(self):
        super().__init__()

    def __call__(self, simulation, entity_type, quantity):
        free_cells = [(y, x) for x in range(simulation.map.size) for y in range(simulation.map.size) if simulation.map.map_rows[y][x] is None]
        if len(free_cells) < quantity:
            logging.warning(f"Requested {quantity} {entity_type.__name__}, but only {len(free_cells)} free cells available")
            quantity = len(free_cells)
        shuffle(free_cells)
        for _ in range(quantity):
            if not free_cells:
                logging.warning(f"No free cells left for spawning {entity_type.__name__}")
                break
            loc = free_cells.pop()
            entity = entity_type(loc)
            simulation.map.add_entity(entity, loc)
            logging.info(f"Spawned {entity_type.__name__} at {loc}")


class RespawnEntity(Action):

    def __init__(self, entity_type, threshold, spawn_quantity, max_entities):
        super().__init__()
        self.entity_type = entity_type
        self.threshold = threshold
        self.spawn_quantity = spawn_quantity
        self.max_entities = max_entities
    
    def __call__(self, simulation):
        entity_count = simulation.map.count_entities(self.entity_type)
        logging.debug(f"Checking respawn for {self.entity_type.__name__}: current={entity_count}, \
                        threshold={self.threshold}, max={self.max_entities}")
        if entity_count < self.threshold and entity_count + self.spawn_quantity < self.max_entities:
            logging.info(f"Respawning {self.spawn_quantity} {self.entity_type.__name__} (current: {entity_count})")
            SpawnEntity(simulation, self.entity_type, self.spawn_quantity)
