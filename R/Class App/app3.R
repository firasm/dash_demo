# Here we add some components and a slightly interactive table

### NOTE THIS VERSION IS A WORK IN PROGRESS

library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(dashTable)
library(tidyverse)
library(plotly)
library(gapminder)

app <- Dash$new(external_stylesheets = "https://codepen.io/chriddyp/pen/bWLwgP.css")

# Selection components
#We can get the years from the dataset to make ticks on the slider
yearMarks <- lapply(unique(gapminder$year), as.character)
names(yearMarks) <- unique(gapminder$year)
yearSlider <- dccRangeSlider(
  marks = yearMarks,
  # Note: this does not work despite being exactly as per documentation
  # marks = lapply(unique(gapminder$year), function(x){paste("", x)}),
  min = 1952,
  max = 2007,
  step=5,
  value = list(1952, 2007)
)

continentDropdown <- dccDropdown(
  # lapply can be used as a shortcut instead of writing the whole list
  # especially useful if you wanted to filter by country!
  options = lapply(
    levels(gapminder$continent), function(x){
    list(label=x, value=x)
  }),
  value = levels(gapminder$continent), #Selects all by default
  multi = TRUE
)

yaxisDropdown <- dccDropdown(
  options=list(
    list(label = "GDP Per Capita", value = "gdpPercap"),
    list(label = "Life Expectancy", value = "lifeExp"),
    list(label = "Population", value = "pop")
  ),
  value = "gdpPercap"
)

# Graph (no change from app2)
p <- ggplot(gapminder, aes(x=year, y=gdpPercap, colour=continent)) +
  geom_point(alpha=0.6) +
  scale_color_manual(name="Continent", values=continent_colors) +
  xlab("Year") +
  ylab("GDP Per Capita") +
  theme_bw()

graph <- dccGraph(
  id = 'gap-graph',
  figure=ggplotly(p)
)

# Table that can be sorted by column
table <- dashDataTable(
  id = "table",
  # these make the table scrollable
  fixed_rows= list(headers = TRUE, data = 0),
  style_table= list(
    maxHeight = '200',
    overflowY = 'scroll'
  ),
  columns = lapply(colnames(gapminder), 
                   function(colName){
                     list(
                       id = colName,
                       name = colName
                     )
                   }),
  data = df_to_list(gapminder),
  sort_action="native"
)

app$layout(
  htmlDiv(
    list(
      htmlH1('Gapminder Dash Demo'),
      htmlH2('Looking at country data interactively'),
      #selection components go here
      htmlLabel('Select a year range:'),
      yearSlider,
      htmlIframe(height=15, width=10, style=list(borderWidth = 0)), #space
      htmlLabel('Select continents:'),
      continentDropdown,
      htmlLabel('Select y-axis metric:'),
      yaxisDropdown,
      #end selection components
      graph,
      #table goes here
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      htmlLabel('Try sorting by table columns!'),
      table,
      #end table
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      dccMarkdown("[Data Source](https://cran.r-project.org/web/packages/gapminder/README.html)")
    )
  )
)

app$run_server()

### App created by Kate Sedivy-Haley as part of the DSCI 532 Teaching Team