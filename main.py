# Imports necessary libraries
import pygame
import random
import math

# Imports food and cell classes
from food import Food
from cell import Cell

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

# Functions
def generate_food():
    new_food = 25 - len(food)
    for x in range(new_food):
        food.append(Food(random.randint(1, WIDTH), random.randint(1, HEIGHT)))

# Main and menu functions
def main():
    run = True
    generate_food()
    for x in range(30):
        cells.append(
            Cell(127.5, 127.5, 127.5, 127.5, random.randint(1, WIDTH), random.randint(1, HEIGHT), random.randint(1, WIDTH),
                 random.randint(1, HEIGHT), 30, 0, 0, 1, 0, []))

    time_count = 0

    def redraw_window():
        # Draw background
        WIN.blit(background, (0, 0))
        # Draw text (averages for all traits will get drawn in the left corner of the window)
        # Draw food and cells on the screen
        for i in food:
            i.draw_food(WIN)
        for cell in cells:
            cell.draw_cell(WIN)
            cell.life_time += 1
            if cell.life_time >= 5000:
                if cell.food_count == 0 and cell.c_num == 0:
                    cell.cell_state = 0
                cell.c_num = 0
                cell.life_time = 0
            if cell.cell_state == 0:
                cells.remove(cell)
        for cell in cells:
            cell.move(cells, food, WIN, WIDTH, HEIGHT)

            cell.reproduce(cells, WIDTH, HEIGHT)
        # Display update
        pygame.display.update()

    while run:
        time_count += 1
        if time_count == 10000:
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




