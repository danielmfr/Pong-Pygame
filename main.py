from curses.textpad import Textbox
import random

import pygame
import sys

# Inicialização
pygame.init()
pygame.mixer.init()

# Configurando a janela
FPS = 60
MS_PER_UPDATE = 1000 / FPS
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960


# Classes
class Entity:
    def update(self, dt):
        pass


class Physics:
    def update(self, world, dt):
        pass


class Observer:
    def update(self, subject):
        pass


# 0: nenhum; 1: defesa do jogador; 2: defesa do oponente; 3: gol jogador; 4: gol oponente; 5: parede
class AudioSystem(Observer):
    def update(self, subject):
        if subject.state == 1 or subject.state == 2:
            pygame.mixer.music.load('Metal.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer_music.play()
        if subject.state == 3 or subject.state == 4:
            pygame.mixer.music.load('Crash.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer_music.play()
        if subject.state == 5:
            pygame.mixer.music.load('Wooden.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer_music.play()


class AchievementSystem(Observer):

    p_score = 0
    o_score = 0
    pht_score = 0
    oht_score = 0

    def update(self, subject):
        if subject.state == 3:
            print("gol do jogador")
            self.p_score += 1
            world.player_score.set_text(str(self.p_score))
            self.pht_score += 1
            self.oht_score = 0
        elif subject.state == 4:
            print("gol do oponente")
            self.o_score += 1
            world.opponent_score.set_text(str(self.o_score))
            self.pht_score = 0
            self.oht_score += 1
        if self.pht_score == 3:
            print("Hat Trick do Player")
            self.pht_score = 0
        if self.oht_score == 3:
            print("Hat Trick do Opponent")
            self.oht_score = 0


class BallPhysics(Physics):
    def update(self, world, dt):
        world.ball.body.x = world.ball.body.x + world.ball.speedX * dt
        world.ball.body.y = world.ball.body.y + world.ball.speedY * dt
        if world.ball.body.top <= 0:
            world.ball.speedY = abs(world.ball.speedY)
            world.ball.state = 5
            world.ball.notify()
        if world.ball.body.bottom >= SCREEN_HEIGHT:
            world.ball.speedY = -abs(world.ball.speedY)
            world.ball.state = 5
            world.ball.notify()
        if world.ball.body.left > SCREEN_WIDTH:
            world.ball.body.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            world.ball.speedX = random.choice((-0.5, 0.5))
            world.ball.state = 3
            world.ball.notify()
        if world.ball.body.right < 0:
            world.ball.body.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            world.ball.speedX = random.choice((-0.5, 0.5))
            world.ball.state = 4
            world.ball.notify()


class Ball(Entity):
    state = 0
    observers = []

    def __init__(self, physics):
        self.physics = physics
        self.body = pygame.Rect(SCREEN_WIDTH / 2 - 15,
                                SCREEN_HEIGHT / 2 - 15, 30, 30)
        self.speedX = 0.4
        self.speedY = 0.4
        audio = AudioSystem()
        self.attach(audio)
        achievement = AchievementSystem()
        self.attach(achievement)

    def draw(self, screen):
        pygame.draw.ellipse(screen, (200, 200, 200), self.body)

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)


# 1: defesa do jogador;
class PlayerPhysics(Physics):
    def update(self, world, dt):
        if world.ball.body.bottom >= world.player.body.top and world.ball.body.top <= world.player.body.bottom and \
                world.ball.body.right >= world.player.body.left:
            delta = world.ball.body.centery - world.player.body.centery
            world.ball.speedY = delta * 0.01
            world.ball.speedX *= -1
            world.ball.state = 1
            world.ball.notify()

        (x, y) = pygame.mouse.get_pos()
        world.player.body.y = y - 70


class Player(Entity):
    state = 0
    observers = []

    def __init__(self, physics):
        self.physics = physics
        self.body = pygame.Rect(
            SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - 70, 10, 140)
        audio = AudioSystem()
        self.attach(audio)
        achievement = AchievementSystem()
        self.attach(achievement)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.body)

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class OpponentPhysics(Physics):
    def update(self, world, dt):
        if world.opponent.body.bottom < world.ball.body.y:
            world.opponent.body.bottom += world.opponent.speed
        if world.opponent.body.top > world.ball.body.y:
            world.opponent.body.top -= world.opponent.speed
        if world.ball.body.bottom >= world.opponent.body.top and world.ball.body.top <= world.opponent.body.bottom \
                and world.ball.body.left <= world.opponent.body.right:
            delta = world.ball.body.centery - world.opponent.body.centery
            world.ball.speedY = delta * 0.01
            world.ball.speedX *= -1
            world.ball.state = 2
            world.ball.notify()


class Opponent(Entity):
    state = 0
    observers = []

    def __init__(self, physics):
        self.physics = physics
        self.body = pygame.Rect(10, SCREEN_HEIGHT / 2 - 70, 10, 140)
        self.speed = 8
        audio = AudioSystem()
        self.attach(audio)
        achievement = AchievementSystem()
        self.attach(achievement)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.body)

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)


'''def inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()'''


'''def draw():
    screen.fill((0, 0, 0))
    pygame.draw.ellipse(screen, (200, 200, 200), world.ball.body)
    pygame.draw.rect(screen, (200, 200, 200), world.player.body)
    pygame.draw.rect(screen, (200, 200, 200), world.opponent.body)
    # Atualizando a janela 60fps
    pygame.display.flip()'''


class Text(Entity):
    def __init__(self, x, y, text_size, text, physics):
        self.physics = physics
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('chalkduster.ttf', text_size)
        self.text = text

    def draw(self, screen):
        text_titulo = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_titulo, (self.x, self.y))

    def set_text(self, new_text):
        self.text = new_text


class World:
    lag = 0
    pygame.display.set_caption('Pong')

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        ballPhysics = BallPhysics()
        self.ball = Ball(ballPhysics)
        playerPhysics = PlayerPhysics()
        self.player = Player(playerPhysics)
        opponentPhysics = OpponentPhysics()
        self.opponent = Opponent(opponentPhysics)

        self.player_score = Text(SCREEN_WIDTH/2+50, 70, 72, str(0), Physics())
        self.opponent_score = Text(
            SCREEN_WIDTH/2-50, 70, 72, str(0), Physics())

        self.entities = []
        self.entities.append(self.ball)
        self.entities.append(self.player)
        self.entities.append(self.opponent)
        self.entities.append(self.player_score)
        self.entities.append(self.opponent_score)

    def game_loop(self):
        previous = pygame.time.get_ticks()
        while True:
            current = pygame.time.get_ticks()
            elapsed = current - previous
            previous = current
            self.lag += elapsed

            # Entradas
            self.inputs()

            # Atualização
            while self.lag >= MS_PER_UPDATE:
                # Atualização
                self.update()
                self.lag -= MS_PER_UPDATE

            # Desenho
            self.draw()

    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for e in self.entities:
            e.draw(self.screen)
        pygame.display.flip()

    def update(self):
        for e in self.entities:
            e.physics.update(self, MS_PER_UPDATE)


# Objetos
world = World()
world.game_loop()

'''previous = pygame.time.get_ticks()
lag = 0
FPS = 60
MS_PER_UPDATE = 1000 / FPS
while True:
    current = pygame.time.get_ticks()
    elapsed = current - previous
    previous = current
    lag += elapsed
    # Entradas
    inputs()
    # Atualização
    while lag >= MS_PER_UPDATE:
        # Atualização
        for e in world.entities:
            e.physics.update(world, MS_PER_UPDATE)
        lag -= MS_PER_UPDATE
    # Desenho
    draw()
'''
