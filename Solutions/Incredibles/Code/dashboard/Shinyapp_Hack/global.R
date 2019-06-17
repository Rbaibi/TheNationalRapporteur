#global script

library(tm)
# library(qdap)
# library(qdapDictionaries)
library(RColorBrewer)
library(ggplot2)
library(reshape2)
library(magrittr)
library(scales)
library(wordcloud)
library(readxl)
library(utils)
library(RSSL)
library(tidyverse)
library(e1071)
library(stringr)
library(shinyWidgets)
library(shinycssloaders)
library(plyr)
library(dplyr)
library(rjson)
library(jsonlite)
rename = dplyr::rename

gen_dir = "C:/Users/Totta/Desktop/Shinyapp_Hack/"

#static df for topic modeling
df_tops <- as.data.frame(c("slachtoffer", "mensenhandel"), stringsAsFactors = FALSE) 
colnames(df_tops) <- "Topics"

getDataForCloud <- function(dt){
  if(nrow(dt)==0)
    return
  
  ext_stop_words_list = read.csv(paste0(gen_dir,'INPUT/stopwoorden.txt'),header = 0, stringsAsFactors=F)
  ext_stop_words_list2 = read.csv(paste0(gen_dir,'INPUT/stop-words-nl.txt'),header = 0,stringsAsFactors=F)
  ext_stop_words_list = ext_stop_words_list$V1
  ext_stop_words_list2 = ext_stop_words_list2$V1
  docs <- Corpus(VectorSource(dt$paragraphs_text))
  #basic data clean if necessary may need to change
  toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
  docs <-tm_map(docs, toSpace, "/")
  docs <- tm_map(docs, toSpace, "@")
  docs <- tm_map(docs, toSpace, "\\|")
  # Convert the text to lower case
  docs <- tm_map(docs, content_transformer(tolower))
  # Remove numbers
  docs <- tm_map(docs, removeNumbers)
  # Remove some common stopwords
  # dutch_stop_w = tm_map(docs, removeWords, c(stopwords("dutch"),ext_stop_words_list,ext_stop_words_list2, "wel","ten"))
  # eng_stop_w = tm_map(docs, removeWords, c(stopwords("en")))
  # docs <- ifelse(dt$language=="dutch", dutch_stop_w, eng_stop_w )
  
  docs <- tm_map(docs, removeWords, c(stopwords("en"),"the","thb"))
  
  if(unique(dt$language)=="dutch"){
    docs <- tm_map(docs, removeWords, c(stopwords("dutch"),ext_stop_words_list,ext_stop_words_list2, "wel","ten"))
  }else{
    docs <- tm_map(docs, removeWords, c(stopwords("en")))
    docs <- tm_map(docs, removeWords, c(stopwords("english"),"the","thb"))
  }
  
  # Remove punctuations
  docs <- tm_map(docs, removePunctuation)
  # Eliminate extra white spaces
  docs <- tm_map(docs, stripWhitespace)
  # Text stemming
  docs <- tm_map(docs, stemDocument)
  
  #convert to term doc matrix
  dtm <- TermDocumentMatrix(docs)
  m <- as.matrix(dtm)
  v <- sort(rowSums(m),decreasing=TRUE)
  d <- data.frame(word = names(v),freq=v)
  return(d)
}

df <- read.csv(paste0(gen_dir,"INPUT/final.csv"),check.names=TRUE, stringsAsFactors = FALSE)
df = df %>%  rename(createdAt=created_at, paragraphs_text=paragraph, docType = type)
df <- df %>% filter(nchar(paragraphs_text) > 200)
# df$paragraphs_text <- paste0(substr(df$paragraphs_text, start = 1, stop = 500),".....")
df$paragraphs_text <- gsub('[^\x20-\x7E]', '', df$paragraphs_text)
df$docType = ifelse(df$docType=='raport','rapport', df$docType)
df$docType = ifelse(df$docType=='rappot','rapport', df$docType)
print(unique(df$docType))

# df$picturefile = "test.png"

# df$score = seq(1,394,by=1)/300
# df$is_opinion = 1
# df[1:10,"is_opinion"]= 0

# names(df) <- gsub("\\.", "_", names(df))
# df$paragraphs_pagenumber <- gsub(":",",",df$paragraphs_pagenumber)

categories = as.data.frame(c("Relevance", "Opinion"), stringsAsFactors = FALSE) 
colnames(categories) <- "Categories"

# doc_type = as.data.frame(c("Brief", "Jaarplan", "Publicatie", "Rapport", "Toespraak"), stringsAsFactors = FALSE)
# colnames(doc_type) <- "Documents"

# language = as.data.frame(c("Dutch", "English"), stringsAsFactors = FALSE)
# colnames(language) <- "Language"


library(topicmodels)
get_lda <- function(dt){

  docs <- Corpus(VectorSource(dt))
  #basic data clean if necessary may need to change
  toSpace <- content_transformer(function (x , pattern ) gsub(pattern, " ", x))
  docs <-tm_map(docs, toSpace, "/")
  docs <- tm_map(docs, toSpace, "@")
  docs <- tm_map(docs, toSpace, "\\|")
  # Convert the text to lower case
  docs <- tm_map(docs, content_transformer(tolower))
  # Remove numbers
  docs <- tm_map(docs, removeNumbers)
  # Remove some common stopwords
  docs <- tm_map(docs, removeWords, c(stopwords("dutch"),ext_stop_words_list,ext_stop_words_list2, "wel","ten"))
  docs <- tm_map(docs, removeWords, c(stopwords("en"),"also"))
  docs <- tm_map(docs, removeWords, c(stopwords("english")))
  # Remove punctuations
  docs <- tm_map(docs, removePunctuation)
  # Eliminate extra white spaces
  docs <- tm_map(docs, stripWhitespace)
  # Text stemming
  docs <- tm_map(docs, stemDocument)

  #convert to term doc matrix
  dtm <- DocumentTermMatrix(docs)
  m <- as.matrix(dtm)
  v <- sort(rowSums(m),decreasing=TRUE)
  d <- data.frame(word = names(v),freq=v)
  return(dtm)
}

ext_stop_words_list = read.csv(paste0(gen_dir,'INPUT/stopwoorden.txt'),header = 0, stringsAsFactors=F)
ext_stop_words_list2 = read.csv(paste0(gen_dir,'INPUT/stop-words-nl.txt'),header = 0,stringsAsFactors=F)
ext_stop_words_list = ext_stop_words_list$V1
ext_stop_words_list2 = ext_stop_words_list2$V1

ap_lda <- LDA(get_lda(df$paragraph), k = 2, control = list(seed = 42))
ap_lda

library(tidytext)

ap_topics <- tidytext::tidy(ap_lda, matrix = "beta", na.action= na.omit)
ap_top_terms <- ap_topics %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
top_terms = ap_top_terms %>%
  mutate(term = reorder(term, beta)) %>% dplyr::select(term)
top_terms=top_terms$term
