
scriptDir <- commandArgs()[4]%>%
  str_sub(8)%>%
  dirname()

inFile <- commandArgs(trailingOnly=TRUE)[1]
inFile <- read.csv(inFile)
