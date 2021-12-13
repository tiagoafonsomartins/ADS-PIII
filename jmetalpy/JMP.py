from jmetal.algorithm.multiobjective import NSGAII
from jmetal.algorithm.multiobjective.nsgaiii import NSGAIII, UniformReferenceDirectionFactory
from jmetal.operator.crossover import PMXCrossover, SBXCrossover
from jmetal.operator.mutation import PermutationSwapMutation, IntegerPolynomialMutation, PolynomialMutation
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations
from typing import List
import numpy as np
import random


from experimenting_scores_alloc.AndreAllocProblem import AndreAllocProblem
from file_manager.Manipulate_Documents import Manipulate_Documents
from metrics.Metric import *


class JMP:

    def run_algorithm(self, alg_name: str, lessons: list, classrooms: list, metrics: list,
                      roomless_weight = 0.5, overbooking_weight = 0.5, underbooking_weight = 0.5, badclassroom_weight = 0.5) -> list:

        alg = getattr(JMP, alg_name)

        problem = AndreAllocProblem(lessons, classrooms, metrics)
        #problem = TimeTablingProblem(lessons, classrooms, metrics)
        #problem = Problem(lessons, classrooms, metrics)

        algorithm = alg(problem)

        start = time.time()
        algorithm.run()
        elapsed_time = time.time() - start
        print("Elapsed time: ", elapsed_time)

        solutions = algorithm.get_result()
        front = get_non_dominated_solutions(solutions)


        #print(alg_name)
        #[print(f.objectives, f.variables[:len(lessons)]) for f in front]
        #answers = [f.variables for f in front][:len(lessons)]
        #print(new_classrooms)

        result = self.get_best_result(front, roomless_weight, overbooking_weight, underbooking_weight, badclassroom_weight)
        new_classrooms = [classroom for classroom in result.variables]
        new_schedule = [(lessons[i], new_classrooms[i]) for i in range(len(lessons))]

        return new_schedule
        #return [f.variables for f in front][:len(lessons)]


    # The weights are in a range of 0 to 1
    def get_best_result(self, front, roomless_weight, overbooking_weight, underbooking_weight, badclassroom_weight):

        # Making lists of each objective's value
        roomlesses    = [result.objective[0] for result in front]
        overbookings  = [result.objective[1] for result in front]
        underbookings = [result.objective[2] for result in front]
        badclassrooms = [result.objective[3] for result in front]

        # Getting the max and min of each objective
        roomless_lims     = (min(roomlesses), max(roomlesses))
        overbooking_lims  = (min(overbookings), max(overbookings))
        underbooking_lims = (min(underbookings), max(underbookings))
        badclassroom_lims = (min(badclassrooms), max(badclassrooms))

        # Choosing the percentage said in the weight within the range of each objective
        roomless_score     = (roomless_lims[1] - roomless_lims[0]) * roomless_weight + roomless_lims[0]
        overbooking_score  = (overbooking_lims[1] - overbooking_lims[0]) * overbooking_weight + overbooking_lims[0]
        underbooking_score = (underbooking_lims[1] - underbooking_lims[0]) * underbooking_weight + underbooking_lims[0]
        badclassroom_score = (badclassroom_lims[1] - badclassroom_lims[0]) * badclassroom_weight + badclassroom_lims[0]

        # Choosing which result is closer on average of
        chosen_result = None
        chosen_proximity = float('inf')
        for result in front:
            new_prox = self.distance(result.objective[0], roomless_score) + \
                              self.distance(result.objective[1], overbooking_score) + \
                              self.distance(result.objective[2], underbooking_score) + \
                              self.distance(result.objective[3], badclassroom_score)
            if new_prox < chosen_proximity:
                chosen_result = result
                chosen_proximity = new_prox

        return chosen_result

    def distance(self, num1: float, num2: float) -> float:
        return abs(num1 - num2)

    def nsgaii(problem):
        return NSGAII(
            problem=problem,
            population_size=100,
            offspring_population_size=100,
            mutation=PermutationSwapMutation(probability=0.5),  # (probability=1.0 / problem.number_of_variables),
            crossover=PMXCrossover(probability=0.5),
            termination_criterion=StoppingByEvaluations(max_evaluations=10) # TODO
        )

    def floatnsgaii(problem):
        return NSGAII(
            problem=problem,
            population_size=100,
            offspring_population_size=100,
            mutation=PolynomialMutation(probability=0.5),  # (probability=1.0 / problem.number_of_variables),
            crossover=SBXCrossover(probability=0.5),
            termination_criterion=StoppingByEvaluations(max_evaluations=10) # TODO
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
    md = Manipulate_Documents("../input_documents", "../output_documents", "../input_classrooms")
    gangs, l = md.import_schedule_documents(False)
    classrooms = md.import_classrooms()
    metrics = [Overbooking(), Underbooking(), BadClassroom()]
    # metrics = [Overbooking()]
    lessons = [le[0] for le in l][:100]

    print(JMP().run_algorithm("nsgaii", lessons, classrooms, metrics))

if __name__ == "__main__":
   testar()
