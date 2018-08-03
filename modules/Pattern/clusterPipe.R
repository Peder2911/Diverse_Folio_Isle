#!/usr/local/bin/rscript
# Feed it indata, and the proper command Arguments!
# There must be some bugs in these functions...

suppressPackageStartupMessages(library(magrittr))
suppressPackageStartupMessages(library(stringr))

myPath <- commandArgs()[4]%>%
  str_sub(8)%>%
  dirname()

source(paste(myPath,'functions/munging.R',sep='/'))
source(paste(myPath,'functions/sent2vec.R',sep='/'))
source(paste(myPath,'functions/idealCluster.R',sep='/'))

tracerFile <- commandArgs(trailingOnly=TRUE)[1]
s2v <- commandArgs(trailingOnly=TRUE)[2]
mod_vec <- commandArgs(trailingOnly=TRUE)[3]

inData <- read.csv(text = readLines('stdin'),stringsAsFactors = FALSE)%>%
  as.sentence.df()
tracerData <- read.delim(tracerFile,stringsAsFactors = FALSE,col.names = 'sentence')

out <- selectByIdeal(inData,tracerData,s2v,mod_vec,kTries = 10,sentColumn = 'sentence')

write.csv(out,row.names = FALSE)
