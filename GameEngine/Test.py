import pygame
import GameEngine.GameEngine.GameMeneger as meneger
import GameEngine.GameEngine.ColorLib as colors

meneger.FPS = 60
screen = meneger.Screen(800, 800, None, colors.YELLOW)
cam = meneger.Camera(screen)

ball = meneger.GameObject(meneger.Renderer(r"C:\Users\olegb\OneDrive\Рабочий стол\Code\Для программ\Successful projects\Python\Snake\Apple0.png", colors.WHITE),
                          meneger.Transform(meneger.Position(100, 60), rotation=0, size=meneger.Size(20, 20)), cam)
#ball.Rotate(45)
ball.phisical_obj = meneger.Phisics(ball, 0.07, meneger.KINEMATIC, meneger.Collider(ball))

b = meneger.GameObject(meneger.Renderer(r"C:\Users\olegb\OneDrive\Рабочий стол\Code\Для программ\Successful projects\Python\Snake\Apple.png", colors.WHITE), meneger.Transform(meneger.Position(400, 300), 0, meneger.Size(64, 64)), cam)
b.phisical_obj = meneger.Phisics(b, 0.05, meneger.STATIC, meneger.Collider(b))

def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            meneger.Quit()

#ball.phisical_obj.AddForce(meneger.Vector(0.5, -3), 6)

while True:
    check_for_exit()
    cam.drawAll()

    col = ball.phisical_obj.collider.OnCollisionEnter()
    if (col):

        ball.phisical_obj.velocity = meneger.Vector(0,0)

    #print(ball.phisical_obj.collider.overLapped(b.phisical_obj.collider))
    #print(ball.phisical_obj.collider.overLapped(b.phisical_obj.collider))
    #ball.phisical_obj.usePhisics()
    #ball.phisical_obj.addForce(meneger.Vector(1, -1), 5, 'Force')
    #if meneger.Coroutuine(100):
     #   print("JUMP")
        #ball.phisical_obj.AddForce(meneger.Vector(1, -2), 8)

    print(meneger.TICK)
    meneger.Tick(meneger.FPS)