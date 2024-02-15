import settings
from tkinter import Tk, Canvas
import asyncio

def update(grid, update_list):
    #print(f"Rafraîchissement de {len(update_list)} tuiles : {update_list}")

    for y, x in update_list:

        intensity = grid[y][x][0]
        R, G, B = grid[y][x][1]
        R = int(R*intensity)
        G = int(G*intensity)
        B = int(B*intensity)

        canvas.itemconfigure(display[y][x], fill=f'#{R:02x}{G:02x}{B:02x}')

        root.update()

step = settings.screen_width/settings.width
year_sec = 365*24*60*60
click = None

# Créer la fenêtre
root = Tk()
root.title("Projet Urnes Jeanne Coriou - Développe par Etienne Coriou")
canvas = Canvas(root, width=settings.screen_width, height=settings.screen_height, borderwidth=0, highlightthickness=0)

# Créer la grille dans le canvas
display = [[canvas.create_rectangle(x * step, y * step, (x + 1) * step, (y + 1) * step, fill="black") for x in range(settings.width)] for y in range(settings.height)]


if settings.show_image:
    # Charger l'image avec transparence
    from PIL import ImageTk, Image
    image = Image.open("foreground.png")
    ratio = max(settings.screen_width / image.width, settings.screen_height / image.height)
    image_width = int(image.width * ratio)
    image_height = int(image.height * ratio)
    resized_image = image.resize((image_width, image_height))
    photo = ImageTk.PhotoImage(resized_image)
    image_item = canvas.create_image((settings.screen_width-image_width)//2, (settings.screen_height-image_height)//2, anchor="nw", image=photo)

canvas.pack()
