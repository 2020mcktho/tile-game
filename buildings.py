import os

from settings import *


building_images = {}

def create_images(filepath="images/buildings/"):
    for file in os.listdir(filepath):
        name, ext = os.path.splitext(file)
        print(name, ext)

class Building:
    def __init__(self, pos: np.ndarray, name: str):
        self.pos = pos
        self.name = name

        if self.name in building_images:
            self.image = pygame.transform.scale(building_images[self.name], (tile_size, tile_size))
        else:
            self.image = None

    def display(self, screen: pygame.Surface, offset: (np.ndarray|tuple)):
        if self.image is None:
            return

        screen.blit(self.image, offset)