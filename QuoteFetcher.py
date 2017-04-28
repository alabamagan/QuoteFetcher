import os
import requests
import datetime
import time
import pytz
import logging
import QuoteFetcherDict
import yahoo_finance

if not os.path.isdir("./Logs"):
    os.mkdir("./Logs")
logging.basicConfig(
    filename='./Logs/QuoteFetcher_%s.txt' % (datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d"))
    , level=logging.DEBUG, format='[%(process)d: %(levelname)s] - %(asctime)s %(message)s')

def YahooGetQuote(yahoodict):
    outdict = {}
    for symbol in yahoodict['symbols']:
        stock = yahoo_finance.Share(symbol)
        fieldMapper = yahoodict['FieldMapper']

        # Check if the trading time difference is arround 15 minutes
        quoteTime = stock.data_set[yahoodict['TimeKey']]
        quoteTime = datetime.datetime.strptime(quoteTime, yahoodict['TimeString'])
        quoteTime = quoteTime.astimezone(pytz.timezone("Asia/Hong_Kong"))
        localtime = datetime.datetime.now(pytz.timezone("Asia/Hong_Kong"))
        dt = quoteTime - localtime
        for key in fieldMapper:
            val = stock.data_set[key]
            outkey = fieldMapper[key]

            if (outkey == 'LastTradingPrice' or outkey == 'Volume'):
                outdict[outkey] = float(val)



def GoogleGetQuote():
    pass



def FindClosestTradingTime():
    # Check if timezone correct

    localtime = datetime.datetime.now(pytz.timezone("Asia/Hong_Kong"))
    weekday = localtime.weekday()


    starttime = datetime.datetime.now(pytz.timezone("Asia/Hong_Kong")).replace(hour=9, minute=30, second=0, microsecond=0)
    endtime = datetime.datetime.now(pytz.timezone("Asia/Hong_Kong")).replace(hour=16, minute=25, second=0, microsecond=0)

    offset = 0
    nextworkingday = datetime.datetime.now(pytz.timezone("Asia/Hong_Kong"))
    nextworkingday = nextworkingday.replace(hour=9, minute=30, second=0, microsecond=0)
    if (weekday >= 4): # if Friday, Sat or Sun
        offset = (-weekday)%7
    else:
        offset = 1

    dend = localtime - endtime
    dstart = localtime - starttime
    if(dend.total_seconds() < 0 and dstart.total_seconds() >= 0):
        return localtime # Within trading period
    else:
        nextworkingday = nextworkingday.replace(day=localtime.day + offset, minute=30, hour=9, second=0)
        return nextworkingday # Not within trading period


def main():
    while(True):
        try:
            # Check if within trading time
            ct = FindClosestTradingTime()
            dt = ct - datetime.datetime.now(pytz.timezone("Asia/Hong_Kong"))

            if (dt <= 0.01):
                pass
            else:
                logging.info("Not within trading period, sleeping until %s"%ct.ctime())
                time.sleep(abs(dt.total_seconds()))
            time.sleep(1)
            pass
        except():
            logging.critical("Unknown error occured, please refer to the log for more information.")
            time.sleep(1)
            continue




if __name__ == '__main__':
    # Creates output directories
    if not os.path.isdir("./Output"):
        logging.info("Generating Output directory...")
        try:
            os.mkdir("./Output")
        except():
            logging.error("Generating Output folder failed!")

    logging.info("Start quote fetcher...")
    main()
