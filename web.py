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
if spn_num1 <= 1:
    z = '8'
elif spn_num1 <= 2:
    z = '7'
elif spn_num1 <= 5:
    z = '6'
elif spn_num1 <= 9:
    z = '5'
elif spn_num1 <= 19:
    z = '4'
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
delta1 = 1.2
delta2 = 1.2
pygame.draw.rect(screen, (0, 0, 0), (0, 0, 150, 50))
pygame.draw.rect(screen, (255, 255, 255), (400, 0, 198, 40))
pygame.draw.rect(screen, (0, 0, 0), (398, 0, 200, 40), 2)
pygame.draw.rect(screen, (0, 0, 0), (398, 40, 60, 40))
pygame.draw.rect(screen, (0, 0, 0), (529, 40, 70, 40))
pygame.draw.rect(screen, (255, 255, 255), (10, 380, 580, 30))
pygame.draw.rect(screen, (0, 0, 0), (8, 380, 582, 30), 2)
pygame.draw.rect(screen, (255, 255, 255), (10, 330, 60, 40))
pygame.draw.rect(screen, (0, 0, 0), (8, 330, 62, 40), 2)
font = pygame.font.Font(None, 40)
text = font.render("CHANGE", True, (255, 255, 255))
text2 = font.render("OK", True, (255, 255, 255))
text3 = font.render("DEL", True, (255, 255, 255))
text4 = font.render("OFF", True, (0, 0, 0))
screen.blit(text, (9, 13))
screen.blit(text2, (405, 45))
screen.blit(text3, (535, 45))
screen.blit(text4, (10, 336))
pygame.display.flip()
type_map = ['map', 'sat', 'sat,skl']
pts = []
lnum = 0
text4 = ''
input_rect = pygame.Rect(400, 0, 198, 40)
active = False
ok = False
post_active = False
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
            if 10 <= event.pos[0] <= 70 and 330 <= event.pos[1] <= 370:
                post_active = not post_active
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
            num = int(z)
            if num < 4:
                num = num / 100
            elif num < 6:
                num = num / 50
            elif num < 8:
                num = num / 10
            elif num < 10:
                num = num / 5
            elif num < 12:
                num = num / 2
            elif num < 13:
                num = num * 4
            elif num < 14:
                num = num * 16
            elif num < 15:
                num = num * 32
            elif num < 16:
                num = num * 100
            if event.key == pygame.K_UP:
                coords_num[1] = min(85, coords_num[1] + delta2 / num)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_DOWN:
                coords_num[1] = max(-85, coords_num[1] - delta2 / num)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_LEFT:
                coords_num[0] = max(0, coords_num[0] - delta1 / num)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_RIGHT:
                coords_num[0] = min(180, coords_num[0] + delta1 / num)
                coords = ','.join([str(i) for i in coords_num])
                renew = True
            if event.key == pygame.K_PAGEUP:
                z = str(int(z) - 1)
                if int(z) < 1:
                    z = '1'
                renew = True
            if event.key == pygame.K_PAGEDOWN:
                z = str(int(z) + 1)
                if int(z) > 17:
                    z = '17'
                renew = True
    if renew:
        serv = 'http://static-maps.yandex.ru/1.x/'
        if delete and pts != []:
            pts = pts[:-1]
            delete = False
            text4 = ''
        if ok and ask != '':
            toponym_to_find = ask
            params = {
                'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                'geocode': toponym_to_find,
                'format': 'json'
            }
            resp = requests.get(f"http://geocode-maps.yandex.ru/1.x/", params=params)
            try:
                try:
                    post = resp.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                        'metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
                except Exception:
                    print(resp.json())
                    post = ''
                coords_num1 = resp.json()['response']['GeoObjectCollection']['featureMember'][0][
                    'GeoObject']['Point']['pos'].split()
                coords_num = [float(coords_num1[0]), float(coords_num1[1])]
                coords = ','.join(coords_num1)
                params2 = {
                    'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                    'geocode': coords,
                    'format': 'json',
                }
                resp2 = requests.get(f"http://geocode-maps.yandex.ru/1.x/", params=params2)
                place = resp2.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                    'metaDataProperty']['GeocoderMetaData']['text']
                font2 = pygame.font.Font(None, 20)
                if post_active:
                    place = f'{place} {post}'
                text4 = font2.render(place, True, (0, 0, 0))
                ok = False
                ask = ''
                serv = 'http://static-maps.yandex.ru/1.x/'
                if pts:
                    map_request = f"{serv}?ll={coords}&z={z}&l={type_map[lnum]}&pt={coords}~{'~'.join(pts)}"
                else:
                    map_request = f"{serv}?ll={coords}&z={z}&l={type_map[lnum]}&pt={coords}"
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
            serv = 'http://static-maps.yandex.ru/1.x/'
            if pts:
                map_request = f"{serv}?ll={coords}&z={z}&l={type_map[lnum]}&pt={'~'.join(pts)}"
            else:
                map_request = f"{serv}?ll={coords}&z={z}&l={type_map[lnum]}"
        map_file = "map.png"
        response = requests.get(map_request)
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
        pygame.draw.rect(screen, (255, 255, 255), (10, 380, 580, 30))
        pygame.draw.rect(screen, (0, 0, 0), (8, 380, 582, 30), 2)
        text = font.render(ask, True, (250, 0, 150))
        text2 = font.render("OK", True, (255, 255, 255))
        text3 = font.render("DEL", True, (255, 255, 255))
        if not post_active:
            text5 = font.render("OFF", True, (0, 0, 0))
            pygame.draw.rect(screen, (255, 255, 255), (10, 330, 60, 40))
            pygame.draw.rect(screen, (0, 0, 0), (8, 330, 62, 40), 2)
            screen.blit(text5, (10, 336))
        else:
            text5 = font.render("ON", True, (255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 0), (10, 330, 60, 40))
            pygame.draw.rect(screen, (255, 255, 255), (8, 330, 62, 40), 2)
            screen.blit(text5, (10, 336))
        if text4:
            screen.blit(text4, (15, 387))
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
