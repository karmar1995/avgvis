from simulation.experiments.executable_experiments.agv_random_task_scheduling import run
from simulation.experiments_utils.test_graphs_builders import *


#run(tasksNumber=100, agvsNumber=2, stationsNumber=10, graphBuilderClass=DebugGraphBuilder, subdirectory='debug')
run(tasksNumber=300, agvsNumber=10, stationsNumber=30, graphBuilderClass=VeryLongServiceTimeFullGraphBuilder, subdirectory='long_service_many_agvs')
#run(tasksNumber=3000, agvsNumber=75, stationsNumber=120, graphBuilderClass=LongServiceTimeFullGraphBuilder, subdirectory='long_service_few_agvs')
#run(tasksNumber=3000, agvsNumber=300, stationsNumber=30, graphBuilderClass=ShortServiceTimeFullGraphBuilder, subdirectory='short_service_many_agvs')