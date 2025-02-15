def convertTime(period):
    if 'day' in period:
        return period[0] + "d"
    elif 'month' in period:
        return period[0] + 'mo'
    elif 'year' in period:
        return period[0] + 'y'
    else:
        return period 