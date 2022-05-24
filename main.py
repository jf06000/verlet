# This is a sample Python script.
import pygame
import numpy as np
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class Verlet:
    def __init__(self, x: float, y: float, r: float):
        self.radius = r
        self.pos_current = np.array([x, y], dtype=float)
        self.pos_old = self.pos_current
        self.acceleration = np.array([0.0, 0.0])

    def update_pos(self, dt):
        velocity = self.pos_current - self.pos_old
        self.pos_old = self.pos_current
        self.pos_current = self.pos_current + velocity + self.acceleration * dt * dt
        # print("y = " + self.pos_current[1])
        self.acceleration = np.array([0.0, 0.0])

    def accelerate(self, acc):
        self.acceleration += acc


class Solver:
    gravity = np.array([0.0, 1000.0])

    def __init__(self):
        self.group = []

    def create(self, x, y, r):
        self.group.append(Verlet(x, y, r))

    def update(self, dt):
        self.apply_gravity()
        self.apply_constraint()
        self.apply_collisions()
        self.update_position(dt)

    def update_position(self, dt):
        for obj in self.group:
            obj.update_pos(dt)

    def apply_gravity(self):
        for obj in self.group:
            obj.accelerate(Solver.gravity)

    def apply_constraint(self):
        center = np.array([350.0, 250.0])
        radius = 220.0
        for obj in self.group:
            to_obj = obj.pos_current - center
            dist = np.linalg.norm(to_obj)
            if dist > (radius - obj.radius):
                v = to_obj / dist
                obj.pos_current = center + v * (radius - obj.radius)

    def apply_collisions(self):
        for i in range(len(self.group)):
            obj1 = self.group[i]
            for j in range(len(self.group) - i - 1):
                obj2 = self.group[i + j + 1]
                collision = obj1.pos_current - obj2.pos_current
                dist = np.linalg.norm(collision)
                if  dist < (obj1.radius + obj2.radius):
                    v = collision / dist
                    delta = obj1.radius + obj2.radius - dist
                    obj1.pos_current += 0.5 * delta * v
                    obj2.pos_current += -0.5 * delta * v

class Display:
    def __init__(self, solv, screen):
        self.solv = solv
        self.screen = screen

    def update(self, dt):
        carryOn = True
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                carryOn = False  # Flag that we are done so we can exit the while loop
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if event.button == 1:
                    self.solv.create(x, y, 8.0)
        self.solv.update(dt)
        self.display()
        return carryOn

    def display(self):
        for obj in self.solv.group:
            pygame.draw.circle(self.screen, (255, 255, 255),
                               obj.pos_current, obj.radius, 1)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pygame.init()
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("verlet simulation")
    solv = Solver()
    disp = Display(solv, screen)
    clock = pygame.time.Clock()
    carryOn = True
    while carryOn:

                # First, clear the screen to white.

        # The you can draw different shapes and lines or add text to your background stage.
        #pygame.draw.rect(screen, RED, [55, 200, 100, 70], 0)
        #pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
        #pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2)
        screen.fill((128, 128, 128))
        pygame.draw.circle(screen, BLACK, [350,250], 220)
        carryOn = disp.update(1/60.0)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    pygame.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
