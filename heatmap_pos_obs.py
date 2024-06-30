import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import interpolation as ip


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

def heatmap(csv):
    
    x_col, y_col = ip.interpolate(csv, 1, 4)
    # change the last two arguments to the columns of the csv you are working with
    # 1, 4 -> learner nose

    print("x:", x_col)
    main_sesh_x = []
    main_sesh_y = []

    # time stamp in seconds for the correct and incorrect trials by left and right
    left_corr = [417] #10, 126, 153, 185, 292, 417
    right_corr = [429] #38, 253, 406, 429
    left_incorr = [21] #21, 194, 327, 452
    right_incorr = [476] #105, 135, 207, 301, 439, 476


    # use this for left nosepoke trials
    for i in range(len(left_corr)):
        frame = left_corr[i]*15
        main_sesh_x += x_col[frame:frame+60]
        main_sesh_y += y_col[frame:frame+60]
    
    print(main_sesh_x)

    # use this for right nosepoke trials
    # for i in range(len(right_corr)):
    #      frame = right_corr[i]*15
    #      main_sesh_x += flip(x_col[frame:frame+5])
    #      main_sesh_y += y_col[frame:frame+5] 



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

heatmap("MATLAB/ibns csv/05252023 98 + 117DeepCut_resnet50_IBNS Social AERIALJun10shuffle1_255000.csv") #change this based on what CSV file you are generating heatmap for
