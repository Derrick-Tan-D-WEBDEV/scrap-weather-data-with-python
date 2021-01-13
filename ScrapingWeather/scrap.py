from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pprint import pprint
from sys import exit
from datetime import datetime,timedelta,date
import mysql.connector

#Import ASCII Text Library
from termcolor import cprint 
from pyfiglet import figlet_format

mydb = mysql.connector.connect(
    host="sql138.main-hosting.eu",
    user="u874427471_API",
    password="Api123456",
    database="u874427471_API"
)
def check_database(date):
    try: 
        mycursor = mydb.cursor()
        sql = "SELECT * FROM weather WHERE date = %s"
        val = (date,)
        mycursor.execute(sql,val)
        
        myresult = mycursor.fetchone()
        if myresult:
            return True
        else:
            return False

    except Exception as error:
        print(error)

#print nice title
cprint(figlet_format('lets', font='starwars'),'blue', attrs=['blink'])
cprint(figlet_format('scrap', font='starwars'),'blue', attrs=['bold'])

PATH = "D:\Youtube\Python Projects\WebScrapingProjects\ScrapingWeather\chromedriver\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")
driver = webdriver.Chrome(PATH,options=options)

driver.get("https://www.google.com/search?rlz=1C1GCEU_enMY930MY931&ei=a6zQX-m3Dvf6z7sP2M2-gAQ&q=google+weather&oq=google+weather&gs_lcp=CgZwc3ktYWIQAzIHCAAQyQMQQzIKCAAQsQMQgwEQQzIECAAQQzIECAAQQzICCAAyBAgAEEMyAggAMgIIADICCAAyAggAOgcIABBHELADOgcIABCwAxBDOgcIABCxAxBDOgUIABCxAzoICAAQsQMQgwFQtRNYqiJgyiNoA3ACeAGAAZUCiAGKDZIBBTcuNy4xmAEAoAEBqgEHZ3dzLXdperABAMgBCsABAQ&sclient=psy-ab&ved=0ahUKEwipmZ3X3cDtAhV3_XMBHdimD0AQ4dUDCA0&uact=5")

weather_date = date.today()
for n in range(1,9):
    print("Date: " + str(weather_date))
    driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[4]/div/div['+str(n)+']').click()
    
    #full_day (saturday,sunday,etc)
    full_day = driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/span/div[2]').text
    if full_day.find("am") != -1 or full_day.find("pm") != -1:
        full_day = full_day.split(' ')[0]
    print("Day: " + full_day)
    
    #temperature
    temp = driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]/div/div[1]/span[1]').text
    print("Temperature: " + temp)
    
    #humidity
    humid = driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/span').text
    humid = humid.replace("%", "")
    print("Humidity: " + humid)

    #wind
    wind = driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[1]/div/div[2]/div[3]/span/span[1]').text
    wind = wind.replace(" km/h","")
    print("Wind: " + wind)

    #condition 
    cond = driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/span/div[3]/span').text
    print("Weather Condition: "+cond)

    if check_database(weather_date):
        try: 
            mycursor = mydb.cursor()

            sql = "UPDATE weather SET temperature = %s, humidity = %s, wind = %s, weather_cond = %s, full_day = %s WHERE date = %s"
            val = (temp,humid,wind,cond,full_day,weather_date)
            mycursor.execute(sql,val)

            mydb.commit()

        except Exception as error:
            print(error)

    else:
        try: 
            mycursor = mydb.cursor()

            sql = "INSERT INTO weather (date, temperature, humidity, wind, weather_cond,full_day) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (weather_date,temp,humid,wind,cond,full_day)
            mycursor.execute(sql,val)

            mydb.commit()

        except Exception as error:
            print(error)

    weather_date = weather_date + timedelta(days=1)

