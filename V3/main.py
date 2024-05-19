import pygame
import os

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Clue Solver')

WHITE = (255, 255, 255)
BLUE = (74, 175, 212)

FPS = 60

PEACOCK_IMAGE = pygame.image.load(os.path.join('V3','Assets', 'peacock.png'))

def draw_window():
    WIN.fill(BLUE)
    WIN.blit(PEACOCK_IMAGE, (25, 60))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()