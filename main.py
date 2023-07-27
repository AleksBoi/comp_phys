from typing import List
from random import randint as rand
import matplotlib.pyplot as plt


from planete import get_planets, Planet, WIDTH, HEIGHT




def task2(planets: List[Planet]):
    for planet in planets:
        planet.create_orbit()
    plt.show()


def task4(planets: List[Planet]):
    plt.axes(projection='3d')
    for planet in planets:
        planet.create_orbit_z()
    plt.show()


def pygame_func():
    import pygame
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    run = True
    clock = pygame.time.Clock()

    planets: List[Planet] = get_planets()
    frames = 0
    if input("first four?")[0] == 'y':
        planets = planets[:4]
        for planet in planets:
            planet.SCALE = 150/Planet.AU
    else:
        planets = planets[4:]
    while run:
        clock.tick(60)
        pygame.display.update()
        frames += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #planets = planets[3:] # get just mercury

        for planet in planets:
            if frames % 2 == 0:
                WIN.fill((0,0,0))
            togethercoords, locations = planet.create_orbit()
            planet.DRAW(WIN,locations[frames])
            pygame.draw.lines(WIN, planet.color, False, togethercoords, 2)
        pygame.display.update()
    pygame.quit()



def task5():
    planets: List[Planet] = get_planets()
    planets = planets[:1]
    for planet in planets:
        Planet.time_at_certain_angles(planet)




def main():
    planets: List[Planet] = get_planets()
    #task2(planets)
    #task4(planets)
    #pygame_func()
    task5()


if __name__ == '__main__':
    main()
