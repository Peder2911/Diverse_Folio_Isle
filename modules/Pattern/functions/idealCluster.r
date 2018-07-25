require(tidyverse,warn.conflicts = FALSE,quietly = TRUE)
require(stats,warn.conflicts = FALSE)
require(broom,warn.conflicts = FALSE)

# Functions depend on the following format:
# sent | dim1 | dim2 ... dimn 

selectByIdeal <- function(data,tracerData,s2v,mod_vec,kTries = 10,sentColumn = 'sent'){
  
  if(!exists('sentenceVectors')){
    stop('selectByIdeal requires sent2vec (did you remember to source it?)')
  }
  
  datVec <- sentenceVectors(data[,sentColumn],s2v,mod_vec)
  tracVec <- sentenceVectors(tracerData[,sentColumn],s2v,mod_vec)
  
  datVec$class <- 0
  tracVec$class <- 1
  
  tot <- rbind(datVec,tracVec)
  ideal <- idealK(tot,kTries)
  
  km <- kmeans(tot%>%
                 select(contains('dim')),ideal)
  tot$cluster <- km$cluster
  
  cl_sum <- tot%>%
    group_by(cluster)%>%
    summarize(pos_sum = sum(class),
              prop = pos_sum/n())
  
  best <- as.numeric(cl_sum[cl_sum$prop == max(cl_sum$prop),'cluster'])
  
  toOut <- tot%>%
    filter(cluster == best,
           class == 0)
  
  out <- data[data$sent %in% toOut$sentences,]
}

#####################################

# Gives increments of vector
increments <- function(x){
  y <- 0
  for(i in 1:length(x)){
    if(i<length(x)){
      y <- c(y,x[i+1]-x[i])      
    }
  }
  y
}

#####################################

kmStats <- function(data,k){
  # Make kmeans model
  km <- kmeans(data%>%
                 select(contains('dim')),k)
  # Get class and cluster to summarise
  toSum <- tibble(class = data$class,cluster = km$cluster)
  
  # Get stats abt. model using tidy
  km <- tidy(km)
  r_max <- max(km$withinss)
  r_min <- min(km$withinss)
  r_mean <- mean(km$withinss)
  r_sd <- sd(km$withinss)
  
  # Summarise positive occurrence and clusters
  r_sum <- toSum%>%
    group_by(cluster)%>%
    summarise(n_pos = sum(class),
              prop = n_pos/n())
  
  # stats
  r_maxN <- max(r_sum$n_pos)
  r_maxProp <- max(r_sum$prop)
  r_onePstProp <- r_maxProp / 100
  r_propLowC <- nrow(r_sum[r_sum$prop < r_onePstProp,])
  
  # Stat output for this k
  row <- list(k=k,
              maxss = r_max,
              minss = r_min,
              meanss = r_mean,
              sdss = r_sd,
              maxN = r_maxN,
              maxProp = r_maxProp,
              onePstProp = r_onePstProp
  )
  # Bind to out
  row
}

idealK <- function(data,max = 15,method = 'maxss'){
  # Product
  out <- tibble(k=numeric(),
                maxss = numeric(),
                minss = numeric(),
                meanss = numeric(),
                sdss = numeric(),
                maxN = numeric(),
                maxProp = numeric(),
                onePstProp = numeric()
  )
  
  # Walk through k's
  for(k in seq(2,max)){
    out <- bind_rows(out,kmStats(data,k))
  }
  
  if(method == 'maxss'){
    inc <- increments(out$maxss)
    minInc <- -(max(out$maxss)/11)
    ideal <- 0
    
    n = 1
    while(ideal == 0){
      if(inc[n] <= minInc){
        ideal <- n+1
      }
      n <- n+1  
    }
  }else if(method == 'occurrence'){
    
  }
  ideal
}