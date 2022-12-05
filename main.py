import pygame
from pygame.locals import *
from random import randint
from time import sleep

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
            body_sprite = self.rotated_sprite(num_body) # Sprite rotacionado da parte do corpo em específico
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

class Game:
    def __init__(self, resolution):
        pygame.init() # Inicia o módulo pygame
        self.screen = pygame.display.set_mode(resolution, pygame.RESIZABLE|pygame.DOUBLEBUF) # Define a resolução do jogo
        self.screen.fill((0,200,0)) # Preenche o background com a cor preta
        self.snake = Snake(self.screen) # Cria o objeto COBRA
        self.apples = [Apple(self.screen, unit_square)] # Cria o objeto MAÇÃ
        self.lumberjack = Lumberjack(self.screen, unit_square) # Cria o objeto LENHADOR
        self.bigfont = pygame.font.SysFont("comicsans", 50, True)
        self.font = pygame.font.SysFont("comicsans", 30, True) # Define a fonte dos textos
        self.current_effects = {} # Dicionário com todos os efeitos que estão ocorrendo
        self.fps = 60 # Define o FPS do jogo para 60
        self.score = 0 # Cria um atributo de pontuação
        self.state = "main menu"
        self.multiplier_points = 1
        self.multiplier_apples = 1
        self.selected_game = None
        self.selected_enemies = None
        self.mute = False

    def apply_effects(self, speed):
        self.snake.speed = speed # Reseta a velocidade da cobra 
        self.multiplier_points = 1 # Reseta o multiplicador de pontos da cobra 
        self.multiplier_apples = 1 # Reseta o multiplicador de maças no jogo 
        self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito_desativado01.png").convert_alpha(), (120,120)), (1090, 200))
        self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito_desativado02.png").convert_alpha(), (120,120)), (1070, 300))
        self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito_desativado04.png").convert_alpha(), (120,120)), (1070, 400))
        self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito_desativado03.png").convert_alpha(), (120,120)), (1070, 500))
        
        # Percorre todos os efeitos atuais
        for effect in self.current_effects:
            # Roda o efeito caso ainda exista duração
            if self.current_effects[effect] > 0: 
                if effect == "faster": 
                    self.snake.speed = speed*3/2
                    self.screen.blit(self.font.render(str(round(self.current_effects[effect]/self.fps, 1)), 1, (255,255,0)), (1070,200))
                    self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito01.png").convert_alpha(), (120,120)), (1090, 200))
                elif effect == "slower":
                    self.snake.speed = speed/2
                    self.screen.blit(self.font.render(str(round(self.current_effects[effect]/self.fps, 1)), 1, (255,0,200)), (1070,300))
                    self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito02.png").convert_alpha(), (120,120)), (1070, 300))
                elif effect == "double points":
                    self.multiplier_points = 2
                    self.screen.blit(self.font.render(str(round(self.current_effects[effect]/self.fps, 1)), 1, (255,255,0)), (1070,400))
                    self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito04.png").convert_alpha(), (120,120)), (1070, 400))
                elif effect == "triple apples":
                    self.multiplier_apples = 3
                    self.screen.blit(self.font.render(str(round(self.current_effects[effect]/self.fps, )), 1, (255,150,150)), (1070,500))
                    self.screen.blit(pygame.transform.scale(pygame.image.load("./imgs/effects/efeito03.png").convert_alpha(), (120,120)), (1070, 500))
                self.current_effects[effect] -= 1 # Atualiza a duração do efeito

    
    def run(self):
        running = True
        clock = pygame.time.Clock() # Cria um objeto de relógio
        count_ask_dificults = 0
        sound_game_over = False
        
        while running:
            clock.tick(self.fps)
            if self.mute:
                pygame.mixer.stop()
            if self.state == "main menu":
                mouse_x, mouse_y = pygame.mouse.get_pos()

                click = False
                for event in pygame.event.get():
                    if event.type == QUIT: # Sai do jogo caso o jogador o feche
                        running = False
                    
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.state = "running"
                    
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True

                self.screen.fill((0,0,0)) # Preenche a tela com um retângulo preto (para atualizar as posições)

                self.screen.blit(self.bigfont.render("BOITATÁ: O DEFENSOR DAS FLORESTAS" , 1, (255,255,255)), (100,75))
                
                self.screen.blit(self.font.render("Dificuldade do Jogo" , 1, (255,255,255)), (200,225))

                easy_game = pygame.Rect(125, 325, 300, 40)
                if easy_game.collidepoint(mouse_x, mouse_y) or self.selected_game == "easy":
                    self.screen.blit(self.font.render("Fácil" , 1, (100,255,100)), (200,325))
                    if click:
                        self.selected_game = "easy"
                else:
                    self.screen.blit(self.font.render("Fácil" , 1, (200,255,200)), (200,325))

                medium_game = pygame.Rect(125, 375, 300, 40)
                if medium_game.collidepoint(mouse_x, mouse_y) or self.selected_game == "medium":
                    self.screen.blit(self.font.render("Médio" , 1, (100,100,255)), (200,375))
                    if click:
                        self.selected_game = "medium"
                else:
                    self.screen.blit(self.font.render("Médio" , 1, (200,200,255)), (200,375))
                
                hard_game = pygame.Rect(125, 425, 300, 40)
                if hard_game.collidepoint(mouse_x, mouse_y) or self.selected_game == "hard":
                    self.screen.blit(self.font.render("Difícil" , 1, (255,100,100)), (200,425))
                    if click:
                        self.selected_game = "hard"
                else:
                    self.screen.blit(self.font.render("Difícil" , 1, (255,200,200)), (200,425))

                self.screen.blit(self.font.render("Dificuldade do Obstáculo", 1, (255,255,255)), (740,225))

                easy_enemies = pygame.Rect(725, 325, 300, 40)
                if easy_enemies.collidepoint(mouse_x, mouse_y) or self.selected_enemies == "easy":
                    self.screen.blit(self.font.render("Fácil (sem graça)" , 1, (100,255,100)), (740,325))
                    if click:
                        self.selected_enemies = "easy"
                else:
                    self.screen.blit(self.font.render("Fácil (sem graça)" , 1, (200,255,200)), (740,325))

                medium_enemies = pygame.Rect(725, 375, 300, 40)
                if medium_enemies.collidepoint(mouse_x, mouse_y) or self.selected_enemies == "medium":
                    self.screen.blit(self.font.render("Médio" , 1, (100,100,255)), (740,375))
                    if click:
                        self.selected_enemies = "medium"
                else:
                    self.screen.blit(self.font.render("Médio" , 1, (200,200,255)), (740,375))

                mute_game = pygame.Rect(175, 550, 300, 40)
                if mute_game.collidepoint(mouse_x, mouse_y) or self.mute:
                    self.screen.blit(self.font.render("Silenciar jogo" , 1, (100,100,100)), (200,550))
                    if click:
                        self.mute = True 
                else:
                    self.screen.blit(self.font.render("Silenciar jogo" , 1, (200,200,200)), (200,550))


                play_button = pygame.Rect(775, 525, 300, 100)
                
                if play_button.collidepoint(mouse_x, mouse_y):
                    self.screen.blit(self.bigfont.render("JOGAR" , 1, (100,100,100)), (850,525))
                    if click:
                        if self.selected_enemies == None or self.selected_game == None:
                            count_ask_dificults = 1
                        else:
                            self.state = "running"
                else:
                    self.screen.blit(self.bigfont.render("JOGAR" , 1, (200,200,200)), (850,525))


                if count_ask_dificults > 0:
                    count_ask_dificults += 1
                    self.screen.blit(self.font.render("Selecione as dificuldades primeiro" , 1, (255,50,50)), (700,600))
                    if count_ask_dificults >= self.fps*5:
                        count_ask_dificults = 0
                
                pygame.display.update() # Atualiza a tela
                continue

            elif self.state == "pause":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                click = False
                for event in pygame.event.get():
                    if event.type == QUIT: # Sai do jogo caso o jogador o feche
                        running = False

                    if event.type == KEYDOWN: # Obtém todas as teclas pressionadas
                        if event.key == K_ESCAPE:
                            self.state = "running"

                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True
                
                pygame.draw.rect(self.screen, (119, 221, 119), (0, 0, 380, 736))
                
                return_game = pygame.Rect(40, 250, 300, 40)
                self.screen.blit(self.font.render("Retornar ao jogo" , 1, (0,0,0)), (38,252))
                if return_game.collidepoint(mouse_x, mouse_y):
                    self.screen.blit(self.font.render("Retornar ao jogo" , 1, (60,255,60)), (40,250))
                    if click:
                        self.state = "running"
                else:
                    self.screen.blit(self.font.render("Retornar ao jogo" , 1, (255,255,255)), (40,250))
                
                restart_game = pygame.Rect(40, 350, 300, 40)
                self.screen.blit(self.font.render("Voltar para o menu" , 1, (0,0,0)), (38,352))
                if restart_game.collidepoint(mouse_x, mouse_y):
                    self.screen.blit(self.font.render("Voltar para o menu" , 1, (60,255,60)), (40,350))
                    if click:
                        running = False
                        # pygame.quit()
                        RESOLUTION = (1280,736) # Resolução do jogo
                        game = Game(RESOLUTION) # Cria o objeto jogo do tipo GAME
                        game.run() # Começa a rodar o jogo
                else:
                    self.screen.blit(self.font.render("Voltar para o menu" , 1, (255,255,255)), (40,350))
                
                quit_game = pygame.Rect(40, 450, 300, 40)
                self.screen.blit(self.font.render("Sair do jogo" , 1, (0,0,0)), (38,452))
                if quit_game.collidepoint(mouse_x, mouse_y):
                    self.screen.blit(self.font.render("Sair do jogo" , 1, (60,255,60)), (40,450))
                    if click:
                        running = False
                else:
                    self.screen.blit(self.font.render("Sair do jogo" , 1, (255,255,255)), (40,450))


                pygame.display.update() # Atualiza a tela
                continue
            
            elif self.state == "game over":
                click = False
                for event in pygame.event.get():
                    if event.type == QUIT: # Sai do jogo caso o jogador o feche
                        running = False
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True

                if sound_game_over == False:
                    sleep(1)
                    random = randint(1,3)
                    game_over_sound = pygame.mixer.Sound(f"./sounds/game_over/game_over{random}.opus")
                    game_over_sound.set_volume(10)
                    game_over_sound.play()
                    sound_game_over = True
                
                self.screen.fill((0,0,0))
                self.screen.blit(self.bigfont.render("GAME OVER" , 1, (140,40,40)), (500,275))
                mouse_x, mouse_y = pygame.mouse.get_pos()

                quit_game = pygame.Rect(125, 375, 300, 40)
                if quit_game.collidepoint(mouse_x, mouse_y):
                    self.screen.blit(self.font.render("Sair do jogo" , 1, (255,60,60)), (250,375))
                    if click:
                        running = False
                else:
                    self.screen.blit(self.font.render("Sair do jogo" , 1, (255,255,255)), (250,375))
                
                restart_game = pygame.Rect(725, 375, 300, 40)
                if restart_game.collidepoint(mouse_x, mouse_y):
                    self.screen.blit(self.font.render("Voltar para o menu" , 1, (255,60,60)), (740,375))
                    if click:
                        running = False
                        # pygame.quit()
                        RESOLUTION = (1280,736) # Resolução do jogo
                        game = Game(RESOLUTION) # Cria o objeto jogo do tipo GAME
                        game.run() # Começa a rodar o jogo
                else:
                    self.screen.blit(self.font.render("Voltar para o menu" , 1, (255,255,255)), (740,375))

                pygame.display.update() # Atualiza a tela
                continue

            game_back = pygame.image.load("./imgs/background/image_final.png").convert_alpha()
            self.screen.blit(game_back, (0,0))
            game_arena = pygame.image.load("./imgs/background/image2_final.png").convert_alpha()
            self.screen.blit(game_arena, (game_screen[0],game_screen[2]))

            resolution = self.screen.get_size() # Armazena a resolução da tela 
            self.screen.blit(self.font.render("Pontuação: " + str(self.score), 1, (0,0,0)), (1047,15)) # Escreve a pontuação na tela
            self.screen.blit(self.font.render("Pontuação: " + str(self.score), 1, (255,255,255)), (1050,10)) # Escreve a pontuação na tela


            if self.selected_game == "easy":
                self.apply_effects(1/7)
            elif self.selected_game == "medium":
                self.apply_effects(1/4)
            elif self.selected_game == "hard":
                self.apply_effects(1/2)

            for event in pygame.event.get():
                if event.type == QUIT: # Sai do jogo caso o jogador o feche
                    running = False

                if event.type == KEYDOWN: # Obtém todas as teclas pressionadas
                    self.snake.change_direction(event.key) # Altera a direção da cobra com os respectivos comandos
                    if event.key == K_ESCAPE:
                        self.state = "pause"
            
            self.snake.move() # Roda a função para a cobra se mover

            if self.multiplier_apples > len(self.apples):
                self.apples.append(Apple(self.screen, unit_square))

            if self.selected_enemies == "medium":
                self.lumberjack.move(self.apples[0]) # Roda a movimentação do lenhador

            # Condicional da cobra passar pelo lenhador
                if (self.snake.x,self.snake.y) == (self.lumberjack.x, self.lumberjack.y):

                    # Adiciona o efeito do lenhador
                    if self.lumberjack.effect == 0:
                        self.current_effects["faster"] = 2*self.fps # Deixar a cobra mais lenta
                    elif self.lumberjack.effect == 1:
                        self.current_effects["slower"] = 2*self.fps # Deixar a cobra mais rápida
                    elif self.lumberjack.effect == 2:
                        self.current_effects["double points"] = 7*self.fps # Dobra os pontos
                    elif self.lumberjack.effect == 3:
                        self.current_effects["triple apples"] = 4*self.fps # Triplica o número de maças
        
                    del self.lumberjack # Remove o lenhador
                    pygame.mixer.Sound("./sounds/eating_lumberjack.mp3").play()
                    self.score += 1 # Adiciona 1 à pontuação
                    self.lumberjack = Lumberjack(self.screen, unit_square) # Cria um novo lenhador na tela

            for apple in self.apples:
                apple.draw() # Desenha a maça

                # Condicional da cobra passar pela maçã
                if (self.snake.x,self.snake.y) == (apple.x, apple.y):
                    self.apples.remove(apple)
                    del apple # Remove a maça
                    pygame.mixer.Sound("./sounds/eating_apple.mp3").play()
                    self.score += self.multiplier_points # Adiciona 1 à pontuação
                    self.snake.body_size += 1 # Adiciona 1 ao corpo da cobra
                    if randint(0,1):
                        pygame.mixer.Sound("./sounds/appear_apple1.mp3").play()
                    else:
                        pygame.mixer.Sound("./sounds/appear_apple2.mp3").play()

                # Condicional do lenhador passar pela maçã
                elif (apple.x,apple.y) == (self.lumberjack.x, self.lumberjack.y) and self.selected_enemies == "medium":
                    self.apples.remove(apple)
                    del apple # Remove a maça
                    self.score -= self.multiplier_points # Remove 1 da pontuação

            if self.snake.isdeph:
                self.state = "game over"

            pygame.display.update() # Atualiza a tela


if __name__  == "__main__":
    RESOLUTION = (1280,736) # Resolução do jogo
    game = Game(RESOLUTION) # Cria o objeto jogo do tipo GAME
    game.run() # Começa a rodar o jogo
