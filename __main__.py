import sys, pygame
pygame.init()

size = width, height = 1024, 524
aspect_ratio = width / height
SCALE_FACTOR = 0.4
image_size = (int(width * SCALE_FACTOR), int(height * SCALE_FACTOR))
image_pos = 0, 0
step = 'Frame Count: 0'

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0, 0
blue = 0, 0, 255, 0

screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.font.init()
font = pygame.font.SysFont("Modern Sans", 30)

image = pygame.image.load("0f5.gif")
image = pygame.transform.scale(image, image_size)
button_next_dim = (width / 2 + 30, height / 2, 60, 20)
button_prev_dim = (width / 2 - 60,  height - 100, 60, 20)
next_button = pygame.Rect(button_prev_dim)
prev_button = pygame.Rect(button_next_dim)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("MOUSE PRESSED")
            mouse_pos = event.pos
            if next_button.collidepoint(mouse_pos):
                print("Next button pushed")
            elif prev_button.collidepoint(mouse_pos):
                print("Prev button pushed")
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            width, height = screen.get_width(), screen.get_height()
            gap_width = height // 10
            text_pos = width - 200, height - gap_width
            image_size = width, height - gap_width
            button_next_dim = (width // 2 + 60, height - gap_width // 1.5, 60, gap_width // 2)
            button_prev_dim = (width // 2 - 120,  height - gap_width // 1.5, 60, gap_width // 2)
            next_button = pygame.Rect(button_next_dim)
            prev_button = pygame.Rect(button_prev_dim)

    text_screen = font.render(step, False, black)
    image = pygame.transform.scale(image, image_size)

    screen.fill(white)
    screen.blit(image, image_pos)
    screen.blit(text_screen, text_pos)
    pygame.draw.rect(screen, green, next_button )
    pygame.draw.rect(screen, red, prev_button)
    pygame.display.flip()
