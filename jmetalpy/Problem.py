'''
 -Recebe as métricas a serem avaliadas
 -Evaluate recebe uma Solution do algorítmo
 -Evaluate pega na solution gerada pelo algorítmo e gera um score
para a solução apresentada para cada objetivo
 -A Solution é retornada com o score guardado e o algorítmo volta
a iterar para devolver nova solução
 -Tem um método create_solution(self) que cria a primeira Solution para o algorítmo'''
from abc import ABC
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, SPXCrossover, PolynomialMutation, BitFlipMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
import random


class Problem(IntegerProblem, ABC):
    def __init__(self, lessons: list, classrooms: list, metrics: list):
        self.lessons = lessons
        self.classrooms = classrooms
        self.metrics = metrics

        self.number_of_objectives = 1 # len(metrics)
        self.number_of_variables = len(self.lessons) #1
        self.number_of_constraints = 0

        self.obj_directions = [self.MAXIMIZE]
        self.obj_labels = ['Sum']

    def evaluate(self, solution: IntegerSolution):
        created_schedule = []

        '''1 inteiro e juntar classroom com lesson atual'''
        #for i, classroom in enumerate(solution.variables[0]):
        #    created_schedule.append((self.lessons[i], self.classrooms[classroom]))


        #for i in range(len(self.metrics)):
        #    for j in created_schedule:
        #        m = self.metrics[i].calculate(j)

        #    solution.objectives[i] = self.metrics[i].get_total_metric_value()
        #    solution.objectives[i] = self.metrics[i].get_total_metric_value()
        score = 0
        for i in solution.variables:
            if i == 1:
                score += 1
        solution.objectives[0] = -1 * score

        return solution

    def create_solution(self) -> IntegerSolution:
        new_solution = IntegerSolution([0], [len(self.classrooms)], self.number_of_objectives) # No clue about lower and upper

        #new_solution.variables[0] = [random.randint(0, len(self.classrooms)) for _ in self.classrooms]
        #new_solution.variables[0] = [random.randint(0, len(self.classrooms)) for _ in self.classrooms]


        new_solution.variables[0] = 1
        for i in range(len(self.lessons)):
            new_solution.variables.append(random.randint(0, len(self.classrooms)))
        #print(new_solution.variables)
        return new_solution

    def get_name(self) -> str:
        return "timetabling";