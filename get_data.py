import requests
import pandas as pd
import datetime
from arguments import parse_args

args = parse_args()

def get_flights_airport_month(airport, month, access_key):
  print(f'Month={month}')
  fdom = '01'
  if month in ['01', '03', '05', '07', '08', '10', '12']:
    ldom = '31'
    if month == '01':
      fdom = '03'  # Getting around API 1 year historical limit
  elif month == '02':
    ldom = '28'
  elif month == '12':
    ldom = str(datetime.datetime.today().day - 4)
  else:
    ldom = '30'
  
  responses = []
  for iata in ['FR', 'LH', 'KL', 'LS', 'BY', 'VS']:
    print(f'airline={iata}')
    response = requests.get(f'https://app.goflightlabs.com/advanced-flights-history?access_key={access_key}&code={airport}&type=departure&date_from=2022-{month}-{fdom}&date_to=2022-{month}-05&airline_iata={iata}')
    if response.json()['success'] == True: responses.append(response)
    response = requests.get(f'https://app.goflightlabs.com/advanced-flights-history?access_key={access_key}&code={airport}&type=departure&date_from=2022-{month}-06&date_to=2022-{month}-10&airline_iata={iata}')
    if response.json()['success'] == True: responses.append(response)
    response = requests.get(f'https://app.goflightlabs.com/advanced-flights-history?access_key={access_key}&code={airport}&type=departure&date_from=2022-{month}-11&date_to=2022-{month}-15&airline_iata={iata}')
    if response.json()['success'] == True: responses.append(response)
    response = requests.get(f'https://app.goflightlabs.com/advanced-flights-history?access_key={access_key}&code={airport}&type=departure&date_from=2022-{month}-16&date_to=2022-{month}-20&airline_iata={iata}')
    if response.json()['success'] == True: responses.append(response)
    if month != '12':
      response = requests.get(f'https://app.goflightlabs.com/advanced-flights-history?access_key={access_key}&code={airport}&type=departure&date_from=2022-{month}-21&date_to=2022-{month}-25&airline_iata={iata}')
      if response.json()['success'] == True: responses.append(response)
      response = requests.get(f'https://app.goflightlabs.com/advanced-flights-history?access_key={access_key}&code={airport}&type=departure&date_from=2022-{month}-26&date_to=2022-{month}-{ldom}&airline_iata={iata}')
      if response.json()['success'] == True: responses.append(response)
    print(response)
    print(response.json())
  
  data_list = []
  for response in responses:
    if '200' in str(response):
      data = pd.json_normalize(response.json(), 'data')
      data_list.append(data)

  try:
    df = pd.concat(data_list)
    return df
  except ValueError as E:
    print(E)


def get_flights_airport(airport_lst, access_key):
  airport_dfs = []
  for airport in airport_lst:
    print(f'Airport={airport}')
    df_months_lst = []
    for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
      df_month = get_flights_airport_month(airport, month, access_key)
      df_months_lst.append(df_month)

    try:
      df_year = pd.concat(df_months_lst)
      airport_dfs.append(df_year)
      df_year.to_csv(f'data/flights_{airport}_2022.csv', index=False)
    except ValueError as E:
      print(E)
  
  df = pd.concat(airport_dfs)
  df_year.to_csv(f'data/flights_2022.csv', index=False)

  return df


if __name__ == __main__:

    airport_lst = ['MAN', 'LPL', 'LGW', 'BHX', 'LHR', 'GLA', 'NCL', 'EDI', 'ABZ', 'BRS',
     'CWL', 'LBA', 'EMA', 'STN', 'LTN', 'BHD', 'NWI', 'EXT', 'BFS', 'SOU', 'DSA', 'BOH',
     'BZZ', 'LCY', 'NQY', 'HUY', 'BLK', 'MME', 'SEN', 'KOI']
    df = get_flights_airport(airport_lst, access_key)