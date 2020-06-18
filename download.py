import requests 
import pandas as pd

date1 = '2020-01-02'
date2 = '2020-06-05'


def format_url(startDate, endDate):
    url_base = 'https://spotifycharts.com/viral/es/weekly/'
    startDate = startDate.split(' ')[0]
    endDate = endDate.split(' ')[0]
    url_base += startDate + '--' + endDate + '/download'
    print(url_base)
    return url_base




dates = pd.date_range(date1, date2, freq='W-THU').tolist()

with open('test.csv', 'a') as f:
    for i in range(0, len(dates)):
        if (i < len(dates)):
            url = format_url(str(dates[i]),  str(dates[i]))
            r = requests.get(url)
            csv = r.text
            csv.replace('Position,"Track Name",Artist,URL', '')
            f.write(csv.encode('utf-8'))
