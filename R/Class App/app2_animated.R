#Let's put an animated plot on

library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(tidyverse)
library(plotly)
library(gapminder)

# We'll replace our styles with an external stylesheet 
# for simplicity
app <- Dash$new(external_stylesheets = "https://codepen.io/chriddyp/pen/bWLwgP.css")

p <- ggplot(gapminder, aes(gdpPercap, lifeExp, color = continent)) +
  geom_point(aes(size = pop, 
                 frame = year, 
                 ids = country)) +
  theme_bw() +
  labs(x = 'GDP Per capita ($)',
       y = 'Life Expectancy (years)',
       title = "Hans Rosling's famous gapminder bubble chart") + 
  scale_x_log10() + 
  theme(legend.title = element_blank())

gp <- ggplotly(p, width = 700, height = 400) %>% 
  animation_opts(
    frame = 100, 
   # easing = "elastic", 
    redraw = FALSE
  ) %>% 
  animation_button(
    x = 1, xanchor = "right", y = 0.02, yanchor = "bottom"
  ) %>%
  animation_slider(
    currentvalue = list(prefix = "YEAR: ", font = list(color="red"))
  ) %>% 
  config(displayModeBar = FALSE)

# To push your ggplotly object to plotly servers, follow these instructions
# https://plot.ly/ggplot2/getting-started/#initialization-for-online-plotting
api_create(gp, filename='gapminder_animated')

Iframe <- htmlIframe(src = "//plot.ly/~firasm/7.embed", 
                    width="900", height="800",
                    style=list(borderWidth = 0))

app$layout(
  htmlDiv(
    list(
      htmlH1('Gapminder Dash Demo'),
      htmlH2('Looking at country data interactively'),
      Iframe,
      htmlDiv(), #spacer
      dccMarkdown("[Data Source](https://cran.r-project.org/web/packages/gapminder/README.html)")
    )
  )
)

app$run_server()

### App created by Kate Sedivy-Haley as part of the DSCI 532 Teaching Team