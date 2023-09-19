import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

#checks if input is null - returns True if not null
def notNull(x):
    return (x[1] == x[1])

#interpolation function - takes in 2 tuples of (index, value) and returns a list of tuples with interpolates values
def interpolate_mid(pair1, pair2):
    first_idx = pair1[0]
    first_val = pair1[1]
    sec_idx = pair2[0]
    sec_val = pair2[1]

    dist = sec_val - first_val
    idx_dist = sec_idx - first_idx

    step = dist / idx_dist

    filled = []

    for i in range(idx_dist):
        filled.append((first_idx+i, first_val+(step*i)))

    return filled


def heatmap(csv):
    data_frame = pd.read_csv('ibns csv/' + csv) #might have to change based on your directory name


    head_coords = data_frame.iloc[2:,1:4].copy() #obs nose x, y, likelihood coords
    print(head_coords.shape) # 10 frames per second 

    #gets list of column names
    col_names = list(head_coords.columns)

    #filter out low likelihoods for the head coordinates
    for i in range(head_coords.shape[1]):
        head_coords[col_names[i]] =  pd.to_numeric(head_coords[col_names[i]])


    #filter out low likelihoods for the head coordinates
    for row in range(head_coords.shape[0]):
        if head_coords.iloc[row,2] < 0.95:
            head_coords.iloc[row,0] = None
            head_coords.iloc[row,1] = None

    #enumerates the x and y coordinates (makes a list of tuples -> (index, value))
    list_head_coords_x = enumerate(list(head_coords.iloc[:, 0]))
    list_head_coords_y = enumerate(list(head_coords.iloc[:, 1]))

    #filters out nulls
    filtered_x = list(filter(notNull, list_head_coords_x))
    filtered_y = list(filter(notNull, list_head_coords_y))
   

   # print(list(filter(notNull, list_head_coords)))

    #interpolates remaining values
    interpolated_x = interpolate_mid(filtered_x[0], filtered_x[1])
    interpolated_y = interpolate_mid(filtered_y[0], filtered_y[1])

    all_x = []
    all_y = []
    #interpolates remaining values
    for i in range(1, len(filtered_x)):
        interpolated_x = interpolate_mid(filtered_x[i-1], filtered_x[i])
        interpolated_y = interpolate_mid(filtered_y[i-1], filtered_y[i])
        all_x.append(interpolated_x)
        all_y.append(interpolated_y)

    #iterates to get just the values for the x and y coordinates (without the indices)
    x_col = []
    for i in all_x:
        for j in i:
            x_col.append(j)

    y_col = []
    for i in all_y:
        for j in i:
            y_col.append(j)

    #the frames for the main session - not including the first and last 5 mins (these frame numbers might change)
    main_sesh_x = x_col[3000:6200]
    main_sesh_y = y_col[3000:6200]

    #the corner coordinates of the box on DLC
    xmin = 90
    xmax = 930
    ymin = 85
    ymax = 1110

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


    sns.heatmap(freq, xticklabels=False, yticklabels=False, cmap='plasma', cbar=True, vmin=0, vmax=50)
    plt.title('Full Trial (Learner Correct) - Teacher') #change this based on what you are generating heatmap for
    plt.show() 

heatmap("05252023 98 + 117DeepCut_resnet50_IBNS Social AERIALJun10shuffle1_255000.csv") #change this based on what CSV file you are generating heatmap for

