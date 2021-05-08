from typing import Dict, List
from pprint import pprint


class InfectionState:

    UNINFECTED = 0
    PRESYMPTOMS = 1
    SYMPTOMS = 2
    ISOLATED = 3
    HOSPITALIZED = 4
    DEAD = 5

    P_TRANSITIONS = {
        UNINFECTED: {PRESYMPTOMS: 0.0001},
        PRESYMPTOMS: {UNINFECTED: 0.05, SYMPTOMS: 0.5, ISOLATED: 0.01},
        SYMPTOMS: {UNINFECTED: 0.1, PRESYMPTOMS: 0.05, ISOLATED: 0.5, HOSPITALIZED: 0.05, DEAD: 0.001},
        ISOLATED: {HOSPITALIZED: 0.05, DEAD: 0.001},
        HOSPITALIZED: {DEAD: 0.1}
    }


class Citizen:
    def __init__(self, id, infection_state: InfectionState, is_vaxxed=False):
        self.id = id
        self.infection_state = infection_state
        self.days_in_state = 0
        self.is_vaxxed = is_vaxxed


class Location:
    def __init__(self, name, n_min, n_max, is_indoor, mask_compliance, is_home):
        self.name = name
        self.n_min = n_min
        self.n_max = n_max
        self.is_indoor = is_indoor
        self.mask_compliance = mask_compliance
        self.is_home = is_home


class State:
    def __init__(self,
                 citizens: List[Citizen],
                 locations: List[Location],
                 citizen_location_map: Dict[int, str]):
        self.citizen_location_map = citizen_location_map
        self.citizens = citizens
        self.citizens_dict = {c.id: c for c in self.citizens}
        self.locations = locations
        self.locations_dict = {l.name: l for l in self.locations}
        self.location_citizen_map = {x.name: [] for x in self.locations}
        if len(list(citizen_location_map.keys())):
            for i, name in self.citizen_location_map.items():
                if name:
                    self.location_citizen_map[name].append(i)

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
    def __init__(self, n_infected=0, n_hospitalized=0, n_dead=0, n_vaxxed=0, n_new_infections=0, n_new_recoveries=0,
                 n_new_deaths=0, n_new_vaxxed=0):
        self.n_infected = n_infected
        self.n_hospitalized = n_hospitalized
        self.n_dead = n_dead
        self.n_vaxxed = n_vaxxed
        self.n_new_infections = n_new_infections
        self.n_new_recoveries = n_new_recoveries
        self.n_new_deaths = n_new_deaths
        self.n_new_vaxxed = n_new_vaxxed

    def __str__(self):
        return str(self.__dict__)
