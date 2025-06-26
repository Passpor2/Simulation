from entities.entities import Grass, Herbivore, Predator, Rock, Tree
import logging

BASE_ENTITIES = [
    (Grass, 10),
    (Rock, 5),
    (Tree, 5),
    (Herbivore, 6),
    (Predator, 3)
]

RESPAWN_RULES = [
    {"entity_type": Grass, "threshold": 5, "spawn_quantity": 3, "max_entities": 20},
    {"entity_type": Herbivore, "threshold": 5, "spawn_quantity": 3, "max_entities": 10}
]

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('simulation.log')
        ]
    )
