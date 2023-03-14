# Import the pygame module
import random

import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

from pygame.locals import RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT

class Player(pygame.sprite.Sprite):
    def __init__(self, init_pos=(0,0)):
        super(Player, self).__init__()
        radius = 10
        lw = 2
        self.surf = pygame.Surface((2*(radius+lw),2*(radius+lw)))
        pygame.draw.circle(self.surf, (255,10,10), (radius+lw,radius+lw), radius, 2)
        self.surf.set_colorkey((255,255,255), RLEACCEL) # set transparent color
        self.rect = self.surf.get_rect(center=init_pos)

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            print("up")
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            print("down")
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            print("left")
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            print("right")
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object by extending pygame.sprite.Sprite

# The surface you draw on the screen is now an attribute of 'enemy'

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        init_pos = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                    random.randint(0, SCREEN_HEIGHT))
        self.rect = self.surf.get_rect(center=init_pos)
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup game clock
clock = pygame.time.Clock()
target_fps = 60

# Create custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500) # spawn new ENEMIES every X ms

#screen.fill((255, 255, 255))

# Create player
player = Player(init_pos=(200,SCREEN_HEIGHT/2))

# Create sprite groups
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True
# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Get key presses
    pressed_keys = pygame.key.get_pressed()

    # Update player position
    player.update(pressed_keys)

    # Update enemy positions
    enemies.update() # calls 'update' method for each enemy

    # Refill screen to remove old player/enemy positions
    screen.fill((0,0,0))

    # Draw sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check for collisions
    if pygame.sprite.spritecollideany(player, enemies):
        print("Player was hit!")
        player.kill()
        running = False

    # Render the display (flip everything to the display)
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(target_fps)

