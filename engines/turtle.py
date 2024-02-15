import settings
import turtle

def update(grid, update_list):
    #print(f"Rafraîchissement de {len(update_list)} tuiles")

    for y, x in update_list:

        intensity = grid[y][x][0]
        R, G, B = grid[y][x][1]
        R = int(R*intensity)
        G = int(G*intensity)
        B = int(B*intensity)

        pen.goto(coordinates((y, x)))
        #print("value", grid[i][j][0])
        #print("RGB", R, G, B)
        pen.color((R, G, B))
        draw_tile()

    turtle.update()
    return grid

def coordinates(location):
    x = -settings.screen_width/2 + location[1]*step
    y = settings.screen_height/2 - location[0]*step
    return x, y

def draw_tile():
    pen.pendown()
    pen.begin_fill()
    for i in range(4):
        pen.forward(step)
        pen.right(90)

    pen.end_fill()
    pen.penup()

def draw_rayon(length, color):
    pen.color(color)
    pen.goto(0, -length*step)
    pen.pendown()
    pen.circle(length*step)
    pen.penup()
    turtle.update()


step = settings.screen_width/settings.width
year_sec = 365*24*60*60

turtle.setup(settings.screen_width, settings.screen_height)
turtle.tracer(0)
pen = turtle.Turtle()
pen.penup()
turtle.colormode(255)
turtle.bgcolor(0, 0, 0)

