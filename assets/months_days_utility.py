def GetMonth(month)->str:
    if int(month) == 1:
        return "January"
    elif int(month) == 2:
        return "February"
    elif int(month) == 3:
        return "March"
    elif int(month) == 4:
        return "April"
    elif int(month) == 5:
        return "May"
    elif int(month) == 6:
        return "June"
    elif int(month) == 7:
        return "July"
    elif int(month) == 8:
        return "August"
    elif int(month) == 9:
        return "September"
    elif int(month) == 10:
        return "October"
    elif int(month) == 11:
        return "November"
    else:
        return "December"
            
def GetDay(day)->str:
    if day == '01' or day == '21' or day == '31':
        return "st"
    elif day == '02' or day == '22':
        return "nd"
    elif day == '03' or day == '23':
        return "rd"
    else:
        return "th"
            
def RemoveZero(day)->str:
    if int(day[0]) == 0:
        return day[1]
    else:
        return day