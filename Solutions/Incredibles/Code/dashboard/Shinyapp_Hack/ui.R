ui <- fluidPage(
  navbarPage("National Rapporteur Database",
             tabPanel("Hackathon For Peace 2019",
                      img(src='logo.png', align = "right",height = 100, width = 280),
                      sidebarLayout(
                        sidebarPanel(
                          #                           #tags$style(type='text/css', ".form-control{height: 300px; }"),
                          #                           #textInput("text", label = h3("Meldingen"),value = "", width = "100%")#S, add enter button for full message (action button)
                          textAreaInput("text", label = h3("Term(s)"),value = "",width = "100%", height = '50px')
                          ,actionButton("button", "search"),
                          #can limit to top 10 terms
                          #need to make reactive
                          selectizeInput( inputId = "topics", label = "Several topic recomendations:", c(Choose = '',as.vector( top_terms))),
                          selectizeInput( inputId = "cats", label = "What is the purpose of your search?", c(Choose = '', categories$Categories)),
                          selectizeInput( inputId = "doc", label = "What type of document are you searching for?", c(Choose = '', df$docType)),
                          selectizeInput( inputId = "lang", label = "Language?", c(Choose = '', df$language))
                        ),
                        mainPanel(
                          #textOutput("test_tx", container = if (inline) span else div, inline = FALSE)
                          #plotOutput("plot2") %>% withSpinner(color="#0dc5c1")
                          tabPanel("test",
                                   fluidRow(style = "border: 2px solid black;",
                                            tableOutput("table") #%>% withSpinner(color="#0dc5c1")
                                   )),
                          tabPanel("WordCloud",plotOutput("plot2") %>% withSpinner(color="#0dc5c1"))
                          
                          
                        )
                        
                      )
             )
  )
)


#ui <- dashboardPage(  dashboardHeader(),  dashboardSidebar(),  dashboardBody())