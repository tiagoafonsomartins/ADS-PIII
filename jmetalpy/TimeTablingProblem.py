from jmetal.core.problem import PermutationProblem
from jmetal.core.solution import PermutationSolution
import random


class TimeTablingProblem(PermutationProblem):
    def __init__(self, lessons: list, classrooms: list, metrics: list):
        super(PermutationProblem, self).__init__()

        self.lessons = lessons
        self.classrooms = classrooms
        self.metrics = metrics

        self.number_of_objectives = 1 # len(metrics)
        self.number_of_variables = len(self.lessons)
        self.number_of_constraints = 0

        self.obj_directions = [self.MAXIMIZE]
        self.obj_labels = ['Lower_half']

    def evaluate(self, solution: PermutationSolution):
        created_schedule = []

        for i, classroom in enumerate(solution.variables):
            created_schedule.append((self.lessons[i], self.classrooms[classroom]))

        for i, metric in enumerate(self.metrics):
            for j in created_schedule:
                metric.calculate(j[0], j[1])
            # metric.calculate(created_schedule)
            solution.objectives[i] = metric.get_total_metric_value()

        return solution

    def create_solution(self) -> PermutationSolution:
        new_solution = PermutationSolution(self.number_of_variables, self.number_of_objectives) # No clue about lower and upper

        new_solution.variables = random.sample(range(len(self.classrooms)), len(self.lessons))

        return new_solution

    def get_name(self) -> str:
        return "permutation timetabling";