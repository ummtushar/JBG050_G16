
# Load necessary libraries
library(dplyr)

# Step 1: Load the CSV file into a data frame
data <- read.csv("no_multicollinearity.csv")


column_names <- colnames(data)

# Define a function to evaluate model performance
# evaluate_model <- function(model) {
#   # Use adjusted R-squared and coefficient names as criteria for a good model
#   summary_model <- summary(model)
#   p_value <- summary_model$coefficients[length(summary_model$coefficients)-1, "Pr(>|t|)"]
#   coefficient_names <- rownames(summary_model$coefficients)[-1]
#   print(coefficient_names[[1]])
#   return(p_value)
#   # return(list(p_value = p_value, coefficient_names = coefficient_names))
# }

evaluate_model <- function(model) {
  # Use adjusted R-squared and coefficient names as criteria for a good model
  summary_model <- summary(model)
  # Access the p-value of the last coefficient
  p_value <- summary_model$coefficients[nrow(summary_model$coefficients), "Pr(>|t|)"]
  coefficient_names <- rownames(summary_model$coefficients)[nrow(summary_model$coefficients)]
  print(coefficient_names[[length(coefficient_names)]])
  return(p_value)
  # return(list(p_value = p_value, coefficient_names = coefficient_names))
}

# Initialize a list to store good models
good_models <- list()

# Step 3: Iterate over pairs of columns
for (i in 1:(length(column_names) - 1)) {
  for (j in (i + 1):length(column_names)) {
    column1 <- column_names[i]
    column2 <- column_names[j]
    if (column1 == "Y" || column2 == "Y" || column1 == "X" || column2 == "X" ) {
      next
    }
    # Step 4: Fit a linear model with interaction term
    formula <- as.formula(paste("Y ~", column1, "*", column2, "+ ."))
    print(formula)
    model <- lm(formula, data = data)
    # Evaluate the model
    p_val <- evaluate_model(model)
    print(p_val)
    print(summary(model)$adj.r.squared)
    # Define a threshold for a good model (e.g., adjusted R-squared > 0.7)
    if (p_val <= 0.00001 && summary(model)$adj.r.squared > 0.10){
      # Store the model if it meets the criteria
      
      good_models[[paste(column1, column2, p_val, sep = " and ")]] <- model
    }
  }
}

print("Good models:")
#print(summary(good_models[[65]]))

print(names(good_models))


# Optionally, save the good models to a file
#save(good_models, file = "/mnt/data/good_models.RData")
