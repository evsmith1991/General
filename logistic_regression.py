#Best for cases when your main correlate metric is binary

pip install pandas statsmodels
import pandas as pd

df = datasets["Raw for Python"] #import data, might also use format df = pd.read_csv('path_to_your_file.csv')

import statsmodels.api as sm

# Set the independent variables (predictors) and the dependent variable
X = df[['content_views', 'app_opens', 'email_opens', 'email_sends', 'strategies_invested']]
y = df['day_28_retention']

# Add a constant (intercept) to the predictors
X = sm.add_constant(X)

# Run logistic regression
model = sm.Logit(y, X).fit()
print(model.summary())

#This summary will provide various pieces of information:

# coef: Estimated coefficient for each predictor variable. For logistic regression, the coefficients represent the log odds. If you exponentiate these coefficients, you get the odds ratios.
# z: z-statistic value. This is a measure of how statistically significant the coefficient is.
# P>|z|: P-value. A smaller P-value (typically < 0.05) suggests that the predictor is statistically significant.
# Pseudo R-squ.: A measure of how well the model fits the data. Unlike linear regression's R-squared, the values here are generally much lower.

odds_ratios = np.exp(model.params)
print(odds_ratios)

# odds ratios give you a sense of the change in odds of the outcome (being retained on day 28) for a one-unit change in the predictor. An odds ratio of 1 suggests no effect, greater than 1 suggests an increase in odds, and less than 1 suggests a decrease in odds
