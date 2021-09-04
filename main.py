# Imports necessary libraries
import pygame
import random
import math

from datetime import datetime

from pygame.time import set_timer

# Imports food and cell classes
from food import Food
from cell import Cell

# Window setup & global variables
pygame.init()
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Evolution')
background = pygame.Surface(WIN.get_size())
background = background.convert()
background.fill((0, 0, 0))
pygame.font.init()
cells = []
food = []
set_time = 10

# Functions
def generate_food():
    new_food = 30 - len(food)
    for x in range(new_food):
        food.append(Food(random.randint(1, WIDTH), random.randint(1, HEIGHT)))

# Main and menu functions
def main(set_time):
    run = True
    generate_food()
    for x in range(20):
        cells.append(
            Cell(127.5, 127.5, 127.5, 127.5, random.randint(1, WIDTH), random.randint(1, HEIGHT), random.randint(1, WIDTH),
                 random.randint(1, HEIGHT), random.randint(1, 2), 0, 0, 1, 0, []))

    time_count = 0

    def redraw_window():
        average_font = pygame.font.SysFont("monospace", 20)
        all_averages = [0, 0, 0, 0]
        # Draw background
        WIN.blit(background, (0, 0))
        # Draw text (averages for all traits will get drawn in the left corner of the window)
        # Draw food and cells on the screen
        for i in food:
            i.draw_food(WIN)
        for cell in cells:
            cell.find_goal(cells, food, WIN, WIDTH, HEIGHT, set_time)
        for cell in cells:
            cell.go_goal(set_time)
        for cell in cells:
            cell.draw_cell(WIN)
            cell.life_time += (set_time * 0.001)
            if cell.life_time >= 5000:
                if cell.food_count == 0 and cell.c_num == 0:
                    cell.cell_state = 0
                cell.c_num = 0
                cell.life_time = 0
            if cell.cell_state == 0:
                food.append(Food(cell.x_cell, cell.y_cell))
                cells.remove(cell)
            cell.reproduce(cells, WIDTH, HEIGHT)

            all_averages[0] += cell.s_radius
            all_averages[1] += cell.speed
            all_averages[2] += cell.p_radius
            all_averages[3] += cell.reproduction_rate
        all_averages[:] = [round(x / len(cells)) for x in all_averages]
        sr_average = average_font.render("Size Radius :" + str(all_averages[0]), 1, (250, 250, 250))
        s_average = average_font.render("Speed :" + str(all_averages[1]), 1, (250, 250, 250))
        pr_average = average_font.render("Perception Radius :" + str(all_averages[2]), 1, (250, 250, 250))
        rr_average = average_font.render("Reproduction Rate :" + str(all_averages[3]), 1, (250, 250, 250))
        time = average_font.render("Time :" + str(set_time), 1, (250, 250, 250))
        food_count = average_font.render("Food :" + str(len(food)), 1, (250, 250, 250))
        cell_count = average_font.render("Cell :" + str(len(cells)), 1, (250, 250, 250))
        WIN.blit(sr_average, (20, 20))
        WIN.blit(s_average, (20, 40))
        WIN.blit(pr_average, (20, 60))
        WIN.blit(rr_average, (20, 80))
        WIN.blit(food_count, (20, 120))
        WIN.blit(cell_count, (20, 140))
        WIN.blit(time, (20, 160))
        # Display update
        pygame.display.update()


    while run:
        time_count += 1
        if time_count >= (10 * set_time):
            generate_food()
            time_count = 0

        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if set_time - 1 >= 10:
                        set_time = set_time - 1
                if event.key == pygame.K_RIGHT:
                    set_time = set_time + 1
                if event.key == pygame.K_SPACE:
                    f = open("storage", "a")
                    f.write(datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + "\n")
                    food1 = []
                    for x in food:
                        food1.append([x.x_food, x.y_food])
                    f.write(str(food1) + "\n")
                    cells1 = []
                    for x in cells:
                        cells1.append([x.speed, x.s_radius, x.p_radius, x.reproduction_rate, x.x_cell, x.y_cell, x.x_goal, x.y_goal, x.food_type, x.food_count, x.c_num, x.cell_state, x.life_time, x.memory])
                    f.write(str(cells1) + "\n")
                    f.write(str(set_time) + "\n")
                    f.close()
            
def settings():
    setting_font = pygame.font.SysFont("monospace", 20)
    title_font = pygame.font.SysFont("monospace", 50)
    button_font = pygame.font.SysFont("monospace", 15)
    run = True
    while run:
        WIN.blit(background, (0, 0))
        settings_title = title_font.render("SETTINGS", 1, (250, 250, 250))
        f_num_txt = setting_font.render("Amount of food:", 1, (250, 250, 250))
        c_num_txt = setting_font.render("Initial amount of cells:", 1, (250, 250, 250))
        w_set = setting_font.render("Window width:", 1, (250, 250, 250))
        set_button = button_font.render("menu", 1, (0, 0, 0))
        WIN.blit(settings_title, (WIDTH/2 - settings_title.get_width()/2, 10))
        WIN.blit(f_num_txt, (20, 100))
        WIN.blit(c_num_txt, (20, 200))
        WIN.blit(w_set, (20, 300))
        mbx = 100
        mby = 700
        pygame.draw.circle(WIN, (250, 250, 250), (mbx, mby), 50)
        WIN.blit(set_button, (mbx-20, mby-10))
        pygame.display.update()
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and math.sqrt((mousex - mbx) ** 2 + (mousey - mby) ** 2) < 50:
                main_menu()
def main_menu(set_time):
    title_font = pygame.font.SysFont("monospace", 50)
    button_font = pygame.font.SysFont("monospace", 15)
    run = True
    while run:
        WIN.blit(background, (0, 0))
        title1 = title_font.render("PRESS ENTER TO RUN", 1, (250, 250, 250))
        title2 = title_font.render("EVOLUTION SIMULATION", 1, (250, 250, 250))
        set_button = button_font.render("settings", 1, (0, 0, 0))
        WIN.blit(title1, (WIDTH / 2 - title1.get_width() / 2, 350))
        WIN.blit(title2, (WIDTH / 2 - title2.get_width() / 2, 400))
        sbx = 100
        sby = 700
        pygame.draw.circle(WIN, (250, 250, 250), (sbx, sby), 50)
        WIN.blit(set_button, (sbx-35, sby - 10))
        pygame.display.update()
        mousex, mousey = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(set_time)
            if event.type == pygame.MOUSEBUTTONDOWN and math.sqrt((mousex - sbx) ** 2 + (mousey - sby) ** 2) < 50:
                settings()
    pygame.quit()
main_menu(set_time)
