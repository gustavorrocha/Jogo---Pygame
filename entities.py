import pygame
from pygame.locals import *
from random import randint

# Declarando variáveis que serão utilizadas no decorrer do código
unit_square = 32
game_screen = (1*unit_square, 1280 - 10*unit_square, 1*unit_square, 736 - 2*unit_square)


def import_image(image_path, dif_size = 0):
    image_surface = pygame.image.load(image_path)
    image_right_size = pygame.transform.scale(image_surface, (unit_square + dif_size, unit_square + dif_size))
    return image_right_size


class Snake:
    def __init__(self, screen):
        self.screen = screen # Configura a tela em que a cobra aparecerá
        self.x = 10*unit_square # Define a coordenada x da cobra
        self.y = 10*unit_square # Define a coordenada y da cobra
        self.speed = 1/15 # Velocidade da cobra
        self.body_size = 2 # Tamanho do corpo da cobra (excluindo a cabeça)
        self.body = [(10*unit_square, 11*unit_square, "up"), (10*unit_square, 12*unit_square, "up")] # Lista com as coordenadas das partes do corpo da cobra
        self.direction = "right" # Armazena a direção da cobra
        self.direction_cache = "right" # Caso a direção não possa ser mudada, armazena um cache até que seja possível
        self.count_frames = 0 # Cria o contador de frames
        self.head_sprite = import_image("./imgs/snake/cabeca32.png")
        self.body_sprite = import_image("./imgs/snake/corpo32.png")
        self.corner_sprite = import_image("./imgs/snake/curva32.png")
        self.tail_sprite = import_image("./imgs/snake/cauda32.png")
        self.head = self.head_sprite
        self.isdeph = False
        self.draw() # Desenha a cobra
    
    def rotated_sprite(self, num_body):
        # Caso a parte do corpo seja a última, utiliza o sprite da cauda
        if num_body == self.body_size - 1:
            # Rotaciona a cauda de acordo com a direção que a cobra está "apontando"
            if self.body[num_body][2] == "up":
                sprite = self.tail_sprite
            elif self.body[num_body][2] == "left":
                sprite = pygame.transform.rotate(self.tail_sprite, 90)
            elif self.body[num_body][2] == "right":
                sprite = pygame.transform.rotate(self.tail_sprite, -90)
            elif self.body[num_body][2] == "down":
                sprite = pygame.transform.rotate(self.tail_sprite, 180)

        else:
            try:
                # Faz a rotação do sprite do corpo de acordo com as direções armazenadas
                if self.body[num_body][2] in ("up", "down"):
                    sprite = self.body_sprite
                elif self.body[num_body][2]  in ("right", "left"):
                    sprite = pygame.transform.rotate(self.body_sprite, 90)

                # Faz a rotação do sprite da curva do corpo de acordo com as direções armazenadas
                if (self.body[num_body][2] == "up" and self.body[num_body + 1][2] == "right") or (self.body[num_body][2] == "left" and self.body[num_body + 1][2] == "down"):
                    sprite = self.corner_sprite
                elif (self.body[num_body][2] == "down" and self.body[num_body + 1][2] == "right") or (self.body[num_body][2] == "left" and self.body[num_body + 1][2] == "up"):
                    sprite = pygame.transform.rotate(self.corner_sprite, 90)
                elif (self.body[num_body][2] == "right" and self.body[num_body + 1][2] == "down") or (self.body[num_body][2] == "up" and self.body[num_body + 1][2] == "left"):
                    sprite = pygame.transform.rotate(self.corner_sprite, -90)
                elif (self.body[num_body][2] == "right" and self.body[num_body + 1][2] == "up") or (self.body[num_body][2] == "down" and self.body[num_body + 1][2] == "left"):
                    sprite = pygame.transform.rotate(self.corner_sprite, 180)
            except:
                print(self.body)
        
        return sprite

    def draw(self):
        self.screen.blit(self.head, (self.x, self.y)) # Desenha a cabeça da cobra

        # Percorre todos as partes do corpo da cobra
        for num_body in range(self.body_size):
            try:
                body_sprite = self.rotated_sprite(num_body) # Sprite rotacionado da parte do corpo em específico
            except:
                body_sprite = self.body_sprite
            self.screen.blit(body_sprite, (self.body[num_body][0], self.body[num_body][1])) # Desenha o sprite encontrado na tela

    # Altera a direção caso alguma das teclas "wasd" sejam apertadas
    def change_direction(self, key):
        if (key == K_w or key == K_UP) and self.direction != "down":
            self.direction_cache = "up"
        if (key == K_a or key == K_LEFT) and self.direction != "right":
            self.direction_cache = "left"
        if (key == K_s or key == K_DOWN) and self.direction != "up":
            self.direction_cache = "down"
        if (key == K_d or key == K_RIGHT) and self.direction != "left":
            self.direction_cache = "right"

    def move(self):
        self.count_frames += 1 # Incrementa o contador de frames
    
        # Remove as coordenadas antigas que não serã usadas
        while len(self.body) > self.body_size:
            self.body.pop(-1)

        if self.isdeph == False:
            

            # Utiliza o contador de frames para alterar a velocidade da cobra        
            if self.count_frames % round(1/self.speed) == 0:
                self.direction = self.direction_cache # Tenta alterar a direção até que seja viável

                self.body.insert(0, (self.x, self.y, self.direction)) # Adiciona as coordenadas antigas da cabeça da cobra, para que seja utilizada no corpo

                # Movimentação básica da cobra
                if self.direction == "left":
                    if self.x <= game_screen[0] or any(map(lambda t: t[0] == self.x-unit_square and t[1] == self.y, self.body[1:self.body_size])):
                        self.isdeph = True
                        pygame.mixer.Sound("./sounds/snake_dying.mp3").play()
                    else:
                        self.head = pygame.transform.rotate(self.head_sprite, 90) 
                        self.x -= unit_square
                elif self.direction == "right":
                    if self.x >= game_screen[1] or any(map(lambda t: t[0] == self.x and t[1] == self.y, self.body[1:self.body_size])):
                        self.isdeph = True
                        pygame.mixer.Sound("./sounds/snake_dying.mp3").play()
                    else:       
                        self.head = pygame.transform.rotate(self.head_sprite, -90)
                        self.x += unit_square
                elif self.direction == "up":
                    if self.y <= game_screen[2] or any(map(lambda t: t[0] == self.x and t[1] == self.y, self.body[1:self.body_size])):
                        self.isdeph = True
                        pygame.mixer.Sound("./sounds/snake_dying.mp3").play()
                    else: 
                        self.head = self.head_sprite
                        self.y -= unit_square
                elif self.direction == "down":
                    if self.y >= game_screen[3] or any(map(lambda t: t[0] == self.x and t[1] == self.y+unit_square, self.body[1:self.body_size])):
                        self.isdeph = True
                        pygame.mixer.Sound("./sounds/snake_dying.mp3").play()
                    else: 
                        self.head = pygame.transform.rotate(self.head_sprite, 180)
                        self.y += unit_square 
            
        self.draw() # Redesenha a cobra na sua nova posição
         
    def eat_apple(self):
        self.body_size += 1 # Altera o tamanho do corpo, caso a cobra coma uma maça


class Apple:
    def __init__(self, screen, size):
        self.screen = screen
        resolution = self.screen.get_size() # Armazena a resolução da tela
        self.x = randint(game_screen[0], game_screen[1] - unit_square)//unit_square*unit_square # Randomiza a posição x da maçã (utilizando o tamanho do quadrado)
        self.y = randint(game_screen[2], game_screen[3] - unit_square)//unit_square*unit_square # Randomiza a posição y da maçã (utilizando o tamanho do quadrado)
        self.sprite = import_image("./imgs/apple.png") # Sprite da imagem da maçã
        self.draw() # Desenha a maçã

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y)) # Desenha a maçã

class Lumberjack:
    def __init__(self, screen, size):
        self.screen = screen
        resolution = self.screen.get_size() # Armazena a resolução da tela
        self.x = randint(game_screen[0],game_screen[1] - unit_square)//unit_square*unit_square # Randomiza a posição x do lenhador (utilizando o tamanho do quadrado)
        self.y = randint(game_screen[2],game_screen[3] - unit_square)//unit_square*unit_square # Randomiza a posição y do lenhador (utilizando o tamanho do quadrado)
        self.direction = 0 # Armazena a direção do lenhador
        self.speed = 1/30 # Velocidade do lenhador
        self.count_frames = 0 # Cria o contador de frames
        self.is_smart = randint(0,1) # Randomiza se o lenhador será inteligente (irá atrás das maçãs) ou não
        self.effect = randint(0,3) # Adiciona efeitos para a ingestão do lenhador
        self.sprite1 = import_image("./imgs/lumberjack/lumberjack1.png", unit_square//4) # Primeiro sprite da imagem do lenhador
        self.sprite2 = import_image("./imgs/lumberjack/lumberjack2.png", unit_square//4) # Segundo sprite da imagem do lenhador
        self.draw() # Desenha o lenhador

    def draw(self):
        # Define o sprite do lenhador, metade do tempo no primeiro e metade no segundo
        if self.count_frames % round(1/self.speed) < round(1/self.speed)/2:
            sprite = self.sprite1
        else: 
            sprite = self.sprite2

        # Caso a direção do lenhador seja para esquerda, vira a imagem
        if self.direction == 0:
            sprite = pygame.transform.flip(sprite, True, False)

        self.screen.blit(sprite, (self.x - unit_square/4, self.y - unit_square/4)) # Desenha o lenhador
    
    def stay_in_screen(self):
        resolution = self.screen.get_size() # Armazena a resolução da tela

        # Não permite que o lenhador ultrapasse os limites da tela
        if self.x <= game_screen[0] and self.direction == 0:
            self.direction = 1
        elif self.x >= game_screen[1] - unit_square and self.direction == 1:
            self.direction = 0
        if self.y <= game_screen[2] and self.direction == 2:
            self.direction = 3
        elif self.y >= game_screen[3] - unit_square and self.direction == 3:
            self.direction = 2

    def follow_target(self, target):
        # Persegue um objeto alvo
        if target.x < self.x:
            self.direction = 0
        elif target.x > self.x:
            self.direction = 1
        elif target.y < self.y:
            self.direction = 2
        elif target.y > self.y:
            self.direction = 3

    def move(self, apple):
        self.count_frames += 1 # Incremeta o contador de frames

        # Utiliza o contador de frames para fazer com que a movimentação do lenhador seja mais lenta      
        if self.count_frames % round(1/self.speed) == 0:

            if self.is_smart: # Se o lenhador for inteligente, o faz seguir a maçã
                self.follow_target(apple)

            # 1% de chance de alterar a direção do lenhador
            if randint(1,10) == 1:
                self.direction = randint(0,3)
    
            self.stay_in_screen() # Faz com que o lenhador não saia da tela

            # Movimentação básica do lenhador
            if self.direction == 0:
                self.x -= unit_square
            elif self.direction == 1:
                self.x += unit_square
            elif self.direction == 2:
                self.y -= unit_square
            elif self.direction == 3:
                self.y += unit_square

        self.draw() # Redesenha o lenhador na sua nova posição