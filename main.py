import pygame
from pygame.locals import *
from random import randint

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
        self.body_size = 0 # Tamanho do corpo da cobra (excluindo a cabeça)
        self.body = [] # Lista com as coordenadas das partes do corpo da cobra
        self.direction = "" # Armazena a direção da cobra
        self.direction_cache = "" # Caso a direção não possa ser mudada, armazena um cache até que seja possível
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
            body_sprite = self.rotated_sprite(num_body) # Sprite rotacionado da parte do corpo em específico
            self.screen.blit(body_sprite, (self.body[num_body][0], self.body[num_body][1])) # Desenha o sprite encontrado na tela

    # Altera a direção caso alguma das teclas "wasd" sejam apertadas
    def change_direction(self, key):
        if key == K_w and self.direction != "down":
            self.direction_cache = "up"
        if key == K_a and self.direction != "right":
            self.direction_cache = "left"
        if key == K_s and self.direction != "up":
            self.direction_cache = "down"
        if key == K_d and self.direction != "left":
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
                    else:
                        self.head = pygame.transform.rotate(self.head_sprite, 90) 
                        self.x -= unit_square
                elif self.direction == "right":
                    if self.x >= game_screen[1] or any(map(lambda t: t[0] == self.x and t[1] == self.y, self.body[1:self.body_size])):
                        self.isdeph = True
                    else:       
                        self.head = pygame.transform.rotate(self.head_sprite, -90)
                        self.x += unit_square
                elif self.direction == "up":
                    if self.y <= game_screen[2] or any(map(lambda t: t[0] == self.x and t[1] == self.y, self.body[1:self.body_size])):
                        self.isdeph = True
                    else: 
                        self.head = self.head_sprite
                        self.y -= unit_square
                elif self.direction == "down":
                    if self.y >= game_screen[3] or any(map(lambda t: t[0] == self.x and t[1] == self.y+unit_square, self.body[1:self.body_size])):
                        self.isdeph = True
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
        self.effect = randint(0,1) # Adiciona efeitos para a ingestão do lenhador
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

class Game:
    def __init__(self, resolution):
        pygame.init() # Inicia o módulo pygame
        self.screen = pygame.display.set_mode(resolution, pygame.RESIZABLE|pygame.DOUBLEBUF) # Define a resolução do jogo
        self.screen.fill((0,200,0)) # Preenche o background com a cor preta
        self.snake = Snake(self.screen) # Cria o objeto COBRA
        self.apple = Apple(self.screen, unit_square) # Cria o objeto MAÇÃ
        self.lumberjack = Lumberjack(self.screen, unit_square) # Cria o objeto LENHADOR
        self.font = pygame.font.SysFont("comicsans", 30, True) # Define a fonte dos textos
        self.current_effects = {} # Dicionário com todos os efeitos que estão ocorrendo
        self.fps = 60 # Define o FPS do jogo para 60
        self.score = 0 # Cria um atributo de pontuação
        self.state = "running"

    def apply_effects(self, speed):
        self.snake.speed = speed # Reseta a velocidade da cobra 

        # Percorre todos os efeitos atuais
        for effect in self.current_effects:
            # Roda o efeito caso ainda exista duração
            if self.current_effects[effect] > 0: 
                if effect == "faster": 
                    self.snake.speed = speed*3/2
                elif effect == "slower":
                    self.snake.speed = speed/2
                self.current_effects[effect] -= 1 # Atualiza a duração do efeito

    

    def run(self):
        running = True
        clock = pygame.time.Clock() # Cria um objeto de relógio
        
        while running:
            clock.tick(self.fps) 
            if self.state == "pause":
                for event in pygame.event.get():
                    if event.type == QUIT: # Sai do jogo caso o jogador o feche
                        running = False

                    if event.type == KEYDOWN: # Obtém todas as teclas pressionadas
                        self.snake.change_direction(event.key) # Altera a direção da cobra com os respectivos comandos
                        if event.key == K_ESCAPE:
                            self.state = "running"
                continue
            self.screen.fill((0,200,0)) # Preenche a tela com um retângulo preto (para atualizar as posições)
            pygame.draw.rect(self.screen, (150,75,0), (game_screen[0], game_screen[2], game_screen[1], game_screen[3]))
                

            resolution = self.screen.get_size() # Armazena a resolução da tela 
            self.screen.blit(self.font.render("Pontuação: " + str(self.score), 1, (255,255,255)), (resolution[0] - 250,10)) # Escreve a pontuação na tela

            self.apply_effects(1/5)
            self.apple.draw() # Desenha a maça
            self.lumberjack.move(self.apple) # Roda a movimentação do lehador
            self.snake.move() # Roda a função para a cobra se mover

            for event in pygame.event.get():
                if event.type == QUIT: # Sai do jogo caso o jogador o feche
                    running = False

                if event.type == KEYDOWN: # Obtém todas as teclas pressionadas
                    self.snake.change_direction(event.key) # Altera a direção da cobra com os respectivos comandos
                    if event.key == K_ESCAPE:
                        self.state = "pause"

            # Condicional da cobra passar pela maçã
            if (self.snake.x,self.snake.y) == (self.apple.x, self.apple.y):
                del self.apple # Remove a maça
                pygame.mixer.Sound("./sounds/eating_apple.mp3").play()
                self.score += 1 # Adiciona 1 à pontuação
                self.snake.body_size += 1 # Adiciona 1 ao corpo da cobra
                self.apple = Apple(self.screen, unit_square) # Cria uma nova maça na tela
                if randint(0,1):
                    pygame.mixer.Sound("./sounds/appear_apple1.mp3").play()
                else:
                    pygame.mixer.Sound("./sounds/appear_apple2.mp3").play()

            # Condicional do lenhador passar pela maçã
            if (self.apple.x,self.apple.y) == (self.lumberjack.x, self.lumberjack.y):
                del self.apple # Remove a maça
                self.score -= 1 # Remove 1 da pontuação
                self.apple = Apple(self.screen, unit_square) # Cria uma nova maça na tela

            # Condicional da cobra passar pelo lenhador
            if (self.snake.x,self.snake.y) == (self.lumberjack.x, self.lumberjack.y):

                # Adiciona o efeito do lenhador
                if self.lumberjack.effect == 0:
                    self.current_effects["faster"] = 2*self.fps # Deixar a cobra mais lenta
                elif self.lumberjack.effect == 1:
                    self.current_effects["slower"] = 2*self.fps # Deixar a cobra mais rápida
    
                del self.lumberjack # Remove o lenhador
                pygame.mixer.Sound("./sounds/eating_lumberjack.mp3").play()
                self.score += 1 # Adiciona 1 à pontuação
                self.lumberjack = Lumberjack(self.screen, unit_square) # Cria um novo lenhador na tela

            pygame.display.update() # Atualiza a tela


if __name__  == "__main__":
    RESOLUTION = (1280,736) # Resolução do jogo
    game = Game(RESOLUTION) # Cria o objeto jogo do tipo GAME
    game.run() # Começa a rodar o jogo
