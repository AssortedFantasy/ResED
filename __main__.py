import sys, pygame
pygame.init()

image_pos = 0, 0
step = 0
step_display = "Current Image %d" % step


black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0, 0
blue = 0, 0, 255, 0

image = pygame.image.load("testimage3.jpg")
size = width, height = image.get_rect().size
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.font.init()
font = pygame.font.SysFont("Modern Sans", 30)
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
                step += 1
                step_display = "Current Image %d" % step
            elif prev_button.collidepoint(mouse_pos):
                print("Prev button pushed")
                if step > 0:
                    step += -1
                    step_display = "Current Image %d" % step
                else:
                    pass
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            width, height = screen.get_width(), screen.get_height()
            gap_width = height // 10
            text_pos = width - 200, height - gap_width

            boxwidth, boxheight = width, height - gap_width
            imagewidth, imageheight = image.get_rect().size
            # Fit to width
            if imagewidth > imageheight:
                heightfactor = boxwidth / imagewidth
                imageheight = int(imageheight * heightfactor)
                imagewidth = boxwidth
                image_pos = 0, (boxheight - imageheight)/2

            # Fit to height
            elif imageheight >= imagewidth:
                widthfactor = boxheight / imageheight
                imagewidth = int(imagewidth * widthfactor)
                imageheight = boxheight
                image_pos = (boxwidth - imagewidth)/2, 0
            image_size = imagewidth, imageheight

            button_next_dim = (width // 2 + 60, height - gap_width // 1.5, 60, gap_width // 2)
            button_prev_dim = (width // 2 - 120,  height - gap_width // 1.5, 60, gap_width // 2)
            next_button = pygame.Rect(button_next_dim)
            prev_button = pygame.Rect(button_prev_dim)

    text_screen = font.render(step_display, False, black)
    image = pygame.transform.scale(image, image_size)

    screen.fill(white)
    screen.blit(image, image_pos)
    screen.blit(text_screen, text_pos)
    pygame.draw.rect(screen, green, next_button )
    pygame.draw.rect(screen, red, prev_button)
    pygame.display.flip()
