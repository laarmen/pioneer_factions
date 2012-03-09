import random
from kdtree import KdTreeNode

bool_ = (True, False)
random.seed(19900724)
economies = ["capitalist", "very_capitalist", "planned", "mixed"]
governments = ['colony', 'lib_democratic', 'imperial', 'social_democratic', 'communism',
               'anarchy', 'mil_dictature']

class Galaxy(KdTreeNode):
    def __init__(self):
        coordinates = set()
        nb = 0
        while nb < 1000 :
            coord = (random.randint(0, 99),
                     random.randint(0, 99),
                     random.randint(0, 99))
            if coord not in coordinates:
                nb += 1
                coordinates.add(coord)
        super(Galaxy, self).__init__([
            SystemResources(coord) for coord in coordinates
        ])

galaxy = Galaxy()

class SystemResources(object):
    def __init__(self, coords):
        self.x, self.y, self.z = coords
        self.max_population = random.randint(0, 10)
        self.inhabitable = random.choice(bool_)
        self.minerals = random.randint(0, 3)
        self.terraformable = random.choice(bool_)
        self.very_rare_resource = random.randint(0, 10) == 0

    def dimension(self, depth): # Needed by the KdTree stuff.
        return (self.x, self.y, self.z)[depth % 3]

class System(object):
    def __init__(self, sysresources, economy, government, population):
        self.sysresources = sysresources
        self.faction = None
        self.economy = None
        self.government = None
        self.population = None
        self.shipyards = []
        self.mining_facilities = []
        self.ships = []
        self.technology = 0

    def get_surroundings(self):
        return galaxy.hypercube(16, self.sysresources, 3)


class Faction(object):
    def __init__(self, origin):
        self.systems = [origin]
        self.capital = origin
        self.economies = [origin.economy]
        self.governments = [origin.government]
        self.known_worlds = origin.get_surroundings()
        self.issue_trees = []

    def register_issue(self, issue, tree = None):
        raise NotImplementedError

def Federation(Faction):
    pass

