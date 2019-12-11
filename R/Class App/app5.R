# Adding linked interactivity

library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(dashTable)
library(tidyverse)
library(plotly)
library(gapminder)

app <- Dash$new(external_stylesheets = "https://codepen.io/chriddyp/pen/bWLwgP.css")


# Create selection components ---------------------------------------------


#We can get the years from the dataset to make ticks on the slider
yearMarks <- lapply(unique(gapminder$year), as.character)
names(yearMarks) <- unique(gapminder$year)
yearSlider <- dccRangeSlider(
  id="year",
  marks = yearMarks,
  min = 1952,
  max = 2007,
  step=5,
  value = list(1952, 2007)
)

continentDropdown <- dccDropdown(
  id = "continent",
  options = lapply( # a shortcut for defining your options
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
  id = "y-axis",
  options = lapply(
    1:nrow(yaxisKey), function(i){
      list(label=yaxisKey$label[i], value=yaxisKey$value[i])
    }),
  value = "gdpPercap"
)


# Generating graphs and tables --------------------------------------------


# Use a function make_graph() to create the graph
# Uses default parameters such as all_continents for initial graph
all_continents <- unique(gapminder$continent)
make_graph <- function(years=c(1952, 2007), 
                       continents=all_continents,
                       yaxis="gdpPercap"){

  # gets the label matching the column value
  y_label <- yaxisKey$label[yaxisKey$value==yaxis]
  
  #filter our data based on the year/continent selections
  data <- gapminder %>%
    filter(year >= years[1] & year <= years[2]) %>%
    filter(continent %in% continents)
 
  # make the plot! Notes on arguments: 
  # on converting yaxis string to col reference (quosure) by `!!sym()`
  # see: https://github.com/r-lib/rlang/issues/116
  # NEW: the customdata mapping adds country to the tooltip and allows
  # its selection using clickData.
  p <- ggplot(data, aes(x=year, y=!!sym(yaxis), colour=continent, 
                        customdata=country)) +
    geom_point(alpha=0.6) +
    scale_color_manual(name="Continent", values=continent_colors) +
    scale_x_continuous(breaks = unique(data$year))+
    xlab("Year") +
    ylab(y_label) +
    ggtitle(paste0("Change in ", y_label, " Over Time")) +
    theme_bw()
  
  ggplotly(p) %>%
    # NEW: this is optional but changes how the graph appears on click
    # more layout stuff: https://plotly-r.com/improving-ggplotly.html
    layout(clickmode = 'event+select')
}

# Now we define the graph as a dash component using generated figure
graph <- dccGraph(
  id = 'gap-graph',
  figure=make_graph() # gets initial data using argument defaults
)

# NEW: make a second graph with one country
make_country_graph <- function(years=c(1952, 2007), 
                       country_select="Canada",
                       yaxis="gdpPercap"){
  
  # gets the label matching the column value
  y_label <- yaxisKey$label[yaxisKey$value==yaxis]
  
  #filter our data based on the year/continent selections
  data <- gapminder %>%
    filter(year >= years[1] & year <= years[2]) %>%
    filter(country == country_select)
  
  # make the plot!
  # on converting yaxis string to col reference (quosure) by `!!sym()`
  # see: https://github.com/r-lib/rlang/issues/116
  p <- ggplot(data, aes(x=year, y=!!sym(yaxis), colour=continent)) +
    geom_point() +
    scale_color_manual(name="Continent", values=continent_colors) +
    scale_x_continuous(breaks = unique(data$year))+
    xlab("Year") +
    ylab(y_label) +
    ggtitle(paste0("Change in ", y_label, " Over Time: ", 
                   country_select)) +
    theme_bw()
  
  ggplotly(p)
}

# Now we define the graph as a dash component using generated figure
country_graph <- dccGraph(
  id = 'country-graph',
  figure=make_country_graph() # gets initial data using defaults
)

# Use another function to get filtered data for our table
make_table <- function(years=c(1952, 2007), 
                       continents=all_continents){
  
  gapminder %>%
    filter(year >= years[1] & year <= years[2]) %>%
    filter(continent %in% continents) %>%
    df_to_list()
  
}

# Table that can be sorted by column
table <- dashDataTable(
  id = "gap-table",
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
  data = make_table(), #this gets initial data using argument defaults
  sort_action="native"
)


# Create app layout -------------------------------------------------------


app$layout(
  htmlDiv(
    list(
      htmlH1('Gapminder Dash Demo'),
      htmlH2('Looking at country data interactively'),
      #selection components
      htmlLabel('Select a year range:'),
      yearSlider,
      htmlIframe(height=15, width=10, style=list(borderWidth = 0)), #space
      htmlLabel('Select continents:'),
      continentDropdown,
      htmlLabel('Select y-axis metric:'),
      yaxisDropdown,
      #graphs and table
      graph,
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      country_graph, # NEW
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      htmlLabel('Try sorting by table columns!'),
      table,
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      dccMarkdown("[Data Source](https://cran.r-project.org/web/packages/gapminder/README.html)")
    )
    
  )
)


# Adding callbacks for interactivity --------------------------------------


# We need separate callbacks to update graph and table
# BUT can use multiple inputs for each!
app$callback(
  #update figure of gap-graph
  output=list(id='gap-graph', property='figure'),
  #based on values of year, continent, y-axis components
  params=list(input(id='year', property='value'),
              input(id='continent', property='value'),
              input(id='y-axis', property='value')),
  #this translates your list of params into function arguments
  function(year_value, continent_value, yaxis_value) {
    make_graph(year_value, continent_value, yaxis_value)
  })

# NEW: updates our second graph using linked interactivity
app$callback(output = list(id = 'country-graph', property = 'figure'),
            params = list(input(id='year', property='value'),
                          input(id='y-axis', property='value'),
                          # Here's where we check for graph interactions!
                          input(id='gap-graph', property='clickData')),
            function(year_value, yaxis_value, clickData) {
              # clickData contains $x, $y and $customdata
              # you can't access these by gapminder column name!
              country_name = clickData$points[[1]]$customdata
              make_country_graph(year_value, country_name, yaxis_value)
            })

# Note: you could add filtering by clicked country to this, but it 
# wouldn't let you go back to all countries unless you add another 
# interactive element such as a reset button.
app$callback(
  #update data of gap-table
  output=list(id='gap-table', property='data'),
  params=list(input(id='year', property='value'),
              input(id='continent', property='value')),
  function(year_value, continent_value) {
    make_table(year_value, continent_value, country_name)
  })

app$run_server()