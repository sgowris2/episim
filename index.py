from simulator import Simulator
from sim_utils import SimUtils
from models import *


if __name__ == '__main__':
    n = 1000
    citizens = SimUtils.generate_citizens(n=n, presymptoms_percent=10, symptoms_percent=10, vaxxed_percent=25)
    locations = [
        Location(name='Market', n_min=n//100, n_max=n//10, is_indoor=False, is_masked=False, is_home=False),
        Location(name='Park', n_min=n//500, n_max=n//20, is_indoor=False, is_masked=False, is_home=False),
        Location(name='Work', n_min=n//10, n_max=n//2, is_indoor=False, is_masked=False, is_home=False),
    ]
    for i in range(0, round(n/4)+1):
        locations.append(Location(name='Home{}'.format(i), n_min=0, n_max=5, is_indoor=True, is_masked=False,
                                  is_home=True))

    s = Simulator(citizens=citizens, locations=locations, r0=5, population_density=4000)
    s.state.pprint()


