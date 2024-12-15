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
    def render_game():
        screen.fill((0, 0, 0))
        env.render()
        pygame.display.flip()

    def display_winner(winner_text):
        screen.fill((0, 0, 0))
        text = font.render(winner_text, True, config.RED)
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(3)
    
    def display_restart(restart_text):
        screen.fill((0, 0, 0))
        text = font.render(restart_text, True, config.RED)
        text_rect = text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(3)

    def handle_end_game():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
            elif keys[pygame.K_r]:
                return

    while True:
        run = True
        env = playhockey()

        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('Player vs Player')
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 64)

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            env.move()
            render_game()

            if env.scoreA >= config.WIN_GOAL:
                display_winner("Player A Wins!")
                run = False
            elif env.scoreB >= config.WIN_GOAL:
                display_winner("Player B Wins!")
                run = False

            if env.gg:
                env.reset()

            time.sleep(0.01)

        display_restart("Press R to Restart or Q to Quit")
        handle_end_game()

if __name__ == "__main__":
    play()
