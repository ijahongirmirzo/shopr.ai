import pygame
from grabscreen import grab_screen
import cv2
import time
from getkeys import key_check
import os
import numpy as np

pygame.init()

is_done = False

clock = pygame.time.Clock()

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

starting_value = 0

while True:
    file_name = 'training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists, moving along', starting_value)
        starting_value += 1
    else:
        print('File does not exist, starting fresh!', starting_value)

        break


# -------- Main Program Loop -----------


def main(file_name, starting_value):
    file_name = file_name
    counter = 0
    starting_value = starting_value
    training_data = []

    paused = True
    print('Click P to start and again P to pause it!!!')
    while (True):
        if counter == 25:
            print('Enough, quitting....')
            pygame.quit()
            break

        for event in pygame.event.get():  # User did something.
            if event.type == pygame.QUIT:  # If user clicked close.
                # done = True # Flag that we are done so we exit this loop.
                break
            elif event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
            elif event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

        if not paused:
            gta_screen = grab_screen(region=(0, 40, 800, 640))
            gta_screen = cv2.resize(gta_screen, (160, 120))  # maybe resize to smaller image
            gta_screen = cv2.cvtColor(gta_screen, cv2.COLOR_BGR2GRAY)

            axis_0 = joystick.get_axis(0)  # steering
            axis_3 = joystick.get_axis(5)  # throttle

            output = [axis_0, axis_3]  # [steering, throttle]
            print(output)
            training_data.append([gta_screen, output])
            if len(training_data) % 100 == 0:
                print(len(training_data))

            if len(training_data) == 4000:
                np.save(file_name, np.array(training_data, dtype=object))
                print('Alhamdulillah, done, saved')
                counter = counter + 1
                training_data = []
                starting_value += 1
                file_name = 'feeding_data-{}.npy'.format(starting_value)
            clock.tick(20)

        keys = key_check()
        if 'P' in keys:
            if paused:
                paused = False
                print('unpapused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
    pygame.quit()


if __name__ == '__main__':
    main(file_name, starting_value)
