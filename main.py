import numpy as np
import pygame

from buildings import Building
from settings import *


def get_chunk_key(chunk_pos: np.ndarray):
    return f"{chunk_pos[0]}, {chunk_pos[1]}"


def get_chunk_pos(chunk_key: str):
    return np.array(*chunk_key.split(", "))


def get_chunk_in_pos(pos: np.ndarray):
    return np.floor_divide(pos, chunk_dims)


class Tile:
    def __init__(self, pos: np.ndarray, building: (None|Building)=None):
        self.pos = pos
        self.building = building

        try:
            self.tile_img = pygame.transform.scale(pygame.image.load("tile.png"), (tile_size, tile_size))
        except FileNotFoundError:
            self.tile_img = pygame.Surface((tile_size, tile_size))
            self.tile_img.fill((255, 255, 255))
            pygame.draw.rect(self.tile_img, (0, 255, 0), pygame.Rect(0, 0, tile_size, tile_size), 5)

        if self.building:
            self.building.display(self.tile_img, (0, 0))

    def set_pos(self, pos: np.ndarray):
        self.pos = pos

    def display(self, screen: pygame.Surface, offset: (np.ndarray|tuple)):
        screen.blit(self.tile_img, np.multiply(self.pos, tile_size) + offset)


class Chunk:
    def __init__(self, chunk_pos: np.ndarray):
        self.chunk_pos = chunk_pos  # position in the world of the topleft of the chunk, not chunk position

        top_left_pos = np.multiply(self.chunk_pos, chunk_dims)

        self.data = np.zeros(chunk_dims, dtype=Tile)
        for x in range(chunk_dims[0]):
            for y in range(chunk_dims[1]):
                self.data[x, y] = Tile(top_left_pos + (x, y))

    def set_tile(self, chunk_pos: np.ndarray, data: Tile):
        self.data[chunk_pos] = data

    def get_tile(self, chunk_pos: np.ndarray):
        return self.data[chunk_pos]

    def display(self, screen: pygame.Surface, offset: (np.ndarray|tuple)):
        for row in self.data:
            for tile in row:
                tile.display(screen, offset)


class World:
    def __init__(self):

        self.chunks = {}

        self.camera_pos = np.array((0., 0.))

    def get_world_pos(self, screen_pos: np.ndarray):
        return (screen_pos - screen_size / 2) / tile_size

    def get_chunk_in(self, world_pos: np.ndarray, create_new_chunk: bool = False):
        chunk_in_pos = get_chunk_in_pos(world_pos)
        chunk_key = get_chunk_key(chunk_in_pos)

        if chunk_key in self.chunks:
            return self.chunks[chunk_key]
        elif create_new_chunk:
            return self.create_chunk(chunk_in_pos)

        return None

    def create_chunk(self, chunk_pos: np.ndarray):
        chunk_str = get_chunk_key(chunk_pos)
        chunk = Chunk(chunk_pos)

        self.chunks[chunk_str] = chunk
        print(chunk_str)
        return chunk

    def display(self, screen: pygame.Surface, offset: (np.ndarray|tuple) = (0, 0)):

        # display the chunks around the camera position
        chunk = self.get_chunk_in(self.camera_pos, create_new_chunk=True)
        if chunk is not None:
            new_offset = -np.multiply(self.camera_pos, tile_size) + screen_size / 2
            chunk.display(screen, new_offset)


def main():

    world = World()

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    fps = 60

    running = True
    while running:

        dt = clock.tick(fps) / 1000

        keys = pygame.key.get_pressed()

        mouse_pos = np.array(pygame.mouse.get_pos())
        game_pos = world.get_world_pos(mouse_pos)

        print(game_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys[pygame.K_w]:
            world.camera_pos[1] -= camera_speed * dt
        if keys[pygame.K_s]:
            world.camera_pos[1] += camera_speed * dt
        if keys[pygame.K_a]:
            world.camera_pos[0] -= camera_speed * dt
        if keys[pygame.K_d]:
            world.camera_pos[0] += camera_speed * dt

        pygame.display.set_caption(f"fps: {fps}")

        screen.fill((255, 255, 255))
        world.display(screen)
        pygame.display.flip()


    pygame.quit()


main()
