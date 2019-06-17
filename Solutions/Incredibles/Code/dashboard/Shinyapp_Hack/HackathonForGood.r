
set.seed(42)
library(topicmodels)
# library(rjson)
library(jsonlite)
library("dplyr")
library(tm)
library(tidytext)
library(ggplot2)

result <- fromJSON(txt = 'INPUT/sample_json.json', flatten = T )

df = as.data.frame(result)

colnames(df)

head(df, 2)

sapply(df, class)

df = df %>% mutate(createdAt = as.Date(createdAt) , language="Dutch", docType="Rapport")

df %>%  arrange(desc(createdAt)) %>% head(3)

df %>% filter(grepl("Toespraak",paragraphs.text))

df$paragraphs.pagenumber = vapply(df$paragraphs.pagenumber, paste, collapse = ", ", character(1L))

expDF = df %>% arrange(desc(createdAt))

# write.csv(as.data.frame(expDF), file='dt.csv', row.names=FALSE)

ext_stop_words_list = read.csv('~/Desktop/hack-for-good/stopwoorden.txt',header = 0, stringsAsFactors=F)
ext_stop_words_list2 = read.csv('~/Desktop/hack-for-good/stop-words-nl.txt',header = 0,stringsAsFactors=F)

ext_stop_words_list = ext_stop_words_list$V1
ext_stop_words_list2 = ext_stop_words_list2$V1

get_dtm <- function(dt){
    
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
    return(dtm)
}

dtm = get_dtm(df$paragraphs.text)
freq=rowSums(as.matrix(dtm))

tail(sort(freq,decreasing = F),n=10)

# plot(sort(freq, decreasing = T),col="blue",main="Word TF-IDF frequencies", xlab="TF-IDF-based rank", ylab = "TF-IDF")


ap_lda <- LDA(get_dtm(df$paragraphs.text), k = 2, control = list(seed = 42))
ap_lda

ap_topics <- tidy(ap_lda, matrix = "beta")
head(ap_topics)

ap_top_terms <- ap_topics %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)

ap_top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip()

testData = "The analogue and digital world have become one and the same. The common use and rapid
development of new media are providing fresh challenges when it comes to online personal spaces,
our concept of privacy, the Internet of Things, but also with respect to human trafficking. In 2012 the
researcher Latonero wrote: ‘Our understanding of technology’s role in human trafficking, while
improving, is still in its infancy, while technology without a doubt facilitates trafficking’.
Internet and mobile devices have altered the way society operates entailing that we are living much
more exposed lives. One consequence is that traffickers have greater access to potential victims, both
in terms of numbers and type.
While human traffickers previously looked for potential victims at the school gates or in a sports club
now internet, mobile telephones and social media are increasingly being used to specifically search
for potential prey. Though pundits predict that the shift will continue in the future, obviously, human
traffickers will continue recruiting their candidates in person as long as that proves worthwhile.
Human traffickers use technology as an instrument for keeping victims under control. We know that
webcams are used for keeping an eye on victims and that they are used to make films and photographs
that can later be used for blackmail purposes. We know how Snapchat is used to set up mobile
brothels that can rapidly change location; how WhatsApp is used to threaten victims and we are aware
that it has never been easier to reach potential “customers”. As Bill Gates said: ‘The Internet is
becoming the town square for the global village tomorrow’. This applies equally to human trafficking.
Advertisements for paid sex are being placed online and trafficking victims are the ones on offer.
Appointments are made through social media and transactions are even being paid for in some cases
with bitcoins.
Technology has also changed the concept of human trafficking. Whereas in the past exploitation was
through physical contact these days it is perfectly possible for exploitation to take place entirely
through digital means. Europol has warned of criminal groups forcing people to sexually abuse
children in front of a webcam so that this can be broadcast live through Skype. Allowing the human
traffickers to collect the money from people who pay to watch. Bitcoins are usually used as currency
for reasons of anonymity; and the live stream could also be hosted in the Deep web or potentially on
the Darknet. Too grim for words.
Where human traffickers are learning inventive tricks with technology it is up to us to do the same
and to do it better. We owe it to all those victims who day in day out are exploited in the most
degrading of circumstances. President Obama hit the nail on the head in 2012: ‘We are turning the
tables on traffickers. Just as they are now using technology and the internet to exploit their victims,we are going to harness technology to stop them’. Microsoft asked researchers in 2012 to focus on the
role of technology in human trafficking, earmarking $185,000 for this purpose. Since then the number
of studies has grown alongside the realisation that there are opportunities for tracking, stopping and
prosecuting human traffickers at an early stage.
Human traffickers who use technology like the internet, social media and mobile telephones
repeatedly leave behind their digital footprints. Footprints that constitute a trail of information and
evidence that can be a powerful tool in identifying, tracking and prosecuting them. But technology
offers many more opportunities than simply looking to see how human traffickers have operated in
retrospect. Technology can be deployed for prevention, for discovering new trends and developments
and for spotting and stopping human trafficking situations.
As far as prevention is concerned vulnerable groups can be reached through internet and mobile
phones. The World Bank estimates that 75% of the world population has or has access to a mobile
phone. Besides reaching victims in this way we can also reach vulnerable groups who are being
smuggled. Think of the Syrian refugees who are being smuggled into Europe and who are proving to
be vulnerable to trafficking. This group can be warned of the hazards of the trade by mobile telephone
and internet. Information about where they can find help and protection can also be passed on in a
rapid and simple way.
In the analogue society we have worked with ‘barrière models’ but there are ways of doing this
digitally as well. For example, people who place sex adverts could be required to pay with a credit
card or show their ID. People who are being groomed by a trafficker can be asked to take snapshots
from the chats and pass them on to the police so that they can intervene quickly. Technology allows
us to see fast whether a passport is real or counterfeit or whether the person being checked by the
police is on a list of missing persons or is registered as a possible victim.
Research shows that technology can be used in many ways for spotting victims and finding them. In
the United States for example the database of missing children was linked to websites where people
offered paid sex. And what happened? Some children who had been reported missing were found.
Technology, led by Google and Microsoft, is becoming increasingly better at linking photos, even
when these are photos taken in different places and in which the child for example has a different
colour of hair. It is also possible in the case of a missing victim of human trafficking to convert the
entire country into one huge tracking poster using an Amber Alert. Advertising hoardings, highway
signs, apps, text messages and email can all be used to find the victim. Of course we have to look in
each case to see whether the moment for intervening is opportune.
We can also use ‘web crawlers’ using an algorithm for filtering sex adverts to see if they point to
possible human trafficking. In America self-learning algorithms have been used for looking, for one
thing, at the style in which adverts are written, the prices that are listed and what sexual services are
being offered. Experiments have been carried out and the most suspicious adverts have been placed
with the police so that they can investigate further. Those who placed the adverts have also been
scrutinised, notably their credit card details. In this way investigators in America have discovered that
there are prostitution rings operating. Prostitutes establish themselves for a certain period in a city and
then move on to the next. The data that have been gathered would seem to imply that these switches
are coordinated, a fact that could point to human trafficking networks.
Technology can also gather data on the nature and scope of human trafficking, compare these data
with those in other countries and share best practices. Technology allows us to stand up to humantrafficking not only nationally but internationally. In combating human trafficking the world has also
become a huge village and these days we are only a mouse click away."

# get sentiments



# tokens_content <- testData %>%
#   unnest_tokens(word, content, drop = FALSE) %>%
#   count(id, word, sort = TRUE) %>%
#   ungroup()




