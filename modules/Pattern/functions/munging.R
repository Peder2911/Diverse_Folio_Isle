suppressPackageStartupMessages(library(stringr,warn.conflicts = FALSE))
suppressPackageStartupMessages(library(dplyr,warn.conflicts = FALSE))

as.sentence.df <- function(df,sentence.col = 'body',sep='\n'){
  dfs <- apply(df,1,function(row){
    sentence <- row[sentence.col]%>%
      str_split(sep)%>%
      unlist()
    notSent <- names(row)[names(row)!=sentence.col]
    rest <- row[notSent]%>%
      lapply(rep,length(sentence))
    out <- data.frame(rest,sentence,stringsAsFactors = FALSE)
  })
  dfs <- dfs %>%
    bind_rows()

}

as.dtm <- function(df,textCol = 'sent',type='count',freqTerms=FALSE,...){
  require('tm')
  corp <- VCorpus(VectorSource(df[[textCol]]))
  dtm <- DocumentTermMatrix(corp,...)


  if(is.numeric(freqTerms)){
    ft <- findFreqTerms(dtm,freqTerms)
    dtm <- dtm[,ft]
  }

  if(type=='occurrence'){
    dtm <- apply(dtm,2,function(x){
      x <- as.factor(ifelse(x>0,'yes','no'))
    })%>%
      as.data.frame()
  }

  dtm
}

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
