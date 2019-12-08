library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(tidyverse)
library(plotly)

app <- Dash$new()

#You can change colours and styles in the app
colors <- list(
  text = '#0013a3'
)

textStyle = list(
  textAlign = 'center',
  color = colors$text
)

#let's define our data and make a plot
dat <- data.frame(
  lab_session = factor(c("Lab 1","Lab 2", "Lab 1","Lab 2")),
  likes = factor(c("Data", "Data", "Science", "Science")),
  students = c(35, 22, 15, 28)
)

p <- ggplot(data=dat, aes(x=lab_session, y=students, fill=likes)) +
  geom_bar(stat="identity", position="dodge")

graph <- dccGraph(
  id = 'dsci-graph',
  figure=ggplotly(p)
)

#Here's some text
mdText <- "We can display some text using *Markdown*. 

- Point 1
- Point 2
"

app$layout(
  htmlDiv(
    list(
      #See our styles applied to the headers
      htmlH1('Hello Dash', style = textStyle),
      htmlH2('This is our R Dashboard', style = textStyle),
      dccMarkdown(children=mdText, style=list(color = colors$text)),
      htmlDiv(children = "Let's make a graph!", style = textStyle),
      #we add our graph here
      graph,
      #This image doesn't work and I don't know why
      htmlImg("https://upload.wikimedia.org/wikipedia/commons/8/81/Two_neurons_connected.svg")
    )
  )
)

app$run_server()