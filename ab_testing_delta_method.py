df = datasets["Experiment Assignment Data"]
print(df.head(5))

#Sample Script: using the Delta Method -- 
  
import pandas as pd
import numpy as np
from random import randint
from scipy import stats 
from prettytable import PrettyTable

# #dummy variables
# click_control = [randint(0,20) for i in range(10000)]
# view_control = [randint(1,60) for i in range(10000)]
# view_control2 = [1 for i in range(10000)]  # Hack for getting non-ratio metrics. 

# click_treatment = [randint(0,21) for i in range(1000)]
# view_treatment = [randint(1,60) for i in range(1000)]
# view_treatment2 = [1 for i in range(1000)]  # Hack for getting non-ratio metrics. 

# control = pd.DataFrame({'click':click_control,'view':view_control2})
# treatment = pd.DataFrame({'click':click_treatment,'view':view_treatment2})

def gen_dataset_metric(df, treatment, control, metric_num, metric_den='dummy'):
  df.copy(deep=True)
  """
  num = Numerator
  den = Denominator
  """
  num_treatment = list(df[df['variant'] == treatment][metric_num]) #[randint(0,21) for i in range(1000)]
  num_control = list(df[df['variant'] == control][metric_num])  #[randint(0,20) for i in range(10000)]
  if metric_den == 'dummy':
    den_treatment = [1 for i in range(len(num_treatment))]
    den_control = [1 for i in range(len(num_control))]
  else:
    num_treatment = list(df[df['variant'] == treatment][metric_den])
    num_control = list(df[df['variant'] == control][metric_den])
    
  control = pd.DataFrame({metric_num:num_control, metric_den:den_control})
  treatment = pd.DataFrame({metric_num:num_treatment, metric_den:den_treatment})

  return(treatment, control)


#variance estimation of metrics ratio
def var_ratio(x,y): #x/y
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    var_x = np.var(x, ddof=1)
    var_y = np.var(y, ddof=1)
    cov_xy = np.cov(x, y, ddof=1)[0][1]
    #print(cov_xy) -- used to ensure dummy variable produces 0 for Covariance. 
    result = (var_x/mean_x**2 + var_y/mean_y**2 - 2*cov_xy/(mean_x*mean_y))*(mean_x*mean_x)/(mean_y*mean_y*len(x))
    return result
    
#ttest calculation 
def ttest(mean_control,mean_treatment,var_control,var_treatment):
    diff = mean_treatment - mean_control
    var = var_control+var_treatment
    stde = 1.96*np.sqrt(var)
    lower = diff - stde 
    upper = diff + stde
    z = diff/np.sqrt(var)
    p_val = stats.norm.sf(abs(z))*2

    result = {'mean_control':mean_control,
             'mean_experiment':mean_treatment,
             'var_control':var_control,
             'var_experiment':var_treatment,
             'difference':diff,
             'lower_bound':lower,
             'upper_bound':upper,
             'p-value':p_val}
    return pd.DataFrame(result,index=[0])


def eval_metric(treatment, control, metric_num, metric_den='dummy'):
  var_control = var_ratio(control[metric_num],control[metric_den])
  var_treatment = var_ratio(treatment[metric_num],treatment[metric_den])
  mean_control = control[metric_num].sum()/control[metric_den].sum()
  mean_treatment = treatment[metric_num].sum()/treatment[metric_den].sum()
  n_control = len(control[metric_num])
  n_treatment = len(treatment[metric_num])
  
  # print(ttest(mean_control,mean_treatment,var_control,var_treatment))
  # print()
  
  # Try other option for pct lifts. 
  percent_lift = mean_treatment / mean_control - 1
  weighted_abs_diff = (mean_treatment - mean_control) * (n_treatment + n_control / 2)
  var_percent = (mean_treatment / mean_control) ** 2 * (var_treatment / mean_treatment ** 2 + var_control / mean_control ** 2)
  t_stat = percent_lift / np.sqrt(var_percent) 
  p_value = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))
  conf_int_95 = 1.96 * np.sqrt(var_percent)
  conf_int_99 = 2.576 * np.sqrt(var_percent)
  
  # print('Summarized Stats')
  # print('percent_lift = {0}'.format(percent_lift)) 
  # print('var_percent = {0}'.format(var_percent))
  # print('t_stat = {0}'.format(t_stat))
  # print('p_value = {0}'.format(p_value))
  # print('conf_int_95 = {0}'.format(conf_int_95))
  # print('conf_int_99 = {0}'.format(conf_int_99))
  
  print('Stats for metric: {0}'.format(metric_num))
  print('Treatment Mean per user: {0}'.format(round(mean_treatment,4)))
  print('Treatment Variance per user: {0}'.format(round(var_treatment,4)))
  print('Treatment Samples: {0}'.format(n_treatment))
  print('Control Mean per user: {0}'.format(round(mean_control,4)))
  print('Control Var per user: {0}'.format(round(var_control,4)))
  print('Control Samples: {0}'.format(n_control))
  print('{lft}% +/- {ci95}%, p-value of {pval}\n'.format(
    lft=round(100 * percent_lift,2),
    ci95=round(100 * conf_int_95, 2),
    pval=round(p_value, 4)
  ))
  
  return(percent_lift, var_percent, t_stat, p_value, conf_int_95, conf_int_99, weighted_abs_diff)
  
# var_control = var_ratio(control['click'],control['view'])
# var_treatment = var_ratio(treatment['click'],treatment['view'])
# mean_control = control['click'].sum()/control['view'].sum()
# mean_treatment = treatment['click'].sum()/treatment['view'].sum()

# print(ttest(mean_control,mean_treatment,var_control,var_treatment))
# print()


# Change this to get the new metrics in the value. 
metric_list = ['net_transfers',
'net_deposits',
'net_withdrawals',
'num_transfers',
'users_made_transfer',
'num_deposits',
'users_made_deposit',
'num_withdrawals',
'users_made_withdrawal',
'num_ark_deposits',
'users_made_ark_deposit',
'ark_net_transfers',
'app_user_days',
'app_visits',
'carlyle_net_transfers',
'carlyle_deposits',
'users_made_carlyle_deposit',
'cash_net_transfers',
'cash_deposits',
'users_made_cash_deposit',
'flagship_net_transfers',
'flagship_deposits',
'users_made_flagship_deposit',
'passive_net_transfers',
'passive_deposits',
'users_made_passive_deposit',
'offshore_net_transfers',
'offshore_deposits',
'users_made_offshore_deposit',
'crypto_net_transfers',
'crypto_deposits',
'users_made_crypto_deposit',
'opportunities_net_transfers',
'opportunities_deposits',
'users_made_opportunities_deposit',
'apollo_credit_net_transfers',
'apollo_credit_deposits',
'users_made_apollo_credit_deposit',
'apollo_re_net_transfers',
'apollo_re_deposits',
'users_made_apollo_re_deposit',
'referrals_sent',
'users_sent_referral']


x = PrettyTable()
x.field_names = ["Metric", "Percent Lift", "95% Conf Interval", "P-Value", "Weighted Abs Diff", "Is Stat Sig?"]
for metric in metric_list: 
  df[metric] = df[metric].fillna(0)
  (treatment, control) = gen_dataset_metric(
    df=df, 
    treatment='Cathie Letter', 
    control='No Cathie Letter', 
    metric_num = metric, 
    metric_den = 'dummy'
  )
  
  (percent_lift, var_percent, t_stat, p_value, conf_int_95, conf_int_99, weighted_abs_diff) = eval_metric(treatment=treatment, control=control, metric_num=metric, metric_den='dummy')
  x.add_row([
    metric, 
    '{0}%'.format(round(100 * percent_lift,2)), 
    '{0}%'.format(round(100 * conf_int_95, 2)), 
    round(p_value, 4),
    round(weighted_abs_diff,2),
    'Not Stat-Sig' if p_value > .05 else '**Stat-Sig**'
  ])

x.align = "r"
print(x)
# # Try other option for pct lifts. 
# percent_lift = mean_treatment / mean_control - 1
# var_percent = (mean_treatment / mean_control) ** 2 * (var_treatment / mean_treatment ** 2 + var_control / mean_control ** 2)
# t_stat = percent_lift / np.sqrt(var_percent) 
# p_value = 2 * (1 - stats.norm.cdf(np.abs(t_stat)))
# conf_int_95 = 1.96 * np.sqrt(var_percent)
# conf_int_99 = 2.576 * np.sqrt(var_percent)

# print('Summarized Stats')
# print('percent_lift = {0}'.format(percent_lift)) 
# print('var_percent = {0}'.format(var_percent))
# print('t_stat = {0}'.format(t_stat))
# print('p_value = {0}'.format(p_value))
# print('conf_int_95 = {0}'.format(conf_int_95))
# print('conf_int_99 = {0}'.format(conf_int_99))
