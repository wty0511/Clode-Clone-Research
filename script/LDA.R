library(tm)
library(topicmodels)
library(ldatuning)
topic_number=250
data <- read.csv("C:/Users/wty0511/PycharmProjects/GitComment/commit_message.csv",encoding="UTF-8")
ovid3 <- Corpus(DataframeSource(data),readerControl=list(language="eng"))
length(ovid3)
dtm <- DocumentTermMatrix(ovid3 ) 
print(dtm)
rowTotals <- apply(dtm , 1, sum) #Find the sum of words in each Document
dtm.new   <- dtm[rowTotals> 0, ]           #remove all docs without words

lda <- LDA(dtm.new, control = list(alpha = 1),method = "Gibbs", k =topic_number ,iteration=50)
term <- terms(lda , 20)
print(term[,2])
l <- c()
for (i in 1:topic_number){
	for (j in term[,i]){
		l <-c(l,j)
	}
}

print(l)
library(dplyr)
arrange(as.data.frame(table(l)),Freq)
#topics(lda , 1)
