#Let's start over using the gapminder data set!

library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(tidyverse)
library(plotly)
library(gapminder)

# We'll replace our styles with an external stylesheet 
# for simplicity
app <- Dash$new(external_stylesheets = "https://codepen.io/chriddyp/pen/bWLwgP.css")

#define gapminder graph
p <- ggplot(gapminder, aes(x=year, y=gdpPercap, colour=continent)) +
  geom_point(alpha=0.6) +
  scale_color_manual(name="Continent", values=continent_colors) +
  xlab("Year") +
  ylab("GDP Per Capita") +
  theme_bw()

graph <- dccGraph(
  id = 'dsci-graph',
  figure=ggplotly(p)
  )

app$layout(
  htmlDiv(
    list(
      htmlH1('Gapminder Dash Demo'),
      htmlH2('Looking at country data interactively'),
      graph,
      htmlDiv(), #spacer
      dccMarkdown("[Data Source](https://cran.r-project.org/web/packages/gapminder/README.html)")
    )
  )
)

app$run_server()

### App created by Kate Sedivy-Haley as part of the DSCI 532 Teaching Team