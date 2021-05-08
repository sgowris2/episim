from models import *
from typing import List
from utils import *


class Simulator:

    def __init__(self, r0, citizens: List[Citizen], locations: List[Location], population_density=1000):
        """

        :param r0: R-naught
        :param n_citizens: Number of people in the simulation to start with
        :param population_density: Number of persons per square kilometre
        """
        self.r0 = r0
        self.population_density = population_density
        self.citizens_dict = {c.id: c for c in citizens}
        self.locations_dict = {loc.name: loc for loc in locations}
        self.state = self._initialize()

    def run(self, total_days=30):

        for d in range(0, total_days):
            pass

    def _initialize(self):
        return self._generate_new_state(citizens=list(self.citizens_dict.values()))

    def _generate_new_state(self, citizens: List[Citizen]):

        location_citizen_map = {}
        citizen_location_map = {}

        active_citizens = [x for x in citizens if x.infection_state in [InfectionState.UNINFECTED,
                                                                        InfectionState.PRESYMPTOMS,
                                                                        InfectionState.SYMPTOMS]]

        for name, location in self.locations_dict.items():
            n_location = get_rand_in_range(location.n_min, location.n_max)
            location_citizens, active_citizens = pop_rand_items_from_list(active_citizens, n_location)
            location_citizen_map[name] = location_citizens
            for citizen in location_citizens:
                citizen_location_map[citizen.id] = location

        if len(active_citizens):
            for name, location in self.locations_dict.items():
                if len(active_citizens) == 0:
                    break
                if location.is_home:
                    available_space = location.n_max - len(location_citizen_map[location.name])
                    if available_space > 0:
                        for i in range(0, available_space):
                            if len(active_citizens) == 0:
                                break
                            c = active_citizens.pop()
                            location_citizen_map[name].append(c)
                            citizen_location_map[c.id] = location

        return State(citizen_location_map=citizen_location_map,
                     location_citizen_map=location_citizen_map)
