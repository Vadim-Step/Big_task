import os
import sys

import pygame
import requests

coords = input()
coords_num = coords.split(',')
coords_num = [float(coords_num[0]), float(coords_num[1])]
spn = input()
print(spn)
spn_num1 = float(spn.split(',')[0])
spn_num2 = float(spn.split(',')[1])
map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={spn}&l=map"
response = requests.get(map_request)
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

running = True
delta1 = spn_num1 * 3.25
delta2 = spn_num2 * 1.2
pygame.draw.rect(screen, (0, 0, 0), (0, 0, 150, 50))
font = pygame.font.Font(None, 40)
text = font.render("CHANGE", True, (255, 255, 255))
screen.blit(text, (9, 13))
pygame.display.flip()
type = ['map', 'sat', 'sat,skl']
lnum = 0
while running:
    renew = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= event.pos[0] <= 150 and 0 <= event.pos[1] <= 50:
                lnum = (lnum + 1) % 3
                renew = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                coords_num[1] = min(85, coords_num[1] + delta2)
            if event.key == pygame.K_DOWN:
                coords_num[1] = max(-85, coords_num[1] - delta2)
            if event.key == pygame.K_LEFT:
                coords_num[0] = max(0, coords_num[0] - delta1)
            if event.key == pygame.K_RIGHT:
                coords_num[0] = min(180, coords_num[0] + delta1)
            coords = ','.join([str(i) for i in coords_num])
            renew = True
    if renew:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&spn={spn}&l={type[lnum]}"
        map_file = "map.png"
        response = requests.get(map_request)
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 150, 50))
        font = pygame.font.Font(None, 40)
        text = font.render("CHANGE", True, (255, 255, 255))
        screen.blit(text, (9, 13))
    pygame.display.flip()

os.remove(map_file)
