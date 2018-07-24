library(stringr)

dat <- read.csv(text = readLines('stdin'))

write.csv(dat)
