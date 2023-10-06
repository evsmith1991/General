# best for when your main correlate metric is continuous

pip install pandas statsmodels
import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv('path_to_your_file.csv')

import statsmodels.api as sm

# Set the independent variables (predictors) and the dependent variable
X = df[['content_views', 'app_opens', 'email_opens', 'email_sends', 'strategies_invested']]
y = df['day_28_retention']

# Add a constant (intercept) to the predictors
X = sm.add_constant(X)

# Run regression
model = sm.OLS(y, X).fit()

print(model.summary())

#This summary will provide you with a lot of information:

# coef: Estimated coefficient for each predictor variable, which represents the change in the dependent variable for a one-unit change in the predictor.
# t: t-statistic value. This is a measure of how statistically significant the coefficient is.
# P>|t|: P-value. A lower P-value indicates that you can reject the null hypothesis. Common threshold values are 0.01, 0.05, or 0.10, but it's subjective and based on the problem domain.
# R-squared: Represents how well the model fits the data. A value closer to 1 means a better fit.
# From the results:

#Check the P-values for each predictor. A smaller P-value (typically < 0.05) suggests that the predictor is statistically significant.

#Look at the coefficients. A positive coefficient suggests a positive correlation with the dependent variable, and vice versa.

