import pygame
from menu_painter import MenuPainter
import sqlite3


# game stats:
# omm - on main menu
# wfa - wait for activity
# gmc - game mode choosing
# ig-cl - in game classic
# ig-bt - in game btris
# ig-wt - in game welltris
# nts - notes

def check_click(x_pos, y_pos, x_left, y_top, w, h):
    if x_left <= x_pos <= x_left + w:
        if y_top <= y_pos <= y_top + h:
            return True
    return False


def button_reaction(name):
    global main_status, mp, running
    if name == 'play':
        main_status = 'gmc'
        mp.init_selector()
    elif name == 'classic':
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "tetris.mp3")
        pygame.mixer.music.play(-1)
        main_status = 'ig-cl'
        mp.init_classic(name)
    elif name == "normal":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "tetris.mp3")
        pygame.mixer.music.play(-1)
        main_status = 'ig-cl'
        mp.init_classic(name)
    elif name == "hard":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "tetris.mp3")
        pygame.mixer.music.play(-1)
        main_status = 'ig-cl'
        mp.init_classic(name)
    elif name == "btris_20":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "btris.wav")
        pygame.mixer.music.play(-1)
        main_status = 'ig-bt'
        mp.init_btris(20)
    elif name == "btris_10":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "btris.wav")
        pygame.mixer.music.play(-1)
        main_status = 'ig-bt'
        mp.init_btris(10)
    elif name == "btris_5":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "btris.wav")
        pygame.mixer.music.play(-1)
        main_status = 'ig-bt'
        mp.init_btris(5)
    elif name == "_easy":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "welltris.wav")
        pygame.mixer.music.play(-1)
        main_status = "ig-wt"
        mp.init_welltris("easy")
    elif name == "_normal":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "welltris.wav")
        pygame.mixer.music.play(-1)
        main_status = "ig-wt"
        mp.init_welltris("normal")
    elif name == "_hard":
        pygame.mixer.init()
        pygame.mixer.music.load("Data\\" + "Music\\" + "welltris.wav")
        pygame.mixer.music.play(-1)
        main_status = "ig-wt"
        mp.init_welltris("hard")
    elif name == "exit":
        running = False
    elif name == "notes":
        main_status = "nts"
    elif name == "left":
        change_volume(-0.02)
    elif name == "right":
        change_volume(0.02)


def change_volume(value):
    global volume
    connection = sqlite3.connect("Data\\" + "AData.sqlite")
    cursor = connection.cursor()
    volume = cursor.execute("SELECT Volume FROM Settings").fetchall()[0][0]
    if volume + value > 0:
        cursor.execute(f"UPDATE Settings SET Volume = {volume + value}")
        connection.commit()
    connection.close()


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load("Data\\" + "Music\\" + "mt.wav")
    con = sqlite3.connect("Data\\" + "AData.sqlite")
    cur = con.cursor()
    volume = cur.execute("SELECT Volume FROM Settings").fetchall()[0][0]
    con.close()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)
    sounds = []
    fps = 30
    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 1280, 720
    screen = pygame.display.set_mode(size)
    running = True
    pygame.display.set_caption('Atris')
    main_status = 'wfa'
    mp = MenuPainter(screen)
    following_bt = False
    while running:
        con = sqlite3.connect("Data\\" + "AData.sqlite")
        cur = con.cursor()
        volume = cur.execute("SELECT Volume FROM Settings").fetchall()[0][0]
        con.close()
        pygame.mixer.music.set_volume(volume)
        screen.fill((0, 0, 0))
        if main_status == 'omm':
            mp.draw_main_menu()
        elif main_status == "wfa":
            mp.draw_waiting()
        elif main_status == 'gmc':
            mp.draw_selector()
        elif main_status == 'ig-cl':
            mp.draw_and_step()
        elif main_status == "ig-bt":
            mp.btris.update_particles()
            mp.btris.draw_self()
            if following_bt:
                mp.btris.update(pygame.mouse.get_pos())
        elif main_status == "ig-wt":
            mp.draw_and_step_w()
        elif main_status == "nts":
            mp.draw_notes()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if main_status == "wfa":
                    if check_click(event.pos[0], event.pos[1], 480, 620, 320, 64):
                        main_status = "omm"
                        mp.init_main_menu()
                        screen.fill((100, 0, 100))
                elif main_status in ["omm", "gmc"]:
                    group = list(mp.buttons)
                    for i in range(len(list(mp.buttons))):
                        if group[i].rect.collidepoint(event.pos):
                            group[i].change_stat('ps')
                    sprites = pygame.sprite.Group()
                    for elem in group:
                        sprites.add(elem)
                    mp.buttons = sprites
                elif main_status == "ig-bt":
                    if mp.btris.catch_mbd(event.pos):
                        following_bt = True
            elif event.type == pygame.KEYDOWN:
                if main_status == "gmc" and event.key == 120:
                    main_status = "omm"
                    mp.init_main_menu()
                    pygame.mixer.Sound("Data\\" + "Music\\" + "death.wav").play()
                elif main_status == 'omm' and event.key == 120:
                    main_status = "wfa"
                    mp.buttons = []
                    pygame.mixer.Sound("Data\\" + "Music\\" + "death.wav").play()
                elif main_status == "wfa" and event.key == 120:
                    running = False
                    pygame.mixer.Sound("Data\\" + "Music\\" + "death.wav").play()
                elif main_status == "nts" and event.key == 120:
                    main_status = "omm"
                elif main_status == "ig-cl":
                    if event.key != 120:
                        mp.tetris.catch(event)
                    else:
                        pygame.mixer.init()
                        pygame.mixer.music.load("Data\\" + "Music\\" + "mt.wav")
                        pygame.mixer.music.play(-1)
                        mp.tetris.terminate()
                        pygame.mixer.Sound("Data\\" + "Music\\" + "death.wav").play()
                        main_status = "gmc"
                        mp.init_selector()
                elif main_status == "ig-bt":
                    if event.key != 120:
                        mp.btris.catch(event)
                    else:
                        pygame.mixer.init()
                        pygame.mixer.music.load("Data\\" + "Music\\" + "mt.wav")
                        pygame.mixer.music.play(-1)
                        pygame.mixer.Sound("Data\\" + "Music\\" + "death.wav").play()
                        mp.btris.terminate()
                        main_status = "gmc"
                        mp.init_selector()
                elif main_status == "ig-wt":
                    if event.key != 120:
                        mp.welltris.catch(event)
                    else:
                        pygame.mixer.init()
                        pygame.mixer.music.load("Data\\" + "Music\\" + "mt.wav")
                        pygame.mixer.music.play(-1)
                        mp.welltris.terminate()
                        main_status = "gmc"
                        mp.init_selector()
            elif event.type == pygame.MOUSEBUTTONUP:
                if main_status == "ig-bt":
                    if following_bt:
                        mp.btris.catch_mbu(event.pos)
                        following_bt = False
                else:
                    try:
                        group = list(mp.buttons)
                    except TypeError:
                        break
                    for i in range(len(list(mp.buttons))):
                        if group[i].stat == 'ps':
                            if group[i].rect.collidepoint(event.pos):
                                if group[i].name != "right" and group[i].name != 'left':
                                    sound = pygame.mixer.Sound("Data\\" + "Music\\" + "bt_ps.wav")
                                    sound.set_volume(volume + 0.02)
                                    sound.play()
                                group[i].change_stat('uw')
                                button_reaction(group[i].name)
                            else:
                                group[i].change_stat('st')
                                sprites = pygame.sprite.Group()
                                for elem in group:
                                    sprites.add(elem)
                                mp.buttons = sprites
            else:
                if mp.buttons is not False and main_status in ['omm', 'gmc']:
                    group = list(mp.buttons)
                    for i in range(len(group)):
                        if group[i].rect.collidepoint(pygame.mouse.get_pos()):
                            group[i].change_stat("uw")
                        else:
                            group[i].change_stat("st")
                    btns = pygame.sprite.Group()
                    for elem in group:
                        btns.add(elem)
                    mp.upload_buttons(btns)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
