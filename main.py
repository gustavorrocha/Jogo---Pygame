import pygame
from pygame.locals import *
from random import randint


class Snake:
    def __init__(self, screen):
        self.__screen = screen # Configura a tela em que a cobra aparecerá
        self.__largura = 10 # Define a largura da cobra
        self.__altura = 10 # Define a altura da cobra
        self.x = 100 # Define a coordenada x da cobra
        self.y = 100 # Define a coordenada y da cobra
        self.speed = 1 # Velocidade da cobra
        self.body_size = 0 # Tamanho do corpo da cobra (excluindo a cabeça)
        self.__old_coords = [] # Lista com as coordenadas das partes do corpo da cobra
        self.__direction = "" # Armazena a direção da cobra
        self.__direction_cache = "" # Caso a direção não possa ser mudada, armazena um cache até que seja possível
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
        if self.x % 10 == 0 and self.y % 10 == 0:
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
        self.__old_coords.append((self.x, self.y)) # Adiciona as coordenadas antigas da cabeça da cobra, para que seja utilizada no corpo
        while len(self.__old_coords) > self.body_size:
            self.__old_coords.pop(0)
        print(self.__old_coords)

        self.check_direction("") # Tenta mudar a direção, caso ela não tenha sido mudada

        # Movimentação básica da cobra
        if self.direction == "left":
            self.x -= self.speed*10
        elif self.direction == "right":
            self.x += self.speed*10
        elif self.direction == "up":
            self.y -= self.speed*10
        elif self.direction == "down":
            self.y += self.speed*10

        self.draw() # Redesenha a cobra na sua nova posição
    
    def eat_apple(self):
        self.body_size += 1 # Altera o tamanho do corpo, caso a cobra coma uma maça


class Apple:
    def __init__(self, screen, size):
        self.screen = screen
        resolution = self.screen.get_size() # Armazena a resolução da tela
        self.size = size
        self.x = randint(0,resolution[0] - size)//10*10 # Randomiza a posição x da maçã
        self.y = randint(0,resolution[1] - size)//10*10 # Randomiza a posição y da maçã
        self.draw() # Desenha a maçã

    def draw(self):
        pygame.draw.rect(self.screen, (255,0,0), (self.x, self.y, self.size, self.size)) # Desenha a maçã


class Game:
    def __init__(self, resolution):
        pygame.init() # Inicia o módulo pygame
        self.screen = pygame.display.set_mode(resolution) # Define a resolução do jogo
        self.screen.fill((0,0,0)) # Preenche o background com a cor preta
        self.snake = Snake(self.screen) # Cria o objeto COBRA
        self.apple = Apple(self.screen, 10) # Cria o objeto MAÇÃ
        self.font = pygame.font.SysFont("comicsans", 30, True) # Define a fonte dos textos
        self.score = 0 # Cria um atributo de pontuação

    def run(self):
        running = True
        clock = pygame.time.Clock() # Cria um objeto de relógio

        while running:
            clock.tick(30) # Define o FPS do jogo para 30
            self.screen.fill((0,0,0)) # Preenche a tela com um retângulo preto (para atualizar as posições)
            resolution = self.screen.get_size() # Armazena a resolução da tela 
            self.screen.blit(self.font.render("Pontuação: " + str(self.score), 1, (255,255,255)), (resolution[0] - 250,10)) # Escreve a pontuação na tela
            self.apple.draw() # Desenha a maça
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
                self.apple = Apple(self.screen, 10) # Cria uma nova maça na tela

            pygame.display.update() # Atualiza a tela


if __name__  == "__main__":
    RESOLUTION = (600,600) # Resolução do jogo
    game = Game(RESOLUTION) # Cria o objeto jogo do tipo GAME
    game.run() # Começa a rodar o jogo
