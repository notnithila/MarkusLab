#### 1. Preliminaries ####

# prep the workspace  
rm(list=ls()) #always have something to clear your workspace

# load in libraries as needed
library(nonlinearTseries)
library(tseriesChaos)
library(dplyr)
library(crqa)
library(ggplot2)
library(xlsx)

# set working directory to appropriate location
setwd('./Downloads')

# read in the data (15 frames/sec, each trial is 60 frames)
data = read.csv('./971_3.3.2020_Rat+SALDeepCut_resnet50_Operant_V2May20shuffle1_960000.csv')

incorrect = list(17, 101, 131, 190, 203, 297, 325, 435, 448, 472, 555, 579, 696, 710, 729, 741, 782, 807, 878)

obs_nose_x <- numeric()
obs_nose_y <- numeric()

for (i in 1:length(incorrect)) {
  frame <- incorrect[[i]] * 15
  frames_x <- as.numeric(data[frame:(frame + 59), 2])  # Extract the corresponding frames
  frames_y <- as.numeric(data[frame:(frame + 59), 3])
  obs_nose_x <- c(obs_nose_x, as.numeric(unlist(frames_x)))  # Append the frames to the correct_frames vector
  obs_nose_y <- c(obs_nose_y, as.numeric(unlist(frames_y)))
  
}

light_x <- numeric()
light_y <- numeric()

for (i in 1:length(incorrect)) {
  frame <- incorrect[[i]] * 15
  frames_x <- as.numeric(data[frame:(frame + 59), 11])  # Extract the corresponding frames
  frames_y <- as.numeric(data[frame:(frame + 59), 12])
  light_x <- c(light_x, as.numeric(unlist(frames_x)))  # Append the frames to the correct_frames list
  light_y <- c(light_y, as.numeric(unlist(frames_y)))
}

#obs_nose_x = as.numeric(data[3:4440, 2]) #obs nose x coordinates for frames (2 mins) - first 74 trials
#obs_nose_y = as.numeric(data[3:4440, 3]) #obs nose y coordinates for frames 

#light_x = as.numeric(data[3:4440, 20]) #demo light x coordinates for all frames
#light_y = as.numeric(data[3:4440, 21]) #demo light y coordinates for all frames


#calculates the squared distance from the obs's nose to the light's x coordinate and stores in dist_x
dist_x <- vector("numeric", length = length(obs_nose_x))
for (i in seq_along(obs_nose_x)) {
  dist_x[i] <- (obs_nose_x[i] - light_x[i])**2
}

#calculates the squared distance from the obs's nose to the light's y coordinate and stores in dist_y
dist_y <- vector("numeric", length = length(obs_nose_y))
for (i in seq_along(obs_nose_y)) {
  dist_y[i] <- (obs_nose_y[i] - light_y[i])**2
}



#### 2. Plotting your data ####

plot(dist_x)
plot(dist_y)

#### 3. Recurrence quantification analysis ####

######## 3a. Recurrence parameter setting ########

# decide Theiler window parameter
rec_theiler_window = 0

# target rescale type (mean or max)
rec_rescale_type = 'mean'
# rec_rescale_type = 'max'

######## 3b. Determine delay ########

# determine delay
rec_ami = mutual(dist_x,
                 lag.max = 800)
#lag = how much we lose for each copy, we'll lose more if lag goes up

# visualize your AMI results
plot(rec_ami)

# select your delay from the AMI data
rec_chosen_delay = 40 #first local minimum, finding first iteration
rec_remaining_mutual_info = rec_ami[rec_chosen_delay + 1] #y value


######## 3c. Determine embedding parameter ########

# determine embedding - are these points still neighbors after we add dimensions?
rec_max_embedding = 10 #embedding: the natural number of dimensions the system lives in
rec_fnn = false.nearest(dist_x,
                        m=rec_max_embedding,
                        d=rec_chosen_delay,
                        t=rec_theiler_window)

# visualize your FNN results
# shows the % of false nearest neighbors, which goes down as embedding dimension goes up
# means we are more able to clearly see the neighbors since we are looking in more dimensions
plot(rec_fnn)

# select your embedding dimension from the FNN data
rec_chosen_embedding = 8
rec_remaining_fnn = rec_fnn[,rec_chosen_embedding]

######## 3d. Select radius and run CRQA ########

# rescale your data (mean or max) -- not related to the distance matrix rescaling
if (rec_rescale_type == 'mean'){
  rescaled_dist_x = dist_x / mean(dist_x)
} else if (rec_rescale_type == 'max'){
  rescaled_dist_x = dist_x / max(dist_x)
}

# run RQA 
rec_analysis = crqa(ts1 = rescaled_dist_x, 
                    ts2 = rescaled_dist_x,
                    delay = rec_chosen_delay, 
                    embed = rec_chosen_embedding, 
                    r = 2, # you can keep playing with this to find something that works
                    normalize = 0, 
                    rescale = 0, # distance matrix rescaling option -- see documentation
                    mindiagline = 2,
                    minvertline = 2, 
                    tw = rec_theiler_window, 
                    whiteline = FALSE,
                    recpt=FALSE)

######## 3e. Create the recurrence plot ########


# use the standard plotting functions
par = list(unit = 2, 
           labelx = "Frames (15 Hz)", 
           labely = "Frames (15 Hz)", 
           cols = "red", 
           pcex = 1, 
           pch = 16)

plotRP(rec_analysis$RP, par) 

abline(v=seq(1, 1560, by=60), col="blue")
abline(h=seq(1, 1560, by=60), col="blue")

#adds time stamp labels
axis(side = 1)
axis(side = 2)

legend(1, 861, legend=c("Every trial"),
       col=c("blue"), lty=1:2, cex=0.8)


######## 3f. Inspect the CRQA metrics ########

# take a look at the quantification metrics for CRQA across x- and y-axis movement
rec_analysis$RR # rate of recurrence
rec_analysis$DET # % determinism
rec_analysis$NRLINE # total number of lines on the plot
rec_analysis$maxL # maximum line length on plot
rec_analysis$L # average line length on plot
rec_analysis$ENTR # entropy
rec_analysis$rENTR # normalized entropy
rec_analysis$LAM # laminarity
rec_analysis$TT # trapping time

