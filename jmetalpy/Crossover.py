import copy
import random
from typing import List

from jmetal.core.operator import Crossover
from jmetal.core.solution import IntegerSolution


class DrenasCrossover(Crossover[IntegerSolution, IntegerSolution]):
    """ This operator receives two parameters: the current individual and an array of three parent individuals. The
    best and rand variants depends on the third parent, according whether it represents the current of the "best"
    individual or a random_search one. The implementation of both variants are the same, due to that the parent selection is
    external to the crossover operator.
    """

    def __init__(self):
        super(DrenasCrossover, self).__init__(probability=1.0)

        #self.current_individual: IntegerSolution = None

    def execute(self, parents: List[IntegerSolution]) -> List[IntegerSolution]:
        """ Execute the differential evolution crossover ('best/1/bin' variant in jMetal).
        """
        if len(parents) != 2:
            raise Exception('The number of parents is not {}: {}'.format(self.get_number_of_parents(), len(parents)))

        child = copy.deepcopy(parents[0])
        rand = random.randint(0, len(parents[0].variables))
        child.variables = parents[0].variables[:rand] + parents[1].variables[rand:]

        return [child]


    def get_number_of_parents(self) -> int:
        return 2


    def get_number_of_children(self) -> int:
        return 1


    def get_name(self) -> str:
        return 'DrenasCrossover'
