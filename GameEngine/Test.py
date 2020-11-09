import pygame
import GameManager as manager
import ColorLib as colors

manager.FPS = 60
screen = manager.Screen(1000, 800, color=colors.LIME, resizeable=True)
cam = manager.Camera(screen)

ball = manager.GameObject(manager.Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple0.png", colors.WHITE),
                          manager.Transform(manager.Position(200, 180), rotation=0, size=manager.Size(20, 20)), cam)
ball.rigidbody = manager.Rigidbody(ball, 0.05)
ball.rigidbody.collider = manager.Collider(ball)


b = manager.GameObject(manager.Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple0.png", colors.WHITE),
                          manager.Transform(manager.Position(100, 500), rotation=0, size=manager.Size(100, 20)), cam)
b.rigidbody = manager.Rigidbody(b, 0.05, mode=manager.STATIC)
b.rigidbody.collider = manager.Collider(b)
# print(type("hello"))
ball.rigidbody.AddForce(manager.Vector(0, -1), 3)

@manager.run
def run():
    # print(manager.Input.GetKeyDown("e"))
    if ball.rigidbody.collider.OnCollisionEnter():
        ball.rigidbody.Bounce()
        print("B")

run()