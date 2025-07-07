import numpy as np
import pygame

tile_size = 30
camera_speed = 2.
chunk_dims = np.array((8, 8))
screen_size = np.array((500, 500))
half_screen = screen_size / 2.0