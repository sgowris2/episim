from typing import List

from models import *
from utils import *


class Simulator:

    def __init__(self, r0, citizens: List[Citizen], locations: List[Location], infectious_period=14,
                 population_density=1000, isolation_period=14, hospitalization_period=14, outdoor_factor=0.25):
        """

        :param r0: R-naught
        :param n_citizens: Number of people in the simulation to start with
        :param population_density: Number of persons per square kilometre
        """
        self.r0 = r0
        self.infectious_period = infectious_period
        self.population_density = population_density
        self.citizens_dict = {c.id: c for c in citizens}
        self.locations_dict = {loc.name: loc for loc in locations}
        self.isolation_period = isolation_period
        self.hospitalization_period = hospitalization_period
        self.outdoor_factor = outdoor_factor
        self.state = self._initialize()
        self.day_stats = DayStats()
        self.results = []

    def run(self, total_days=30):

        for d in range(0, total_days):
            self.day_stats = DayStats()
            self.state = self._apply_transitions(self.state)
            self.state = self._assign_new_locations(self.state)
            self.state = self._process_infections_at_locations(self.state)
            self._store_day_stats(self.state)
            print(self.day_stats)

        return self.results

    def _initialize(self):
        return self._generate_new_state(state=State(citizens=list(self.citizens_dict.values()), locations=list(self.locations_dict.values()),
                                        citizen_location_map=dict()))

    def _apply_transitions(self, state):

        def _perform_transition(citizens: List[Citizen], transition_matrix):

            new_infections = 0
            new_recoveries = 0
            new_deaths = 0

            for c in citizens:
                new_infection_state = get_transition_for_element(c.infection_state, transition_matrix)
                if c.infection_state == new_infection_state:
                    c.days_in_state += 1
                    c = self._check_isolation_completion(c)
                    c = self._check_hospitalization_completion(c)
                else:
                    if new_infection_state > InfectionState.UNINFECTED and c.infection_state == InfectionState.UNINFECTED:
                        new_infections += 1
                    elif c.infection_state > InfectionState.UNINFECTED and new_infection_state == InfectionState.UNINFECTED:
                        new_recoveries += 1
                    elif new_infection_state == InfectionState.DEAD and c.infection_state < InfectionState.DEAD:
                        new_deaths += 1
                    c.days_in_state = 0
                c.infection_state = new_infection_state

            self._save_transition_stats(new_infections, new_recoveries, new_deaths)
            return citizens

        new_citizens = []

        uninfected = [x for x in state.citizens if x.infection_state == InfectionState.UNINFECTED]
        presymptoms = [x for x in state.citizens if x.infection_state == InfectionState.PRESYMPTOMS]
        symptoms = [x for x in state.citizens if x.infection_state == InfectionState.SYMPTOMS]
        isolated = [x for x in state.citizens if x.infection_state == InfectionState.ISOLATED]
        hospitalized = [x for x in state.citizens if x.infection_state == InfectionState.HOSPITALIZED]
        dead = [x for x in state.citizens if x.infection_state == InfectionState.DEAD]

        new_citizens.extend(_perform_transition(uninfected, InfectionState.P_TRANSITIONS[InfectionState.UNINFECTED]))
        new_citizens.extend(_perform_transition(presymptoms, InfectionState.P_TRANSITIONS[InfectionState.PRESYMPTOMS]))
        new_citizens.extend(_perform_transition(symptoms, InfectionState.P_TRANSITIONS[InfectionState.SYMPTOMS]))
        new_citizens.extend(_perform_transition(isolated, InfectionState.P_TRANSITIONS[InfectionState.ISOLATED]))
        new_citizens.extend(
            _perform_transition(hospitalized, InfectionState.P_TRANSITIONS[InfectionState.HOSPITALIZED]))
        new_citizens.extend(dead)

        return self._get_state_with_updated_citizens(self.state, new_citizens)

    def _save_transition_stats(self, new_infections, new_recoveries, new_deaths):
        self.day_stats.n_new_infections += new_infections
        self.day_stats.n_new_recoveries += new_recoveries
        self.day_stats.n_new_deaths += new_deaths

    def _assign_new_locations(self, state):
        return self._generate_new_state(state)

    def _process_infections_at_locations(self, state):

        new_citizens_dict = {c.id: c for c in state.citizens}

        for location in state.locations:

            citizens_dict = {c.id: c for c in state.citizens if c.id in state.location_citizen_map[location.name]}
            infected_citizens = [x for x in citizens_dict.values() if
                                 InfectionState.UNINFECTED < x.infection_state < InfectionState.DEAD]
            uninfected_citizens = [x for x in citizens_dict.values() if x.infection_state == InfectionState.UNINFECTED]

            if len(infected_citizens) == 0:
                continue
            else:
                beta = self._get_reproduction_factor_for_location(location)
                n_new_infections = min(len(uninfected_citizens), round(len(infected_citizens) * (1 + beta)) - len(infected_citizens))
                if n_new_infections > 0:
                    self.day_stats.n_new_infections += n_new_infections
                    new_infected_citizens = get_rand_items_from_list(uninfected_citizens, n_new_infections)
                    for i in new_infected_citizens:
                        i.infection_state = InfectionState.PRESYMPTOMS
                    if len(new_infected_citizens) > 0:
                        for nic in new_infected_citizens:
                            citizens_dict[nic.id] = nic
                    for i, c in citizens_dict.items():
                        new_citizens_dict[i] = c

        return self._get_state_with_updated_citizens(self.state, list(new_citizens_dict.values()))

    def _get_reproduction_factor_for_location(self, location):

        beta = (self.r0 / self.infectious_period) * (self.population_density / 1000) * \
               (1 if location.is_indoor else self.outdoor_factor) * \
               (1 - 0.95 * location.mask_compliance)
        return beta

    def _store_day_stats(self, state: State):

        self.day_stats.n_infected = len([x for x in state.citizens if
                                         x.infection_state > InfectionState.UNINFECTED and x.infection_state < InfectionState.DEAD])
        self.day_stats.n_hospitalized = len(
            [x for x in state.citizens if x.infection_state == InfectionState.HOSPITALIZED])
        self.day_stats.n_dead = len([x for x in state.citizens if x.infection_state == InfectionState.DEAD])
        self.day_stats.n_vaxxed = len([x for x in state.citizens if x.is_vaxxed])

        self.results.append(self.day_stats)

    @staticmethod
    def _get_state_with_updated_citizens(state, citizens):
        return State(citizens=citizens, locations=state.locations, citizen_location_map=state.citizen_location_map)

    def _check_isolation_completion(self, c):
        if c.infection_state == InfectionState.ISOLATED and c.days_in_state > self.isolation_period:
            c.infection_state = InfectionState.UNINFECTED
            c.days_in_state = 0
        return c

    def _check_hospitalization_completion(self, c):
        if c.infection_state == InfectionState.HOSPITALIZED and c.days_in_state > self.hospitalization_period:
            c.infection_state = InfectionState.UNINFECTED
            c.days_in_state = 0
        return c

    def _generate_new_state(self, state):

        active_citizens = [x for x in state.citizens if x.infection_state in [InfectionState.UNINFECTED,
                                                                        InfectionState.PRESYMPTOMS,
                                                                        InfectionState.SYMPTOMS]]

        inactive_citizens = [x for x in state.citizens if x.infection_state not in [InfectionState.UNINFECTED,
                                                                              InfectionState.PRESYMPTOMS,
                                                                              InfectionState.SYMPTOMS]]

        for name, location in self.locations_dict.items():
            n_location = get_rand_in_range(location.n_min, location.n_max)
            location_citizens, active_citizens = pop_rand_items_from_list(active_citizens, n_location)
            for citizen in location_citizens:
                state.citizen_location_map[citizen.id] = location.name

        citizen_location_map = self._assign_to_homes(active_citizens, state.citizen_location_map, state.location_citizen_map)

        citizen_location_map = self._assign_to_isolation(inactive_citizens, citizen_location_map)

        return State(citizens=state.citizens,
                     locations=state.locations,
                     citizen_location_map=citizen_location_map)

    def _assign_to_homes(self, active_citizens, citizen_location_map, location_citizen_map):
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
                            citizen_location_map[c.id] = location.name
        return citizen_location_map

    def _assign_to_isolation(self, inactive_citizens, citizen_location_map):

        for i in inactive_citizens:
            citizen_location_map[i.id] = None
        return citizen_location_map
