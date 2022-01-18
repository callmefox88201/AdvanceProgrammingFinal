from turtle import delay
import pygame
from src.Loop import Loop


game = Loop()
levelNo = 1
result = 0
while True:
    result = game.loop(str(levelNo), result)
    print(result)

    if result == 'exit' or result == 'lose':
        pygame.quit()
        break

    levelNo += 1

    if levelNo == 36:
        levelNo = 1
    pygame.time.wait(3000)