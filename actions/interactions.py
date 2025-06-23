from abc import ABC, abstractmethod
from collections import deque
from actions.actions import Action


class FindPath(Action):
    '''
    Действие, рассчитывающее кратчайшую траекторию движения существа к своей цели
    '''
    def __init__(self):
        super().__init__()
    
    def __call__(self, simulation, creature, target_type):
        if hasattr(creature, 'target') and creature.target and creature.target in simulation.map.entities.get(target_type, []):
            target_loc = creature.target
        else:
            target_locations = simulation.map.entities.get(target_type, [])
            if not target_locations:
                creature.target = None
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
            else:
                creature.target = None
                return None
            
        queue = deque([((creature.location[0], creature.location[1]), [])])
        visited = {(creature.location[0], creature.location[1])}
        while queue:
            (y, x), path = queue.popleft()
            if (y, x) == target_loc:
                return path[0] if path else None
            for new_y, new_x in simulation.map.get_adjacent_positions(y, x):
                if (new_y, new_x) not in visited:
                    visited.add((new_y, new_x))
                    queue.append(((new_y, new_x), path + [(new_y, new_x)]))
        creature.target = None
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
