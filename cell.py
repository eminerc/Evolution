# Imports necessary libraries
import pygame
import random
import math
pygame.init()

# Cell class
class Cell:
    def __init__(self, speed, s_radius, p_radius, reproduction_rate, x_cell, y_cell, x_goal, y_goal, food_type, food_count,
                 c_num, cell_state, life_time, memory):
        self.life_time = life_time
        self.c_num = c_num
        self.food_count = food_count
        self.food_type = food_type
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

        for i in self.memory:
            pygame.draw.circle(surface, (0, 0, 255), (i[0], i[1]), 10, 1)
            pygame.draw.line(surface, (0, 0, 255), [i[0], i[1]], [self.x_cell, self.y_cell], 1)
        pygame.draw.circle(surface, (25, 25, 100), (self.x_cell, self.y_cell), self.p_radius/2 + (self.s_radius * 20 / 510),
                           width=2)
        pygame.draw.circle(surface, (255, 100, 100), (self.x_cell, self.y_cell), (self.p_radius/2 + (self.s_radius * 20 / 510)) / 2, width=2)
        #if self.food_type != 3:
        pygame.draw.circle(surface, self.color, (self.x_cell, self.y_cell), 5 + (self.s_radius * 20 / 510))
        #else:
            #pygame.draw.circle(surface, (255, 100, 100), (self.x_cell, self.y_cell), 5 + (self.s_radius * 20 / 510))

        if self.y_cell != self.y_goal and self.x_cell != self.x_goal:

            try:
                z = 10 / math.sqrt(1 + (((self.y_goal - self.y_cell)/(self.x_goal - self.x_cell)) * ((self.y_goal - self.y_cell)/(self.x_goal - self.x_cell))))
            except:
                z = 10 / 0.000000000001

            #pygame.draw.circle(surface, (0, 255, 0), (self.x_cell + z, self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))), 5)
            mxy = -1 * ((self.x_goal-self.x_cell)/(self.y_goal-self.y_cell))
            x = (self.x_cell + z) + 1 * 1000
            #y = (self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) + mxy * 1000
            #x1 = (self.x_cell + z) - 1 * 1000
            #y1 = (self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) - mxy * 1000
            #pygame.draw.line(surface, (100, 255, 100), [x, y], [x1, y1], 1)

            k = 10

            z1 = k / math.sqrt(1 + (-1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell))) * (-1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell))))

            #pygame.draw.circle(surface, (0, 255, 0), (self.x_cell + z + z1, (self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) + mxy * z1), 5)
            #pygame.draw.circle(surface, (0, 255, 0), (self.x_cell + z - z1, (self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) - mxy * z1), 5)

            m2 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) + mxy * z1)) / (self.x_cell - (self.x_cell + z + z1))
            z2 = (self.p_radius/2 + (self.s_radius * 20 / 510)) / math.sqrt(1 + m2 * m2)

            if (self.x_goal-self.x_cell) == 0:
                m3 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/0.000000001)) - mxy * z1)) / (self.x_cell - (self.x_cell + z - z1))
            elif (self.x_cell - (self.x_cell + z - z1)) == 0:
                m3 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) - mxy * z1)) / 0.00000000001
            else:
                m3 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) - mxy * z1)) / (self.x_cell - (self.x_cell + z - z1))
            z3 = (self.p_radius/2 + (self.s_radius * 20 / 510)) / math.sqrt(1 + m3 * m3)

            m4 = (self.y_goal - self.y_cell) / (self.x_goal - self.x_cell)
            z4 = ((self.p_radius/2 + (self.s_radius * 20 / 510)) - 1) / math.sqrt(1 + m4 * m4)

            m5 = -1 / m4
            z5 = ((self.p_radius/2 + (self.s_radius * 20 / 510)) - 1) / math.sqrt(1 + m5 * m5)

            points1 = [[self.x_cell - z5, self.y_cell - (z5 * m5)], [self.x_cell - z4, self.y_cell - (z4 * m4)], [self.x_cell + z5, self.y_cell + (z5 * m5)], [self.x_cell + z4, self.y_cell + (z4 * m4)]]

            points1_copy = []

            for x in points1:
                points1_copy.append([x[0] + random.randint(0, 30), x[1] + random.randint(0, 30)])
                points1_copy.append([x[0] + random.randint(0, 30), x[1] + random.randint(0, 30)])
                points1_copy.append([x[0] + random.randint(0, 30), x[1] + random.randint(0, 30)])
                points1_copy.append([x[0] - random.randint(0, 30), x[1] - random.randint(0, 30)])
                points1_copy.append([x[0] - random.randint(0, 30), x[1] - random.randint(0, 30)])
                points1_copy.append([x[0] - random.randint(0, 30), x[1] - random.randint(0, 30)])

            points1 = points1_copy

            points = [[self.x_cell + z2, self.y_cell + (z2 * m2), 0], [self.x_cell + z3, self.y_cell + (z3 * m3), 0], [self.x_cell - z2, self.y_cell - (z2 * m2), 0], [self.x_cell - z3, self.y_cell - (z3 * m3), 0]]

            for x in points:
                x[2] = math.sqrt((x[0] - self.x_goal) ** 2 + (x[1] - self.y_goal) ** 2)

            points = sorted(points, key=lambda x: x[2])

            setting_font = pygame.font.SysFont("monospace", 20)

            pygame.draw.line(surface, (100, 100, 255), [self.x_cell, self.y_cell], [points[0][0], points[0][1]], 2)
            #pygame.draw.circle(surface, (255, 0, 255), (points[0][0], points[0][1]), 10)
            pygame.draw.line(surface, (100, 100, 255), [self.x_cell, self.y_cell], [points[1][0], points[1][1]], 2)
            #pygame.draw.circle(surface, (0, 255, 0), (points[1][0], points[1][1]), 10)

    def find_goal(self, cells, food, surface, surface_width, surface_height, set_time):
        def scope_check(x):
            if self.y_cell != self.y_goal and self.x_cell != self.x_goal:

                try:
                    z = 10 / math.sqrt(1 + (((self.y_goal - self.y_cell)/(self.x_goal - self.x_cell)) * ((self.y_goal - self.y_cell)/(self.x_goal - self.x_cell))))
                except:
                    z = 10 / 0.000000000001

                mxy = -1 * ((self.x_goal-self.x_cell)/(self.y_goal-self.y_cell))
                #x = (self.x_cell + z) + 1 * 1000

                k = 10

                z1 = k / math.sqrt(1 + (-1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell))) * (-1 * ((self.x_goal - self.x_cell)/(self.y_goal - self.y_cell))))

                m2 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) + mxy * z1)) / (self.x_cell - (self.x_cell + z + z1))
                z2 = (self.p_radius/2 + (self.s_radius * 20 / 510)) / math.sqrt(1 + m2 * m2)

                if (self.x_goal-self.x_cell) == 0:
                    m3 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/0.000000001)) - mxy * z1)) / (self.x_cell - (self.x_cell + z - z1))
                elif (self.x_cell - (self.x_cell + z - z1)) == 0:
                    m3 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) - mxy * z1)) / 0.00000000001
                else:
                    m3 = (self.y_cell - ((self.y_cell + z * ((self.y_goal-self.y_cell)/(self.x_goal-self.x_cell))) - mxy * z1)) / (self.x_cell - (self.x_cell + z - z1))
                z3 = (self.p_radius/2 + (self.s_radius * 20 / 510)) / math.sqrt(1 + m3 * m3)

                points = [[self.x_cell + z2, self.y_cell + (z2 * m2), 0], [self.x_cell + z3, self.y_cell + (z3 * m3), 0], [self.x_cell - z2, self.y_cell - (z2 * m2), 0], [self.x_cell - z3, self.y_cell - (z3 * m3), 0]]

                for t in points:
                    t[2] = math.sqrt((t[0] - self.x_goal) ** 2 + (t[1] - self.y_goal) ** 2)

                points = sorted(points, key=lambda t: t[2])

                if math.sqrt((x[0] - self.x_cell) ** 2 + (x[1] - self.y_cell) ** 2) < self.p_radius/2 + (self.s_radius * 20 / 255):
                    if (points[0][0] > self.x_cell and points[1][0] > self.x_cell) or (points[0][0] < self.x_cell and points[1][0] < self.x_cell):
                        if self.y_goal > self.y_cell:
                            if abs(((self.y_cell-points[1][1])/(self.x_cell-points[1][0]))) < abs(((self.y_cell-points[0][1])/(self.x_cell-points[0][0]))):
                                if x[1] - self.y_cell > ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell < ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell):
                                    return True
                                else:
                                    return False
                            else:
                                if x[1] - self.y_cell < ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell > ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell):
                                    return True
                                else:
                                    return False
                        else:
                            if abs(((self.y_cell-points[1][1])/(self.x_cell-points[1][0]))) > abs(((self.y_cell-points[0][1])/(self.x_cell-points[0][0]))):
                                if x[1] - self.y_cell > ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell < ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell):
                                    return True
                                else:
                                    return False
                            else:
                                if x[1] - self.y_cell < ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell > ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell):
                                    return True
                                    #print("Four Slopes: " + str((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) + " " + str((self.y_cell-points[0][1])/(self.x_cell-points[0][0])))
                                else:
                                    return False
                    elif self.y_goal > self.y_cell:
                        if x[1] - self.y_cell > ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell > ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell):
                            #x[1] - self.y_cell < ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell < ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell)
                            return True
                        else:
                            return False
                    else:
                        if x[1] - self.y_cell < ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell < ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell):
                            #x[1] - self.y_cell < ((self.y_cell-points[1][1])/(self.x_cell-points[1][0])) * (x[0] - self.x_cell) and x[1] - self.y_cell < ((self.y_cell-points[0][1])/(self.x_cell-points[0][0])) * (x[0] - self.x_cell)
                            return True
                        else:
                            return False

                else:
                    return False


        #aggression = random.randint(0, self.anger)
        dc = []
        for i in cells:
            if (i.x_cell, i.y_cell) != (self.x_cell, self.y_cell):
                dc.append([math.sqrt((i.x_cell - self.x_cell) ** 2 + (i.y_cell - self.y_cell) ** 2), i, math.sqrt((i.x_cell - self.x_cell) ** 2 + (i.y_cell - self.y_cell) ** 2)])
        dc = sorted(dc, key=lambda x: x[0])
        if len(dc) > 0 and dc[0][0] < ((self.p_radius/2 + (self.s_radius * 20 / 510)) / 2) and dc[0][1].s_radius >= self.s_radius:
            x_e, y_e = dc[0][1].x_cell, dc[0][1].y_cell
            #x_goal, y_goal = dc[0][1].x_goal, dc[0][1].y_goal
            #if self.s_radius > dc[0][1].s_radius and dc[0][1].life_time > 0 and self.life_time > 0:
                #self.cell_state = 0
            #else:
            # self.p_radius/2 + (self.s_radius * 20 / 510)
            try:
                m = (self.y_cell - y_e) / (self.x_cell - x_e)
            except:
                m = (self.y_cell - y_e) / 0.0000001
            z = 20 / math.sqrt(1 + m * m)

            if dc[0][1].x_cell < self.x_cell and dc[0][1].y_cell < self.y_cell:
                self.x_goal = self.x_cell + z
                self.y_goal = self.y_cell + z * m
            elif dc[0][1].x_cell > self.x_cell and dc[0][1].y_cell < self.y_cell:
                self.x_goal = self.x_cell - z
                self.y_goal = self.y_cell - z * m
            elif dc[0][1].x_cell > self.x_cell and dc[0][1].y_cell > self.y_cell:
                self.x_goal = self.x_cell - z
                self.y_goal = self.y_cell - z * m
            elif dc[0][1].x_cell < self.x_cell and dc[0][1].y_cell > self.y_cell:
                self.x_goal = self.x_cell + z
                self.y_goal = self.y_cell + z * m
            """
            if x_e > self.x_cell:
                self.x_goal = self.x_cell - self.p_radius
                self.y_goal = self.y_cell
            else:
                self.x_goal = self.x_cell + self.p_radius
                self.y_goal = self.y_cell
            """
        #"""
        #elif self.food_type == 3:
            #if len(dc) > 0 and dc[0][0] < ((self.p_radius / 2 + (self.s_radius * 20 / 510)) / 2) and dc[0][
                #1].s_radius < self.s_radius and dc[0][1].speed < self.speed:
                #self.x_goal = dc[0][1].x_cell
                #self.y_goal = dc[0][1].y_cell
                #if dc[0][0] < 10:
 #                   #dc[0][1].cell_state = 0
 #                   #self.food_count += dc[0][1].food_count
 #           #elif self.x_goal == self.x_cell and self.y_goal == self.y_cell:
 #               #self.x_goal = random.randint(1, surface_width)
 #               #self.y_goal = random.randint(1, surface_height)
#
 #           if math.sqrt((self.x_goal - self.x_cell) ** 2 + (self.y_goal - self.y_cell) ** 2) <= (
 #                   self.speed / set_time):
 #               self.x_cell = self.x_goal
 #               self.y_cell = self.y_goal
 #       elif self.food_type == 4:
 #           all_targets = []
 #           for x in dc:
 #               all_targets.append(x)
#
 #           df = []
 #           for i in food:
 #               df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
 #           for i in self.memory[:]:
 #               if math.sqrt((i[0] - self.x_cell) ** 2 + (i[1] - self.y_cell) ** 2) <= self.p_radius/2 + (
 #                       self.s_radius * 20 / 510) and (scope_check([i[0], i[1]]) or (i[0] == self.x_cell and i[1] == self.y_cell)):
 #                   self.memory.remove(i)
 #           for i in df:
 #               if i[0] <= self.p_radius/2 + (self.s_radius * 20 / 510) and scope_check([i[1].x_food, i[1].y_food]):
 #                   self.memory.append([i[1].x_food, i[1].y_food, 0])
#
 #           for i in range(len(self.memory)):
 #                       self.memory[i][2] = math.sqrt(
 #                           (self.memory[i][0] - self.x_cell) ** 2 + (self.memory[i][1] - self.y_cell) ** 2)
#
 #           for x in self.memory:
 #               all_targets.append(x)
#
 #           all_targets = sorted(all_targets, key=lambda x: x[2])
#
 #           try:
 #               all_targets[0][1].self.x = all_targets[0][1].self.x
 #               if all_targets[0][0] < ((self.p_radius / 2 + (self.s_radius * 20 / 510)) / 2) and all_targets[0][
 #               1].s_radius < self.s_radius and all_targets[0][1].speed < self.speed:
 #                   self.x_goal = all_targets[0][1].x_cell
 #                   self.y_goal = all_targets[0][1].y_cell
 #                   if all_targets[0][0] < 10:
 #                       all_targets[0][1].cell_state = 0
 #                       self.food_count += all_targets[0][1].food_count
 #                       print("I ate some food!")
 #               elif self.x_goal == self.x_cell and self.y_goal == self.y_cell:
 #                   self.x_goal = random.randint(1, surface_width)
 #                   self.y_goal = random.randint(1, surface_height)
#
 #               if math.sqrt((self.x_goal - self.x_cell) ** 2 + (self.y_goal - self.y_cell) ** 2) <= (
 #                       self.speed / set_time):
 #                   self.x_cell = self.x_goal
 #                   self.y_cell = self.y_goal
 #           except:
 #               df = []
 #               if self.x_cell == self.x_goal and self.y_cell == self.y_goal:
 #                   if len(self.memory) > 0:
 #                       for i in range(len(self.memory)):
 #                           self.memory[i][2] = math.sqrt(
 #                               (self.memory[i][0] - self.x_cell) ** 2 + (self.memory[i][1] - self.y_cell) ** 2)
 #                       self.memory = sorted(self.memory, key=lambda x: x[2])
 #                       self.x_goal = self.memory[0][0]
 #                       self.y_goal = self.memory[0][1]
 #                   else:
 #                       self.x_goal = random.randint(1, surface_width)
 #                       self.y_goal = random.randint(1, surface_height)
 #               for i in food:
 #                   df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
 #               for i in self.memory[:]:
 #                   if math.sqrt((i[0] - self.x_cell) ** 2 + (i[1] - self.y_cell) ** 2) <= self.p_radius/2 + (
 #                           self.s_radius * 20 / 510) and (scope_check([i[0], i[1]]) or (i[0] == self.x_cell and i[1] == self.y_cell)):
 #                       self.memory.remove(i)
 #               for i in df:
 #                   if i[0] <= self.p_radius/2 + (self.s_radius * 20 / 510) and scope_check([i[1].x_food, i[1].y_food]):
 #                       self.memory.append([i[1].x_food, i[1].y_food, 0])
 #               df = sorted(df, key=lambda x: x[0])
 #               for i in food:
 #                   df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
 #               df = sorted(df, key=lambda x: x[0])
 #               if len(df) > 0:
 #                   if df[0][0] < self.p_radius/2 + (self.s_radius * 20 / 255) and scope_check([df[0][1].x_food, df[0][1].y_food]):
 #                       self.x_goal = df[0][1].x_food
 #                       self.y_goal = df[0][1].y_food
 #               if math.sqrt((self.x_goal - self.x_cell) ** 2 + (self.y_goal - self.y_cell) ** 2) <= (
 #                       self.speed / set_time):
 #                   self.x_cell = self.x_goal
 #                   self.y_cell = self.y_goal
 #                   for i in food:
 #                       if i.x_food == self.x_cell and i.y_food == self.y_cell:
 #                           food.remove(i)
 #                           self.food_count += 1
#
 #           #print("All Targets : " + str(all_targets))
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
                        self.s_radius * 20 / 510) and (scope_check([i[0], i[1]]) or (i[0] == self.x_cell and i[1] == self.y_cell)):
                    self.memory.remove(i)
            for i in df:
                if i[0] <= self.p_radius/2 + (self.s_radius * 20 / 510) and scope_check([i[1].x_food, i[1].y_food]):
                    self.memory.append([i[1].x_food, i[1].y_food, 0])
            df = sorted(df, key=lambda x: x[0])
            for i in food:
                df.append([math.sqrt((i.x_food - self.x_cell) ** 2 + (i.y_food - self.y_cell) ** 2), i])
            df = sorted(df, key=lambda x: x[0])
            if len(df) > 0:
                if df[0][0] < self.p_radius/2 + (self.s_radius * 20 / 255) and scope_check([df[0][1].x_food, df[0][1].y_food]):
                    self.x_goal = df[0][1].x_food
                    self.y_goal = df[0][1].y_food
            if math.sqrt((self.x_goal - self.x_cell) ** 2 + (self.y_goal - self.y_cell) ** 2) <= (
                    self.speed / set_time):
                self.x_cell = self.x_goal
                self.y_cell = self.y_goal
                for i in food:
                    if i.x_food == self.x_cell and i.y_food == self.y_cell:
                        food.remove(i)
                        self.food_count += 1


    def go_goal(self, set_time):
        if self.x_cell == self.x_goal:
            if self.y_goal < self.y_cell:
                self.y_cell -= (self.speed / set_time)
            if self.y_goal > self.y_cell:
                self.y_cell += (self.speed / set_time)
        try:
            slope = ((self.y_cell - self.y_goal) / (self.x_cell - self.x_goal))
        except:
            slope = ((self.y_cell - self.y_goal) / (0.000000000000000000000000001))
        motion = (self.speed / set_time) / math.sqrt(1 + slope * slope)
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
                new_p = self.p_radius
            elif m_chance == 1:
                y = True
                while y:
                    new_speed = self.speed + change
                    new_p = self.p_radius - change
                    if new_speed >= 0 and new_speed <= 255 and new_p >= 0 and new_p <= 255:
                        y = False
                    else:
                        change -= 1
            elif m_chance == 2:
                y = True
                while y:
                    new_speed = self.speed - change
                    new_p = self.p_radius + change
                    if new_speed >= 0 and new_speed <= 255 and new_p >= 0 and new_p <= 255:
                        y = False
                    else:
                        change -= 1

            m_chance = random.randint(0, 2)
            change = random.randint(1, 55)
            if m_chance == 0:
                new_s = self.s_radius
                new_rr = self.reproduction_rate
            elif m_chance == 1:
                y = True
                while y:
                    new_s = self.s_radius + change
                    new_rr = self.reproduction_rate - change
                    if new_s >= 0 and new_s <= 255 and new_rr >= 0 and new_rr <= 255:
                        y = False
                    else:
                        change -= 1
            elif m_chance == 2:
                y = True
                while y:
                    new_s = self.s_radius + change
                    new_rr = self.reproduction_rate - change
                    if new_s >= 0 and new_s <= 255 and new_rr >= 0 and new_rr <= 255:
                        y = False
                    else:
                        change -= 1

            new_x = self.x_cell + 5
            new_y = self.y_cell + 5

            cells.append(
                Cell(new_speed, new_s, new_p, new_rr, new_x, new_y, random.randint(0, surface_width), random.randint(0, surface_height), random.randint(1, 3), 0, 1,
                     1, -1000, []))

            self.c_num += 1
            self.food_count = 0
