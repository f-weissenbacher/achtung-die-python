import pygame 
from math import sin, cos, pi
import random


speed = 0.45
dtheta = 0.3

radius = 5
path_radius = 5

screen_size = (5*240,5*180)

p1_color = (255,255,255)
p2_color = (0,255,255)
p1_path_color = (255,255,0)
p2_path_color = (255,0,255)

BLACK = (0,0,0)





def main():
    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    running = True


    empty_path_change = 0.0005

    empty_time_max = int(50/speed)
    empty_time_min = int(empty_time_max/4.)

    p1_timeout = 0
    p2_timeout = 0

    p1_time_limit = 0
    p2_time_limit = 0


    p1_draw_empty = False
    p2_draw_empty = False

    p1_pos = [random.randint(10,screen_size[0]), random.randint(10,screen_size[1])]#[32,32]
    p2_pos = [random.randint(10,screen_size[0]), random.randint(10,screen_size[1])]#[64,64]

    
    p1_theta = choose_angle(p1_pos)#2*pi*random.random()
    p2_theta = choose_angle(p2_pos)#2*pi*random.random()

    p1_path = []
    p2_path = []
    

    while running:
        #screen.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    p1_theta += dtheta
                if event.key == pygame.K_RIGHT:
                    p1_theta -= dtheta

                if event.key == pygame.K_q:
                    p2_theta += dtheta
                if event.key == pygame.K_w:
                    p2_theta -= dtheta

           

        
        """
        keys_pressed = pygame.key.get_pressed()

        
        if keys_pressed[pygame.K_LEFT]:
            p1_theta += dtheta
        elif keys_pressed[pygame.K_RIGHT]:
            p1_theta -= dtheta

        if keys_pressed[pygame.K_q]:
            p2_theta += dtheta
        elif keys_pressed[pygame.K_w]:
            p2_theta -= dtheta
        """


        if random.random() < empty_path_change and not p1_draw_empty:
            p1_draw_empty = True
            p1_time_limit = random.randint(empty_time_min,empty_time_max)
            p1_timeout = 0

        if random.random() < empty_path_change and not p2_draw_empty:
            p2_draw_empty = True
            p2_time_limit = random.randint(empty_time_min,empty_time_max)
            p2_timeout = 0


        if p1_draw_empty and p1_timeout <= p1_timeout:
            draw_player(BLACK, [int(p1_pos[0]), int(p1_pos[1])], screen)
            p1_timeout += 1
            if p1_timeout > p1_time_limit:
                p1_draw_empty = False
        else:
            draw_player(p1_path_color, [int(p1_pos[0]), int(p1_pos[1])], screen)
        

        if p2_draw_empty and p2_timeout <= p2_timeout:
            draw_player(BLACK, [int(p2_pos[0]), int(p2_pos[1])], screen)
            p2_timeout += 1
            if p2_timeout > p2_time_limit:
                p2_draw_empty = False
        else:
            draw_player(p2_path_color, [int(p2_pos[0]), int(p2_pos[1])], screen)
        


        
        

        p1_pos = update_pos(p1_theta, p1_pos)
        p2_pos = update_pos(p2_theta, p2_pos)


        draw_player(p1_color, [int(p1_pos[0]), int(p1_pos[1])], screen)
        draw_player(p2_color, [int(p2_pos[0]), int(p2_pos[1])], screen)
        
        #pygame.display.update()
        pygame.display.flip()


        if check_border(p1_pos) or check_path_collision(p1_path, p2_path, p1_pos):
            print("player 1 lost")
            running = False
        elif check_border(p2_pos) or check_path_collision(p1_path, p2_path, p2_pos):
            print("player 2 lost")
            running = False
        if not p1_draw_empty:
            p1_path = add_to_path(p1_path,p1_pos)
        if not p2_draw_empty:
            p2_path = add_to_path(p2_path,p2_pos)


def draw_player(color, center, surface):
    pygame.draw.circle(surface, color, center, radius)

def draw_path(path, screen, color):
    for point in path:
        pygame.draw.circle(screen, color, [int(point[0]), int(point[1])],path_radius)
    

def update_pos(angle, pos):
    pos[0] += speed*sin(angle)
    pos[1] += speed*cos(angle)

    return pos

def add_to_path(path, pos):
    int_pos = [int(pos[0]), int(pos[1])]
    if int_pos not in path:
        path.append(int_pos)
    
    return path

def check_border(pos):
    if pos[0]+radius > screen_size[0] or pos[0]-radius < 0:
        return True
    elif pos[1]+radius > screen_size[1] or pos[1]-radius < 0:
        return True
    else:
        return False

def check_path_collision(path1, path2, pos):
    int_pos = [int(pos[0]), int(pos[1])]

    if int_pos in path1[:-2] or int_pos in path2[:-2]:
        return True
    else:
        return False


def choose_angle(pos):
    angle = 0
    factor = 0.5*(-.5+random.random())
    if pos[0] < screen_size[0]/2. and pos[1] < screen_size[1]/2.:
        angle = 0.25*pi + factor
    elif pos[0] < screen_size[0]/2. and pos[1] > screen_size[1]/2.:
        angle = 0.75*pi + factor
    elif pos[0] > screen_size[0]/2. and pos[1] > screen_size[1]/2.:
        angle = 1.25*pi + factor
    elif pos[0] > screen_size[0]/2. and pos[1] < screen_size[1]/2.:
        angle = 1.75*pi + factor

    return angle
if __name__ == "__main__":
    main()