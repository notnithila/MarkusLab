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

# read in the data
data = read.csv('./971_3.3.2020_Rat+SALDeepCut_resnet50_Operant_V2May20shuffle1_960000.csv')

trials = list(6, 17, 34, 48, 55, 64, 85, 96, 101, 117, 122, 131, 149, 165, 175, 181, 190, 203, 220, 231, 237, 249, 263, 278, 284, 288, 297, 315, 325, 337, 346, 358, 371, 378, 386, 390, 402, 413, 425, 435, 448, 465, 472, 490, 494, 503, 515, 528, 539, 545, 555, 569, 579, 598, 608, 614, 623, 630, 636, 658, 666, 673, 686, 696, 710, 729, 741, 759, 763, 777, 782, 795, 807, 815, 838, 846, 850, 865, 873, 878)

demo_nose_x <- numeric()
demo_nose_y <- numeric()

for (i in 1:length(trials)) {
  frame <- trials[[i]] * 15
  frames_x <- as.numeric(data[frame:(frame + 59), 14])  # Extract the corresponding frames
  frames_y <- as.numeric(data[frame:(frame + 59), 15])
  demo_nose_x <- c(demo_nose_x, as.numeric(unlist(frames_x)))  # Append the frames to the correct_frames vector
  demo_nose_y <- c(demo_nose_y, as.numeric(unlist(frames_y)))
  
}

light_x <- numeric()
light_y <- numeric()

for (i in 1:length(trials)) {
  frame <- trials[[i]] * 15
  frames_x <- as.numeric(data[frame:(frame + 59), 23])  # Extract the corresponding frames
  frames_y <- as.numeric(data[frame:(frame + 59), 24])
  light_x <- c(light_x, as.numeric(unlist(frames_x)))  # Append the frames to the correct_frames list
  light_y <- c(light_y, as.numeric(unlist(frames_y)))
}



#calculates the squared distance from the demo's nose to the light's x coordinate and stores in dist_x
dist_x <- vector("numeric", length = length(demo_nose_x))
for (i in seq_along(demo_nose_x)) {
  dist_x[i] <- (demo_nose_x[i] - light_x[i])**2
}

#calculates the squared distance from the demo's nose to the light's y coordinate and stores in dist_y
dist_y <- vector("numeric", length = length(demo_nose_y))
for (i in seq_along(demo_nose_y)) {
  dist_y[i] <- (demo_nose_y[i] - light_y[i])**2
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
rec_chosen_delay = 30 #first local minimum, finding first iteration
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
rec_chosen_embedding = 10 #pick lowest point
rec_remaining_fnn = rec_fnn[,rec_chosen_embedding]

######## 3d. Select radius and run CRQA ########

# rescale your data (mean or max) -- not related to the distance matrix rescaling
if (rec_rescale_type == 'mean'){
  rescaled_dist_x = dist_x / mean(dist_x)
} else if (rec_rescale_type == 'max'){
  rescaled_dist_x = dist_x / max(dist_x)
}

# run RQA - radius is 1.75
rec_analysis = crqa(ts1 = rescaled_dist_x, 
                    ts2 = rescaled_dist_x,
                    delay = rec_chosen_delay, 
                    embed = rec_chosen_embedding, 
                    r = 1.6, # you can keep playing with this to find something that works
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
           pch = 20)
plotRP(rec_analysis$RP, par) 

abline(v=seq(1, 4800, by=60), col="blue")
abline(h=seq(1, 4800, by=60), col="blue")

#adds time stamp labels
axis(side = 1)
axis(side = 2)

legend(1, 4531, legend=c("Every trial"),
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
