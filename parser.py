import schedule
import sqlite3
import time
import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver import Opera
#------------------------------------------------------------------#
def get_diff():
    today = date.today()
    global d1
    d1 = today.strftime("%d/%m/%Y")
    utc = datetime.datetime.utcnow()
    local = datetime.datetime.now()
    diff = local.hour - utc.hour
    us_time = datetime.time(5, 55)
    ul_time = datetime.time(7)
    global ls_time
    ls_time = datetime.time(us_time.hour + diff, 55).strftime("%H:%M")
    global ll_time
    ll_time = datetime.time(ul_time.hour + diff).strftime("%H:%M")
def parse():
    url = 'https://www.investing.com/currencies/eur-usd-technical'
    browser = webdriver.Opera()
    browser.get(url)
    time.sleep(10)
    global houravg, minavg, priceatsix
    houravg = browser.find_element_by_xpath('/html/body/div[5]/section/div[10]/div[4]/table/tbody/tr[5]/td[3]/span').text
    time.sleep(10)
    browser.find_element_by_xpath('//*[@id="timePeriodsWidget"]/li[2]/a').click()
    time.sleep(10)
    minavg = browser.find_element_by_xpath('/html/body/div[5]/section/div[10]/div[4]/table/tbody/tr[5]/td[3]/span').text
    priceatsix = browser.find_element_by_xpath('/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]').text
    browser.quit()
def firsttrade():
    parse()
    global conclusion
    if houravg != minavg:
        conclusion = houravg
    else:
        conclusion = "Not today"
    conn = sqlite3.connect("trades.db")
    db = conn.cursor() 
    db.execute("INSERT INTO trades ('dateoftrade', 'hour_conclusion', 'min_conclusion', 'global_conclusion', 'priceatsix') VALUES ( ?, ?, ?, ?, ?)", (d1, houravg, minavg, conclusion, priceatsix))
    conn.commit()
def secondtrade():
    url = 'https://www.investing.com/currencies/eur-usd-technical'
    browser = webdriver.Opera()
    browser.get(url)
    time.sleep(10)
    priceatseven = browser.find_element_by_xpath('/html/body/div[5]/section/div[4]/div[1]/div[1]/div[2]/div[1]/span[1]').text
    browser.quit()
    global will_repeat
    if(((priceatseven < priceatsix) and conclusion == "Sell") or ((priceatseven > priceatsix) and conclusion == "Buy")):
        will_repeat = False
    elif (conclusion == "Not today"):
        will_repeat = False
    else:
        will_repeat = True
    conn = sqlite3.connect("trades.db")
    db = conn.cursor()
    db.execute("UPDATE trades SET priceatseven = ?, will_repeat = ? WHERE dateoftrade = ?", (priceatseven, will_repeat, d1))
    conn.commit()
#------------------------------------------------------------------#
get_diff()
firsttrade()
secondtrade()
#schedule.every().day.at(ls_time).do(firsttrade)
#schedule.every().day.at(ll_time).do(secondtrade)
#------------------------------------------------------------------#
while True:
    schedule.run_pending()
    time.sleep(1)
