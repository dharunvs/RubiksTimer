import pygame
import sys
import os
from random import randint, choice

# COLORS

WHEAT = (255, 255, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

TIMER_SIZE = 90


class App:

    def __init__(self):
        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rubix Timer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.font_name = "monospace"
        self.space_state = "press"

        self.bg_color = WHEAT

        self.minutes = 0
        self.seconds = 0
        self.milliseconds = -1

        self.watch = f"{self.minutes}:{self.seconds}:{self.milliseconds}"

        self.last_time = "none"
        self.temp = ""
        self.score = {}
        self.timer()

        self.all_keys = [
            pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i,
            pygame.K_o, pygame.K_p, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h,
            pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_b, pygame.K_v,
            pygame.K_c, pygame.K_x, pygame.K_z, pygame.K_SPACE, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH,
            pygame.K_SEMICOLON, pygame.K_QUOTE
        ]

        self.patterns = []
        self.all_scores = []
        self.show_scores = ""
        self.sh = 20
        self.load_patterns()

    def run(self):
        self.reset_choice()
        while self.running:
            if self.state == 'start':
                self.start_event()
                self.start_draw()
            elif self.state == 'play':
                self.playing_event()
                self.playing_draw()
            elif self.state == 'pause':
                self.pause_event()
                self.pause_draw()
            elif self.state == 'score':
                self.score_event()
                self.score_draw()
            else:
                self.running = False
            self.clock.tick(100)

        pygame.quit()
        sys.exit()

# ----------------------------------------------------------------------------------------------------------------------

    def draw_text(self, text, pos, size, color, centered=False):
        pygame.font.init()
        font = pygame.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_width = text_surface.get_width()
        pos_x = pos[0]
        pos_y = pos[1]

        if centered:
            pos_x = int(self.width/2) - int(text_width/2)

        position = (int(pos_x), int(pos_y))
        self.screen.blit(text_surface, position)

    def timer(self):

        self.milliseconds += 1

        if self.milliseconds == 100:
            self.seconds += 1
            self.milliseconds -= 100

        if self.seconds == 60:
            self.minutes += 1
            self.seconds -= 60

        self.watch = f"{self.minutes}:{self.seconds}:{self.milliseconds}"

    def show_timer(self, color):
        self.draw_text(self.watch, (0, (self.height//2)-50), TIMER_SIZE,
                       color, centered=True)

    def load_patterns(self):
        if os.path.isfile('pattern.txt'):
            with open('pattern.txt', 'r') as f:
                temp = f.read()
                temp = temp.split('\n')
                pattern = temp

        for i in pattern:
            self.patterns.append(i)

    def load_scores(self):
        if os.path.isfile('score.txt'):
            with open('score.txt', 'r') as f:
                temp = f.read()
                temp = temp.split('\n')
                score = temp

        for i in score:
            self.all_scores.append(i)

    def reset_choice(self):
        self.scramble = choice(self.patterns)

    def save(self):
        with open("score.txt", "a") as f:
            for i in self.score:
                f.write(f"{i} - {self.score[i]}\n")

# ----------------------------------------------------------------------------------------------------------------------

    def start_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save()
                self.running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.state = 'play'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.space_state = "release"
                if event.key == pygame.K_s:
                    self.state = 'score'
                    self.load_scores()

    def start_draw(self):
        self.screen.fill(self.bg_color)
        self.draw_text("Rubix Timer", (0, 50), 38,
                       BLACK, centered=True)
        self.draw_text(self.scramble, (0, 150), 18,
                       BLACK, centered=True)

        self.draw_text(f"Last Time: {self.last_time}", (0, (self.height//2)+50), 18,
                       BLACK, centered=True)

        if self.space_state == "press":
            self.draw_text("Press and hold Space bar", (0, 630), 28,
                           BLACK, centered=True)
        elif self.space_state == "release":
            self.draw_text("Release Space bar to start", (0, 630), 28,
                           BLACK, centered=True)
        self.show_timer(BLACK)

        pygame.display.update()

# ----------------------------------------------------------------------------------------------------------------------

    def playing_event(self):
        self.timer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save()
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key in self.all_keys:
                    self.state = 'pause'
                    self.temp = self.watch

    def playing_draw(self):
        self.screen.fill(self.bg_color)
        self.draw_text("Rubix Timer", (0, 50), 38,
                       BLACK, centered=True)
        self.draw_text(f"Last Time: {self.last_time}", (0, (self.height//2)+50), 18,
                       BLACK, centered=True)
        self.show_timer(GREEN)

        pygame.display.update()

# ----------------------------------------------------------------------------------------------------------------------

    def pause_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state = 'start'
                    self.minutes = 0
                    self.seconds = 0
                    self.milliseconds = 0
                    self.watch = f"{self.minutes}:{self.seconds}:{self.milliseconds}"
                    self.space_state = "press"
                    self.last_time = self.temp
                    self.score[self.last_time] = self.scramble
                    self.save()
                    self.reset_choice()

    def pause_draw(self):
        self.screen.fill(self.bg_color)
        self.draw_text("Rubix Timer", (0, 50), 38,
                       BLACK, centered=True)
        self.draw_text(f"Last Time: {self.last_time}", (0, (self.height//2)+50), 18,
                       BLACK, centered=True)
        self.show_timer(RED)
        self.draw_text("Press R to reset", (0, 630), 28,
                       BLACK, centered=True)

        pygame.display.update()

# ----------------------------------------------------------------------------------------------------------------------

    def score_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save()
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.state = "start"

    def score_draw(self):
        self.screen.fill(self.bg_color)
        self.draw_text("Score", (0, 50), 38,
                       BLACK, centered=True)

        self.draw_text("hi\nhi", (0, 90), 24,
                       BLACK, centered=True)

        pygame.display.update()


if __name__ == "__main__":
    app = App()
    app.run()
