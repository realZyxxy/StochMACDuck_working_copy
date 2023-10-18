import yfinance as yf
# see https://pypi.org/project/yfinance/

def _stock_query(stock_ticker, first_date, last_date):
  # Download the historical data for the asset
  stock = yf.Ticker(stock_ticker)

  info = {key : stock.info.get(key, None) for key in ('longName', 'country', 'exchange', 'quoteType')}
  
  result = stock.history(start=first_date, end=last_date)
  #dates = [d.date() for d in data.axes[0].to_pydatetime().tolist()]
  
  result.rename({s : s.lower() for s in ['Open', 'High', 'Low', 'Close', 'Volume']}, axis=1, inplace=True)
  index = result.index
  index = index.tz_localize(tz=None)
  result.index = index
  #history_indicators[ticker].index = history_indicators[ticker].index.tz_localize(None)
  result['Data Date'] = result.index.strftime('%Y-%m-%d')
  # https://stackoverflow.com/questions/61104362/how-to-get-actual-stock-prices-with-yfinance
  # current_price = stock.info.get('regularMarketPrice', stock.info.get('currentPrice', result['close'].iloc[-1]))
  #print(result.tail(1))
  #print('current prices for', stock_ticker, current_price, result['close'].iloc[-1], (current_price / result['close'].iloc[-1] - 1))
  extrapolate = max([abs( result[label].iloc[-1]) for label in ["open", "high", "low"]]) < 1E-8
  info['extrapolated'] = extrapolate
  if extrapolate:
    result['open'].iloc[-1] = result['close'].iloc[-2]
    result['low' ].iloc[-1] = result['low'  ].iloc[-2]
    result['high'].iloc[-1] = result['high' ].iloc[-2]
    #result.drop(result.tail(1).index,inplace=True)
    #print('DROPS')
  
  return info, result

def get_longname(stock_ticker):
  return get_info(stock_ticker, what_info='longName')

def get_info(stock_ticker, what_info):
  ticker_obj = yf.Ticker(stock_ticker)
  # if ticker_obj.info fails, run the following line in Shell
  # pip install --upgrade yfinance 
  if isinstance(what_info, str):
    result = ticker_obj.info[what_info]
  else:
    result = [ticker_obj.info[w] for w in what_info] 
  return result

# get_info(stock_ticker, ('longName'))
  