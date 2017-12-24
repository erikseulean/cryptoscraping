import datetime

def addPeriods(inputDate, numPeriods, periodType):
    numDays = 0
    numWeeks = 0
    numYears = 0
    numMonths = 0
    if periodType == "d":
        numDays = numPeriods
    if periodType == "m":
        numDays = 30 * numPeriods
    if periodType == "y":
        numWeeks = 52 * numPeriods
    if periodType == "w":
        numWeeks = numPeriods

    return inputDate + datetime.timedelta(days = numDays, weeks = numWeeks)

def dateRange(startDate, endDate, frequency, periodType):
    dates = []
    date = startDate
    while date <= endDate:
        dates.append(date)
        date = addPeriods(date, frequency, periodType)
    if endDate not in dates:
        dates.append(endDate)

    return dates
