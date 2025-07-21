
library(fixest)
library(ggplot2)
library(viridis)
library(patchwork)

df <- read.csv("non_high_income_data.csv")

continuousAidPoisson <- function(data) {
  model <- feglm(
    all_cause_deaths ~ per_capita_spend | location_name,
    offset = ~log(population),
    family = poisson(),
    data = data
  )
  return(model)
}


set.seed(1234)
pValues <- c()
coeffs <- c()
for (i in 1:1000) {
  unique_countries <- unique(df$location_name)
  num_to_drop <- ceiling(0.10 * length(unique_countries))
  countries_to_drop <- sample(unique_countries, num_to_drop, replace = FALSE)
  filtered <- df[!(df$location_name %in% countries_to_drop), ]
  model <- continuousAidPoisson(filtered)
  pValues <- append(pValues, summary(model)$coeftable["per_capita_spend", "Pr(>|z|)"])
  coeffs <- append(coeffs, model$coeftable$Estimate)
}

hist_coeff <- ggplot(data.frame(x = coeffs), aes(x)) +
  geom_histogram(bins = 30, fill = viridis(1, begin = 0.2), color = "white", alpha = 0.9) +
  geom_vline(xintercept = -0.00456, linetype = "dashed", color = "red", linewidth = 1) +
  labs(
    title = "per_capita_spend_coefficients",
    x = "Coefficient Estimate",
    y = "Count"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 16),
    axis.title = element_text(size = 13)
  )

hist_pval <- ggplot(data.frame(x = pValues), aes(x)) +
  geom_histogram(bins = 30, fill = viridis(1, begin = 0.6), color = "white", alpha = 0.9) +
  geom_vline(xintercept = 0.026981, linetype = "dashed", color = "red", linewidth = 1) +
  labs(
    title = "per_capita_spend_pvalues",
    x = "P-Value",
    y = "Count"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 16),
    axis.title = element_text(size = 13)
  )

print(hist_coeff + hist_pval)

