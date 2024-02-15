import settings
import ws2812b

def update(grid, update_list):
    #print("Attribution LEDs ", end='')
    for y, x in update_list:
        intensity = grid[y][x][0]
        R, G, B = grid[y][x][1]
        R = int(R*intensity)
        G = int(G*intensity)
        B = int(B*intensity)

        # Gestion des LEDs multiples
        multi_y = y * settings.case_height
        multi_x = x * settings.case_width
        for i in range(settings.case_height):
            for j in range(settings.case_width):

                # Calcul position LED
                index_hauteur = (multi_y+i) * settings.case_width * settings.width
                index_largeur = (multi_x+j) * settings.case_height
                décalage = multi_y*settings.led_gap

                # Gestion de l'inversement des lignes impaires
                if y % 2 == 1:
                    index_largeur = settings.width*settings.case_width - index_largeur - 1

                led_id = index_hauteur + index_largeur + décalage

                strip.set_pixel(led_id, R, G, B)
                #print(f'{led_id}:{R},{G},{B}, ', end='')
    #print()
    strip.show()
    return grid

def flush():
    strip.fill(0,0,0)
    strip.show()

year_sec = 365*24*60*60

strip = ws2812b.ws2812b(settings.led_count, 0, settings.led_pin)
