import requests
import time
import json
import winsound
from browser import headers

link="https://www.cvs.com/immunizations/covid-19-vaccine/immunizations/covid-19-vaccine.vaccine-status.TX.json?vaccineinfo"
filename = 'cvs.csv'

wait_time = input("Wait time between pings (secs):")
alert_enable = input("Play alert if available (y/n) :")
if alert_enable == 'y':
    alert_city = input("City for alert (ALL CAPS) :")

while True:
    source=requests.get(link,headers=headers).text
    jcode = json.loads(source)
    
    #tx is an array with city and status information in JSON 'TX'
    tx = jcode['responsePayloadData']['data']['TX']
    
    for city_status in tx:
        time_status = jcode['responsePayloadData']['currentTime'] + ',' + city_status['status'] + ',' + city_status['city']
        print(time_status)

        #Beep if status is Available
        if city_status['status'] == 'Available' and alert_enable == 'y' and city_status['city'] == alert_city: 
            duration = 1000  # milliseconds
            freq = 1000      # Hz
            winsound.Beep(freq, duration)

        #Write results to file    
        with open(filename, "a", encoding="utf-8") as f:
            f.write(time_status)
            f.write('\n')
            
    time.sleep(int(wait_time)) #Wait for entered seconds
    f.close()
