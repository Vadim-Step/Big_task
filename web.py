import os
import sys

import pygame
import requests

coords = input()
coords_num = coords.split(',')
coords_num = [float(coords_num[0]), float(coords_num[1])]
spn = input()
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
delta1 = spn_num1 * 1.2
delta2 = spn_num2 * 1.2
pygame.draw.rect(screen, (0, 0, 0), (0, 0, 150, 50))
pygame.draw.rect(screen, (255, 255, 255), (400, 0, 198, 40))
pygame.draw.rect(screen, (0, 0, 0), (398, 0, 200, 40), 2)
pygame.draw.rect(screen, (0, 0, 0), (398, 40, 60, 40))
pygame.draw.rect(screen, (0, 0, 0), (529, 40, 70, 40))
font = pygame.font.Font(None, 40)
text = font.render("CHANGE", True, (255, 255, 255))
text2 = font.render("OK", True, (255, 255, 255))
text3 = font.render("DEL", True, (255, 255, 255))
screen.blit(text, (9, 13))
screen.blit(text2, (405, 45))
screen.blit(text3, (535, 45))
pygame.display.flip()
type_map = ['map', 'sat', 'sat,skl']
pts = []
lnum = 0
input_rect = pygame.Rect(400, 0, 198, 40)
active = False
ok = False
delete = False
err = False
ask = ''
clock = pygame.time.Clock()
while running:
    renew = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 0 <= event.pos[0] <= 150 and 0 <= event.pos[1] <= 50:
                lnum = (lnum + 1) % 3
                renew = True
            if 398 <= event.pos[0] <= 458 and 40 <= event.pos[1] <= 100 and ask != '':
                ok = True
                renew = True
            if 529 <= event.pos[0] <= 599 and 40 <= event.pos[1] <= 80:
                delete = True
                renew = True
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    ask = ask[:-1]
                else:
                    ask += event.unicode
                renew = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                coords_num[1] = min(85, coords_num[1] + delta2)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_DOWN:
                coords_num[1] = max(-85, coords_num[1] - delta2)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_LEFT:
                coords_num[0] = max(0, coords_num[0] - delta1)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_RIGHT:
                coords_num[0] = min(180, coords_num[0] + delta1)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_PAGEUP:
                s_num = [str(float(spn.split(',')[0]) - 0.5), str(float(spn.split(',')[1]) - 0.5)]
                if float(s_num[0]) < 0:
                    s_num[0] = '0'
                if float(s_num[1]) < 0:
                    s_num[1] = '0'
                if float(s_num[0]) > 10:
                    s_num[0] = '10'
                if float(s_num[1]) > 10:
                    s_num[0] = '10'
                spn = ','.join(s_num)
                renew = True
            if event.key == pygame.K_PAGEDOWN:
                s_num = [str(float(spn.split(',')[0]) + 0.5), str(float(spn.split(',')[1]) + 0.5)]
                spn = ','.join(s_num)
                renew = True
    if renew:
        if delete and pts != []:
            pts = pts[:-1]
            delete = False
        if ok and ask != '':
            toponym_to_find = ask
            params = {
                'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                'geocode': toponym_to_find,
                'format': 'json'
            }
            resp = requests.get(f"http://geocode-maps.yandex.ru/1.x/", params=params)
            try:
                coords_num1 = resp.json()['response']['GeoObjectCollection']['featureMember'][0][
                    'GeoObject']['Point']['pos'].split()
                coords_num = [float(coords_num1[0]), float(coords_num1[1])]
                coords = ','.join(coords_num1)
                ok = False
                ask = ''
                serv = 'http://static-maps.yandex.ru/1.x/'
                if pts:
                    map_request = f"{serv}?ll={coords}&spn={spn}&l={type_map[lnum]}&pt={coords}~{'~'.join(pts)}"
                else:
                    map_request = f"{serv}?ll={coords}&spn={spn}&l={type_map[lnum]}&pt={coords}"
                pts1 = []
                if coords in pts:
                    for i in pts:
                        if i != coords:
                            pts1.append(i)
                    pts1.append(coords)
                    pts = pts1
            except IndexError:
                err = True
                ok = False
                text = font.render("ERR", True, (255, 0, 0))
                screen.blit(text, (460, 45))
                pygame.display.flip()
            else:
                pts.append(coords)
        else:
            print(spn)
            serv = 'http://static-maps.yandex.ru/1.x/'
            if pts:
                map_request = f"{serv}?ll={coords}&spn={spn}&l={type_map[lnum]}&pt={'~'.join(pts)}"
            else:
                map_request = f"{serv}?ll={coords}&spn={spn}&l={type_map[lnum]}"
        map_file = "map.png"
        response = requests.get(map_request)
        s_num2 = [float(spn.split(',')[0]), float(spn.split(',')[1])]
        delta1 = s_num2[0] * 1.2
        delta2 = s_num2[1] * 1.2
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 150, 50))
        font = pygame.font.Font(None, 40)
        text = font.render("CHANGE", True, (255, 255, 255))
        screen.blit(text, (9, 13))
        pygame.draw.rect(screen, (255, 255, 255), (400, 0, 198, 40))
        pygame.draw.rect(screen, (0, 0, 0), (398, 0, 200, 40), 2)
        pygame.draw.rect(screen, (0, 0, 0), (398, 40, 60, 40))
        pygame.draw.rect(screen, (0, 0, 0), (529, 40, 70, 40))
        text = font.render(ask, True, (250, 0, 150))
        text2 = font.render("OK", True, (255, 255, 255))
        text3 = font.render("DEL", True, (255, 255, 255))
        screen.blit(text3, (535, 45))
        screen.blit(text2, (405, 45))
        screen.blit(text, (400, 7))
        if err:
            text = font.render("ERR", True, (255, 0, 0))
            screen.blit(text, (460, 45))
            err = False
            ok = False
    pygame.display.flip()
    clock.tick(60)

os.remove(map_file)
