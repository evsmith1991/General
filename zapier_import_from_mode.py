import os
import os.path
import requests
from datetime import datetime
import json
import logging
from requests.auth import HTTPBasicAuth

MODE_BASE_URL = 'https://modeanalytics.com/'
MODE_BASE_URL1 = 'https://modeanalytics.com'
un = '------------'
pw = '----------------------'

def _mode_api_get(endpoint_url):
    """
    Send a GET request to a Mode API endpoint.
    """
    return requests.get(
               endpoint_url,
               auth=('59df028f6e65', 'c2f413ecfd7b2cf5af4ade30')
           ).json()

def get_report_runs(url):
    """
    Retrieve report run metadata.
    """
    report_runs_data = _mode_api_get(url + '/runs')

    # Pagination
    total_pages = report_runs_data['pagination']['total_pages']
    max_pagination_pages = 10

    payload = [report_runs_data]

    while report_runs_data['pagination']['page'] < min(total_pages, max_pagination_pages):
        report_runs_data = _mode_api_get(MODE_BASE_URL + report_runs_data['_links']['next_page']['href'])
        payload.append(report_runs_data)

    report_run_result_endpoint = report_runs_data['_embedded']['report_runs'][0]['_links']['latest_successful_report_run_api_url']['href']
    return get_report_run_result(report_run_result_endpoint)
    #return report_run_result_endpoint
    
def get_report_run_result(report_run_result_endpoint):
  url = '%s%s/results/content.json' % (MODE_BASE_URL1, report_run_result_endpoint)
  #return _mode_api_get(url)
  results = _mode_api_get(url)
  
  return results

query_results = get_report_runs('https://modeanalytics.com/api/titanvest/reports/5df475a7cf20/')

issues = ''
for i in range(len(query_results)):
  if query_results[i]['test_metric_value'] == 1:
    issue = query_results[i]['test_metric']
    if len(issues) > 1:
      issues = issues + ', ' + issue + ' was higher than expected'
    else:
      issues = issue + ' was higher than expected'
  if query_results[i]['test_metric_value'] == -1:
    issue = query_results[i]['test_metric']
    if len(issues) > 1:
      issues = issues + ', ' + issue + ' was lower than expected'
    else:
      issues = issue + ' was lower than expected'
  if query_results[i]['test_metric_value'] == -2:
    issue = query_results[i]['test_metric']
    if len(issues) > 1:
      issues = issues + ', ' + issue + ' went to 0'
    else:
      issues = issue + ' went to 0'

if len(issues) > 1:
  #issues = 'None'
  return {'issues': issues}
#return {'issues': issues}
