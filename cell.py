# Imports necessary libraries
import pygame
import random
import math
pygame.init()

# Cell class
class Cell:
    def __init__(self, speed, s_radius, p_radius, reproduction_rate, x_cell, y_cell, x_goal, y_goal, anger, food_count,
                 c_num, cell_state, life_time, memory):
        self.life_time = life_time
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
        self.color = (speed, reproduction_rate, s_radius)
        self.reproduction_rate = reproduction_rate
        self.memory = memory

    def draw_cell(self, surface):
        pygame.draw.line(surface, (100, 255, 100), [self.x_cell, self.y_cell], [self.x_goal, self.y_goal], 1)

        k = 500

        if self.y_cell != self.y_goal and self.x_cell != self.x_goal:

            try:
                z = 10 / math.sqrt(1 + (((self.y_goal - self.y_cell)/(self.x_goal - self.x_cell)) * ((self.y_goal - self.y_cell)/(self.x_goal - self.x_cell))))
            except:
                z = 10 / 0.000000000001
            p = self.x_cell + z
            p1 = self.y_cell + (z * ((self.y_goal - self.y_cell)/(self.x_goal - self.x_cell)))
            z1 = k / math.sqrt(1 + (-1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell))) * (-1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell))))

            m = ((p1 + (z1 * -1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell)))) - self.y_cell) / ((p + z1) - self.x_cell)
            m1 = ((p1 - (z1 * -1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell)))) - self.y_cell) / ((p - z1) - self.x_cell)

            #print("slopes : " + str(m1) + "  : " + str(m))

            z2 = (self.p_radius/2 + (self.s_radius * 20 / 510)) / math.sqrt(1 + m * m)
            z3 = (self.p_radius/2 + (self.s_radius * 20 / 510)) / math.sqrt(1 + m1 * m1)

            pygame.draw.line(surface, (125, 0, 125), [self.x_cell, self.y_cell], [self.x_cell + z2, self.y_cell + m * z2], 1)
            pygame.draw.line(surface, (125, 0, 125), [self.x_cell, self.y_cell], [self.x_cell + z3, self.y_cell + m1 * z3], 1)

        for i in self.memory:
            pygame.draw.circle(surface, (0, 0, 255), (i[0], i[1]), 10, 1)
            pygame.draw.line(surface, (0, 0, 255), [i[0], i[1]], [self.x_cell, self.y_cell], 1)
        pygame.draw.circle(surface, (100, 100, 255), (self.x_cell, self.y_cell), self.p_radius/2 + (self.s_radius * 20 / 510),
                           width=2)
        pygame.draw.circle(surface, (255, 100, 100), (self.x_cell, self.y_cell), 20 + (self.s_radius * 20 / 510), width=2)
        pygame.draw.circle(surface, self.color, (self.x_cell, self.y_cell), 5 + (self.s_radius * 20 / 510))

    def move(self, cells, food, surface, surface_width, surface_height):
        def find_goal():
            aggression = random.randint(0, self.anger)
            dc = []
            for i in cells:
                if (i.x_cell, i.y_cell) != (self.x_cell, self.y_cell):
                    dc.append([math.sqrt((i.x_cell - self.x_cell) ** 2 + (i.y_cell - self.y_cell) ** 2), i])
            dc = sorted(dc, key=lambda x: x[0])
            if len(dc) > 0 and dc[0][0] < 20 + (self.s_radius * 20 / 510) and dc[0][1].s_radius >= self.s_radius:
                x_e, y_e = dc[0][1].x_cell, dc[0][1].y_cell
                x_goal, y_goal = dc[0][1].x_goal, dc[0][1].y_goal
                if aggression == 0 and self.s_radius > dc[0][1].s_radius and dc[0][1].life_time > 0 and self.life_time > 0:
                    self.cell_state = 0
                else:
                    if x_e > self.x_cell:
                        self.x_goal = self.x_cell - self.p_radius
                        self.y_goal = self.y_cell
                    else:
                        self.x_goal = self.x_cell + self.p_radius
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
                        self.x_goal = random.randint(1, surface_width)
                        self.y_goal = random.randint(1, surface_height)
                for i in food:
                    df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
                for i in self.memory[:]:
                    if math.sqrt((i[0] - self.x_cell) ** 2 + (i[1] - self.y_cell) ** 2) <= self.p_radius/2 + (
                            self.s_radius * 20 / 510):
                        self.memory.remove(i)
                for i in df:
                    if i[0] <= self.p_radius/2 + (self.s_radius * 20 / 510):
                        self.memory.append([i[1].x_food, i[1].y_food, 0])
                df = sorted(df, key=lambda x: x[0])
                for i in food:
                    df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
                df = sorted(df, key=lambda x: x[0])
                if len(df) > 0:
                    if df[0][0] < self.p_radius/2 + (self.s_radius * 20 / 255):
                        self.x_goal = df[0][1].x_food
                        self.y_goal = df[0][1].y_food
                if math.sqrt((self.x_goal - self.x_cell) ** 2 + (self.y_goal - self.y_cell) ** 2) <= (
                        self.speed / 1000):
                    self.x_cell = self.x_goal
                    self.y_cell = self.y_goal
                    for i in food:
                        if i.x_food == self.x_cell and i.y_food == self.y_cell:
                            food.remove(i)
                            self.food_count += 1

        def go_goal():
            if self.x_cell == self.x_goal:
                if self.y_goal < self.y_cell:
                    self.y_cell -= (self.speed / 1000)
                if self.y_goal > self.y_cell:
                    self.y_cell += (self.speed / 1000)
            try:
                slope = ((self.y_cell - self.y_goal) / (self.x_cell - self.x_goal))
            except:
                slope = ((self.y_cell - self.y_goal) / (0.000000000000000000000000001))
            motion = (self.speed / 1000) / math.sqrt(1 + slope * slope)
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

        find_goal()
        go_goal()

    def reproduce(self, cells, surface_width, surface_height):
        if self.reproduction_rate <= 63.75:
            food_limit = 5
        elif self.reproduction_rate > 63.75 and self.reproduction_rate <= 127.5:
            food_limit = 4
        elif self.reproduction_rate > 127.5 and self.reproduction_rate <= 191.25:
            food_limit = 3
        elif self.reproduction_rate > 191.25 and self.reproduction_rate <= 255:
            food_limit = 2
        if self.food_count >= food_limit:
            m_chance = random.randint(0, 2)
            new_speed = 0
            change = random.randint(1, 55)
            if m_chance == 0:
                new_speed = self.speed
                new_s = self.s_radius
            elif m_chance == 1:
                y = True
                while y:
                    new_speed = self.speed + change
                    new_s = self.s_radius - change
                    if new_speed >= 0 and new_speed <= 255 and new_s >= 0 and new_s <= 255:
                        y = False
                    else:
                        change -= 1
            elif m_chance == 2:
                y = True
                while y:
                    new_speed = self.speed - change
                    new_s = self.s_radius + change
                    if new_speed >= 0 and new_speed <= 255 and new_s >= 0 and new_s <= 255:
                        y = False
                    else:
                        change -= 1

            m_chance = random.randint(0, 2)
            change = random.randint(1, 55)
            if m_chance == 0:
                new_p = self.p_radius
                new_rr = self.reproduction_rate
            elif m_chance == 1:
                y = True
                while y:
                    new_p = self.p_radius + change
                    new_rr = self.reproduction_rate - change
                    if new_p >= 0 and new_p <= 255 and new_rr >= 0 and new_rr <= 255:
                        y = False
                    else:
                        change -= 1
            elif m_chance == 2:
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

            cells.append(
                Cell(new_speed, new_s, new_p, new_rr, new_x, new_y, random.randint(0, surface_width), random.randint(0, surface_height), 30, 0, 1,
                     1, -1000, []))

            self.c_num += 1
            self.food_count = 0
