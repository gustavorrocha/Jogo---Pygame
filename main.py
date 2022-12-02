import pygame
from pygame.locals import *
from random import randint


class Snake:
    def __init__(self, screen):
        self.__screen = screen # Configura a tela em que a cobra aparecerá
        self.__largura = 20 # Define a largura da cobra
        self.__altura = 20 # Define a altura da cobra
        self.x = 100 # Define a coordenada x da cobra
        self.y = 100 # Define a coordenada y da cobra
        self.speed = 1/4 # Velocidade da cobra
        self.body_size = 0 # Tamanho do corpo da cobra (excluindo a cabeça)
        self.__old_coords = [] # Lista com as coordenadas das partes do corpo da cobra
        self.__direction = "" # Armazena a direção da cobra
        self.__direction_cache = "" # Caso a direção não possa ser mudada, armazena um cache até que seja possível
        self.count_frames = 0 # Cria o contador de frames
        self.draw() # Desenha a cobra
    
    def draw(self):
        pygame.draw.rect(self.__screen, (255,195,0), (self.x, self.y, self.__largura, self.__altura)) # Desenha a cabeça da cobra

        # Desenha as partes do corpo da cobra (necessário consertar para funcionar adequadamente com a mudança de velocidade)
        for num_body in range(self.body_size):
            pygame.draw.rect(self.__screen, (255,195,0), (self.__old_coords[num_body][0], self.__old_coords[num_body][1], self.__largura, self.__altura))
        
    
    # "Getter" da direção da cobra
    @property
    def direction(self):
        return self.__direction

    # "Setter" para a direção da cobra (só muda em posições múltiplas de 10)
    @direction.setter
    def direction(self, direction):
        if self.x % 20 == 0 and self.y % 20 == 0:
            self.__direction = direction

    # Altera a direção caso alguma das teclas "wasd" sejam apertadas
    def check_direction(self, key):
        if key == K_w and self.direction != "down":
            self.__direction_cache = "up"
        if key == K_a and self.direction != "right":
            self.__direction_cache = "left"
        if key == K_s and self.direction != "up":
            self.__direction_cache = "down"
        if key == K_d and self.direction != "left":
            self.__direction_cache = "right"
        self.direction = self.__direction_cache # Tenta alterar a direção até que seja viável

    def move(self):
        self.count_frames += 1 # Incrementa o contador de frames

        # Remove as coordenadas antigas que não serã usadas
        while len(self.__old_coords) > self.body_size:
            self.__old_coords.pop(-1)

        # Utiliza o contador de frames para alterar a velocidade da cobra        
        if self.count_frames % round(1/self.speed) == 0:
            self.check_direction("") # Tenta mudar a direção, caso ela não tenha sido mudada

            self.__old_coords.insert(0, (self.x, self.y)) # Adiciona as coordenadas antigas da cabeça da cobra, para que seja utilizada no corpo


            # Movimentação básica da cobra
            if self.direction == "left":
                self.x -= 20
            elif self.direction == "right":
                self.x += 20
            elif self.direction == "up":
                self.y -= 20
            elif self.direction == "down":
                self.y += 20    
                
        self.draw() # Redesenha a cobra na sua nova posição
    
    def eat_apple(self):
        self.body_size += 1 # Altera o tamanho do corpo, caso a cobra coma uma maça


class Apple:
    def __init__(self, screen, size):
        self.screen = screen
        resolution = self.screen.get_size() # Armazena a resolução da tela
        self.size = size
        self.x = randint(0,resolution[0] - size)//size*size # Randomiza a posição x da maçã
        self.y = randint(0,resolution[1] - size)//size*size # Randomiza a posição y da maçã
        self.draw() # Desenha a maçã

    def draw(self):
        pygame.draw.rect(self.screen, (255,0,0), (self.x, self.y, self.size, self.size)) # Desenha a maçã

class Lumberjack:
    def __init__(self, screen, size):
        self.screen = screen
        resolution = self.screen.get_size() # Armazena a resolução da tela
        self.size = size
        self.x = randint(0,resolution[0] - size)//size*size # Randomiza a posição x do lenhador
        self.y = randint(0,resolution[1] - size)//size*size # Randomiza a posição y do lenhador
        self.direction = 0 # Armazena a direção do lenhador
        self.count_frames = 0 # Cria o contador de frames
        self.is_smart = randint(0,1) # Randomiza se o lenhador será inteligente (irá atrás das maçãs) ou não
        self.draw() # Desenha a maçã

    def draw(self):
        pygame.draw.rect(self.screen, (0,0,255), (self.x, self.y, self.size, self.size)) # Desenha a maçã
    
    def stay_in_screen(self):
        resolution = self.screen.get_size() # Armazena a resolução da tela

        # Não permite que o lenhador ultrapasse os limites da tela
        if self.x == 0 and self.direction == 0:
            self.direction = 1
        elif self.x == resolution[0] - self.size and self.direction == 1:
            self.direction = 0
        if self.y == 0 and self.direction == 2:
            self.direction = 3
        elif self.y == resolution[1] - self.size and self.direction == 3:
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

        # Utiliza o contador de frames para fazer com que a movimentação do lenhador deja mais lenta      
        if self.count_frames % 10 == 0:

            if self.is_smart: # Se o lenhador for inteligente, o faz seguir a maçã
                self.follow_target(apple)

            # 1% de chance de alterar a direção do lenhador
            if randint(1,10) == 1:
                self.direction = randint(0,3)
    
            self.stay_in_screen() # Faz com que o lenhador não saia da tela

            # Movimentação básica do lenhador
            if self.direction == 0:
                self.x -= 20
            elif self.direction == 1:
                self.x += 20
            elif self.direction == 2:
                self.y -= 20
            elif self.direction == 3:
                self.y += 20

        self.draw() # Redesenha o lenhador na sua nova posição

class Game:
    def __init__(self, resolution):
        pygame.init() # Inicia o módulo pygame
        self.screen = pygame.display.set_mode(resolution, pygame.RESIZABLE|pygame.DOUBLEBUF) # Define a resolução do jogo
        self.screen.fill((0,0,0)) # Preenche o background com a cor preta
        self.snake = Snake(self.screen) # Cria o objeto COBRA
        self.apple = Apple(self.screen, 20) # Cria o objeto MAÇÃ
        self.lumberjack = Lumberjack(self.screen, 20) # Cria o objeto LENHADOR
        self.font = pygame.font.SysFont("comicsans", 30, True) # Define a fonte dos textos
        self.score = 0 # Cria um atributo de pontuação

    def run(self):
        running = True
        clock = pygame.time.Clock() # Cria um objeto de relógio

        while running:
            clock.tick(60) # Define o FPS do jogo para 30
            self.screen.fill((0,0,0)) # Preenche a tela com um retângulo preto (para atualizar as posições)
            resolution = self.screen.get_size() # Armazena a resolução da tela 
            self.screen.blit(self.font.render("Pontuação: " + str(self.score), 1, (255,255,255)), (resolution[0] - 250,10)) # Escreve a pontuação na tela
            self.apple.draw() # Desenha a maça
            self.lumberjack.move(self.apple) # Roda a movimentação do lehador
            self.snake.move() # Roda a função para a cobra se mover

            for event in pygame.event.get():
                if event.type == QUIT: # Sai do jogo caso o jogador o feche
                    running = False

                if event.type == KEYDOWN: # Obtém todas as teclas pressionadas
                    self.snake.check_direction(event.key) # Altera a direção da cobra com os respectivos comandos

            # Condicional da cobra passar pela maçã
            if (self.snake.x,self.snake.y) == (self.apple.x, self.apple.y):
                del self.apple # Remove a maça
                self.score += 1 # Adiciona 1 à pontuação
                self.snake.body_size += 1 # Adiciona 1 ao corpo da cobra
                self.apple = Apple(self.screen, 20) # Cria uma nova maça na tela

            # Condicional do lenhador passar pela maçã
            if (self.apple.x,self.apple.y) == (self.lumberjack.x, self.lumberjack.y):
                del self.apple # Remove a maça
                self.score -= 1 # Remove 1 da pontuação
                self.apple = Apple(self.screen, 20) # Cria uma nova maça na tela

            # Condicional da cobra passar pelo lenhador
            if (self.snake.x,self.snake.y) == (self.lumberjack.x, self.lumberjack.y):
                del self.lumberjack # Remove o lenhador
                self.score += 1 # Adiciona 1 à pontuação
                self.lumberjack = Lumberjack(self.screen, 20) # Cria um novo lenhador na tela

            pygame.display.update() # Atualiza a tela


if __name__  == "__main__":
    RESOLUTION = (600,600) # Resolução do jogo
    game = Game(RESOLUTION) # Cria o objeto jogo do tipo GAME
    game.run() # Começa a rodar o jogo
