import sys, pygame
pygame.init()

size = width, height = 1024, 524
SCALE_FACTOR = 0.4
IMAGE_SIZE = (int(width * SCALE_FACTOR), int(height * SCALE_FACTOR))
black = 0, 0, 0
white = 255, 255, 255
step = 0

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.font.init()
font = pygame.font.SysFont("Modern Sans", 30)

image = pygame.image.load("0f5.gif")
image = pygame.transform.scale(image, IMAGE_SIZE)
image_rect = image.get_rect()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    text_screen = font.render(step, False, black)

    screen.fill(white)
    screen.blit(image, (0, 0))
    screen.blit(text_screen, (900, 500))
    pygame.display.flip()