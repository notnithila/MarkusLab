import pandas as pd
import numpy as np
import seaborn as sns
import interpolation as ip
import matplotlib.pylab as plt
import math

# frames for right nosepoke correct trials (flipped)

def flip(tup):
    temp = []
    for i, j in tup:
        new_val = 425 - j
        temp.append((i, new_val))

    col = []
    for k, l in temp:
        newest_val = 210 + l
        col.append((k, newest_val))

    return col

def calculate_distance(x, y, target_x=315, target_y=315):
    distances = []
    for i in range(len(x)):
        distance = math.sqrt((x[i][1] - target_x)**2 + (y[i][1] - target_y)**2)
        distances.append(distance)
    return distances

def heatmap(csv):

    x_col, y_col = ip.interpolate(csv, 1, 4) 
    # change the last two arguments to the columns of the csv you are working with
    # 10, 13 -> teacher nose

    # time stamp in seconds for the correct and incorrect trials by left and right
    left_corr = [417] #10, 126, 153, 185, 292, 417
    right_corr = [429] #38, 253, 406, 429
    left_incorr = [452] #21, 194, 327, 452
    right_incorr = [476] #105, 135, 207, 301, 439, 476

    correct = [10, 38, 126, 153, 185, 253, 292, 406, 417, 429]
    incorrect = [21, 105, 135, 194, 207, 301, 327, 439, 452, 476]

    main_sesh_x = []
    main_sesh_y = []

    # use this for left nosepoke trials
    # for i in range(len(left_incorr)):
    #     frame = left_incorr[i]*15
    #     main_sesh_x += x_col[frame:frame+60]
    #     main_sesh_y += y_col[frame:frame+60]
    

    # use this for right nosepoke trials
    for i in range(len(right_incorr)):
         frame = right_incorr[i]*15
         main_sesh_x += flip(x_col[frame:frame+60])
         main_sesh_y += y_col[frame:frame+60] 

    # dist_x = calculate_distance(main_sesh_x, main_sesh_y)
    # time_points = [i * 15 for i in range(len(dist_x))] 

    # plt.plot(time_points, dist_x)
    # plt.xlabel('Time')
    # plt.ylabel('Squared Distance (dist_x)')
    # plt.title('Squared Distance (dist_x) over Time')
    # plt.grid(True)
    # plt.show()

    #the corner coordinates of the box on DLC
    xmin = 200
    xmax = 440
    ymin = 190
    ymax = 360

    xmin_ = xmin
    ymin_ = ymin


    size = 50
    x_step = (xmax - xmin) / size
    y_step = (ymax - ymin) / size

    freq = np.zeros((size, size), int)

    for row in range(len(main_sesh_x)): #change this based on what part of the video you are generating heatmap for
        flag = False
        x = main_sesh_x[row][1]
    #  print("x:", x, "type:", type(x))
        y = main_sesh_y[row][1]
    #  print("y:", y, "type:", type(y))
        for i in range(size):
            ymax_ = ymin + y_step*(i+1)
            for j in range(size):
                xmax_ = xmin + x_step*(j+1)
                if (xmin_ <= x < xmax_) and (xmax_ <= xmax) and (ymin_ <= y < ymax_) and (ymax_ <= ymax):
                    freq[i, j] = freq[i, j] + 1
                    flag = True
                    break
                xmin_ = xmax_
            if flag:
                break
            ymin_ = ymax_
        xmin_ = xmin
        ymin_ = ymin
        xmax_ = 0
        ymax_ = 0


    sns.heatmap(freq, xticklabels=False, yticklabels=False, cmap='plasma', cbar=True, vmin=0, vmax=3)
    plt.title('Teacher Correct Learner Incorrect 4') #change this based on what you are generating heatmap for
    plt.show() 

heatmap("~/Downloads/971_3.3.2020_Rat+SALDeepCut_resnet50_Operant_V2May20shuffle1_960000.csv") #change this based on what CSV file you are generating heatmap for