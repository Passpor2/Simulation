from collections import deque
from actions.actions import Action
import logging


class FindPath(Action):
    '''
    Действие, рассчитывающее кратчайшую траекторию движения существа к своей цели
    '''
    def __init__(self):
        super().__init__()
    
    def __call__(self, simulation, creature, target_type):
        logging.info(f'{creature.__class__.__name__} started to seek a target')
        if hasattr(creature, 'target') and creature.target and creature.target in simulation.map.entities.get(target_type, []):
            logging.info('First if operator satisfied')
            target_loc = creature.target
        else:
            logging.info('First if operator NOT satisfied')
            target_locations = simulation.map.entities.get(target_type, [])
            if not target_locations:
                logging.info('Second if operator satisfied')
                creature.target = None
                logging.debug(f"No {target_type.__name__} found for {creature.__class__.__name__} at {creature.location}")
                return None
            min_dist = float('inf')
            nearest_loc = None
            for loc in target_locations:
                dist = abs(creature.location[0] - loc[0]) + abs(creature.location[1] - loc[1])
                if dist < min_dist:
                    min_dist = dist
                    nearest_loc = loc
            if nearest_loc:
                creature.target = nearest_loc
                target_loc = nearest_loc
                logging.info(f'{creature.__class__.__name__} found target at {target_loc=}')
            else:
                creature.target = None
                logging.debug(f"No valid {target_type.__name__} target for {creature.__class__.__name__} at {creature.location}")
                return None
            
        queue = deque([(creature.location, [])])
        visited = {creature.location}
        max_steps = creature.speed
        logging.info(f'{creature.__class__.__name__} launches a while loop with {target_loc=} (bfs find path)')
        while queue:
            logging.debug(f'(while)\t{queue=}')
            (y, x), path = queue.popleft()
            if (y, x) == target_loc:
                if path:
                    logging.debug(f"\tPath found to {target_type.__name__} at {target_loc}: {path}")
                    return path[0]
                return None
            if len(path) >= max_steps:
                continue
            logging.info(f'\t{creature.__class__.__name__} launches a for loop with {target_loc=}')
            for new_y, new_x in simulation.map.get_adjacent_positions(y, x):
                logging.debug(f'\t\t{new_y=}, {new_x=}, {path=}')
                if (new_y, new_x) not in visited:
                    visited.add((new_y, new_x))
                    queue.append(((new_y, new_x), path + [(new_y, new_x)]))
            logging.debug(f'{queue}')
        creature.target = None
        logging.debug(f"No path found to {target_type.__name__} at {target_loc} for {creature.__class__.__name__}")
        return None
    

class Eat(Action):
    '''
    Действие, описывающее поглощение пищи существом
    '''
    def __init__(self):
        super().__init__()

    def __call__(self, simulation, creature, target):
        from entities.entities import Herbivore, Predator, Grass
        if isinstance(creature, Herbivore) and isinstance(target, Grass):
            simulation.map.remove_entity(target)
            creature.hp = min(creature.hp + 10, creature.max_hp)
            creature.target = None
        elif isinstance(creature, Predator) and isinstance(target, Herbivore) and target.hp <= 0:
            simulation.map.remove_entity(target)
            creature.hp = min(creature.hp + 10, creature.max_hp)
            creature.target = None


class Attack(Action):
    '''
    Действие, описывающее нанесение урона одним существом другому
    '''
    def __init__(self):
        super().__init__()

    def __call__(self, simulation, creature, target):
        from entities.entities import Herbivore, Predator
        if isinstance(creature, Predator) and isinstance(target, Herbivore):
            target.hp -= creature.attack
            creature.target = None
