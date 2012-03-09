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

class Issue(object):
    pass

class Surpopulation(Issue):
    def __init__(self, system):
        self.system = system
        self.remaining = system.population - system.sysresources.max_population
    def get_resolution_conditions(self):
        # TODO
        return []

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

    def introspect(self):
        if self.population >= self.max_population and not self.signaled['surpopulation']:
            self.signaled['surpopulation'] = Surpopulation(self)
            self.faction.register_issue(self.signaled['surpopulation'])


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

# The way I want to go for the issue management is to have several trees of issues,
# each node containing an issue and its dependencies as children nodes. As long as
# the dependencies are not resolved, we don't treat the issue.
# An issue can be here a general problem (surpopulation) or a specific need such as 1 ton
# of minerals, or some specific needed in a specific system.
# The issue registration is always delegated to the Faction implementations because some
# regimes can ignore some benign requests, etc...
def Federation(Faction):
    def register_issue(self, issue, tree = None):
        if isinstance(issue, Surpopulation):
            print 'A system is too crowded !'
        if tree = None: # tree can easily be [], so we can't use the 'or' trick.
            tree = []
            self.issue_trees.append(tree)
        subtree = []
        tree.append((issue, subtree))
        for c in issue.get_resolution_conditions():
            self.assess_condition(c, subtree)

def main():
    # Select a system suitable for the origin.
    sol_like = (lambda n, depth:
                n.element.max_population == 5 and n.element.inhabitable and n.element.minerals >= 2 and n.element.terraformable and not n.element.terraformable)
    recurs_pred = lambda n, depth: [] if sol_like(n, depth) else [x for x in (n.left_child, n.right_child) if x]

    sol = System(galaxy.subset(sol_like, recurs_pred)[0], "capitalist", "lib_democratic")   # Let's assume there is at least one result.

    sol.population = 10     # Sol is in surpopulation.
    earth_federation = Federation(sol)
    factions = [earth_federation]

