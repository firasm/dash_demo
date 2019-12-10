### NOTE THIS VERSION IS A WORK IN PROGRESS
### Lines listed as as "TODO" are where YOU need to add code to enable full functionality
### Below is a helpful table that lists all the things to do , use it to mark your progress
# [X] # TODO: Read this table and the instructions
# [ ] # TODO: Add id to component - RangeSlider
# [ ] # TODO: Add id to component - Dropdown
# [ ] # TODO: Add id to component - Dropdown
# [ ] # TODO: use yaxisKey (from above) and refactor the code below using - Dropdown
# [ ] # TODO: Use a function make_graph() to create the graph. 
# [ ] # TODO: Update line below to call make_graph() instead of calling ggplotly(p)
# [ ] # TODO: once you create make_graph, remove this static ggplot plot below
# [ ] # TODO: Update line below to call make_graph() instead of calling ggplotly(p)
# [ ] # TODO: Add callbacks to enable interactivity

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
yearMarks <- map(unique(gapminder$year), as.character)
names(yearMarks) <- unique(gapminder$year)
yearSlider <- dccRangeSlider(
  # TODO: Add id to component
  marks = yearMarks,
  min = 1952,
  max = 2007,
  step=5,
  value = list(1952, 2007)
)

continentDropdown <- dccDropdown(
  # TODO: Add id to component
  # purrr:map can be used as a shortcut instead of writing the whole list
  # especially useful if you wanted to filter by country!
  options = map(
    levels(gapminder$continent), function(x){
    list(label=x, value=x)
  }),
  value = levels(gapminder$continent), #Selects all by default
  multi = TRUE
)

# Storing the labels/values as a tibble means we can use this both 
# to create the dropdown and convert colnames -> labels when plotting
yaxisKey <- tibble(label = c("GDP Per Capita", "Life Expectancy", "Population"),
                   value = c("gdpPercap", "lifeExp", "pop"))

yaxisDropdown <- dccDropdown(
  # TODO: Add id to component
  # TODO: use yaxisKey (from above) and refactor the code below using
  # purrr:map (tidyverse) instead of manually listing each option
  # Reference: https://adv-r.hadley.nz/functionals.html
  options=list(
    list(label = "GDP Per Capita", value = "gdpPercap"),
    list(label = "Life Expectancy", value = "lifeExp"),
    list(label = "Population", value = "pop")
  ),
  value = "gdpPercap"
)

# TODO: Use a function make_graph() to create the graph.  
# Note: The make_graph() function is created for you already.
# Once you understand how it works, uncomment it out to use it
# and then delete the static plot starting after this chunk.
#
############ START make_graph() function to use ############
# Uses default parameters such as all_continents for initial graph
# all_continents <- unique(gapminder$continent)
# make_graph <- function(years=c(1952, 2007), 
#                        continents=all_continents,
#                        yaxis="gdpPercap"){

#   # gets the label matching the column value
#   y_label <- yaxisKey$label[yaxisKey$value==yaxis]
  
#   #filter our data based on the year/continent selections
#   data <- gapminder %>%
#     filter(year >= years[1] & year <= years[2]) %>%
#     filter(continent %in% continents)
 
#   # make the plot!
#   # on converting yaxis string to col reference (quosure) by `!!sym()`
#   # see: https://github.com/r-lib/rlang/issues/116
#   p <- ggplot(data, aes(x=year, y=!!sym(yaxis), colour=continent)) +
#     geom_point(alpha=0.6) +
#     scale_color_manual(name="Continent", values=continent_colors) +
#     scale_x_continuous(breaks = unique(data$year))+
#     xlab("Year") +
#     ylab(y_label) +
#     ggtitle(paste0("Change in ", y_label, " Over Time")) +
#     theme_bw()
  
#   ggplotly(p)
# }
############ END make_graph() function to use ############

# Graph (no change from app2)
# TODO: once you create make_graph, remove this static ggplot plot below
### START CODE TO REMOVE
p <- ggplot(gapminder, aes(x=year, y=gdpPercap, colour=continent)) +
  geom_point(alpha=0.6) +
  scale_color_manual(name="Continent", values=continent_colors) +
  xlab("Year") +
  ylab("GDP Per Capita") +
  theme_bw()
### END CODE TO REMOVE

graph <- dccGraph(
  id = 'gap-graph',
  # TODO: Update line below to call make_graph() instead of calling ggplotly(p)
  figure = ggplotly(p)
)

app$layout(
  htmlDiv(
    list(
      htmlH1('Gapminder Dash Demo (No interactivity yet!)'),
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
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      dccMarkdown("[Data Source](https://cran.r-project.org/web/packages/gapminder/README.html)")
    )
  )
)

### # TODO: Add callbacks to enable interactivity

# # Adding callbacks for interactivity
# app$callback(
#   # update figure of gap-graph
#   output=list(id = 'gap-graph', property='figure'),
#   
#   # based on values of year, continent, y-axis components
#   # TODO: Update the IDs of the components (note: remember that order matters!!)
#   params=list(input(id = 'CORRECT_ID_HERE', property='value'),
#               input(id = 'CORRECT_ID_HERE', property='value'),
#               input(id = 'CORRECT_ID_HERE', property='value')),
#
#   # this translates your list of params into function arguments
#   function(year_value, continent_value, yaxis_value) {
#     make_graph(year_value, continent_value, yaxis_value)
#   })

app$run_server()

### App created by Kate Sedivy-Haley as part of the DSCI 532 Teaching Team