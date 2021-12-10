from jmetal.algorithm.multiobjective import NSGAII, SPEA2, GDE3
from jmetal.algorithm.singleobjective.evolution_strategy import EvolutionStrategy
from jmetal.operator import BitFlipMutation, IntegerPolynomialMutation, SPXCrossover, SBXCrossover, NullCrossover
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.util.termination_criterion import StoppingByEvaluations

from classroom.Classroom import Classroom
from file_manager.Manipulate_Documents import Manipulate_Documents
from jmetalpy.Problem import Problem
from lesson.Lesson import Lesson

md = Manipulate_Documents("../input_documents", "../output_documents","../input_classrooms")
lessons, gangs = md.import_schedule_documents()
classrooms = md.import_classrooms()
print(len(lessons))



# c1 = Classroom('Edifício Sedas Nunes (ISCTE-IUL)', 'Auditório 4', 250, 125, ["cenas", "mais cenas"])
# c2 = Classroom('Edifício 2', 'B203', 150, 125, ["cenas", "mais cenas", "ainda mais cenas"])
# c3 = Classroom('Edifício 69', 'Auditório 420', 50, 25, ["cenas"])
# c4 = Classroom('Edifício Sedas Nunes (ISCTE-IUL)', 'Auditório 4', 250, 125, ["cenas", "mais cenas", "outras cenas"])
# c5 = Classroom('Edifício Sedas Nunes (ISCTE-IUL)', 'Sala daquelas tipo fixes', 250, 125, ["cenas", "mais cenas"])
#
# c = [c1, c2, c3, c4, c5]
#
# l1 = Lesson("MEI", "ADS", "69420blz", "t-69", 69, "Sex", "10:00:00", "10:00:00", "4/23/2005",
#             "Good, Not stinky, Very good")
# l2 = Lesson("LEI", "PCD", "69420blzit", "t-420", 420, "Qui", "3:00:00", "10:00:00", "12/23/2005",
#             "Good, Not stinky")
# l3 = Lesson("ETI", "Irrelevant stuff", "42069blz", "t-1337", 420, "Sex", "3:00:00", "10:00:00", "4/06/2005",
#             "Good, Very good")
# l4 = Lesson("MEI", "GSI", "4269blzit", "t-69", 42069, "Sex", "3:00:00", "10:00:00", "9/14/2015",
#             "Not stinky, Very good")
# l5 = Lesson("MEI", "SRSI", "Ya drenas", "t-69", 420, "Qua", "3:00:00", "10:00:00", "5/31/2069", "Not stinky")
#
# l = [l1, l2, l3, l4, l5]

problem = Problem(lessons, classrooms, [])

max_evaluations = 1000

algorithm1 = NSGAII(
    problem=problem,
    population_size=200,
    offspring_population_size=200,
    mutation=IntegerPolynomialMutation(probability=0.9),  # (probability=1.0 / problem.number_of_variables),
    crossover=NullCrossover(),
    termination_criterion=StoppingByEvaluations(max_evaluations)
)

algorithm2 = SPEA2(
    problem=problem,
    population_size=200,
    offspring_population_size=200,
    mutation=IntegerPolynomialMutation(probability=1.0 / problem.number_of_variables),
    crossover=NullCrossover(),
    termination_criterion=StoppingByEvaluations(max_evaluations)
)

algorithm3 = GDE3(
    problem=problem,
    population_size=100,
    cr=0.5,
    f=0.5,
    termination_criterion=StoppingByEvaluations(max_evaluations)
)

algorithm4 = EvolutionStrategy(
    problem=problem,
    mu = 100,
    lambda_= 10,
    elitist = False,
    mutation = IntegerPolynomialMutation(probability=0.9),
    termination_criterion = StoppingByEvaluations(max_evaluations)
)



algorithm = algorithm3

algorithm.run()
solutions = algorithm.get_result()

#for solution in solutions:
#    print(solution.objectives, "\n")

#print(solutions)
front = get_non_dominated_solutions(solutions)
for f in front:
   print("\n", f.objectives)

