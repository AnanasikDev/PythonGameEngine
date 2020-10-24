import pygame
import GameManager as manager
import ColorLib as colors
import time

manager.FPS = 60
screen = manager.Screen(800, 800, None, colors.YELLOW)
cam = manager.Camera(screen)

ball = manager.GameObject(manager.Renderer(r"C:\Users\olegb\OneDrive\Рабочий стол\Code\Для программ\Successful projects\Python\Snake\Apple0.png", colors.WHITE),
                          manager.Transform(manager.Position(100, 60), rotation=0, size=manager.Size(20, 20)), cam)
#ball.Rotate(45)
ball.rigitbody = manager.Rigitbody(ball, 0.03, manager.KINEMATIC, manager.Collider(ball))

for i in range(10):
    ball = manager.GameObject(manager.Renderer(
        r"C:\Users\olegb\OneDrive\Рабочий стол\Code\Для программ\Successful projects\Python\Snake\Apple0.png",
        colors.WHITE),
                              manager.Transform(manager.Position(100, 60), rotation=0, size=manager.Size(20, 20)), cam)
    # ball.Rotate(45)
    ball.rigitbody = manager.Rigitbody(ball, 0.03, manager.KINEMATIC, manager.Collider(ball))
    ball.rigitbody.AddForce(manager.Vector(1, -2), 4)

b = manager.GameObject(manager.Renderer(r"C:\Users\olegb\OneDrive\Рабочий стол\Code\Для программ\Successful projects\Python\Snake\Apple.png", colors.WHITE),
                       manager.Transform(manager.Position(100, 700), 0, manager.Size(200, 20)), cam)
b.rigitbody = manager.Rigitbody(b, 0.05, manager.STATIC, manager.Collider(b))

def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            manager.Quit()

while True:
    check_for_exit()
    cam.drawAll()

    col = ball.rigitbody.collider.OnCollisionEnter()
    if (col):

        ball.rigitbody.velocity = manager.Vector(0, 0)

    #print(ball.phisical_obj.collider.overLapped(b.phisical_obj.collider))
    #print(ball.phisical_obj.collider.overLapped(b.phisical_obj.collider))
    #ball.phisical_obj.usePhisics()
    #ball.phisical_obj.addForce(meneger.Vector(1, -1), 5, 'Force')
    #if meneger.Coroutuine(100):
     #   print("JUMP")
        #ball.phisical_obj.AddForce(meneger.Vector(1, -2), 8)

    print(manager.TICK)
    manager.Tick(manager.FPS)