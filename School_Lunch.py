from requests import get
import datetime
from urllib import urlencode

user_agent = {
    "User_Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36"
    }
def encode(month, year):
    """returns a url string with month and year parameters from input, encodes from payload dict."""
    if month < 10:
        if str(month).find('0') == -1:
            month = '0' + str(month)
    year = str(year)
    payload = {
        "view":"print", "month" : month, "year": year, "tmpl":"component", "print":"1", "pop":"1", "layout":"default", "page":"1", "option":"com_lunchmenu", "Itemid":"499"
        }
    url = "http://www.sf.k12.sd.us/index.php?"
    url += urlencode(payload)
    return url

def get_page(url):
    return get(url, headers=user_agent).text

def find_lunch(month, day, year):
    """returns a raw html source code from first to last letter of lunch-menu for the day.
(includes <br />, \n)"""
    date = datetime.date(year, month, day)
    day = date.weekday()
    weekend = (5,6)
    if day in weekend:
        print "Is yo mamma gonna come to school and cook for you?"
        return None
                                                    # just finding different tags step by step.
                                                    # This method won't work if any changes are made to the html code of the secondary lunch menu. :(
    raw_calender = get_page(encode(month, year))
    date_pos = raw_calender.find('>'+str(date.day)+'<')

    day_menu = raw_calender.find('<div class="day-menu">', date_pos)
    br_tag_start = raw_calender.find('<br', day_menu)
    br_tag_end = raw_calender.find('>', br_tag_start)
    end_of_menu = raw_calender.find('</div>', br_tag_end)
    return raw_calender[br_tag_end + 1 : end_of_menu]


def cook_lunch(raw_lunch):
    """return a list, gets rid of '\n' and '<br />' form source string. Converts encoding to 'ascii'."""
    if raw_lunch == None:
        return None
    raw_lunch = raw_lunch.split('<br />')           # split at "line break" tags

    lunch_menu = [i.encode('ascii') for i in raw_lunch]
    cooked_lunch = []

    for i in lunch_menu:
        cooked_lunch.append(i.replace('\n', ''))    # filter 'new-line' characters

    return cooked_lunch

##print encode(9, 2013)
##print ''
##print cook_lunch(find_lunch(9, 6, 2013))

def leap(year):
    if year % 400==0:
        return True
    elif year % 100==0:
        return False
    elif year % 4==0:
        return True
    else:
        return False

# print leap(2013)
def weekdates(month, year):
    assert month <= 12
    assert month >= 1
    month_days = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if leap(year):
        month_days[2] = 29
    week_end = (5, 6)
    week_dates = [i for i in range(1, month_days[month] + 1) if datetime.date(year, month, i).weekday() not in week_end]
    return week_dates

##for i in weekdates(9, 2013):
##    print i

def weekday(month, day, year):
    days_of_wk = {
        0: 'Mon',
        1: 'Tues',
        2: 'Wed',
        3: 'Thurs',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun'
        }
    date = datetime.date(year, month, day)
    return days_of_wk[date.weekday()]

# print weekday(9, 7, 2013)

def lunch_for_month(month, year):
    lunch_index = []
    dates_to_cook = weekdates(month, year)

    for day in dates_to_cook:
        lunch_index.append([day, weekday(month, day, year), cook_lunch(find_lunch(month, day, year))]) # [day, day of week, [Item1, Item2, ...]]
    return lunch_index      #[[day, day of week, [Item1, Item2, ...]], ...]

##for i in lunch_for_month(9, 2013):
##    print "Day", i[0],i[1]
##    for i in i[2]:
##        print i
##    print ''


def lunch_today():
    date = datetime.date.today().isoformat().split('-') # ['YYYY', 'MM', 'DD']

    lunch = cook_lunch(find_lunch(int(date[1]), int(date[2]), int(date[0])))
    return lunch

# print lunch_today()









