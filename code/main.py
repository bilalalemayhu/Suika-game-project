import pygame
import random

pygame.init()

class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, points, speed_x=0, speed_y=0):
        super().__init__()
        self.size = size
        self.color = color
        self.points = points
        self.speed_y = speed_y
        self.speed_x = speed_x
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.falling = False
        self.has_stopped = False
        self.fell = False
        self.bounce_factor = 0.7
        self.merged = False
        self.bounce_count = 0

    def update(self):
        global spawn
        
        if self.merged or self.has_stopped:
            return 
        
        jar_thickness = 10
        
        if self.falling:
            self.speed_y += gravity
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x

            if self.rect.left <= jar.rect.left + jar_thickness or self.rect.right >= jar.rect.right - jar_thickness:
                if self.bounce_count > 3:
                    self.speed_x = -self.speed_x * self.bounce_factor
                    self.bounce_count += 1
                    if self.rect.left <= jar.rect.left + jar_thickness:
                        self.rect.left = jar.rect.left + jar_thickness
                    elif self.rect.right >= jar.rect.right - jar_thickness:
                        self.rect.right = jar.rect.right - jar_thickness
                else:
                    self.stop_fruit()

            if self.rect.bottom >= jar.rect.bottom - jar_thickness:
                self.rect.bottom = jar.rect.bottom - jar_thickness
                if abs(self.speed_y) > 0.1:
                    self.speed_y = -self.speed_y * self.bounce_factor
                elif abs(self.s):
                    self.stop_fruit()
            else:
                collided_fruits = pygame.sprite.spritecollide(self, fruit_group, False)
                for fruit in collided_fruits:
                    if fruit != self:
                        if self.points != fruit.points:
                            self.bounce(fruit)
                        elif fruit.has_stopped and not self.merged:
                            self.rect.bottom = fruit.rect.top
                            self.stop_fruit()
                            self.merge(fruit)
                            break

        elif not self.fell:
            if not self.merged:
                mouse_x, _ = pygame.mouse.get_pos()
                jar_left_limit = jar.rect.left + jar_thickness
                jar_right_limit = jar.rect.right - self.rect.width - jar_thickness
                self.rect.x = max(jar_left_limit, min(mouse_x - self.rect.width // 2, jar_right_limit))

    def stop_fruit(self):
        self.speed_y = 0
        self.speed_x = 0
        self.falling = False
        self.has_stopped = True
        self.fell = True  
        self.merged = True

    def start_fall(self):
        self.falling = True

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def merge(self, other_fruit):
        global fruit_types, score
        if self.points == other_fruit.points:
            next_fruit_index = next(
                (index for index, fruit in enumerate(fruit_types) if fruit['points'] == self.points), 
                None
            )
            if next_fruit_index is not None and next_fruit_index + 1 < len(fruit_types):
                next_fruit = fruit_types[next_fruit_index + 1]

                merge_x = (self.rect.centerx + other_fruit.rect.centerx) // 2
                merge_y = (self.rect.centery + other_fruit.rect.centery) // 2

                jar_bottom = jar.rect.bottom - 10
                merge_y = max(merge_y, jar_bottom - next_fruit['size'] - 10)

                jar_left_limit = jar.rect.left + 10
                jar_right_limit = jar.rect.right - next_fruit['size'] - 10

                merge_x = max(jar_left_limit, min(merge_x, jar_right_limit))

                while self.check_collision(merge_x, merge_y, next_fruit['size']):
                    merge_x += random.choice([-10, 10])
                    merge_y += random.choice([-10, 10])

                merged_fruit = Fruit(
                    merge_x, merge_y, 
                    next_fruit['size'], next_fruit['color'], next_fruit['points'],
                    speed_x=random.choice([-3, 3]),  
                    speed_y=-5  
                )
                fruit_group.add(merged_fruit)
                fruit_group.remove(self)
                fruit_group.remove(other_fruit)

                score += self.points * 2

                self.merged = True
                other_fruit.merged = True
                merged_fruit.merged = True 

                merged_fruit.start_fall()

    def check_collision(self, x, y, size):
        test_rect = pygame.Rect(x, y, size, size)
        for fruit in fruit_group:
            if test_rect.colliderect(fruit.rect):
                return True
        if not jar.rect.colliderect(test_rect):
            return True
        return False

    def bounce(self, other_fruit):
        if self.rect.colliderect(other_fruit.rect):
            self.speed_x = -self.speed_x * self.bounce_factor
            other_fruit.speed_x = -other_fruit.speed_x * self.bounce_factor

            self.speed_y = -self.speed_y * self.bounce_factor
            other_fruit.speed_y = -other_fruit.speed_y * self.bounce_factor

            if self.rect.bottom > other_fruit.rect.top:
                self.rect.bottom = other_fruit.rect.top
            else:
                self.rect.top = other_fruit.rect.bottom

            if abs(self.speed_y) < 1 and abs(self.speed_x) < 1:
                self.stop_fruit()
                other_fruit.stop_fruit()


class Jar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(200, 100, 400, 500)
        self.black = (0, 0, 0)
        
    def update(self):
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.black, self.rect, 10)
        pygame.draw.line(screen, background_color, (200, 104), (600, 104), 10)


width = 800
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Suika Game')

gravity = 0.5
background_color = (255, 224, 173)
spawn_timer = 0
spawn_interval = 2000  # Spawn interval in milliseconds
running = True
game_active = False

score = 0
fruit_group = pygame.sprite.Group()
jar = Jar()

fruit_types_spawn = [
    {'size': 20, 'color': (255, 0, 0), 'points': 1},
    {'size': 30, 'color': (0, 255, 0), 'points': 2},
    {'size': 40, 'color': (0, 0, 255), 'points': 4},
    {'size': 50, 'color': (255, 255, 0), 'points': 8},
    {'size': 60, 'color': (255, 165, 0), 'points': 16},
]

fruit_types = [
    {'size': 20, 'color': (255, 0, 0), 'points': 20},    # Rød frukt
    {'size': 30, 'color': (0, 255, 0), 'points': 25},    # Grønn frukt
    {'size': 40, 'color': (0, 0, 255), 'points': 30},    # Blå frukt
    {'size': 50, 'color': (255, 255, 0), 'points': 35},  # Gul frukt
    {'size': 60, 'color': (255, 165, 0), 'points': 40},  # Oransje frukt
    {'size': 70, 'color': (128, 0, 128), 'points': 45},  # Lilla frukt
    {'size': 80, 'color': (255, 192, 203), 'points': 50},# Rosa frukt
    {'size': 90, 'color': (0, 255, 255), 'points': 55},  # Cyan frukt
    {'size': 100, 'color': (0, 128, 0), 'points': 60},   # Mørk grønn frukt
    {'size': 110, 'color': (128, 128, 0), 'points': 65}, # Oliven frukt
    {'size': 120, 'color': (128, 0, 0), 'points': 75}    # Mørk rød frukt
]

def start_screen():
    font = pygame.font.SysFont('Arial', 50)
    title_text = font.render('Welcome to Suika Game', True, (0, 0, 0))
    start_text = font.render('Press SPACE to Start', True, (0, 0, 0))

    while not game_active:
        screen.fill(background_color)
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 100))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 + 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        pygame.display.flip()
        clock.tick(60)

game_active = start_screen()


while running:
    screen.fill(background_color)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_active:
        all_fruits_stopped = all(fruit.has_stopped for fruit in fruit_group)

 
        if all_fruits_stopped:
                print(3)
                fruit_type = random.choice(fruit_types_spawn)
                fruit = Fruit(random.randint(200, 550), 0, fruit_type['size'], fruit_type['color'], fruit_type['points'])
                fruit_group.add(fruit)
                score += fruit_type['points']

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            for fruit in fruit_group:
                if not fruit.falling and not fruit.has_stopped and not fruit.merged:
                    fruit.start_fall()

        jar.update()
        jar.draw(screen)

        fruit_group.update()
        fruit_group.draw(screen)

        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    clock.tick(120)
    pygame.display.flip()

pygame.quit()
