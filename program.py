import os
import sys
from random import randint
import pygame

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
ASSIST = ('koleco.png', 'kluch.png', "box.png", "bomb.png")
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
                  "колес,ящики и гаечных ключей",
                  "избегать выезд с полотна",
                  "при нажатие пробела, наступает пауза в игре",
                  "при повторном нажатие на паузу игра продолжатся"]

    fon = pygame.transform.scale(load_image('fon_01.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, BLACK)
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
    image_boom = load_image("boom.png")

    def __init__(self, x, surf, group):
        pygame.sprite.Sprite.__init__
        (self)
        super().__init__(all_sprites)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, 0))
        self.add(group)
        self.speed = randint(1, 5)
        self.www = 0

    def update(self):
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else:
            self.kill()
        if pygame.sprite.spritecollideany(self, my_cars):
            if self.www < 3:
                self.www += 1
                self.image = self.image_boom
            else:
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
        self.www = 0

    def update(self):
        if self.rect.y < HEIGHT:
            self.rect.y += self.speed
        else:
            self.kill()
        if pygame.sprite.spritecollideany(self, my_cars):
            if self.www < 3:
                self.www += 1
                self.image = self.image_boom
            else:
                self.kill()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        print(x1, y1, x2, y2)
        print(x1 + 1, y1 + 1, x2 + 1, y2 + 1)

        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class My_Car(pygame.sprite.Sprite):
    image_boom = load_image("boom.png")

    def __init__(self, x, surf, group):
        pygame.sprite.Sprite.__init__(self)
        super().__init__(all_sprites)
        self.image = surf
        self.original = surf
        self.rect = self.image.get_rect(center=(x, HEIGHT - 30))
        self.add(group)
        self.direction = None

    def function(self):
        if self.direction == 1073741904:
            player.rect.x += 3
        elif self.direction == 1073741903:
            player.rect.x -= 3
        elif self.direction == 1073741906:
            player.rect.y += 3
        elif self.direction == 1073741905:
            player.rect.y -= 3

    def update(self):
        self.image = self.original
        if pygame.sprite.spritecollideany(self, cars):
            self.image = self.image_boom
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.image = self.image_boom
            self.function()
        elif pygame.sprite.spritecollideany(self, vertical_borders):
            self.image = self.image_boom
            self.function()
        else:
            if self.direction == 1073741904:
                motion = LEFT
            elif self.direction == 1073741903:
                motion = RIGHT
            elif self.direction == 1073741906:
                motion = UP
            elif self.direction == 1073741905:
                motion = DOWN


class Over(pygame.sprite.Sprite):
    image = load_image("game2.jpeg")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Over.image
        self.rect = self.image.get_rect()
        self.rect.x = - 600
        self.rect.y = 0


start_screen()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
Border(5, 5, WIDTH - 5, 5)
Border(5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5)
Border(5, 5, 5, HEIGHT - 5)
Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)
cars = pygame.sprite.Group()
my_cars = pygame.sprite.Group()
flowers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
paused = (False, 1)
running = True
Car(randint(1, WIDTH), CARS_SURF[randint(0, 3)], cars)
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
            print(player.rect[0], player.rect[1], player.rect[2], player.rect[3])
            if event.key == pygame.K_LEFT:
                motion = LEFT
            elif event.key == pygame.K_RIGHT:
                motion = RIGHT
            elif event.key == 1073741906:
                motion = UP
            elif event.key == 1073741905:
                motion = DOWN
            if event.key == 32:
                if paused[1] % 2 == 1:
                    paused = (True, 0)
                else:
                    paused = (False, 1)
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, 1073741906, 1073741905]:
                motion = STOP
    if motion == LEFT and player.rect[0] >= 0:
        player.rect.x -= 3
    elif motion == RIGHT and player.rect[0] <= 571:
        player.rect.x += 3
    elif motion == UP and player.rect[1] >= 0:
        player.rect.y -= 3
    elif motion == DOWN and player.rect[1] <= 750:
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