from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.operator import SBXCrossover, SPXCrossover, PolynomialMutation, BitFlipMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
import random

class SubsetSum(BinaryProblem):
    def __init__(self, C: int, W: list):
        super(SubsetSum, self).__init__()
        self.C = C
        self.W = W

        self.number_of_bits = len(self.W)

        self.number_of_objectives = 2
        self.number_of_variables = 1
        self.number_of_constraints = 0

        self.obj_directions = [self.MAXIMIZE, self.MINIMIZE]
        self.obj_labels = ['Sum', 'No. of Objects']

    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        total_sum = 0.0
        number_of_objects = 0

        for index, bits in enumerate(solution.variables[0]):
            if bits:
                total_sum += self.W[index]
                number_of_objects += 1

        if total_sum > self.C:
            total_sum = self.C - total_sum * 0.1

            if total_sum < 0.0:
                total_sum = 0.0

        solution.objectives[0] = -1.0 * total_sum
        solution.objectives[1] = number_of_objects

        return solution

    def create_solution(self) -> BinarySolution:
        new_solution = BinarySolution(number_of_variables=self.number_of_variables,
                                      number_of_objectives=self.number_of_objectives)
        new_solution.variables[0] = \
            [True if random.randint(0, 1) == 0 else False for _ in range(self.number_of_bits)]

        return new_solution

    def get_name(self) -> str:
        return "sss";

sss = SubsetSum(150, [1,2,3,4,5,7,8, 10, 50, 87])
problem = sss

max_evaluations = 10000

algorithm = NSGAII(
    problem=problem,
    population_size=100,
    offspring_population_size=100,
    mutation=BitFlipMutation(probability=1.0 / problem.number_of_variables),
    crossover=SPXCrossover(probability=1.0),
    termination_criterion=StoppingByEvaluations(max_evaluations)
)

"""algorithm = NSGAII(
    problem=problem,
    population_size=100,
    offspring_population_size=100,
    mutation=PolynomialMutation(probability=1.0 / problem.number_of_variables, distribution_index=20),
    crossover=SBXCrossover(probability=1.0, distribution_index=20),
    termination_criterion=StoppingByEvaluations(max=max_evaluations)
)"""

algorithm.run()
solutions = algorithm.get_result()

for solution in solutions:
    print(solution.objectives, "\n")

front = get_non_dominated_solutions(solutions)
for f in front:
    print("\n", f)



