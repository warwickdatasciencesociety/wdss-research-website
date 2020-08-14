clean_general <- function(general) {
  # Change incorrect numbers of votes
  general$elections.2008.total[1346] <- 16323
  general$elections.2008.dem[727] <- 12368
  general$elections.2008.total[727] <- 12368 + 17019 + 545
  
  # Remove counties with the number of votes missing
  general %<>% filter(!is.na(employed), state != 'Alaska') %>%
    select(-employed)
  
  # Change column names to more workable ones
  general %<>%
    # Age variables
    rename_all(~str_replace(., r'{.*\.(\d+)-(\d+)}', r'{\1to\2}')) %>%
    rename(`85+` = `age_demographics.85+`) %>%
    # Race variables
    rename_all(~str_remove(., 'race_demographics.')) %>%
    rename(
      AsianF = asian_alone_female,
      AsianM = asian_alone_male,
      BlackF = black_alone_female,
      BlackM = black_alone_male,
      HispanicF = hispanic_female,
      HispanicM = hispanic_male,
      WhiteF = non_hispanic_white_alone_female,
      WhiteM = non_hispanic_white_alone_male
    ) %>%
    # Employment
    rename(UnemploymentRate = unemployment_rate)
  
  # Add variables of interest
  general %>%
    mutate(
      # Proportional votes
      gop08 = elections.2008.gop / elections.2008.total,
      gop12 = elections.2012.gop / elections.2012.total,
      gop16 = elections.2016.gop / elections.2016.total,
      dem08 = elections.2008.dem / elections.2008.total,
      dem12 = elections.2012.dem / elections.2012.total,
      dem16 = elections.2016.dem / elections.2016.total,
      # Differences with 2016
      diff0816 = gop16 - gop08,
      diff1216 = gop16 - gop12,
      # Logarithm of income
      IncomeLog = log(avg_income)
    ) %>%
    select(-starts_with('elections'), -avg_income)
}

clean_economy <- function(poverty) {
  poverty %>%
    mutate_at(vars(County), tolower) %>%
    mutate(County = replace(County, str_detect(State, 'do.a ana county'), 
                            'doña ana county'))
}

clean_education <- function(education) {
  education %>%
    mutate_at(vars(area_name), tolower) %>%
    # Data includes national and state level observations. We remove these
    # by filtering for observations that have a corresponding state
    filter(!is.na(state_abbreviation)) %>%
    mutate(state = mapvalues(state_abbreviation, state.abb, state.name)) %>%
    select(-state_abbreviation, `High School` = `HighSchool grad`)
}

clean_religion <- function(religion) {
  religion %>%
    mutate_at(vars(CNTYNAME), tolower) %>%
    mutate_at(vars(ends_with('RATE')), ~replace_na(., 0)) %>%
    # Only include religions with mean rate of 1% or higher
    gather(key = 'religion', value = 'rate', ends_with('RATE')) %>%
    group_by(religion) %>%
    filter(mean(rate) > 10) %>%
    ungroup() %>%
    spread(religion, rate) %>%
    # Combine similar religions
    transmute(
      state = STNAME, county = CNTYNAME,
      Mainline = MPRTRATE + LCMSRATE + ELCARATE + UMCRATE,
      Evangelical = EVANRATE + SBCRATE + AGRATE,
      Catholic = CATHRATE + CTHRATE,
      `Black Prot` = BPRTRATE
    )
}
