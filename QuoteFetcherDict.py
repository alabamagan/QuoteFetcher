GOOGLE_FINANCE_DICT = {
    'Symbols': ['HKG:0005', 'HKG:0136'],
    'FieldsMapper': {
        'lt': "LastTradingTime",
        'l': "LastTradingPrice",
    },
    'TimeKey': "lt_dts",
    'TimeString': "%Y-%m-%dT%H:%M:%SZ"
}

YAHOO_FINANCE_DICT = {
    'Symbols': ['0005.HK', '0136.HK'],
    'FieldsMapper': {
        'LastTradeTime': 'LastTradingTime',
        'LastTradePriceOnly': 'LastTradingPrice',
        'Volume': 'Volume'
    },
    'TimeKey': 'LastTradeDateTimeUTC',
    'TimeString': '%Y-%m-%d %H:%M:%S %Z%z'
}