import pygame
import sys
import numpy as np
from math import *

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('3d projection')

clock = pygame.time.Clock()

scale = 130
circle_pos = [WIDTH/2, HEIGHT/2]
angle = 0

points = [
    np.matrix([-1, -1, 1]),
    np.matrix([1, -1, 1]),
    np.matrix([1, 1, 1]),
    np.matrix([-1, 1, 1]),
    np.matrix([-1, -1, -1]),
    np.matrix([1, -1, -1]),
    np.matrix([1, 1, -1]),
    np.matrix([-1, 1, -1]),
]

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

def connect_points(p1, p2, points):
    pygame.draw.line(window, WHITE, points[p1], points[p2], 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])

    angle += 0.013

    window.fill(BLACK)

    projected_points = []

    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d = np.dot(rotation_y, rotated2d)
        rotated2d = np.dot(rotation_x, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)

        x = int(projected2d[0, 0] * scale) + circle_pos[0]
        y = int(projected2d[1, 0] * scale) + circle_pos[1]

        projected_points.append([x, y])

        pygame.draw.circle(window, YELLOW, (x, y), 15)

    for p in range(4):
        connect_points(p, (p + 1) % 4, projected_points)        # Connect top face
        connect_points(p + 4, ((p + 1) % 4) + 4, projected_points)  # Connect bottom face
        connect_points(p, p + 4, projected_points)              # Connect top and bottom faces

    pygame.display.update()

    clock.tick(60)
