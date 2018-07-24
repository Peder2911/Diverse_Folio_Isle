
library(e1071)
library(randomForest)
library(gmodels)

sentences_vec[,-ncol(sentences_vec)] <- sentences_vec[,-ncol(sentences_vec)]%>%
  sapply(as.numeric)%>%
  as.data.frame()

sentences_vec <- sentences_vec[sample(nrow(sentences_vec)),]

sent_test <- sentences_vec[c(FALSE,TRUE,FALSE),]
sent_train <- sentences_vec[c(TRUE,FALSE,TRUE),]


# modelling ---------------------------------------------------------------

m_bayes <- naiveBayes(class~.,data=sent_train,laplace = 0.1)
m_svm <- svm(class~.,data=sent_train,cost=3)

pred_bayes <- predict(m_bayes,sent_test)
pred_svm <- predict(m_svm,sent_test)
pred_forest <- predict(m_forest,sent_test)

CrossTable(pred_bayes,sent_test$class)
CrossTable(pred_svm,sent_test$class)
CrossTable(pred_forest,sent_test$class)

beepr::beep()
