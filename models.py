from typing import Dict
from pprint import pprint


class InfectionState:

    UNINFECTED = 0
    PRESYMPTOMS = 1
    SYMPTOMS = 2
    ISOLATED = 3
    HOSPITALIZED = 4
    DEAD = 5

    P_TRANSITIONS = {
        UNINFECTED: {PRESYMPTOMS: 0.01},
        PRESYMPTOMS: {UNINFECTED: 0.25, SYMPTOMS: 0.7, ISOLATED: 0.05},
        SYMPTOMS: {UNINFECTED: 0.05, PRESYMPTOMS: 0.05, ISOLATED: 0.79, HOSPITALIZED: 0.1, DEAD: 0.01},
        ISOLATED: {HOSPITALIZED: 0.05, DEAD: 0.01},
        HOSPITALIZED: {DEAD: 0.02}
    }


class Citizen:
    def __init__(self, id, infection_state: InfectionState, is_vaxxed=False):
        self.id = id
        self.infection_state = infection_state
        self.days_in_state = 0
        self.is_vaxxed = is_vaxxed


class Location:
    def __init__(self, name, n_min, n_max, is_indoor, is_masked, is_home):
        self.name = name
        self.n_min = n_min
        self.n_max = n_max
        self.is_indoor = is_indoor
        self.is_masked = is_masked
        self.is_home = is_home


class State:
    def __init__(self,
                 citizen_location_map: Dict[int, Location],
                 location_citizen_map: Dict[str, Citizen]):
        self.citizen_location_map = citizen_location_map
        self.location_citizen_map = location_citizen_map
        self.citizens = []
        for x in self.location_citizen_map.values():
            self.citizens.extend(x)
        self.locations = [x for x in self.citizen_location_map.values()]

    def pprint(self):
        location_map = {name: len(citizens) for name, citizens in self.location_citizen_map.items() if not name.startswith('Home')}
        n_home = sum([len(x) for name, x in self.location_citizen_map.items() if name.startswith('Home')])
        location_map['At Home'] = n_home
        d = {
            'n_citizens': len(self.citizens),
            'n_locations': len(self.locations),
            'n_uninfected': len([x for x in self.citizens if x.infection_state == InfectionState.UNINFECTED]),
            'n_presymptoms': len([x for x in self.citizens if x.infection_state == InfectionState.PRESYMPTOMS]),
            'n_symptoms': len([x for x in self.citizens if x.infection_state == InfectionState.SYMPTOMS]),
            'n_isolated': len([x for x in self.citizens if x.infection_state == InfectionState.ISOLATED]),
            'n_hospitalized': len([x for x in self.citizens if x.infection_state == InfectionState.HOSPITALIZED]),
            'n_dead': len([x for x in self.citizens if x.infection_state == InfectionState.DEAD]),
            'location_map': location_map
        }
        pprint(d)


class DayStats:
    def __init__(self, n_citizens, n_infected, n_hospitalized, n_dead, n_new_infections, n_new_deaths, n_vaxxed):
        self.n_citizens = n_citizens
        self.n_infected = n_infected
        self.n_hospitalized = n_hospitalized
        self.n_dead = n_dead
        self.new_infections = n_new_infections
        self.n_new_deaths = n_new_deaths
        self.n_vaxxed = n_vaxxed
