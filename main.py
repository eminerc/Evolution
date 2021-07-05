# Imports necessary libraries
import pygame
from pygame.locals import *
import random
import math
import time

# Window setup & global variables
pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Evolution')
background = pygame.Surface(WIN.get_size())
background = background.convert()
background.fill((250, 250, 250))
pygame.font.init()
cells = []
food = []


# Classes for food and cells
class Cell:
    def __init__(self, speed, s_radius, p_radius, reproduction_rate, x_cell, y_cell, x_goal, y_goal, anger, food_count,
                 c_num, cell_state, family, life_time, memory):
        self.life_time = life_time
        self.family = family
        self.c_num = c_num
        self.food_count = food_count
        self.anger = anger
        self.cell_state = cell_state
        self.speed = speed
        self.s_radius = s_radius
        self.p_radius = p_radius
        self.x_cell = x_cell
        self.y_cell = y_cell
        self.x_goal = x_goal
        self.y_goal = y_goal
        self.color = (family * 20, s_radius, p_radius)
        self.reproduction_rate = reproduction_rate
        self.memory = memory

    def draw_cell(self):
        pygame.draw.circle(WIN, (100, 100, 255), (self.x_cell, self.y_cell), self.p_radius + (self.s_radius * 20 / 255),
                           width=2)
        pygame.draw.circle(WIN, (255, 100, 100), (self.x_cell, self.y_cell), 20 + (self.s_radius * 20 / 255), width=2)
        pygame.draw.circle(WIN, self.color, (self.x_cell, self.y_cell), 5 + (self.s_radius * 20 / 255))

    def move(self):
        def find_goal():
            aggression = random.randint(0, self.anger)
            dc = []
            for i in cells:
                if (i.x_cell, i.y_cell) != (self.x_cell, self.y_cell):
                    dc.append([math.sqrt((i.x_cell - self.x_cell) ** 2 + (i.y_cell - self.y_cell) ** 2), i])
            dc = sorted(dc, key=lambda x: x[0])
            if len(dc) > 0 and dc[0][0] < 20 + (self.s_radius * 20 / 255) and dc[0][1].s_radius >= self.s_radius:
                x_e, y_e = dc[0][1].x_cell, dc[0][1].y_cell
                x_goal, y_goal = dc[0][1].x_goal, dc[0][1].y_goal
                if (aggression == 0 and dc[0][1].family != self.family):
                    self.cell_state = 0
                else:
                    if x_e > self.x_cell:
                        self.x_goal = self.x_cell - 40
                        self.y_goal = self.y_cell
                    else:
                        self.x_goal = self.x_cell + 40
                        self.y_goal = self.y_cell

            else:
                df = []
                if self.x_cell == self.x_goal and self.y_cell == self.y_goal:
                    if len(self.memory) > 0:
                        for i in range(len(self.memory)):
                            self.memory[i][2] = math.sqrt(
                                (self.memory[i][0] - self.x_cell) ** 2 + (self.memory[i][1] - self.y_cell) ** 2)
                        self.memory = sorted(self.memory, key=lambda x: x[2])
                        self.x_goal = self.memory[0][0]
                        self.y_goal = self.memory[0][1]
                    else:
                        self.x_goal = random.randint(1, 799)
                        self.y_goal = random.randint(1, 799)
                for i in food:
                    df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
                for i in self.memory[:]:
                    if math.sqrt((i[0] - self.x_cell) ** 2 + (i[1] - self.y_cell) ** 2) <= self.p_radius + (
                            self.s_radius * 20 / 255):
                        self.memory.remove(i)
                for i in df:
                    if i[0] <= self.p_radius + (self.s_radius * 20 / 255):
                        self.memory.append([i[1].x_food, i[1].y_food, 0])
                df = sorted(df, key=lambda x: x[0])
                for i in self.memory:
                    pygame.draw.circle(WIN, (0, 0, 255), (i[0], i[1]), 10, 1)
                    pygame.draw.line(WIN, (0, 0, 255), [i[0], i[1]], [self.x_cell, self.y_cell], 1)
                if self.x_cell == self.x_goal and self.y_cell == self.y_goal:
                    self.x_goal = random.randint(1, 799)
                    self.y_goal = random.randint(1, 799)
                for i in food:
                    df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
                df = sorted(df, key=lambda x: x[0])
                if df[0][0] < self.p_radius + (self.s_radius * 20 / 255):
                    self.x_goal = df[0][1].x_food
                    self.y_goal = df[0][1].y_food
                if math.sqrt((self.x_goal - self.x_cell) ** 2 + (self.y_goal - self.y_cell) ** 2) <= (
                        self.speed / 700):
                    self.x_cell = self.x_goal
                    self.y_cell = self.y_goal
                    for i in food:
                        if i.x_food == self.x_cell and i.y_food == self.y_cell:
                            food.remove(i)
                            self.food_count += 1

        def go_goal():
            if self.x_cell == self.x_goal:
                if self.y_goal < self.y_cell:
                    self.y_cell -= (self.speed / 700)
                if self.y_goal > self.y_cell:
                    self.y_cell += (self.speed / 700)
            try:
                slope = ((self.y_cell - self.y_goal) / (self.x_cell - self.x_goal))
            except:
                slope = ((self.y_cell - self.y_goal) / (0.000000000000000000000000001))
            motion = (self.speed / 700) / math.sqrt(1 + slope * slope)
            if math.sqrt(math.pow(self.x_cell - self.x_goal, 2) + math.pow(self.y_cell - self.y_goal, 2)) > math.sqrt(
                    math.pow(self.x_cell + motion - self.x_goal, 2) + math.pow(
                        self.y_cell + motion * slope - self.y_goal,
                        2)):
                self.x_cell += motion
                self.y_cell += motion * slope
            elif math.sqrt(math.pow(self.x_cell - self.x_goal, 2) + math.pow(self.y_cell - self.y_goal, 2)) > math.sqrt(
                    math.pow(self.x_cell - motion - self.x_goal, 2) + math.pow(
                        self.y_cell - motion * slope - self.y_goal,
                        2)):
                self.x_cell -= motion
                self.y_cell -= motion * slope
            pygame.draw.line(WIN, (100, 255, 100), [self.x_cell, self.y_cell], [self.x_goal, self.y_goal], 1)

        find_goal()
        go_goal()

    def reproduce(self):
        if self.reproduction_rate <= 63.75:
            food_limit = 5
        elif self.reproduction_rate > 63.75 and self.reproduction_rate <= 127.5:
            food_limit = 4
        elif self.reproduction_rate > 127.5 and self.reproduction_rate <= 191.25:
            food_limit = 3
        elif self.reproduction_rate > 191.25 and self.reproduction_rate <= 255:
            food_limit = 2
        if self.food_count >= food_limit:
            m_chance = random.randint(0, 3)
            new_speed = 0
            # = 0
            #if new_speed <= 50 or new_speed
            change = random.randint(1, 50)
            if m_chance == 1:
                new_speed = self.speed
                new_s = self.s_radius
            elif m_chance == 2:
                y = True
                while y:
                    new_speed = self.speed + change
                    new_s = self.s_radius - change
                    if new_speed >= 0 and new_speed <= 255 and new_s >= 0 and new_s <= 255:
                        y = False
                    else:
                        change -= 1
            elif m_chance == 3:
                y = True
                while y:
                    new_speed = self.speed - change
                    new_s = self.s_radius + change
                    if new_speed >= 0 and new_speed <= 255 and new_s >= 0 and new_s <= 255:
                        y = False
                    else:
                        change -= 1

            m_chance = random.randint(0, 3)
            change = random.randint(1, 50)
            if m_chance == 1:
                new_p = self.p_radius
                new_rr = self.reproduction_rate
            elif m_chance == 2:
                y = True
                while y:
                    new_p = self.p_radius + change
                    new_rr = self.reproduction_rate - change
                    if new_p >= 0 and new_p <= 255 and new_rr >= 0 and new_rr <= 255:
                        y = False
                    else:
                        change -= 1
            elif m_chance == 3:
                y = True
                while y:
                    new_p = self.speed + change
                    new_rr = self.s_radius - change
                    if new_p >= 0 and new_p <= 255 and new_rr >= 0 and new_rr <= 255:
                        y = False
                    else:
                        change -= 1

            new_x = self.x_cell + 5
            new_y = self.y_cell + 5
            new_family = self.family

            cells.append(
                Cell(new_speed, new_s, new_p, new_rr, new_x, new_y, random.randint(0, 800), random.randint(0, 800), 30,0, 1,
                     1, new_family, 0, []))

            self.c_num += 1
            self.food_count = 0


class Food:
    def __init__(self, x_food, y_food):
        self.x_food = x_food
        self.y_food = y_food

    def draw_food(self):
        pygame.draw.circle(WIN, (0, 0, 0), (self.x_food, self.y_food), 5)


# Functions
def generate_food():
    new_food = 30 - len(food)
    for x in range(new_food):
        food.append(Food(random.randint(1, 799), random.randint(1, 799)))


# Main and menu functions
def main():
    run = True

    generate_food()
    family_num = 0
    for x in range(10):
        family_num += 1
        cells.append(

            Cell(63.75, 63.75, 63.75, 63.75, random.randint(20, 722), random.randint(20, 722), random.randint(20, 722),
                 random.randint(20, 722), 30, 0, 0, 1, family_num, 0, []))

    time_count = 0

    def redraw_window():
        # Draw background
        WIN.blit(background, (0, 0))
        # Draw text (averages for all traits will get drawn in the left corner of the window)
        # Draw sprites on the screen
        for i in food:
            i.draw_food()
        for cell in cells:
            cell.draw_cell()
            cell.life_time += 1
            if cell.life_time >= 10000:
                if cell.food_count == 0 and cell.c_num == 0:
                    cell.cell_state = 0
                cell.c_num = 0
                cell.life_time = 0
            if cell.cell_state == 0:
                cells.remove(cell)
        for cell in cells:
            cell.move()

            cell.reproduce()
        # Display update
        pygame.display.update()

    while run:
        time_count += 1
        if time_count == 5000:
            generate_food()
            time_count = 0

        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


def main_menu():
    title_font = pygame.font.SysFont("monospace", 50)
    run = True
    while run:

        WIN.blit(background, (0, 0))
        title_label1 = title_font.render("PRESS ENTER TO RUN", 1, (0, 0, 0))
        title_label2 = title_font.render("EVOLUTION SIMULATION", 1, (0, 0, 0))
        WIN.blit(title_label1, (WIDTH / 2 - title_label1.get_width() / 2, 350))
        WIN.blit(title_label2, (WIDTH / 2 - title_label2.get_width() / 2, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
main_menu()


