suppressPackageStartupMessages(library(RSQLite))


dbFile <- commandArgs(trailingOnly = TRUE)[1]
if(length(commandArgs(trailingOnly = TRUE)) > 1){
  id <- commandArgs(trailingOnly = TRUE)[2]
}

con <- dbConnect(SQLite(),dbFile)



q <- paste('SELECT * FROM sentences')
if(exists('id')){
  q <- paste(q,' WHERE id = \'',id,'\'',sep = '')
}

writeLines(paste('q =',q),con=stderr())
dat <- dbGetQuery(con,q)

if(nrow(dat) == 0){
  stop('query gave no hits!')
}

write.csv(dat,row.names=FALSE)
