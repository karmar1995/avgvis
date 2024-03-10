from simulation.experiments.executable_experiments.agv_random_task_scheduling import run
from simulation.experiments_utils.test_graphs_builders import *

run(tasksNumber=100, agvsNumber=25, stationsNumber=40, graphBuilderClass=DebugGraphBuilder, subdirectory='debug')
run(tasksNumber=100, agvsNumber=50, stationsNumber=30, graphBuilderClass=VeryLongServiceTimeFullGraphBuilder, subdirectory='long_service_many_agvs')
run(tasksNumber=100, agvsNumber=12, stationsNumber=20, graphBuilderClass=LongServiceTimeFullGraphBuilder, subdirectory='long_service_few_agvs')
run(tasksNumber=100, agvsNumber=50, stationsNumber=10, graphBuilderClass=ShortServiceTimeFullGraphBuilder, subdirectory='short_service_many_agvs')

ShortServiceTimeFullGraphWithBranchesBuilder.branches = 1
run(tasksNumber=100, agvsNumber=50, stationsNumber=10, graphBuilderClass=ShortServiceTimeFullGraphWithBranchesBuilder, subdirectory='short_service_many_agvs_with_branches_k1')
ShortServiceTimeFullGraphWithBranchesBuilder.branches = 3
run(tasksNumber=100, agvsNumber=50, stationsNumber=10, graphBuilderClass=ShortServiceTimeFullGraphWithBranchesBuilder, subdirectory='short_service_many_agvs_with_branches_k3')