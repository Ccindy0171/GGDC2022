class History:
    def __init__(self):
        self.planet_facts = {'Mercury': ['hot', 'small', 'no_moons', 'no_rings', 'solid'],
                             'Venus': ['hot', 'small', 'no_moons', 'no_rings', 'solid'],
                             'Earth': ['warm', 'small', 'has_moons', 'no_rings', 'solid'],
                             'Mars': ['warm', 'small', 'has_moons', 'no_rings', 'solid'],
                             'Jupiter': ['cold', 'big', 'has_moons', 'has_rings', 'gas'],
                             'Saturn': ['cold', 'big', 'has_moons', 'has_rings', 'gas'],
                             'Uranus': ['cold', 'big', 'has_moons', 'has_rings', 'gas'],
                             'Neptune': ['cold', 'big', 'has_moons', 'has_rings', 'gas'],
                             'Pluto': ['cold', 'small', 'has_moons', 'no_rings', 'solid']}

        self.planets_completed = []
        self.souvenirs = []

        # change to False the first time the fox experiences something
        self.never_hot = [True, 'hot']
        self.never_cold = [True, 'cold']
        self.never_warm = [True, 'warm']
        self.never_big = [True, 'big']
        self.never_small = [True, 'small']
        self.never_has_moons = [True, 'has_moons']
        self.never_no_moons = [True, 'no_moons']
        self.never_has_rings = [True, 'has_rings']
        self.never_no_rings = [True, 'no_rings']
        self.never_solid = [True, 'solid']
        self.never_gas = [True, 'gas']
        self.never_done = [self.never_hot, self.never_cold, self.never_warm, self.never_big,
                           self.never_small, self.never_has_moons, self.never_no_moons,
                           self.never_has_rings, self.never_no_rings, self.never_solid,
                           self.never_gas]

    def update(self, planet=None, souvenir=None):
        if planet is not None:
            self.planets_completed.append(planet)
            planet_list = self.planet_facts.get(planet)

            for thing in self.never_done:
                if thing[0] and (thing[1] in planet_list):
                    thing[0] = False

        if souvenir is not None:
            self.souvenirs.append(souvenir)


# TESTING PURPOSES
history = History()
history.update('Mars')
history.update('Earth')
history.update(None, 'gloves')
print(history.never_done, history.planets_completed)
print(history.souvenirs)
