import pygame
import random
colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]
class tela:
    x = 0
    y = 0
    telas = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.telas) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
    def image(self):
        return self.telas[self.type][self.rotation]
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.telas[self.type])
class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    tela = None
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
    def new_tela(self):
        self.tela = tela(3, 0)
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tela.image():
                    if i + self.tela.y > self.height - 1 or \
                            j + self.tela.x > self.width - 1 or \
                            j + self.tela.x < 0 or \
                            self.field[i + self.tela.y][j + self.tela.x] > 0:
                        intersection = True
        return intersection
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
    def go_space(self):
        while not self.intersects():
            self.tela.y += 1
        self.tela.y -= 1
        self.freeze()
    def go_down(self):
        self.tela.y += 1
        if self.intersects():
            self.tela.y -= 1
            self.freeze()
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tela.image():
                    self.field[i + self.tela.y][j + self.tela.x] = self.tela.color
        self.break_lines()
        self.new_tela()
        if self.intersects():
            self.state = "gameover"
    def go_side(self, dx):
        old_x = self.tela.x
        self.tela.x += dx
        if self.intersects():
            self.tela.x = old_x
    def rotate(self):
        old_rotation = self.tela.rotation
        self.tela.rotate()
        if self.intersects():
            self.tela.rotation = old_rotation
pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pygame Tetris")
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0
pressing_down = False
while not done:
    if game.tela is None:
        game.new_tela()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    screen.fill(WHITE)
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
    if game.tela is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.tela.image():
                    pygame.draw.rect(screen, colors[game.tela.color],
                                     [game.x + game.zoom * (j + game.tela.x) + 1,
                                      game.y + game.zoom * (i + game.tela.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
    font = pygame.font.SysFont('Normal', 35, True, False)
    font1 = pygame.font.SysFont('Normal', 75, True, False)
    text = font.render("  Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render(" Game Over", True, (255, 125, 0))
    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
