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
test_types = ["C"]
test_sizes = ["25"]



def configure_experiment(numbers: list, types: list, sizes: list, n_run: int):
    jobs = []


    for num in numbers:
        for ty in types:
            for size in sizes:
                for run in range(n_run):
                    print(run, num, ty, size)
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


                    jobs.append(
                        Job(
                            algorithm = MOEAD(
                            problem=problem,
                            population_size= population_size,
                            crossover=PMXCrossover(probability=crossover_probability),
                            mutation=PermutationSwapMutation(probability=mutation_probability),
                            aggregative_function=WeightedSum(),
                            neighbor_size= neighbor_size,
                            neighbourhood_selection_probability= neighbourhood_selection_probability,
                            max_number_of_replaced_solutions=2,
                            weight_files_path='resources/MOEAD_weights',
                            output_path = os.path.join('data','Classic_MOEAD',"solomon_"+size,ty+num,"Run"+str(run+1),"Snapshots"),
                            termination_criterion=StoppingByEvaluations(max_evaluations)),
                        algorithm_tag='Classic_MOEAD',
                        problem_tag=problem_tag,
                        run=run,
                        )
                    )
    return jobs

# 
n_run = 20
if __name__ == '__main__':
    # Configure the experiments
    jobs = configure_experiment(numbers, test_types, sizes, n_run)
    print("Number of jobs: ", len(jobs))

    # Run the study
    output_directory = 'data'
    experiment = Experiment(output_dir=output_directory, jobs=jobs)
    experiment.run()