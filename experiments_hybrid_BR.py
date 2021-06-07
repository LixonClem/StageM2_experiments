import os
from jmetal.algorithm.multiobjective.moead import MOEAD
from jmetal.algorithm.multiobjective.moead import HybridMOEAD
from jmetal.util.aggregative_function import WeightedSum
from jmetal.operator import PolynomialMutation, DifferentialEvolutionCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.operator.crossover import PMXCrossover
from jmetal.operator.mutation import PermutationSwapMutation
from jmetal.operator.selection import RandomSolutionSelection
from jmetal.operator.extraction import MOPatternExtraction
from jmetal.operator.injection import MOPatternInjection
from jmetal.problem.multiobjective.movrptw import MOVRPTW
from jmetal.lab.experiment import Experiment, Job, generate_summary_from_experiment

from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions

#problem = MOVRPTW("resources\VRPTW_instances\Solomon\solomon_25\C101.txt")
numbers = ["101","102","103","104","105","201","202","203","204","205"]
types = ["C", "R", "RC"] 
sizes = ["25","50","100"]

test_numbers = ["101"]
test_types = ["R"]
test_sizes = ["25","50","100"]



def configure_experiment(numbers: list, types: list, sizes: list, n_run: int):
    jobs = []

    for num in numbers:
        for ty in types:
            for size in sizes:
                for run in range(n_run):
                    instance = os.path.join('resources','VRPTW_instances','Solomon','solomon_'+size,ty+num)+".txt"
                    problem = MOVRPTW(instance)
                    problem_tag = os.path.join('solomon_'+size,ty+num,"Run"+str(run+1),"Final")
                    N = problem.number_of_variables
                    # parameters for both versions
                    if N == 25:
                        max_evaluations = 10000
                    elif N == 50:
                        max_evaluations = 15000
                    elif N == 100:
                        max_evaluations = 20000
                    population_size = 4*N
                    neighbourhood_selection_probability = 1.0 # always = 1.0
                    neighbor_size = 10
                    crossover_probability = 1.0

                    # parameters specific to the normal version
                    mutation_probability = 1.0

                    # parameters specific to the hybrid version
                    max_pattern_size = 5
                    max_dico_size = 2000
                    number_of_patterns_injected = 5
                    number_of_patterns_considered = 4*N
                    extraction_frequency = 0.1
                    injection_frequency = 1.0

                    jobs.append(
                        Job(
                            algorithm = HybridMOEAD(
                                problem = problem,
                                population_size = population_size,
                                extraction_frequency = extraction_frequency,
                                injection_frequency = injection_frequency,
                                max_pattern_size = max_pattern_size,
                                max_dico_size = max_dico_size,
                                number_of_patterns_injected = number_of_patterns_injected,
                                number_of_patterns_considered = number_of_patterns_considered,
                                mutation = PermutationSwapMutation(probability=1.0),
                                crossover = PMXCrossover(probability= crossover_probability),
                                extraction = MOPatternExtraction(),
                                injection = MOPatternInjection(),
                                aggregative_function = WeightedSum(),
                                neighbourhood_selection_probability = neighbourhood_selection_probability,
                                max_number_of_replaced_solutions = 2,
                                neighbor_size = neighbor_size,
                                weight_files_path = 'resources/MOEAD_weights',
                                output_path = os.path.join('data','Hybrid_MOEAD_BR_highInject',"solomon_"+size,ty+num,"Run"+str(run+1),"Snapshots"),
                                termination_criterion = StoppingByEvaluations(max_evaluations)),
                            algorithm_tag='Hybrid_MOEAD_BR_highInject',
                            problem_tag=problem_tag,
                            run=run,
                        )
                    )
    return jobs

# 
n_run = 20
if __name__ == '__main__':
    # Configure the experiments
    jobs = configure_experiment(test_numbers, test_types, test_sizes, n_run)
    print("Number of jobs: ", len(jobs))

    # Run the study
    output_directory = 'data'
    experiment = Experiment(output_dir=output_directory, jobs=jobs)
    experiment.run()