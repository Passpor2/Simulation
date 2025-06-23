from actions.actions import Action
from random import shuffle


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
            quantity = len(free_cells)
        shuffle(free_cells)
        for _ in range(quantity):
            if not free_cells:
                break
            loc = free_cells.pop()
            entity = entity_type(loc)
            simulation.map.add_entity(entity, loc)


class RespawnEntity(Action):

    def __init__(self, entity_type, threshold, spawn_quantity):
        super().__init__()
        self.entity_type = entity_type
        self.threshold = threshold
        self.spawn_quantity = spawn_quantity
    
    def __call__(self, simulation):
        if simulation.map.count_entities(self.entity_type) < self.threshold:
            SpawnEntity()(simulation, self.entity_type, self.spawn_quantity)
