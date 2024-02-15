import settings

def update(grid, update_list):
    for y in range(settings.height):
        for x in range(settings.width):
            print(f'[{float(round(grid[y][x][0], 1))}]', end='')
        print()
    print("--------------------------------------")
    return grid
