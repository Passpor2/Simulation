from actions.actions import Action
from entities.entities import Herbivore, Predator, Creature

class MoveAction(Action):

    def __init__(self):
        super().__init__()

    def __call__(self, simulation):
        for entity_type in [Herbivore, Predator]:
            for y, x in simulation.map.entities.get(entity_type, [])[:]:
                entity = simulation.map.map_rows[y][x]
                if isinstance(entity, Creature):
                    entity.make_move(simulation)
