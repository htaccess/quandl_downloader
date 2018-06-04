#!/usr/bin/python
import quandl
import datetime
import time
from calendar import monthrange
from dateutil.rrule import rrule, DAILY

""" Downloader for quandl futures data
	so you don't have to fuck with their bullshit coding system """
__author__ = "daanishk"

# CME's month code lookup table
monthCode = {
	1: 'F',
	2: 'G',
	3: 'H',
	4: 'J',
	5: 'K',
	6: 'M',
	7: 'N',
	8: 'Q',
	9: 'U',
	10: 'V',
	11: 'X',
	12: 'Z'
	}


def getCMECode(monthNumber, year, prefix="CME/CD{0}{1}"):
	""" Gives you the formatted CME code for a given month and year """
	""" Example call: getCMECode(6, 2018) """
	try:
		return(prefix.format(monthCode[monthNumber], year))
	except KeyError:
		raise ValueError("Invalid month number {} supplied".format(monthNumber))


#ds = quandl.get('CME/CDM2018', start_date='2017-05-31', end_date='2018-05-31')
class CMESeriesDownloader(object):
	def __init__(self, dsCode, startDate, endDate):
		prefix = "CME/" + dsCode + "{0}{1}"
		sd, ed = [datetime.datetime.strptime(d, "%Y-%m-%d") for d in (startDate, endDate)]
		#get unique months between the two dates (to give to quandl)
		months = set([(int(dt.strftime("%m")), int(dt.strftime("%Y"))) for dt in rrule(DAILY, dtstart=sd, until=ed)])
		withLastDay = [(month, year, monthrange(year, month)[1], getCMECode(month, year, prefix)) for (month, year) in months]
		#generates datetime in CME compliant format
		genDt = lambda year, month, date: "{0}-{1}-{2}".format(year, month, date)
		populatedEntries = [CMEDownloadInstrument(fullCode, genDt(year,month,"01"), genDt(year, month, lastDate)) for (month, year, lastDate, fullCode) in withLastDay]

# Container for the merged dataset itself, need to interpolate the OHLC, but NOT the volume (i think?!)
# This class should be immutable
class CMEDataSeries(object):
	def __init__(self, initialData):
		None

	@staticmethod
	def mergeSeriesRollover(s1, s2, rolloverDays=5):
		None
class CMEDownloadInstrument(object):
	def __init__(self, fullCode, startDate, endDate):
		print("Downloading {0} for ({1}, {2})".format(fullCode, startDate, endDate))
		quandl.get(fullCode, start_date=startDate, end_date=endDate)

# Test Call
CMESeriesDownloader("CD", "2017-05-31", "2018-05-31")
	