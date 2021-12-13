import time
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII, UniformReferenceDirectionFactory
from jmetal.operator.crossover import PMXCrossover
from jmetal.operator.mutation import PermutationSwapMutation, IntegerPolynomialMutation
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations
from typing import List

from classroom.Classroom import Classroom
from file_manager.Manipulate_Documents import Manipulate_Documents
from jmetalpy.Crossover import DrenasCrossover
from jmetalpy.Problem import Problem
from jmetalpy.TimeTablingProblem import TimeTablingProblem
from lesson.Lesson import Lesson
from metrics.Metric import *


class JMP:
    def run_algorithm(self, alg_name: str, lessons: list, classrooms: list, metrics: list) -> list:
        alg = getattr(JMP, alg_name)
        problem = TimeTablingProblem(lessons, classrooms, metrics)
        #problem = Problem(lessons, classrooms, metrics)

        algorithm = alg(problem)

        start = time.time()
        algorithm.run()
        elapsed_time = time.time() - start
        print("Elapsed time: ", elapsed_time)

        solutions = algorithm.get_result()
        front = get_non_dominated_solutions(solutions)



        print(alg_name)
        [print(f.objectives, f.variables[:len(lessons)]) for f in front]
        return [f.variables for f in front][:len(lessons)]

    def nsgaii(problem):
        return NSGAII(
            problem=problem,
            population_size=100,
            offspring_population_size=100,
            mutation=PermutationSwapMutation(probability=0.5),  # (probability=1.0 / problem.number_of_variables),
            crossover=PMXCrossover(probability=0.5),
            termination_criterion=StoppingByEvaluations(max_evaluations=1000)
        )

    def nsgaiii(problem):
        return NSGAIII(
            problem=problem,
            population_size=100,
            mutation=PermutationSwapMutation(probability=0.5),  # (probability=1.0 / problem.number_of_variables),
            crossover=PMXCrossover(probability=0.5),
            reference_directions=UniformReferenceDirectionFactory(problem.number_of_objectives, n_points=99),
            termination_criterion=StoppingByEvaluations(max_evaluations=1000)
        )




#    def insgaii(problem):
#        return NSGAII(
#            problem=problem,
#            population_size=500,
#            offspring_population_size=500,
#            mutation=IntegerPolynomialMutation(probability=0.4),  # (probability=1.0 / problem.number_of_variables),
#            crossover=DrenasCrossover(),
#            termination_criterion=StoppingByEvaluations(max_evaluations=1000)
#        )

def testar():
    md = Manipulate_Documents("../input_documents", "../output_documents","../input_classrooms")
    classrooms = md.import_classrooms()
    gangs, l = md.import_schedule_documents("Exemplo_de_horario_segundo_semestre.csv", False)
    metrics = [Overbooking(), Underbooking(), BadClassroom()]
    #metrics = [Overbooking()]
    lessons = [le[0] for le in l][:100]

    JMP().run_algorithm("nsgaiii", lessons, classrooms, metrics)