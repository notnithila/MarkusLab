#level of movement
import pandas as pd
import interpolation as ip

def notNull(x):
   return (x == x)

csv = "MATLAB/971_3.3.2020_Rat+SALDeepCut_resnet50_Operant_V2May20shuffle1_960000.csv"
x_col, y_col = ip.interpolate(csv, 10, 13) #change the columns for observer

def distance(x1, x2, y1, y2, x_scale, y_scale):
   return ((x2[1] - x1[1])**2 + (y2[1] - y1[1])**2)**0.5

# every sec (ryan's vid - 15 hertz) call distance on those two points and return value to a list for whole video

def levelOfMovement(x_scale, y_scale, start, end):
   four_sec = [i for i in range(0, len(x_col), 15)]
   dists = []
   for i in four_sec[start:end+1]:
      x1 = x_col[i-1]
      x2 = x_col[i]
      y1 = y_col[i-1]
      y2 = y_col[i]

      dist = distance(x1, x2, y1, y2, x_scale, y_scale)
      dists.append(dist)

   return dists

filtered_dist_low = list(filter(notNull, levelOfMovement(0.13, 0.14, 60, 75)))

filtered_dist_high = list(filter(notNull, levelOfMovement(0.13, 0.14, 105, 120)))

low_dist = sum(filtered_dist_low) / len(filtered_dist_low)
high_dist = sum(filtered_dist_high) / len(filtered_dist_high)

print('length:', distance([0, 170], [0, 170], [0, 0], [0, 190], 0.13, 0.14))
print('width:', distance([0, 170], [0, 460], [0, 190], [0, 190], 0.13, 0.14))

print(low_dist, 'cm and', high_dist, 'cm')