from typing import List
import math
from random import randint as rand

import matplotlib.pyplot as plt
import pygame

from data import data

WIDTH, HEIGHT = 600,600

class Planet:
    
    AU = 149.6e6 * 1000
    SCALE = 5 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, name, orbital_period, semi_major_axis, mass, eccentricity, inclination,semi_minor_axis,x,y,color):
        self.name = name
        self.orbital_period = orbital_period
        self.semi_major_axis = semi_major_axis
        self.mass = mass
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.semi_minor_axis = semi_minor_axis
        self.color = color
        self.orbit = []
        self.first_four_planets = True

        self.x = x
        self.y = y
        self.distance_to_sun = 0
        self.y_vel = 0
        self.x_vel = 0

    def findr(self, angle):
        return ((self.semi_major_axis*(1-(self.eccentricity**2)))/(1-self.eccentricity * math.cos(math.radians(angle))))

    def centre(self):
        return (Planet.findr(self,0)-Planet.findr(self,180))/2

    def DRAW(self, win, location):
        x = (self.x + Planet.centre(self)*Planet.AU) * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, location, 10.0)

    def ANIMATE(self,win):
        pass

    def get_frames(self):

        if self.first_four_planets:
            number_of_frames = ((360 * self.orbital_period) / (2 * math.pi) / data['earth_orbit_time']) * 60
        else:
            number_of_frames = ((360 * self.orbital_period) / (2 * math.pi) / data['jupiter_orbit_time']) * 60
        indexes_of_together_coords = round(1000/number_of_frames)
        return indexes_of_together_coords
    
    def create_orbit(self):
        xcoords = []
        ycoords = []
        togethercoords = []
        locations = []
        time_elapsed = 0
        #a thousand degrees to represent each of the 360
        for i in range (1000):
            distance = (self.semi_major_axis * (1 - self.eccentricity ** 2)) / (1 - self.eccentricity * math.cos(math.radians((9*i)/25)))
            xcoords.append(distance * math.cos(math.radians((9*i)/25)))
            ycoords.append(distance * math.sin(math.radians((9*i)/25)))
            togethercoords.append(((distance * math.cos(math.radians((9*i)/25)) * Planet.AU) * self.SCALE + WIDTH / 2, (distance * math.sin(math.radians((9*i)/25)) * Planet.AU) * self.SCALE + HEIGHT / 2))
            if i % Planet.get_frames(self) == 0:
                locations.append(((distance * math.cos(math.radians((9*i)/25)) * Planet.AU) * self.SCALE + WIDTH / 2, (distance * math.sin(math.radians((9*i)/25)) * Planet.AU) * self.SCALE + HEIGHT / 2))
            #time_elapsed = (((9*i)/25) * self.orbital_period) / (2 * math.pi)
        #number_of_seconds = time_elapsed/data['earth_orbit_time']
        #frames_per_orbit = round(number_of_seconds * 60)

        #print(f'All the locations: {locations} frames for {self.name}')
        plt.plot(xcoords, ycoords)
        locations = locations * 60 #so there are enough indexes for the planet to loop
        return togethercoords, locations 

    def create_orbit_z(self):
        xcoords = []
        ycoords = []
        zcoords = []
        for i in range (1000):
            distance = (self.semi_major_axis * (1 - self.eccentricity ** 2)) / (1 - self.eccentricity * math.cos(math.radians(i/10)))
            xcoords.append(distance * math.cos(math.radians(i/10)) * math.cos(math.radians(self.inclination)))
            ycoords.append(distance * math.sin(math.radians(i/10)))
            zcoords.append(distance * math.cos(math.radians(i/10)) * math.sin(math.radians(self.inclination)))
        plt.plot(xcoords, ycoords, zcoords)
    
    def time_at_certain_angles(self):
        first_interval = (0, rand(0,1000))
        second_interval = (first_interval[1], rand(first_interval[1],1000))
        third_interval = (second_interval[1], 1000)
        convert_1000_to_360 = (9/25)

        print (first_interval, second_interval, third_interval)


        
        


def find_semi_minor_axis(idx: int) -> float:
    return data['semi_major_axis'][idx]*((1-(data['eccentricity'][idx]**2)))**0.5


def get_planets() -> List[Planet]:
    """Calculates the semi-minor axis of each planet and returns a list of Planet objects."""

    planet_names: List[str] = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
    planet_colors: List[str] = [(128, 128, 128),(245,245,220),(64,224,208),(255,0,0),(255,165,0),(64,224,208),(0,255,0),(0,0,255),(128, 128, 128)]
    #,'Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']

    
    planets: List[Planet] = []
    for idx, name in enumerate(planet_names):
        planet = Planet(
            name,
            data['orbital_periods'][idx],
            data['semi_major_axis'][idx],
            data['masses'][idx],
            data['eccentricity'][idx],
            data['inclination'][idx],
            find_semi_minor_axis(idx),
            data['semi_major_axis'][idx] * Planet.AU, 
            0,
            planet_colors[idx]
        )
        if idx >= 4:
            planet.first_four_planets = False
        planets.append(planet)
    return planets
