import pygame
import settings

def update(grid, update_list):
    #print(f"Rafraîchissement de {len(update_list)} tuiles")

    for y, x in update_list:

        intensity = grid[y][x][0]
        R, G, B = grid[y][x][1]
        R = int(R*intensity)
        G = int(G*intensity)
        B = int(B*intensity)

        pygame.draw.rect(screen, (R, G, B), (x * step, y * step, step, step))

    if settings.show_image:
        # Dessiner l'image au premier plan
        screen.blit(resized_image, ((settings.screen_width - image_width) // 2, (settings.screen_height - image_height) // 2))

    pygame.display.flip()
    return grid

step = settings.screen_width // settings.width
year_sec = 365 * 24 * 60 * 60

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption("Projet Urnes Jeanne Coriou - Développé par Etienne Coriou")

# Création de la grille
for y in range(settings.height):
    for x in range(settings.width):
        pygame.draw.rect(screen, (0, 0, 0), (x * step, y * step, step, step))

if settings.show_image:
    # Chargement de l'image
    image = pygame.image.load("foreground.png")
    ratio = max(settings.screen_width / image.get_width(), settings.screen_height / image.get_height())
    image_width = int(image.get_width() * ratio)
    image_height = int(image.get_height() * ratio)
    resized_image = pygame.transform.scale(image, (image_width, image_height))
