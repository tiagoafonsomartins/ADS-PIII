'''
 -Recebe as métricas a serem avaliadas
 -Evaluate recebe uma Solution do algorítmo
 -Evaluate pega na solution gerada pelo algorítmo e gera um score
para a solução apresentada para cada objetivo
 -A Solution é retornada com o score guardado e o algorítmo volta
a iterar para devolver nova solução
 -Tem um método create_solution(self) que cria a primeira Solution para o algorítmo'''

from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, SPXCrossover, PolynomialMutation, BitFlipMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
import random


class Problem(IntegerProblem):
    def __init__(self, lessons: list, classrooms: list, metrics: list):
        self.lessons = lessons
        self.classrooms = classrooms

        self.number_of_bits = len(self.W) # no clue
        self.number_of_objectives = len(metrics)
        self.number_of_variables = 1
        self.number_of_constraints = 0

        self.obj_directions = [self.MAXIMIZE]
        self.obj_labels = ['Sum']

    def evaluate(self, solution: IntegerSolution):
        created_schedule = []

        '''pegar em 2 inteiros e juntar lesson com classroom ou pegar só 1 inteiro e juntar classroom com lesson atual'''
        for i in solution.variables[0]:
            created_schedule.append(self.classrooms[i])

        for i in len(self.metrics):
            solution.objectives[i] = self.metrics[i].calculate(created_schedule)

        return solution

    def create_solution(self) -> IntegerSolution:
        new_solution = IntegerSolution(None, None, self.number_of_objectives) # No clue about lower and upper
        new_solution.variables[0] = \
            [random.randint(0, len(self.classrooms)) for _ in self.classrooms]

        return new_solution