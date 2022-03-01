import os
import sys
import pygame
from random import randint

pygame.init()

pygame.time.set_timer(pygame.USEREVENT, 3000)

WIDTH = 600
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CARS = ('car_01.png', 'car_02.png', 'car_03.png', 'car_04.png', 'car_05.png',
        'car_06.png', 'car_07.png', 'car_08.png', 'car_09.png', 'car_10.png', 'car_11.png')
ASSIST = ('koleco.png', 'kluch.png', "box.png")
CARS_SURF = []
ASSIST_SURF = []
FPS = 50
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
RIGHT = "to the right"
LEFT = "to the left"
DOWN = "to the down"
UP = "to the up"
STOP = "stop"
motion = STOP


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


for i in range(len(CARS)):
    CARS_SURF.append(load_image(CARS[i]))

for i in range(len(ASSIST)):
    ASSIST_SURF.append(load_image(ASSIST[i]))


def start_screen():
    intro_text = ["Игра - гонки на автомобили",
                  "Правила игры:",
                  "Управление машиной происходит с помощью ",
                  "клавиш-стрелок вверх, вниз, влево, вправо",
                  "в ходе игры необходимо избегать сталкновение",
                  "с другими автомашинами, и собирать больше",
                  "колес и гаечных ключей",
                  "при нажатие пробела, наступает пауза в игре",
                  "при повторном нажатие на паузу игра продолжатся"]

    fon = pygame.transform.scale(load_image('grass.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Flowers(pygame.sprite.Sprite):
    image_boom = load_image("bomb.png")

    def __init__(self, x, surf, group):
        super().__init__(all_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.add(group)
        self.speed = randint(1, 5)

    def update(self):
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else:
            self.kill()
        if pygame.sprite.spritecollideany(self, my_cars):
            self.image = self.image_boom
            self.kill()


class Car(pygame.sprite.Sprite):
    image_boom = load_image("boom.png")

    def __init__(self, x, surf, group):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(all_sprites)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.add(group)
        self.speed = randint(1, 5)

    def update(self):
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else:
            self.kill()
        if pygame.sprite.spritecollideany(self, my_cars):
            self.image = self.image_boom


class My_Car(pygame.sprite.Sprite):
    image_boom = load_image("boom.png")

    def __init__(self, x, surf, group):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(all_sprites)
        self.image = surf
        self.original = surf
        self.rect = self.image.get_rect(center=(x, HEIGHT - 10))
        self.add(group)

    def update(self):
        self.image = self.original
        if pygame.sprite.spritecollideany(self, cars):
            self.image = self.image_boom


class Over(pygame.sprite.Sprite):
    image = load_image("game2.jpeg")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Over.image
        self.rect = self.image.get_rect()
        self.rect.x = - 600
        self.rect.y = 0


start_screen()

cars = pygame.sprite.Group()
my_cars = pygame.sprite.Group()
flowers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
paused = (False, 1)
running = True
Car(randint(1, WIDTH), CARS_SURF[randint(0, 2)], cars)
player = My_Car(WIDTH // 2, load_image('my_car_01.png'), my_cars)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            Car(randint(1, WIDTH), CARS_SURF[randint(0, 10)], cars)
            Flowers(randint(1, WIDTH), ASSIST_SURF[randint(0, 2)], flowers)
            Flowers(randint(1, WIDTH), ASSIST_SURF[randint(0, 2)], flowers)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                motion = LEFT
            elif event.key == pygame.K_RIGHT:
                motion = RIGHT
            elif event.key == 1073741906:
                motion = UP
            elif event.key == 1073741905:
                motion = DOWN
            elif event.key == 32:
                if paused[1] % 2 == 1:
                    paused = (True, 0)
                else:
                    paused = (False, 1)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, 1073741906, 1073741905]:
                motion = STOP

    if motion == LEFT:
        player.rect.x -= 3
    elif motion == RIGHT:
        player.rect.x += 3
    elif motion == UP:
        player.rect.y -= 3
    elif motion == DOWN:
        player.rect.y += 3

    if paused[0]:
        pass
    else:
        screen.fill(WHITE)
        all_sprites.draw(screen)
        clock.tick(FPS)
        all_sprites.update()
        pygame.display.flip()

all_sprites_02 = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
game_over = Over(all_sprites_02)
game_over.image = pygame.transform.scale(game_over.image, (600, 300))
clock = pygame.time.Clock()
running = True
clock.tick(FPS)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
            terminate()
    if game_over.rect.x < 0:
        game_over.rect.x += 1
    screen.fill(BLUE)
    all_sprites_02.draw(screen)
    pygame.display.flip()

pygame.quit()