#interpolation
import pandas as pd

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

def interpolate(csv, start, end):
    data_frame = pd.read_csv(csv) #might have to change based on your directory name

    head_coords = data_frame.iloc[2:,start:end].copy() #demo nose x, y, likelihood coords
    print(head_coords.shape) # 10 frames per second 

    #gets list of column names
    col_names = list(head_coords.columns)

    #changes the column data types from String to float
    for i in range(head_coords.shape[1]):
        head_coords[col_names[i]] =  pd.to_numeric(head_coords[col_names[i]])

    #filter out low likelihoods for the head coordinates
    for row in range(head_coords.shape[0]):
        if head_coords.iloc[row,2] < 0.95:
            head_coords.iloc[row,0] = None
            head_coords.iloc[row,1] = None
    
  #  print(head_coords.head)
  #  print(head_coords.iloc[:, 0].isna().sum())

    #enumerates the x and y coordinates (makes a list of tuples -> (index, value))
    list_head_coords_x = enumerate(list(head_coords.iloc[:,0]))
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

    #iterates to get the (index, val) pairs in a list 
    x_col = []
    for i in all_x:
        for j in i:
            x_col.append(j)

    y_col = []
    for i in all_y:
        for j in i:
            y_col.append(j)

    return x_col, y_col