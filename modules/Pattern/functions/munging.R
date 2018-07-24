library(stringr,warn.conflicts = FALSE)
library(dplyr,warn.conflicts = FALSE)

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
