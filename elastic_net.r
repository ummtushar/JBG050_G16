
# Installing Packages
library("dplyr")
library("glmnet")
library("ggplot2")
library("caret")


data <- read.csv("no_multicollinearity.csv")

# X and Y datasets  # nolint
#nearZeroVar(data)
data <- data[,-nearZeroVar(data)]

X <- data %>%  
     select(Y) %>%  
     scale(center = TRUE, scale = FALSE) %>%  
     as.matrix() 
Y <- data %>%  
    select(-Y) %>%  
    as.matrix() 
  
# Model Building : Elastic Net Regression 
control <- trainControl(method = "repeatedcv", 
                              number = 5, 
                              repeats = 5, 
                              search = "random", 
                              verboseIter = TRUE) 
  
# Training ELastic Net Regression model 
elastic_model <- train(Y ~ ., 
                           data = cbind(X, Y), 
                           method = "glmnet", 
                           preProcess = c("center", "scale"), 
                           tuneLength = 25, 
                           trControl = control) 
  
#elastic_model 
summary(elastic_model)
  
# # Model Prediction 
# x_hat_pre <- predict(elastic_model, Y) 
# x_hat_pre 
  
# # Multiple R-squared 
# rsq <- cor(X, x_hat_pre)^2 
# rsq 
  
# # Plot 
# plot(elastic_model, main = "Elastic Net Regression") 

# # Feature Selection
# selected_featuresid <- predict(elastic_model$finalModel, type = "nonzero")
# selected_features <- colnames(X)[[selected_featuresid]]
# selected_features