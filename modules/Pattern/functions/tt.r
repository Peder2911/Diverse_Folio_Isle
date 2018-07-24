
library(e1071)
library(randomForest)
library(gmodels)
library(stringr)

scriptDir <- commandArgs()[4]%>%
  str_sub(8)%>%
  dirname()

sentences <- read.csv(commandArgs(trailingOnly=TRUE)[1])
model <- commandArgs()

vectors <- system(paste('rscript ',scriptDir,'/'))



if(TRUE){
  vectorized_sentences <- vectorized_sentences[sample(nrow(sentences_vec)),]
  test <- vectorized_sentences[c(FALSE,TRUE,FALSE),]
  train <- vectorized_sentences[c(TRUE,FALSE,TRUE),]
  m_svm <- svm(class~.,data=train)
  pred_svm <- predict(m_svm,test)
}

# modelling ---------------------------------------------------------------

#m_bayes <- naiveBayes(class~.,data=sent_train,laplace = 0.1)
#m_svm <- svm(class~.,data=sent_train,cost=3)

#pred_bayes <- predict(m_bayes,sent_test)
#pred_svm <- predict(m_svm,sent_test)
#pred_forest <- predict(m_forest,sent_test)

#CrossTable(pred_bayes,sent_test$class)
#CrossTable(pred_svm,sent_test$class)
#CrossTable(pred_forest,sent_test$class)

#beepr::beep()
