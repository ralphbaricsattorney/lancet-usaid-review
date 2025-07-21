library(fixest)

df <- read.csv("data/flattened_data/non_high_income_data.csv")


continuousAidPoisson <- function(data) {
  model <- feglm(
    all_cause_deaths ~ per_capita_spend | location_name,
    offset = ~log(population),
    family = poisson(),
    data = data
  )
  return(model)
}

binnedByYearAidPoisson <- function(data) {
  model <- feglm(
    all_cause_deaths ~ is_q2_by_year + is_q3_by_year + is_q4_by_year | location_name,
    offset = ~log(population),
    family = poisson(),
    data = data
  )
  return(model)
}

binnedOverallAidPoisson <- function(data) {
  model <- feglm(
    all_cause_deaths ~ is_q2_overall + is_q3_overall + is_q4_overall | location_name,
    offset = ~log(population),
    family = poisson(),
    data = data
  )
  return(model)
}


continuousAidNB <- function(data) {
  model <- fenegbin(
    all_cause_deaths ~ per_capita_spend | location_name,
    offset = ~log(population),
    data = data
  )
  return(model)
}

binnedOverallAidNB <- function(data) {
  model <- fenegbin(
    all_cause_deaths ~ is_q2_overall + is_q3_overall + is_q4_overall | location_name,
    offset = ~log(population),
    data = data
  )
  return(model)
}


binnedByYearAidNB <- function(data) {
  model <- fenegbin(
    all_cause_deaths ~ is_q2_by_year + is_q3_by_year + is_q4_by_year | location_name,
    offset = ~log(population),
    data = data
  )
  return(model)
}

print(summary(binnedOverallAidPoisson(df)))



