from simulation.experiments.executable_experiments.agv_random_task_scheduling import run
from simulation.experiments_utils.test_graphs_builders import *


run(tasksNumber=1000, agvsNumber=100, stationsNumber=40, graphBuilderClass=VeryLongServiceTimeFullGraphBuilder, subdirectory='long_service_many_agvs')
run(tasksNumber=1000, agvsNumber=25, stationsNumber=40, graphBuilderClass=LongServiceTimeFullGraphBuilder, subdirectory='long_service_few_agvs')
run(tasksNumber=1000, agvsNumber=60, stationsNumber=10, graphBuilderClass=ShortServiceTimeFullGraphBuilder, subdirectory='short_service_many_agvs')