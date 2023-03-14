# Import the pygame module
import logging
import random
import pygame

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards

from pygame.locals import RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

from math import pi,sin,cos,sqrt


class Player(pygame.sprite.Sprite):
    def __init__(self, idx=0, init_pos=(0,0), init_angle=0.0, speed=100.0, color=(255,10,10),
                 steer_left_key=K_LEFT, steer_right_key=K_DOWN):
        super(Player, self).__init__()
        self.idx = idx
        self.pos = pygame.Vector2(init_pos) # x-position in game world (pixel coordinates)
        self.vel = pygame.Vector2
        self.angle = init_angle # angle of velocity vector
        self.speed = speed # distance travelled per game second
        self.history = [init_pos]
        self.steer_left_key = steer_left_key
        self.steer_right_key = steer_right_key

        # Setup sprite == filled circle
        radius = 5
        self.surf = pygame.Surface((2*radius,2*radius))
        pygame.draw.circle(self.surf, color, (radius,radius), radius, 0)
        self.surf.set_colorkey((0,0,0), RLEACCEL) # set transparent color
        self.rect = self.surf.get_rect(center=self.pos)

    @property
    def vel_vec(self):
        vx = self.speed * cos(self.angle)
        vy = self.speed * sin(self.angle)
        return vx,vy

    def apply_steering(self, pressed_keys, dphi:float):
        if pressed_keys[self.steer_left_key]:
            logging.debug("steering to the left")
            self.angle += dphi
        elif pressed_keys[self.steer_right_key]:
            logging.debug("steering to the right")
            self.angle -= dphi

    # let player move for dt seconds
    def move(self, dt):
        vx, vy = self.vel_vec
        dx = vx * dt
        dy = vy * dt
        self.x += dx # update position
        self.y += dy # update position
        #self.rect.move_ip(dx, dy) # update sprite
        logging.debug(f"moving sprite by ({dx},{dy}) to ({self.x},{self.y})")
        self.history.append((self.x, self.y)) # save history


    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.surf, (self.x, self.y))



# Define the enemy object by extending pygame.sprite.Sprite

# The surface you draw on the screen is now an attribute of 'enemy'


class AchtungDieKurveGame:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.player_speed = 0.1 * self.screen_width # pixels travelled per second
        #self.min_turn_radius = 0.2 * self.screen_width # minimum turn radius in pixels
        self.min_turn_radius = 200  # minimum turn radius in pixels
        self.player_turn_rate = self.player_speed / self.min_turn_radius # turn rate (radians per second)
        self.players = pygame.sprite.Group()
        self.target_fps = 30
        self.dt_per_frame = 1/self.target_fps
        self.dphi_per_frame = self.player_turn_rate * self.dt_per_frame # maximum steering angle per frame
        logging.info(f"dphi_per_frame = {self.dphi_per_frame * 180/pi}")


    def _roll_valid_start_position(self, safety_distance, max_attempts=100):
        attempt_counter = 0
        while attempt_counter < max_attempts:
            x = self.min_turn_radius + (self.screen_width - 2 * self.min_turn_radius) * random.random()
            y = self.min_turn_radius + (self.screen_height - 2 * self.min_turn_radius) * random.random()

            for p in self.players:
                dist = sqrt((x - p.x)**2 + (y - p.y)**2)
                if dist < safety_distance:
                    logging.debug("re-rolling start position")
                    break
            else:
                return x,y

            attempt_counter += 1

        raise RuntimeError("Unable to generate valid start position!")


    def detect_wall_collision(self, player:Player):
        return player.x <= 0 or player.x >= self.screen_width or player.y <= 0 or player.y >= self.screen_height

    def run(self):
        # Initialize pygame
        pygame.init()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Setup game clock
        clock = pygame.time.Clock()

        # Create custom event for adding a new enemy
        #ADDENEMY = pygame.USEREVENT + 1
        #pygame.time.set_timer(ADDENEMY, 500) # spawn new ENEMIES every X ms

        #screen.fill((255, 255, 255))

        # Create player
        #player = Player(init_pos=self._roll_valid_start_position(safety_distance=0.5*self.min_turn_radius))
        player = Player(idx=0, init_pos=(200,400), speed=self.player_speed, init_angle=0.0)

        # Create sprite groups
        self.players.add(player)

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

            # Get key presses
            pressed_keys = pygame.key.get_pressed()

            # Refill screen to remove old player/enemy positions
            #screen.fill((0,0,0))

            for p in self.players:
                # Process player input
                p.apply_steering(pressed_keys, self.dphi_per_frame)
                # Update player positions
                p.move(self.dt_per_frame)
                # Draw player at its current position
                p.draw(screen)
                # Detect wall collisions
                if self.detect_wall_collision(p):
                    logging.info(f"Player {p.idx} hit the walls")
                    p.kill()

            # Check for collisions
            #if pygame.sprite.spritecollideany(player, players):
            #    print("Player was hit!")
            #    player.kill()
            #    running = False

            # Render the display (flip everything to the display)
            pygame.display.flip()

            # Ensure program maintains a rate of 30 frames per second
            clock.tick(self.target_fps)



if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="%(relativeCreated)d %(levelname)s [%(funcName)s:%(lineno)d] - %(message)s")

    game = AchtungDieKurveGame()
    game.run()

