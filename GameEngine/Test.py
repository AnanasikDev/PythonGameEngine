from GameEngine.GameManager import *
import GameEngine.ColorLib as colors

screen = Screen(1000, 700, color=colors.BLACK, resizeable=True)
cam = Camera(screen)
text = Text("Physical game engine by Ananasik", Vector.zero(), 50, colors.PURPLE)

ball = GameObject(Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple0.png", colors.WHITE),
                          Transform(Vector(200, 180)))
ball.rigidbody = Rigidbody(ball)
ball.rigidbody.collider = Collider(ball)

ball = GameObject(Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple0.png", colors.WHITE),
                          Transform(Vector(300, 180)))
ball.rigidbody = Rigidbody(ball)
ball.rigidbody.collider = Collider(ball)

b = GameObject(Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple1.png", colors.WHITE),
                          Transform(Vector(100, 500), size=Vector(100, 20)))
b.rigidbody = Rigidbody(b, 0.05, mode=STATIC)
b.rigidbody.collider = Collider(b)

b = GameObject(Renderer(r"C:\GitArchive\Archive\Code\Successful projects\Python\Snake\Apple1.png", colors.WHITE),
                          Transform(Vector(500, 200), size=Vector(20, 100)))
b.rigidbody = Rigidbody(b, 0.05, mode=STATIC)
b.rigidbody.collider = Collider(b)

@run
def run():
    if Input.GetKeyDown('a'):
        ball.rigidbody.AddForce(Vector(-1, 0), 1)
    if Input.GetKeyDown('d'):
        ball.rigidbody.AddForce(Vector(1, 0), 1)
    if Input.GetKeyDown('w'):
        ball.rigidbody.AddForce(Vector(0, -1), 1)
    if Input.GetKeyDown('s'):
        ball.rigidbody.AddForce(Vector(0, 1), 1)

    if ball.rigidbody.collider.OnCollisionExit(): print('\t' * 4 + "EXIT -", True)
    if ball.rigidbody.collider.OnCollisionEnter(): print('\t'*4 + "ENTER -", True)

run()