import pygame
from time import sleep
from pygame.locals import *
from entities import *


unit_square = 32
game_screen = (1*unit_square, 1280 - 10*unit_square, 1*unit_square, 736 - 2*unit_square)


class Game:
    def __init__(self, resolution):
        pygame.init() # Inicia o módulo pygame
        self.screen = pygame.display.set_mode(resolution, pygame.RESIZABLE|pygame.DOUBLEBUF) # Define a resolução do jogo
        self.screen.fill((0,200,0)) # Preenche o background com a cor preta
        self.snake = Snake(self.screen) # Cria o objeto COBRA
        self.apples = [Apple(self.screen, unit_square)] # Cria o objeto MAÇÃ
        self.lumberjacks = [Lumberjack(self.screen, unit_square)] # Cria o objeto LENHADOR
        self.bigfont = pygame.font.SysFont("comicsans", 50, True)
        self.font = pygame.font.SysFont("comicsans", 30, True) # Define a fonte dos textos
        self.current_effects = {} # Dicionário com todos os efeitos que estão ocorrendo
        self.fps = 60 # Define o FPS do jogo para 60
        self.score = 0 # Cria um atributo de pontuação
        self.state = "main menu"
        self.multiplier_points = 1
        self.multiplier_apples = 1
        self.num_lumberjacks = 1
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
                
                medium_enemies = pygame.Rect(725, 425, 300, 40)
                if medium_enemies.collidepoint(mouse_x, mouse_y) or self.selected_enemies == "hard":
                    self.screen.blit(self.font.render("Caótico" , 1, (255,100,100)), (740,425))
                    if click:
                        self.selected_enemies = "hard"
                else:
                    self.screen.blit(self.font.render("Caótico" , 1, (255,200,200)), (740,425))

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
            self.screen.blit(self.font.render("Pontuação: " + str(self.score), 1, (0,0,0)), (1047,13)) # Escreve a pontuação na tela
            self.screen.blit(self.font.render("Pontuação: " + str(self.score), 1, (255,255,255)), (1050,10)) # Escreve a pontuação na tela

            if self.selected_game == "easy":
                self.apply_effects(1/7)
            elif self.selected_game == "medium":
                self.apply_effects(1/4)
            elif self.selected_game == "hard":
                self.apply_effects(1/2)

            if self.selected_enemies == "hard":
                self.num_lumberjacks = self.score // 5 + 1

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
            
            if self.num_lumberjacks > len(self.lumberjacks):
                self.lumberjacks.append(Lumberjack(self.screen, unit_square)) # Cria um novo lenhador na tela

            if self.selected_enemies != "easy":
                for lumberjack in self.lumberjacks:
                    if len(self.apples) > 0:
                        lumberjack.move(self.apples[0]) # Roda a movimentação do lenhador

                     # Condicional da cobra passar pelo lenhador
                    if (self.snake.x,self.snake.y) == (lumberjack.x, lumberjack.y):

                        # Adiciona o efeito do lenhador
                        if lumberjack.effect == 0:
                            self.current_effects["faster"] = 2*self.fps # Deixar a cobra mais lenta
                        elif lumberjack.effect == 1:
                            self.current_effects["slower"] = 2*self.fps # Deixar a cobra mais rápida
                        elif lumberjack.effect == 2:
                            self.current_effects["double points"] = 7*self.fps # Dobra os pontos
                        elif lumberjack.effect == 3:
                            self.current_effects["triple apples"] = 4*self.fps # Triplica o número de maças
            
                        self.lumberjacks.remove(lumberjack)
                        del lumberjack # Remove o lenhador
                        pygame.mixer.Sound("./sounds/eating_lumberjack.mp3").play()
                        self.score += 1 # Adiciona 1 à pontuação
                        continue
                    
                    for apple in self.apples:
                        # Condicional do lenhador passar pela maçã
                        if (apple.x,apple.y) == (lumberjack.x, lumberjack.y):
                            self.apples.remove(apple)
                            del apple # Remove a maça
                            self.score -= self.multiplier_points # Remove 1 da pontuação

            if len(self.apples) > 0:
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

            if self.snake.isdeph:
                self.state = "game over"

            pygame.display.update() # Atualiza a tela
