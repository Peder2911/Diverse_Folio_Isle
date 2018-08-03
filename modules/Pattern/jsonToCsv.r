suppressPackageStartupMessages(library(jsonlite))

dat <- fromJSON(readLines('stdin'))
write.csv(dat)
