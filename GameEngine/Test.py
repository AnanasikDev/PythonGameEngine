import pygame
import GameEngine.GameEngine.GameMeneger as meneger
import time
import math

clock = pygame.time.Clock()
screen = meneger.Screen(800, 800)
cam = meneger.Camera(screen)
ball = meneger.GameObject(meneger.Transform(meneger.Position(100, 0), 0, (64, 64)), r"C:\Users\olegb\OneDrive\Рабочий стол\Code\Для программ\Python\ball.png", cam)
ball.phisical_obj = meneger.Phisics(ball, 0.05, meneger.Collider(ball))

b = meneger.GameObject(meneger.Transform(meneger.Position(400, 300), 0, (64, 64)), r"C:\Users\olegb\OneDrive\Рабочий стол\Code\Для программ\Python\ball.png", cam)
b.phisical_obj = meneger.Phisics(b, 0.05, meneger.Collider(b))

print(ball.phisical_obj.collider.points)

@meneger.Time
def f():
    return 1-2

def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            meneger.Quit()

while True:
    check_for_exit()
    cam.drawAll()
    ball.phisical_obj.addForce(meneger.Vector(1, 0), 6)
    ball.phisical_obj.usePhisics()
    print(ball.phisical_obj.collider.overLapped(b.phisical_obj.collider))
    #ball.phisical_obj.usePhisics()
    #ball.phisical_obj.addForce(meneger.Vector(1, -1), 5, 'Force')
    meneger.SetFPS(60)
