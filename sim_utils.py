from models import *
from typing import List
from utils import *


class SimUtils:

    @staticmethod
    def generate_citizens(n, presymptoms_percent=0.5, symptoms_percent=0.5, vaxxed_percent=0):

        if n < 10:
            raise Exception('Create at least 10 citizens')

        citizens = []
        for i in range(0, n):
            citizens.append(Citizen(id=i, infection_state=InfectionState.UNINFECTED))

        citizens = SimUtils._set_infection(citizens, presymptoms_percent, InfectionState.PRESYMPTOMS)
        citizens = SimUtils._set_infection(citizens, symptoms_percent, InfectionState.SYMPTOMS)
        citizens = SimUtils._set_vaxxed(citizens, vaxxed_percent)

        return citizens

    @staticmethod
    def _set_infection(citizens: List[Citizen], infected_percent, infection_state: InfectionState):
        if infected_percent > 0:
            n_infected = round(len(citizens) * infected_percent / 100)
            for i in range(0, n_infected):
                citizens[get_rand_in_range(0, len(citizens)-1)].infection_state = infection_state
        return citizens

    @staticmethod
    def _set_vaxxed(citizens: List[Citizen], vaxxed_percent):
        if vaxxed_percent > 0:
            n_vaxxed = round(len(citizens) * vaxxed_percent / 100)
            for i in range(0, n_vaxxed):
                citizens[get_rand_in_range(0, len(citizens)-1)].is_vaxxed = True
        return citizens