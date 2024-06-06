# # Load necessary libraries
# library(DAAG)

# # Read the data
# data <- read.csv("data/combined_data(in).csv")

# # Fit the model
# m1 <- lm(data = data, formula = Y ~ .)

# # Perform 5-fold cross-validation
# cv_results <- cv.lm(data, m1, m=5)

# # Print summary of the cross-validation results
# print(summary(cv_results))

# Load necessary libraries
library(DAAG)
library(dplyr)

# Read the data
data <- read.csv("data/combined_data(in).csv")

# Fit the model
m1 <- lm(data = data, formula = Y ~ .)

# Perform 5-fold cross-validation manually to extract coefficients
set.seed(123) # For reproducibility
folds <- sample(1:5, size = nrow(data), replace = TRUE)
coefficients_list <- list()

for (i in 1:5) {
  train_data <- data[folds != i, ]
  test_data <- data[folds == i, ]
  
  model <- lm(data = train_data, formula = Y ~ .)
  coefficients_list[[i]] <- coef(model)
}

# Ensure all coefficient vectors have the same length and names as the original model
for (i in 1:5) {
  missing_vars <- setdiff(names(coef(m1)), names(coefficients_list[[i]]))
  coefficients_list[[i]] <- c(coefficients_list[[i]], setNames(rep(NA, length(missing_vars)), missing_vars))
  coefficients_list[[i]] <- coefficients_list[[i]][names(coef(m1))]
}

# Convert list of coefficients to a data frame
coefficients_df <- do.call(rbind, coefficients_list)

# Calculate the average of the coefficients
average_coefficients <- colMeans(coefficients_df, na.rm = TRUE)

# Extract p-values from the original model summary
model_summary <- summary(m1)
p_values <- coef(model_summary)[, "Pr(>|t|)"]

# Create a data frame with average coefficients and p-values
# results <- data.frame(
#   Variable = names(average_coefficients),
#   Average_Coefficient = average_coefficients,
#   P_Value = p_values[names(average_coefficients)]
# )
results <- data.frame(
  Average_Coefficient = average_coefficients,
  P_Value = p_values[names(average_coefficients)]
)

filtered_results <- results %>% filter(P_Value < 0.05)
# Print the results
print("Average Coefficients and P-Values:")
print(filtered_results)
