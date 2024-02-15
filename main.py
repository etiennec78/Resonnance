import settings
import math
import random

try:
    from utime import time, sleep
    import machine
    platform = "rp2"
except ImportError:
    from time import time, sleep
    platform = "pc"

class Resonance:

    # Importer le moteur de rendu
    if settings.engine == "tk":
        import engines.tk as engine
    elif settings.engine == "pygame":
        import engines.pygame as engine
    elif settings.engine == "LED":
        import engines.LED as engine
    elif settings.engine == "terminal":
        import engines.terminal as engine
    elif settings.engine == "benchmark":
        import engines.benchmark as engine
    elif settings.engine == "turtle":
        import engines.turtle as engine
    else:
        exit()

    def wave(self, time_request, cycles, pulse=False, ease_core=False, reverse=False):
        # Malheureusement reverse n'est plus fonctionnel car je suis arrivé à court de temps. Il l'était mais j'ai dû le supprimer à cause d'un léger bug d'affichage
        print("Wave")

        step = (-1)**int(reverse) * self.max_distance/time_request*self.frametime*cycles

        start = time()

        for _ in range(cycles):
            if reverse:
                rayon_max = rayon_min = self.max_distance
            else:
                rayon_max = rayon_min = 0

            last_frame = time()

            # Déclenchement de la vague
            while 0 <= rayon_min <= self.max_distance:

                update_list = []
                # Regarde si un cube est traversé par un des rayons
                for y in range(settings.height):
                    for x in range(settings.width):

                        closest_point, farthest_point, dist_centre = self.distances[y][x]

                        # Apparition progressive (si pas reverse, point central reste allumé)
                        if closest_point <= rayon_max <= farthest_point:

                            # Calculer l'intensité de la LED en fonction de sa distance au centre (Max 0.5, min 0.25) et sa transpersion de rayon
                            eloignement = 1 - dist_centre / self.max_distance

                            rayon_in_tile = rayon_max - closest_point
                            max_rayon_in_tile = farthest_point - closest_point

                            remplissage = rayon_in_tile / max_rayon_in_tile
                            if remplissage < 0:
                                remplissage = 0
                            intensite = eloignement * remplissage
                            if (y, x) != self.selected:
                                intensite *= 0.5

                            self.grid[y][x][0] = intensite
                            update_list.append((y, x))

                        # Disparition progressive, sauf pour case centrale
                        elif pulse and closest_point <= rayon_min <= farthest_point and (y, x) != self.selected:

                            # Calculer l'intensité de la LED en fonction de sa distance au centre (Max 0.5, min 0.25) et sa transpersion de rayon
                            eloignement = 1 - dist_centre / self.max_distance

                            rayon_in_tile = rayon_min - closest_point
                            max_rayon_in_tile = farthest_point - closest_point
                            # Réparer le bug qui n'efface pas totalement les tuiles
                            if not reverse:
                                rayon_in_tile += step

                            remplissage = 1 - rayon_in_tile / max_rayon_in_tile

                            if remplissage < 0:
                                remplissage = 0
                            intensite = eloignement * remplissage
                            if (y, x) != self.selected:
                                intensite *= 0.5

                            self.grid[y][x][0] = intensite
                            update_list.append((y, x))

                if ease_core and self.selected not in update_list:
                    # Diminuer l'intensité du coeur
                    self.grid[self.selected[0]][self.selected[1]][0] = 1 - rayon_min/self.max_distance
                    update_list.append(self.selected)

                # Rafraichit
                self.engine.update(self.grid, update_list)
                if settings.engine == "turtle":
                    self.engine.draw_rayon(rayon_max, (255, 0, 0))
                    self.engine.draw_rayon(rayon_min, (0, 255, 0))
                update_list = []
                rayon_max += step

                # Calcule le rayon de suppression
                if rayon_max > self.diago_tile:
                    rayon_min = rayon_max + (-1)**(1-int(reverse)) * self.diago_tile

                elapsed_time = time() - last_frame
                if elapsed_time < self.frametime:
                    sleep(self.frametime - elapsed_time)
                else:
                    print("Too slow !")
                last_frame = time()


        score = round(time()-start, 1)
        print(f"Fini en {score} secondes sur {time_request}, ratio de {int(score/time_request*100)}%")

    def clear(self, time_request, clear_center=True):
        print("Clearing")
        value = 1
        old_grid = [[list(item) for item in row] for row in self.grid]
        step = self.frametime/time_request

        last_frame = time()
        start = last_frame

        while value > 0:
            update_list = []
            for y in range(settings.height):
                for x in range(settings.width):

                    # Ne pas appliquer l'effet à l'urne sélectionnée
                    if not clear_center and (y, x) == self.selected:
                        continue

                    self.grid[y][x][0] = old_grid[y][x][0] * self.ease_in_quad(value)
                    update_list.append((y, x))

            self.engine.update(self.grid, update_list)
            value -= step
            elapsed_time = time() - last_frame
            if elapsed_time < self.frametime:
                sleep(self.frametime - elapsed_time)
            else:
                print("Too slow !")
            last_frame = time()

        score = round(time()-start, 1)
        print(f"Fini en {score} secondes sur {time_request}, ratio de {int(score/time_request*100)}%")

    def breathing(self, time_request, cycles):
        print("Breathing")
        old_age = self.grid[self.selected[0]][self.selected[1]][2]
        value = 0
        step = self.frametime/time_request
        update_list = [self.selected]

        last_frame = time()
        start = last_frame

        while value < 1:
            last_visit = old_age * (1-value)
            self.grid[self.selected[0]][self.selected[1]] = [(self.ease_sin(value, cycles)*0.95+0.05), self.color_age(last_visit), last_visit]

            self.engine.update(self.grid, update_list)
            value += step
            elapsed_time = time() - last_frame
            if elapsed_time < self.frametime:
                sleep(self.frametime - elapsed_time)
            else:
                print("Too slow !")
            last_frame = time()

        self.engine.update(self.grid, update_list)
        score = round(time()-start, 1)
        print(f"Fini en {score} secondes sur {time_request}, ratio de {int(score/time_request*100)}%")

    def selection(self, time_request, cycles):
        print("Selection")

        start = time()
        for _ in range(cycles):
            for direction in range(2):
                self.pulse_core(time_request/cycles/2, (-1)**direction)

        score = round(time()-start, 1)
        print(f"Fini en {score} secondes sur {time_request}, ratio de {int(score/time_request*100)}%")

    def pulse_core(self, time_request, direction):
        if direction == 1:
            value = 0
        else:
            value = 1
        step = direction*self.frametime/time_request
        update_list = [self.selected]

        last_frame = time()

        while direction == 1 and value < 1 or direction == -1 and value > 0:

            self.grid[self.selected[0]][self.selected[1]][0] = value
            self.engine.update(self.grid, update_list)
            value += step

            elapsed_time = time() - last_frame
            if elapsed_time < self.frametime:
                sleep(self.frametime - elapsed_time)
            else:
                print("Too slow !")
            last_frame = time()

    def vanish(self, time_request):
        print("Vanish")
        value = 1
        old_value = self.grid[self.selected[0]][self.selected[1]][0]
        step = self.frametime/time_request
        update_list = [self.selected]

        last_frame = time()
        start = last_frame
        while value > 0:

            self.grid[self.selected[0]][self.selected[1]][0] = old_value * value
            self.engine.update(self.grid, update_list)
            value -= step
            elapsed_time = time() - last_frame
            if elapsed_time < self.frametime:
                sleep(self.frametime - elapsed_time)
            else:
                print("Too slow !")
            last_frame = time()
        score = round(time()-start, 1)
        print(f"Fini en {score} secondes sur {time_request}, ratio de {int(score/time_request*100)}%")

    def flush(self):
        self.engine.flush()

    def dist(self, coordinates1, coordinates2):
        squared_distance = sum((x - y) ** 2 for x, y in zip(coordinates1, coordinates2))
        distance = math.sqrt(squared_distance)
        return distance

    def ease_sin(self, x, cycles):
        frequency = cycles * 2 * math.pi
        phase_shift = math.pi / 2
        value = math.sin(frequency * x + phase_shift)
        scaled_value = (value + 1) / 2
        return scaled_value

    def ease_in_out_quad(self, x):
        if x < 0.5:
            return 2 * x * x
        else:
            return 1 - ((-2 * x + 2) ** 2) / 2

    def ease_out_quad(self, x):
        return 1 - (1 - x) ** 2

    def ease_out_sin(self, x):
        return math.sin(x * math.pi / 2)

    def ease_in_quad(self, x):
        return x ** 2

    def color_age(self, last_visit):
        age_percent = last_visit/self.year_sec
        B = 255
        if age_percent <= 0.5:
            R = int(255-255*age_percent*2)
            G = B
        else:
            R = 0
            G = int((1-age_percent)*2*255)
        return R, G, B

    def __init__(self):
        # Calculer les mesures
        self.frametime = 1/settings.fps
        self.diago_tile = math.sqrt(2)
        self.year_sec = 365*24*60*60

        # Créer la grille
        self.grid = []
        for y in range(settings.height):
            self.grid.append([])
            for x in range(settings.width):
                last_visit = random.randint(0, self.year_sec)
                self.grid[y].append([0, self.color_age(last_visit), last_visit])


    def run(self, target):
        global switch_state
        self.selected = target

        # Pré-calculer le rayon maximum
        self.max_distance = 0
        points = [(-0.5, -0.5), (settings.height-0.5, -0.5), (-0.5, settings.width-0.5), (settings.height-0.5, settings.width-0.5)]
        for point in points:
            distance = self.dist(self.selected, point)
            if distance > self.max_distance:
                self.max_distance = distance

        # Pré-calculer les distances des carrés par rapport au centre
        self.distances = []
        for y in range(settings.height):
            self.distances.append([])
            for x in range(settings.width):
                # Calcule la distance entre le centre et les points suivants du carré :
                points = [
                    # Centre
                    (y, x),

                    # Sommets
                    (y - 0.5, x - 0.5),
                    (y - 0.5, x + 0.5),
                    (y + 0.5, x - 0.5),
                    (y + 0.5, x + 0.5),

                    # Centres d'arrêtes
                    (y, x - 0.5),
                    (y, x + 0.5),
                    (y - 0.5, x),
                    (y + 0.5, x),
                ]
                points_distances = [self.dist(self.selected, point) for point in points]
                self.distances[y].append([min(points_distances), max(points_distances), self.dist(self.selected, (y, x))])

        # Rend l'urne sélectionnée abandonnée pour un meilleur effet visuel
        if settings.start_method == "auto":
            self.grid[settings.selected[0]][settings.selected[1]][2] = self.year_sec
            self.grid[settings.selected[0]][settings.selected[1]][1] = self.color_age(self.year_sec)

        switch_state = 1
        self.selection(1, 1)
        self.wave(0.5, 1, pulse=True, ease_core=True)
        self.wave(1, 1, pulse=True, ease_core=True)
        self.wave(4, 1)
        self.clear(3, clear_center=False)
        self.breathing(18, 4)
        self.vanish(10)
        switch_state = 0

if __name__ == "__main__":

    resonance = Resonance()

    if platform == "rp2":
        last_button_press = time()
        switch_state = 0
        def button_pushed(pin):
            global last_button_press, switch_state
            print("pushed")
            current_time = time()
            if current_time - last_button_press > 0.5:
                last_button_press = current_time
                if switch_state == 0:
                    resonance.run(settings.selected)

                else:
                    switch_state = 0
                    stop_flag.set()
                    resonance.flush()

        button_pin = machine.Pin(settings.button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        button_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=button_pushed)

    resonance.run(settings.selected)

    while True:
        pass

# -- Bugs --
# Clearing trop lent sur maquette (ne vient pas de moi)

# -- Optimisations --
# Changer la correction temporaire pour l'effacement wave

