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
from jmetalpy.TimeTablingProblem import TimeTablingProblem
from metrics.Metric import *


class JMP_andre:

    def run_algorithm(self, alg_list: list, lessons: list, classrooms: list, metrics: list) -> list:
        for a in alg_list:
            try:
                alg = getattr(JMP_andre, a)
                break
            except:
                alg = getattr(JMP_andre, "floatnsgaii")

        #problem = TimeTablingProblem(lessons, classrooms, metrics)
        problem = AndreAllocProblem(lessons, classrooms, metrics)

        algorithm = alg(problem)

        start = time.time()
        algorithm.run()
        elapsed_time = time.time() - start
        print("Elapsed time: ", elapsed_time)

        solutions = algorithm.get_result()
        front = get_non_dominated_solutions(solutions)

        for solution in front:
            print("solution: ", solution.objectives, " ,  ", solution.variables)

        #result = self.get_best_result(front, metrics)

        #new_classrooms = [classroom for classroom in result.variables]
        #new_schedule = [(lessons[i], new_classrooms[i]) for i in range(len(lessons))]

        #return new_schedule

    # The weights in each metric are in a range of 0 to 1
    def get_best_result(self, front, metrics):

        # Making lists of each objective's value
        # Getting the max and min of each objective
        # Choosing the percentage said in the weight within the range (as in from min to max) of each objective
        objectives_scores = []
        for i in range(len(metrics)):
            objective      = [result.objectives[i] for result in front]
            objective_lims = (min(objective), max(objective))
            objectives_scores.append((objective_lims[1] - objective_lims[0]) * (1-metrics[i].weight) + objective_lims[0])

        string = "Alg scores: ["
        for score in objectives_scores:
            string += str(score) + ", "
        string = string[:-2] + "]"
        print(string)

        # Choosing which result is closer on average of
        chosen_result = None
        chosen_proximity = float('inf')
        for result in front:
            new_prox = 0
            for i in range(len(objectives_scores)):
                new_prox += self.distance(result.objectives[i], objectives_scores[i])

            if new_prox < chosen_proximity:
                chosen_result = result
                chosen_proximity = new_prox
        print(chosen_result.objectives)
        return chosen_result

    # The weights are in a range of 0 to 1
    def get_best_result_static(self, front, roomless_weight, overbooking_weight, underbooking_weight, badclassroom_weight):

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
            termination_criterion=StoppingByEvaluations(max_evaluations=10000)
        )

    def floatnsgaii(problem):
        return NSGAII(
            problem=problem,
            population_size=100,
            offspring_population_size=100,
            mutation=PolynomialMutation(probability=0.5),  # (probability=1.0 / problem.number_of_variables),
            crossover=SBXCrossover(probability=0.5),
            termination_criterion=StoppingByEvaluations(max_evaluations=1000) # TODO
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


