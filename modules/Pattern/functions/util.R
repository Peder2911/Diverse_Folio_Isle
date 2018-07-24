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



#sentences <- read.csv.folder('data/training/18_07_12/classifiedSentences/',columns=c('sent','class'),sep=';')
#sentences$sent <- str_replace_all(sentences$sent,'\n',' ')
#sentences$sent <- system(command = '../bin/python util/stdTokenize.py',intern = TRUE,input = sentences$sent)
#sentences <- sentences[sentences$sent!='' & sentences$class <=1,]

#sentences$class<-sentences$class%>%
#  as.logical()%>%
#  ifelse('yes','no')%>%
#  as.factor()
