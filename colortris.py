import pygame
import random

pygame.init()

# dá o nome na janela do jogo
pygame.display.set_caption("Colortris!")

# define a janela
res = (700,1000)
screen = pygame.display.set_mode(res)

# define a fonte a usar
font1_size = 60
font2_size = 30 
font1 = pygame.font.SysFont("NotoSans-Regular.ttf", font1_size)
font2 = pygame.font.SysFont("NotoSans-Regular.ttf", font2_size)

# define o texto a escrever com anti-alising
my_text = font1.render("Colortris", True, (255, 255, 0))

# tamanho o círculo
circle_r = res[0]/(2*7)
circle_t = 15

X = [1*circle_r, 3*circle_r, 5*circle_r, 7*circle_r, 9*circle_r, 11*circle_r, 13*circle_r]

# janela dividida em pistas verticais para deteção de colisões
YMAX = [res[1], res[1], res[1], res[1], res[1], res[1], res[1]]

# gere colisões reduzindo altura disponível em cada pista
def collision(curr_circle):
    lane = get_lane(curr_circle)
    bottom = YMAX[lane]
    if get_y(curr_circle) >= bottom - circle_r:
        set_y(curr_circle, bottom - circle_r)
        accumulated_circles.append(curr_circle)
        YMAX[lane] -= 2*circle_r
        return True
    else: return False

def find_line():
    for c1 in accumulated_circles:
        for c2 in accumulated_circles:
            if c1 == c2: continue
            for c3 in accumulated_circles:
                if c2 == c3 or c1 == c3: continue
                # linha horizontal?
                if get_y(c1) == get_y(c2) == get_y(c3) and \
                   get_color(c1) == get_color(c2) == get_color(c3):
                    x_max = max(get_x(c1), get_x(c2), get_x(c3))
                    x_min = min(get_x(c1), get_x(c2), get_x(c3))
                    if x_max - x_min == 4*circle_r:
                        return c1, c2, c3
                # linha vertical?
                if get_x(c1) == get_x(c2) == get_x(c3) and \
                   get_color(c1) == get_color(c2) == get_color(c3):
                    y_max = max(get_y(c1), get_y(c2), get_y(c3))
                    y_min = min(get_y(c1), get_y(c2), get_y(c3))
                    if y_max - y_min == 4*circle_r:
                        return c1, c2, c3
    return None

def update_score():    
    global score
    circles_inline = find_line()
    if circles_inline != None: 
        score += 1
        del_circles(circles_inline[0])
        del_circles(circles_inline[1])
        del_circles(circles_inline[2])

def get_lane(circle):
    return X.index(get_x(circle))

def del_circles(c1):
    ''' updates accumulated_circles YMAX and adjusts down the circles above c1 '''
    accumulated_circles.remove(c1)
    lane = get_lane(c1)
    YMAX[lane] += 2*circle_r
    for c in accumulated_circles:
        if get_x(c1) == get_x(c) and get_y(c1) > get_y(c):
            increment_y(c, 2*circle_r)      # adjusting down circle c
    

def rand_x():
    return random.choice(X)

# velocidade de queda inicial
vy_ini = 5
# velocidade de queda atual
vy = vy_ini
vy_level = vy_ini

# acelaração quando carrega na tecla down
dvy = vy_ini*2

# framerate
delay_period = 15

score = 0
score_level = 0
level_jump = 5
level = 0

cores = [(255, 0, 0), (255, 255, 0), (0, 0, 255), (0, 255, 0)]

def rand_color():
    return random.choice(cores)

def rand_circle():
    return {'xy': [rand_x(), circle_r], 'c': rand_color()}

def get_x(circle):
    return circle['xy'][0]

def get_y(circle):
    return circle['xy'][1]

def increment_y(circle, dy):
    circle['xy'][1] += dy

def get_color(circle):
    return circle['c']

def set_x(circle, x):
    circle['xy'][0] = x

def set_y(circle, y):
    circle['xy'][1] = y


# curr_circle = {'xy': [100, 900], 'c': rand_color()}
def draw_circle(circle):
    pygame.draw.circle(screen, circle['c'], circle['xy'], circle_r, circle_t)

accumulated_circles = []

def draw_accu_circles():
    for c in accumulated_circles:
        draw_circle(c)

def game_status():
    global level, score
    score_text_highlight = font2.render(f"SCORE: {score}", True, (100, 255, 100))
    screen.blit(score_text_highlight, (10 - 1, res[1] - font2_size - 1))
    score_text = font2.render(f"SCORE: {score}", True, (255, 0, 255))
    screen.blit(score_text, (10, res[1] - font2_size))
    score_level_highlight = font2.render(f"Level: {level}", True, (100, 255, 100))
    screen.blit(score_level_highlight, (res[0] / 2 - 1, res[1] - font2_size - 1))
    score_level = font2.render(f"Level: {level}", True, (255, 0, 255))
    screen.blit(score_level, (res[0] / 2, res[1] - font2_size))


def game_loop():
    
    global vy, vy_level, level

    curr_circle = rand_circle()

    while(True):
        level = score // level_jump
        vy_level = vy_ini + level

        if 0 in YMAX: break           # game over?

        pygame.time.delay(delay_period)

        # cor de fundo do ecrã
        screen.fill((0,0,20))

        # dá exit ao jogo
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
            
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_LEFT:
                    lane = get_lane(curr_circle)
                    if lane > 0:
                        lane -= 1
                        set_x(curr_circle, X[lane])
                if event.key == pygame.K_RIGHT:
                    lane = get_lane(curr_circle)
                    if lane < len(X) - 1:
                        lane += 1
                        set_x(curr_circle, X[lane])
                if event.key == pygame.K_DOWN:
                    vy += dvy
                else:
                    vy = vy_level
            else:
                vy = vy_level              


        draw_circle(curr_circle)
        draw_accu_circles()

        increment_y(curr_circle, vy)
        
        if collision(curr_circle):
            update_score()
            curr_circle = rand_circle()

        game_status()
        pygame.display.update()

    
        
    # bye_text = font1.render("Game Over!", True, (255, 0, 255))
    # screen.blit(bye_text, (200, 120))
    screen.fill((0,0,0))

    # dá update do buffer
    pygame.display.update()

    pygame.time.delay(2000)


    
if __name__ == '__main__':
    game_loop()