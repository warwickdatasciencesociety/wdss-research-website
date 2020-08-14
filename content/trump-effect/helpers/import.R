import_general <- function(path) {
  # Source: https://github.com/evangambit/JsonOfCounties
  fromJSON(path) %>%
    map_dfr(~tibble(data = .), .id = 'state') %>%
    mutate(county = names(data)) %>%
    select(state, county, data) %>%
    mutate(data_df = unnest_data(data)) %>%
    select(-data) %>%
    unnest(data_df) %>%
    select(state, county, starts_with('age_demographics'),
           starts_with('race_demographics'), unemployment_rate, employed,
           avg_income, starts_with('elections'), population
    )
}

unnest_data <- Vectorize(function(data_list) {
  data_list %>%
    unlist() %>%
    tibble(key = names(.), value = .) %>%
    spread(key, value, convert = TRUE)
})

import_economy <- function(path) {
  # Source: ?
  read_csv(path, col_types = cols(
    State = col_character(),
    County = col_character()
  )) %>%
  select(State, County, Poverty, Professional:Production)
}

import_education <- function(path) {
  # Source: ?
  read_csv(path, na = c('', 'NA'), col_types = cols(
    area_name = col_character(),
    state_abbreviation = col_character()
  )) %>%
    select(state_abbreviation, area_name, fips,
           popsqmile, `HighSchool grad`, Bachelor)
}

import_religion <- function(path) {
  # Source: ?
  read_csv(path, col_types = cols(
    STNAME = col_character(),
    CNTYNAME = col_character(),
    FIPS = col_skip(),
    STCODE = col_skip(),
    STABBR = col_skip(),
    CNTYCODE = col_skip(),
    POP2010 = col_skip(),
    .default = col_double()
  )) %>%
    select(ends_with('RATE'), -TOTRATE, STNAME, CNTYNAME)
}
