library(stringr)
library(dplyr)

read.csv.folder<-function(folder,columns,sep){
  files <- list.files(folder)
  files <- files[str_detect(files,'.csv')]

  first <- paste(folder,files[1],sep='/')
  out <- read.csv(first,sep = sep,stringsAsFactors = FALSE)%>%
    select(columns)

  for(file in files[-1]){
    tgtFile <- paste(folder,file,sep='/')
    tmpFile <- read.csv(tgtFile,sep=sep,stringsAsFactors = FALSE)%>%
      select(columns)
    out <- rbind(out,tmpFile)
  }

  out
}
