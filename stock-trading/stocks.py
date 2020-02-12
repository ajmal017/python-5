from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import seaborn as sns
from pprint import pprint

api_key = 'DHDHIT86W5FPL4T3'
ts = TimeSeries(key=api_key, indexing_type='date',)

# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL')

pprint(pd.DataFrame(data).transpose())