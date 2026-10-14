from pico2d import *
import random


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
GRASS_CENTER_Y = 30


# Game object class here
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(CANVAS_WIDTH // 2, GRASS_CENTER_Y)

    def update(self): pass

class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 3

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

class Zombie:
    def __init__(self):
        self.x, self.y = 0, 170
        self.frame = 0
        self.image = load_image('zombie_run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 10
        self.x += 5

    def draw(self):
        frame_width = self.image.w // 10
        frame_height = self.image.h
        self.image.clip_draw(self.frame * frame_width, 0, frame_width, frame_height, self.x, self.y, frame_width // 2, frame_height // 2)

class Ball:
    def __init__(self, image_name, ground_y):
        self.image = load_image(image_name)
        self.half_width = self.image.w / 2
        self.half_height = self.image.h / 2
        self.start_y = ground_y + self.half_height
        self.x = random.uniform(
            self.half_width, CANVAS_WIDTH - self.half_width
        )
        self.y = self.start_y
        self.rise_speed = random.randint(5, 15)
        self.state = 0

    def update(self):
        if self.state == 0:
            self.y += self.rise_speed
            if self.y >= CANVAS_HEIGHT - self.half_height:
                self.state = 1
        elif self.state == 1:
            self.y -= 2
            if self.y <= CANVAS_HEIGHT - 40:
                self.state = 2
        elif self.state == 2:
            self.y += 2
            if self.y >= CANVAS_HEIGHT - self.half_height:
                self.state = 1   


    def draw(self):
        self.image.draw(self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running
    global world

    running = True
    world = []

    grass = Grass()
    world.append(grass)

    team = [Boy() for i in range(11)]
    world += team

    zombie = Zombie()
    world.append(zombie)

    ground_y = GRASS_CENTER_Y + grass.image.h / 2
    small_balls = [
        Ball('ball21x21.png', ground_y) for _ in range(10)
    ]
    large_balls = [
        Ball('ball41x41.png', ground_y) for _ in range(10)
    ]
    world += small_balls + large_balls


def update_world():
    for o in world:
        o.update()
  

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()