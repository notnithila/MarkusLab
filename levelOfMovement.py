#level of movement
import pandas as pd
import interpolation as ip

csv = "MATLAB/971_3.3.2020_Rat+SALDeepCut_resnet50_Operant_V2May20shuffle1_960000.csv"
x_col, y_col = ip.interpolate(csv, 10, 13)
print(x_col)
