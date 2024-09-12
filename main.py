import pygame
import time
import sys
import random
from pygame.sprite import Sprite, Group
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption('Космический уничтожитель')
bg = pygame.image.load("Images/bg.png")
battle_sound = mixer.Sound('Sounds/battle.ogg')
shot_sound = mixer.Sound('Sounds/shot.ogg')
defeat_sound = mixer.Sound('Sounds/defeat.ogg')
lose_sound = mixer.Sound('Sounds/lose.ogg')
vol = 0.5
sounds = [shot_sound, battle_sound, lose_sound, defeat_sound]


def main_menu():
    global vol
    selected = "Играть"
    mixer.music.load('Sounds/menu.ogg')
    mixer.music.set_volume(vol)
    mixer.music.play(-1, 1)
    while True:
        screen.fill((127, 127, 127))
        screen.blit(bg, (0, 0))
        title = do_text("Космический уничтожитель", 'Cambria', 40, (255, 255, 0))
        volume_text = do_text("Стрелка влево уменьшает звук, "
                              "Стрелка вправо увеличивает звук  "
                              + str(round(vol * 100)) + ' % ', 'Arial', 15, (255, 255, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "Играть"
                elif event.key == pygame.K_DOWN:
                    selected = "Выйти"
                if event.key == pygame.K_RETURN:
                    if selected == "Играть":
                        mixer.music.stop()
                        game()
                    if selected == "Выйти":
                        sys.exit()
                if event.key == pygame.K_LEFT:
                    if 0.1 < vol:
                        vol -= 0.1
                        mixer.music.set_volume(vol)
                        for mus in sounds:
                            mus.set_volume(vol)
                if event.key == pygame.K_RIGHT:
                    if vol <= 0.9:
                        vol += 0.1
                        mixer.music.set_volume(vol)
                        for mus in sounds:
                            mus.set_volume(vol)

        if selected == "Играть":
            text_start = do_text("ИГРАТЬ", None, 75, (255, 255, 255))
        else:
            text_start = do_text("ИГРАТЬ", None, 75, (0, 0, 0))
        if selected == "Выйти":
            text_quit = do_text("ВЫЙТИ", None, 75, (255, 255, 255))
        else:
            text_quit = do_text("ВЫЙТИ", None, 75, (0, 0, 0))
        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()
        volume_rect = volume_text.get_rect()
        screen.blit(title, (600 / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (600 / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (600 / 2 - (quit_rect[2] / 2), 380))
        screen.blit(volume_text, (600 / 2 - (volume_rect[2] / 2), 650))
        pygame.display.update()


def game():
    gun = Gun(screen)
    stats = Stats()
    bullets = Group()
    aliens = Group()
    hearts = Group()
    create_army(screen, aliens, gun, stats)
    create_heart(screen, stats, hearts)
    battle_sound.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    gun.move_right = True
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    gun.move_left = True
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet(gun, screen)
                    stats.rand = random.randint(0, 9)
                    bullets.add(bullet)
                    shot_sound.play()
                elif event.key == pygame.K_r:
                    game()
                elif event.key == pygame.K_q:
                    main_menu()
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    gun.move_right = False
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    gun.move_left = False
        screen.fill((0, 0, 0))
        update(screen, gun, bullets, aliens, stats, hearts)
        hit(screen, bullets, aliens, gun, stats)
        defeat(screen, aliens, gun, bullets, stats, hearts)
        pygame.display.update()
        if stats.end_screen:
            lose_sound.play()
            while stats.end_screen:
                screen.fill((0, 0, 0))
                screen.blit(bg, (0, 0))
                game_over_text = do_text("Ты проиграл", 'Cambria', 80, (255, 0, 0))
                game_over_text2 = do_text("Нажми Q, если хочешь вернуться в главное меню", 'Arial', 30, (255, 0, 0))
                game_over_text3 = do_text("Нажми R, "
                                          "если хочешь начать играть сначала", 'Arial', 30, (255, 0, 0))
                game_over_text4 = do_text("Счёт : " + str(stats.score) +
                                          "  Рекорд : " + str(stats.high_score), 'Arial', 30, (255, 0, 0))
                game_over_rect = game_over_text.get_rect()
                game_over_rect2 = game_over_text2.get_rect()
                game_over_rect3 = game_over_text3.get_rect()
                game_over_rect4 = game_over_text4.get_rect()
                screen.blit(game_over_text, (600 / 2 - (game_over_rect[2] / 2), 100))
                screen.blit(game_over_text2, (600 / 2 - (game_over_rect2[2] / 2), 270))
                screen.blit(game_over_text3, (600 / 2 - (game_over_rect3[2] / 2), 320))
                screen.blit(game_over_text4, (600 / 2 - (game_over_rect4[2] / 2), 370))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game()
                        if event.key == pygame.K_q:
                            main_menu()
                pygame.display.update()


class Gun():

    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('Images/gun.png')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.move_right = self.move_left = False

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += 3
        elif self.move_left and self.rect.left > self.screen_rect.left:
            self.rect.centerx -= 3


class Bullet(Sprite):

    def __init__(self, gun, screen):
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 6, 10)
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top

    def update(self):
        self.rect.y -= 10

    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect)


class Alien(Sprite):

    def __init__(self, screen, stats):
        super(Alien, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('Images/alien.png')
        self.rect = self.image.get_rect()
        self.y = float(self.rect.y)
        self.speed = float((0.12 * (stats.round / 5)) + 0.08)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y


class Heart(Sprite):

    def __init__(self, screen):
        super(Heart, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('Images/heart.png')
        self.rect = self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, self.rect)

class Stats():
    def __init__(self):
        self.end_screen = False
        self.lifes = 3
        self.score = 0
        self.round = 1
        self.rand = 1
        self.penetration = 3
        with open('Рекорд.txt', 'r') as file:
            self.high_score = int(file.readline())


def update(screen, gun, bullets, aliens, stats, hearts):
    for bullet in bullets.sprites():
        bullet.draw()
    gun.draw()
    aliens.draw(screen)
    hearts.draw(screen)
    gun.update()
    bullets.update()
    aliens.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    scores(screen, stats)


def create_heart(screen, stats, hearts):
    for N_heart in range(stats.lifes):
        heart = Heart(screen)
        heart.rect.x = 5 + N_heart * heart.rect.width
        heart.rect.y = 5
        hearts.add(heart)


def create_army(screen, aliens, gun, stats):
    alien = Alien(screen, stats)
    num_x = (600 - 2 * alien.rect.width) // alien.rect.width
    num_y = (((700 - 2 * alien.rect.width - gun.rect.height) // alien.rect.height) - 1) // 2
    for Row_alien in range(num_y):
        for N_alien in range(num_x):
            alien = Alien(screen, stats)
            alien.rect.x = alien.rect.width + alien.rect.width * N_alien
            alien.y = alien.rect.height + alien.rect.height * Row_alien * 2
            alien.rect.y = alien.y
            aliens.add(alien)


def kill_gun(screen, stats, aliens, bullets, gun, hearts):
    if stats.lifes > 1:
        stats.lifes -= 1
        defeat_sound.play()
        bullets.empty()
        hearts.empty()
        aliens.empty()
        create_heart(screen, stats, hearts)
        create_army(screen, aliens, gun, stats)
        gun.rect.centerx = gun.screen_rect.centerx
        time.sleep(1)
    else:
        bullets.empty()
        hearts.empty()
        aliens.empty()
        stats.end_screen = True


def hit(screen, bullets, aliens, gun, stats):
    if stats.rand != 0:
        coll = pygame.sprite.groupcollide(bullets, aliens, True, True)
    else:
        coll = pygame.sprite.groupcollide(bullets, aliens, False, True)
        for aliens in coll.values():
            stats.penetration -= 1
            if stats.penetration == 0:
                bullets.empty()
                stats.penetration = 3
                break
    if coll:
        for aliens in coll.values():
            stats.score += 10 * len(aliens)
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            with open('Рекорд.txt', 'w') as file:
                file.write(str(stats.high_score))
    if len(aliens) == 0:
        bullets.empty()
        create_army(screen, aliens, gun, stats)
        stats.round += 1


def defeat(screen, aliens, gun, bullets, stats, hearts):
    screen_rect = screen.get_rect()
    if pygame.sprite.spritecollideany(gun, aliens):
        kill_gun(screen, stats, aliens, bullets, gun, hearts)
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            kill_gun(screen, stats, aliens, bullets, gun, hearts)
            break


def do_text(message, textFont, textSize, textColor):
    newFont = pygame.font.SysFont(textFont, textSize)
    return newFont.render(message, False, textColor)


def scores(screen, stats):
    screen_rect = screen.get_rect()
    score_text = do_text('Счёт: ' + str(stats.score), 'Arial', 20, (140, 195, 74))
    high_score_text = do_text('Рекорд: ' + str(stats.high_score), 'Arial', 20, (140, 195, 74))
    round_text = do_text('Раунд ' + str(stats.round), 'Arial', 20, (140, 195, 74))
    score_rect = score_text.get_rect()
    high_score_rect = high_score_text.get_rect()
    round_rect = round_text.get_rect()
    score_rect.right = screen_rect.right - 48
    high_score_rect.right = score_rect.left - 48
    round_rect.right = high_score_rect.left - 48
    score_rect.top = 0
    high_score_rect.top = 0
    round_rect.top = 0
    screen.blit(score_text, score_rect)
    screen.blit(high_score_text, high_score_rect)
    screen.blit(round_text, round_rect)


main_menu()
