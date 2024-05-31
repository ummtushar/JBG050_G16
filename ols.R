data <- read.csv("data/no_multicollinearity.csv")

# perform a lasso regression
m1 <- lm(data = data, formula = Y ~ .)
summary(m1)
