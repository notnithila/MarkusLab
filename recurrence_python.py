import pandas as pd
from pyrqa.analysis_type import Cross
from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation
from pyrqa.computation import RPComputation
from pyrqa.image_generator import ImageGenerator
import interpolation as ip
import math


csv = "MATLAB/971_3.3.2020_Rat+SALDeepCut_resnet50_Operant_V2May20shuffle1_960000.csv"

data = pd.read_csv("MATLAB/971_3.3.2020_Rat+SALDeepCut_resnet50_Operant_V2May20shuffle1_960000.csv")

correct = [10, 38, 126, 153, 185, 253, 292, 406, 417, 429]
incorrect = [21, 105, 135, 194, 207, 297, 301, 327, 439, 452, 476]


x_nose, y_nose = ip.interpolate(csv, 1, 14) 
# to generate the recurrence plots for the teacher, change the last two values to 10 & 13
# to generate the recurrence plots for the learner, change the last two values to 1 & 4

x_light, y_light = ip.interpolate(csv, 19, 22)


demo_nose_x = []
demo_nose_y = []
light_x = []
light_y = []

# to generate for correct trials, use correct array
# to generate for incorrect trials, use incorrect array
for i in range(len(correct)):
    frame = correct[i]*15
    demo_nose_x += x_nose[frame:frame+60]
    demo_nose_y += y_nose[frame:frame+60] 

    light_x += x_light[frame:frame+60]
    light_y += y_light[frame:frame+60] 

distances = []
for i in range(len(demo_nose_x)):
    distance = math.sqrt((demo_nose_x[i][1] - 315)**2 + (demo_nose_y[i][1] - 0)**2)
    distances.append(distance)
  
time_series_x = TimeSeries(distances,
                           embedding_dimension=2,
                           time_delay=30)

settings = Settings(time_series_x,
                    analysis_type=Cross,
                    neighbourhood=FixedRadius(20),
                    similarity_measure=EuclideanMetric,
                    theiler_corrector=0)
computation = RQAComputation.create(settings,
                                    verbose=True)
result = computation.run()
result.min_diagonal_line_length = 2
result.min_vertical_line_length = 2
result.min_white_vertical_line_length = 2
print(result)

computation = RPComputation.create(settings)
result = computation.run()
ImageGenerator.save_recurrence_plot(result.recurrence_matrix_reverse,
                                     'cross_recurrence_plot.png')

