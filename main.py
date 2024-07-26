import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

camera_pos = [0, 0, -5]
camera_speed = 0.05
camera_angle_x = 0
camera_angle_y = 0
cursor_locked = False


def drawcuboid(position, size):
    vertices = (
        (position[0] - size[0] / 2, position[1] - size[1] / 2, position[2] - size[2] / 2),
        (position[0] + size[0] / 2, position[1] - size[1] / 2, position[2] - size[2] / 2),
        (position[0] + size[0] / 2, position[1] + size[1] / 2, position[2] - size[2] / 2),
        (position[0] - size[0] / 2, position[1] + size[1] / 2, position[2] - size[2] / 2),
        (position[0] - size[0] / 2, position[1] - size[1] / 2, position[2] + size[2] / 2),
        (position[0] + size[0] / 2, position[1] - size[1] / 2, position[2] + size[2] / 2),
        (position[0] + size[0] / 2, position[1] + size[1] / 2, position[2] + size[2] / 2),
        (position[0] - size[0] / 2, position[1] + size[1] / 2, position[2] + size[2] / 2)
    )
    faces = (
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 4, 7, 3),
        (1, 5, 6, 2)
    )

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    global camera_angle_x, camera_angle_y, cursor_locked
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(*camera_pos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION and cursor_locked:
                camera_angle_x += event.rel[0] * 0.1
                camera_angle_y += event.rel[1] * 0.1
                camera_angle_y = max(-90, min(camera_angle_y, 90))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_locked = True
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cursor_locked = False
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            walk_dir = [-math.sin(math.radians(camera_angle_x)), 0, math.cos(math.radians(camera_angle_x))]
            camera_pos[0] += walk_dir[0] * camera_speed
            camera_pos[2] += walk_dir[2] * camera_speed
        if keys[pygame.K_s]:
            walk_dir = [math.sin(math.radians(camera_angle_x)), 0, -math.cos(math.radians(camera_angle_x))]
            camera_pos[0] += walk_dir[0] * camera_speed
            camera_pos[2] += walk_dir[2] * camera_speed
        if keys[pygame.K_a]:
            walk_dir = [math.cos(math.radians(camera_angle_x)), 0, math.sin(math.radians(camera_angle_x))]
            camera_pos[0] += walk_dir[0] * camera_speed
            camera_pos[2] += walk_dir[2] * camera_speed
        if keys[pygame.K_d]:
            walk_dir = [-math.cos(math.radians(camera_angle_x)), 0, -math.sin(math.radians(camera_angle_x))]
            camera_pos[0] += walk_dir[0] * camera_speed
            camera_pos[2] += walk_dir[2] * camera_speed

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glRotatef(camera_angle_y, 1, 0, 0)
        glRotatef(camera_angle_x, 0, 1, 0)
        glTranslatef(*camera_pos)
        drawcuboid((0, 0, 0), (2, 2, 2))
        drawcuboid((2, -0.5, 0), (1, 1, 1))
        drawcuboid((-3.5, 0.5, 0), (3, 3, 3))
        pygame.display.flip()
        pygame.time.wait(10)


main()
