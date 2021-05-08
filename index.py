from simulator import Simulator
from sim_utils import SimUtils
from models import *


if __name__ == '__main__':
    n = 5000
    citizens = SimUtils.generate_citizens(n=n, presymptoms_percent=0.001, symptoms_percent=0.001, vaxxed_percent=0)
    locations = [
        Location(name='Market', n_min=n//200, n_max=n//20, is_indoor=False, mask_compliance=0.1, is_home=False),
        Location(name='Park', n_min=n//500, n_max=n//20, is_indoor=False, mask_compliance=0, is_home=False),
        Location(name='Work', n_min=n//10, n_max=n//4, is_indoor=True, mask_compliance=0.5, is_home=False),
    ]
    for i in range(0, round(n/4)+1):
        locations.append(Location(name='Home{}'.format(i), n_min=0, n_max=6, is_indoor=True, mask_compliance=0,
                                  is_home=True))

    s = Simulator(citizens=citizens, locations=locations, r0=5, population_density=1000)
    result = s.run(total_days=30)

    [print(x.n_infected, x.n_new_infections, x.n_new_recoveries, x.n_dead, x.n_new_deaths) for x in result]



