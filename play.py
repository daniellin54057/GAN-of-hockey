import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import pickle
from collections import deque
import matplotlib.pyplot as plt
import pygame
from hockey_env_for_pvp import playhockey
import config
import sys
import time

def play():
    run = True
    env = playhockey()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH , config.SCREEN_HEIGHT))
    pygame.display.set_caption('player vs player')
    clock = pygame.time.Clock()

    def render_game():
        screen.fill((0 , 0 , 0))
        env.render()
        pygame.display.flip()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        env.move()
        render_game()
        if env.gg:
            env.reset()
        time.sleep(0.01)


if __name__ == "__main__":
    play()
