library(tm)
library(topicmodels)
library(ldatuning)
data <- read.csv("C:/Users/wty0511/PycharmProjects/GitComment/code_comment.csv",encoding="UTF-8")
ovid3 <- Corpus(DataframeSource(data),readerControl=list(language="eng"))
length(ovid3)
dtm <- DocumentTermMatrix(ovid3 ) 
print(dtm)
rowTotals <- apply(dtm , 1, sum) #Find the sum of words in each Document
dtm.new   <- dtm[rowTotals> 0, ]           #remove all docs without words

inspect(dtm.new)
optimal.topics <- FindTopicsNumber(dtm.new, topics =  seq(50,650,100),method="Gibbs",metrics=c("Arun2010", "CaoJuan2009", "Griffiths2004","Deveaud2014"),control = list(iter=100))
print(optimal.topics)
FindTopicsNumber_plot(optimal.topics)