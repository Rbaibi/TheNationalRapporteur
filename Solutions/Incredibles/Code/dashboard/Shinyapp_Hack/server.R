
server <- function(input, output, session) {
  
  v <- reactiveValues(doPlot = FALSE)
  
  data <- eventReactive(input$button, {
    runif(1)
  })
  observeEvent(input$button,{
    if(!is.null(input$text)){
      print("inside obs text")
      newDf = df %>% filter( grepl(input$text,paragraphs_text, ignore.case = TRUE)) %>% arrange(desc(score), desc(createdAt)) %>% head(3)
      df_tbl =  df %>% filter( grepl(input$text,paragraphs_text, ignore.case = TRUE)) %>%
        arrange(desc(score), desc(createdAt)) %>% head(3) %>% select(title, createdAt, paragraphs_text) %>% 
        mutate(paragraphs_text = paste0(substr(paragraphs_text, start = 1, stop = 500),".....")  )
      
      if(nrow(newDf)>0){
        output$table <- renderTable(df_tbl)
        
        output$plot2<-renderPlot({
          d = getDataForCloud(newDf)
          # tail(d$words, n =10)
          
          
          create.plot <-  wordcloud(words = d$word, freq = d$freq, min.freq = 1,
                                    max.words=50, random.order=FALSE, rot.per=0.35, 
                                    colors=brewer.pal(8, "Dark2"))
        }, height = 500, width = 500)
      }
      
    }
    # newDf = df %>% filter( grepl(input$text,paragraphs_text, ignore.case = TRUE)) %>% arrange(desc(score), desc(createdAt)) %>% head(3)
    # output$plot3<-renderImage({
    #   # img(src = 'Gewogen risico. Deel 2- Behandeling opleggen aan zedendelinquenten.png', height = '300px')
    #   
    # })
    output$plot3 <- renderImage({
      # A temp file to save the output. It will be deleted after renderImage
      # sends it, because deleteFile=TRUE.
      outfile <- tempfile(fileext='Gewogen risico. Deel 2- Behandeling opleggen aan zedendelinquenten.png')
      
      # Generate a png
      png(outfile, width=400, height=400)
      # Return a list
      list(src = outfile,
           alt = "This is alternate text")
    }, deleteFile = TRUE)
    
  })
  
  eventReactive(input$doc,{
    runif(1)
  })
  observeEvent(input$doc,{
    print("inside obs doc")
    if(input$doc != ''){
      newDf = df %>% filter(docType==input$doc) %>% arrange(desc(score), desc(createdAt)) %>% head(3)
      df_tbl =  df %>% filter(docType==input$doc) %>% arrange(desc(score), desc(createdAt)) %>% head(3) %>% 
        select(title, createdAt, paragraphs_text) %>% 
        mutate(paragraphs_text = paste0(substr(paragraphs_text, start = 1, stop = 500),".....")  )
      output$table <- renderTable(df_tbl)
      
      output$plot2<-renderPlot({
        
        d = getDataForCloud(newDf)
        # tail(d$words, n =10)
        
        create.plot <-  wordcloud(words = d$word, freq = d$freq, min.freq = 1,
                                  max.words=50, random.order=FALSE, rot.per=0.35, 
                                  colors=brewer.pal(8, "Dark2"))
      }, height = 500, width = 500)
    }
  })
  
  eventReactive(input$lang,{
    runif(1)
  })
  observeEvent(input$lang,{
    print("inside obs lang")
    if(input$lang != ''){
      newDf = df %>% filter(language==input$lang) %>% arrange(desc(score),desc(createdAt)) %>% head(3)
      df_tbl =  df %>% filter(language==input$lang) %>% arrange(desc(score), desc(createdAt)) %>% head(3) %>% 
        select(title, createdAt, paragraphs_text) %>% 
        mutate(paragraphs_text = paste0(substr(paragraphs_text, start = 1, stop = 500),".....")  )
      output$table <- renderTable(df_tbl)
      
      output$plot2<-renderPlot({
        
        d = getDataForCloud(newDf)
        # tail(d$words, n =10)
        print(d)
        
        create.plot <-  wordcloud(words = d$word, freq = d$freq, min.freq = 1,
                                  max.words=50, random.order=FALSE, rot.per=0.35, 
                                  colors=brewer.pal(8, "Dark2"))
      }, height = 500, width = 500)
    }
  })
  
  eventReactive(input$cats,{
    runif(1)
  })
  observeEvent(input$cats,{
    print("inside cats opinion")
    if(input$cats == 'Opinion'){
      newDf = df %>% filter(is_opinion==1) %>% arrange(desc(score), desc(createdAt)) %>% head(3)
      df_tbl =  df %>% filter(is_opinion==1) %>% arrange(desc(score), desc(createdAt)) %>% head(3) %>%
        select(title, createdAt, paragraphs_text) %>% 
        mutate(paragraphs_text = paste0(substr(paragraphs_text, start = 1, stop = 500),".....")  )
      output$table <- renderTable(df_tbl)
      
      output$plot2<-renderPlot({
        d = getDataForCloud(newDf)
        
        create.plot <-  wordcloud(words = d$word, freq = d$freq, min.freq = 1,
                                  max.words=50, random.order=FALSE, rot.per=0.35, 
                                  colors=brewer.pal(8, "Dark2"))
      }, height = 500, width = 500)
    } else{
      newDf = df %>% arrange(desc(score), desc(createdAt)) %>% head(3)
      df_tbl =  df %>% arrange(desc(score), desc(createdAt)) %>% head(3) %>% 
        select(title, createdAt, paragraphs_text) %>% 
        mutate(paragraphs_text = paste0(substr(paragraphs_text, start = 1, stop = 500),".....")  )
      output$table <- renderTable(df_tbl)
      
      output$plot2<-renderPlot({
        
        d = getDataForCloud(newDf)
        
        
        create.plot <-  wordcloud(words = d$word, freq = d$freq, min.freq = 1,
                                  max.words=50, random.order=FALSE, rot.per=0.35, 
                                  colors=brewer.pal(8, "Dark2"))
      }, height = 500, width = 500)
    }
  })
  
  output$plot2<-renderPlot({
    
    d = getDataForCloud(df)
    # tail(d$words, n =10)
    
    
    create.plot <-  wordcloud(words = d$word, freq = d$freq, min.freq = 1,
                              max.words=50, random.order=FALSE, rot.per=0.35, 
                              colors=brewer.pal(8, "Dark2"))
  }, height = 500, width = 500)
  
  # inp = output$text 
  # outText = df %>% filter(inp %in% paragraphs) %>% arrange(desc(createdAt)) %>% head(5)
  # output$test_tx{}
  
}