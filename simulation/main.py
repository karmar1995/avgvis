from simulation.experiments.executable_experiments.agv_random_task_scheduling import run
from simulation.experiments_utils.test_graphs_builders import *


run(tasksNumber=3000, agvsNumber=300, stationsNumber=120, graphBuilderClass=VeryLongServiceTimeFullGraphBuilder, subdirectory='long_service_many_agvs')
run(tasksNumber=3000, agvsNumber=75, stationsNumber=120, graphBuilderClass=LongServiceTimeFullGraphBuilder, subdirectory='long_service_few_agvs')
run(tasksNumber=3000, agvsNumber=180, stationsNumber=30, graphBuilderClass=ShortServiceTimeFullGraphBuilder, subdirectory='short_service_many_agvs')