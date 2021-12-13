from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
import random
from alocate.Allocator import Allocator

class AndreAllocProblem(FloatProblem):

    def __init__(self, lessons: list, classrooms: list, metrics: list):
        super(FloatProblem, self).__init__()

        self.lessons = lessons
        self.classrooms = classrooms
        self.metrics = metrics

        self.number_of_objectives = len(metrics)
        self.number_of_variables = 6
        self.number_of_constraints = 0

        self.obj_directions = [m.objective for m in metrics] # metrics[0].objective
        # self.obj_labels = ['Lower_half']

    def evaluate(self, solution: FloatSolution):
        created_schedule = []
        a = Allocator(self.classrooms, self.schedule, self.gangs)

        a.andre_alocation()

        for i, metric in enumerate(self.metrics):
            #for j in created_schedule:
            #    metric.calculate(j[0], j[1])
            metric.calculate(created_schedule)
            solution.objectives[i] = metric.get_total_metric_value()
            metric.reset_metric()

        return solution

    def create_solution(self) -> FloatSolution:
        new_solution = FloatSolution(self.number_of_variables, self.number_of_objectives)
        new_solution.variables = [random.random() for i in range(6)]

        return new_solution

    def get_name(self) -> str:
        return "float andre_alloc";