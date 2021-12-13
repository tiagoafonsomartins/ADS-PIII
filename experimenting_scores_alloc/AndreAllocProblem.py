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

        print("len(metrics): ", len(metrics))
        self.number_of_objectives = len(metrics)
        self.number_of_variables = 6
        self.number_of_constraints = 0

        self.obj_directions = [m.objective for m in metrics] # metrics[0].objective
        # self.obj_labels = ['Lower_half']

    def evaluate(self, solution: FloatSolution):
        created_schedule = []
        a = Allocator(self.classrooms, [(lesson, None) for lesson in self.lessons], [])

        lessons30 = a.andre_alocation(solution.variables[0], solution.variables[1], solution.variables[2], solution.variables[3], solution.variables[4], solution.variables[5])
        created_schedule = []
        for sublist in lessons30.values():
            for item in sublist:
                created_schedule.append(item)

        for i, metric in enumerate(self.metrics):
            #for j in created_schedule:
            #    metric.calculate(j[0], j[1])
            metric.calculate(created_schedule)
            solution.objectives[i] = metric.get_percentage()
            metric.reset_metric()

        return solution

    def create_solution(self) -> FloatSolution:
        new_solution = FloatSolution([0], [100], self.number_of_objectives, self.number_of_constraints)
        new_solution.variables = [99, 20, 4, 10, 50, 50]

        return new_solution

    def get_name(self) -> str:
        return "float andre_alloc";