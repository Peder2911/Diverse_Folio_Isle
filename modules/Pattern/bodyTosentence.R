suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(magrittr))
suppressPackageStartupMessages(library(stringr))

myPath <- commandArgs()[4]%>%
  str_sub(8)%>%
  dirname()

source(paste(myPath,'functions/munging.R',sep='/'))

dat <- read.csv(text = readLines('stdin'),stringsAsFactors=FALSE)%>%
  as.sentence.df()%>%
  rename(body = sentence)

write.csv(dat,row.names = FALSE)
