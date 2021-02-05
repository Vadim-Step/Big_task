import os
import sys

import pygame
import requests
coords = input()
spn = input()
map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={spn}&l=map"
response = requests.get(map_request)
slide = 0
if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass
    pygame.display.flip()

os.remove(map_file)
