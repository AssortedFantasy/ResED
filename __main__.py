import sys
import pygame
import os

pygame.init()
sim_clock = pygame.time.Clock()
FPS = 60
SIMID = 25

image_pos = 0, 0
step = 0
picture_index = 0
step_display = "Current Image %d" % step
images = os.listdir(f"output\\sim{SIMID}")
images = [float(name[:-4]) for name in images if name.endswith(".png")]
images.sort()
images = [str(name) + ".png" for name in images]

playing = False

black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
green = 0, 255, 0, 0
blue = 0, 0, 255, 0

image = pygame.image.load(f"output\\sim{SIMID}\\{images[step]}")
step_display = ""
size = width, height = image.get_rect().size
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.font.init()
font = pygame.font.SysFont("Modern Sans", 30)

button_next_dim = (width / 2 + 30, height / 2, 60, 20)
button_prev_dim = (width / 2 - 60,  height - 100, 60, 20)
button_play_dim = (width / 2 + 90, height / 2, 60, 20)
button_cycle_dim = (width / 2 - 120, height / 2, 60, 20)
next_button = pygame.Rect(button_prev_dim)
prev_button = pygame.Rect(button_next_dim)
play_button = pygame.Rect(button_play_dim)
cycle_button = pygame.Rect(button_cycle_dim)
text_box = pygame.Rect(0, 0, 0, 0)

def next_frame(step, images):
    print(len(images))
    if step < len(images) - 1:
        step += 1
    return image, step_display

def prev_frame(step, images):
    if step > 0:
        step += -1
    return image, step_display

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mouse_pos = event.pos
            if next_button.collidepoint(mouse_pos):
                if step < len(images) - 1:
                    step += 1

            elif prev_button.collidepoint(mouse_pos):
                if step > 0:
                    step += -1

            elif play_button.collidepoint(mouse_pos):
                playing = not playing

            elif cycle_button.collidepoint(mouse_pos):
                step = 0

        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RIGHT:
                if step < len(images) - 1:
                    step += 1
            elif event.key == pygame.K_LEFT:
                if step > 0:
                    step += -1

        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
            width, height = screen.get_width(), screen.get_height()
            gap_width = height // 10
            text_pos = width - 200, height - gap_width
            text_box = pygame.Rect(width - 200, height - gap_width, len(step_display) * 20, 40)
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
            button_play_dim = (width // 2 - 180,  height - gap_width // 1.5, 60, gap_width // 2)
            button_cycle_dim = (width // 2 + 120,  height - gap_width // 1.5, 60, gap_width // 2)
            next_button = pygame.Rect(button_next_dim)
            prev_button = pygame.Rect(button_prev_dim)
            play_button = pygame.Rect(button_play_dim)
            cycle_button = pygame.Rect(button_cycle_dim)

    image = pygame.image.load(f"output\\sim{SIMID}\\{images[step]}")
    text_screen = font.render(step_display, False, black)
    image = pygame.transform.scale(image, image_size)

    if playing:
        if step < len(images) - 1:
            step += 1
        else:
            playing = False

        image = pygame.image.load(f"output\\sim{SIMID}\\{images[step]}")
    step_display = "Current Image %d" % step

    screen.fill(white)
    screen.blit(image, image_pos)
    pygame.draw.rect(screen, white, text_box)
    screen.blit(text_screen, text_pos)
    pygame.draw.rect(screen, green, next_button )
    pygame.draw.rect(screen, red, prev_button)
    pygame.draw.rect(screen, blue, play_button)
    pygame.draw.rect(screen, (255, 255, 0), cycle_button)
    pygame.display.flip()
    sim_clock.tick(FPS)