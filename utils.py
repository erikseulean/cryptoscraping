from datetime import timedelta

def addPeriods(inputDate, numPeriods, periodType):
    numDays = 0
    numWeeks = 0
    period = {
        'd': 1,
        'm': 30,
        'y': 52,
        'w': 1
    }

    return inputDate + timedelta(
        days = numPeriods * period[periodType],
        weeks = numPeriods * period[periodType])

def dateRange(startDate, endDate, frequency, periodType):
    dates = []
    date = startDate
    
    while date <= endDate:
        dates.append(date)
        date = addPeriods(date, frequency, periodType)
    
    if endDate not in dates:
        dates.append(endDate)

    return dates
