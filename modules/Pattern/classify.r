suppressPackageStartupMessages(library(magrittr,warn.conflicts = FALSE))
suppressPackageStartupMessages(library(stringr,warn.conflicts = FALSE))
suppressPackageStartupMessages(library(e1071,warn.conflicts = FALSE))

myPath <- commandArgs()[4]%>%
  str_sub(8)%>%
  dirname()

s2v <- commandArgs(trailingOnly=TRUE)[1]
mod_e <- commandArgs(trailingOnly=TRUE)[2]
mod_c <- commandArgs(trailingOnly=TRUE)[3]

source(paste(myPath,'functions/munging.R',sep='/'))
source(paste(myPath,'functions/sent2vec.R',sep='/'))

#####################################

dat <- read.csv(text=readLines('stdin'),row.names=NULL)
dat <- as.sentence.df(dat)

#####################################

vectors <- sentenceVectors(dat$sentence,s2v,mod_e)

mod_c <- readRDS(mod_c)
pred <- predict(mod_c,vectors)

dat$pred <- pred

#####################################

write.csv(dat,row.names=FALSE)
