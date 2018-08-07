suppressPackageStartupMessages(library(jsonlite))

dat <- fromJSON(readLines('stdin'))
write.csv(dat,row.names = FALSE)
