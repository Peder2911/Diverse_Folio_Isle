
require(tidyr,warn.conflicts = FALSE)
require(stringr,warn.conflicts = FALSE)

sentenceVectors <- function(sentences,s2vPath,modelPath){

  call <- paste(s2vPath,'print-sentence-vectors',modelPath,sep=' ')
  vectors<-system(call,input = sentences,intern = TRUE)

  dims <- vectors[1]%>%
    str_split(' ')%>%
    unlist()%>%
    length() -1

  sentences <- cbind(sentences,vectors)%>%
    as.data.frame(stringsAsFactors=FALSE)

  names <- paste('dim',seq(1,dims),sep='')
  sentences <- sentences%>%
    separate(vectors,names,sep=' ',extra='drop')
  sentences[-1] <- sentences[-1]%>%
    sapply(as.numeric)%>%
    as.data.frame(stringsAsFactors=FALSE)

  sentences
}
