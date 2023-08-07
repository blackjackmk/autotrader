import schedule
import sqlite3
import time
import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
#------------------------------------------------------------------#
def get_diff():
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
    get_diff()
    url = 'https://www.investing.com/currencies/eur-usd-technical'
    driver.get(url)
    time.sleep(10)
    global houravg, minavg, priceatsix
    time.sleep(10)#cookie accept
    driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
    houravg = driver.find_element(By.XPATH,'/html/body/div[6]/section/div[10]/div[1]/div[1]/span').text
    time.sleep(10)
    driver.find_element(By.XPATH,'/html/body/div[6]/section/div[8]/ul/li[1]').click()
    time.sleep(10)
    minavg = driver.find_element(By.XPATH,'/html/body/div[6]/section/div[10]/div[1]/div[1]/span').text
    priceatsix = driver.find_element(By.XPATH,'//*[@id="last_last"]').text
def firsttrade():
    parse()
    global conclusion
    #if houravg != minavg
    if houravg == "SELL" and minavg == "BUY":
        conclusion = "Sell"
    elif houravg == "SELL" and minavg == "STRONG BUY":
        conclusion = "Sell"
    elif houravg == "STRONG SELL" and minavg == "BUY":
        conclusion = "Sell"
    elif houravg == "STRONG SELL" and minavg == "STRONG BUY":
        conclusion = "Sell"
    elif houravg == "BUY" and minavg == "STRONG SELL":
        conclusion = "Buy"
    elif houravg == "BUY" and minavg == "SELL":
        conclusion = "Buy"
    elif houravg == "STRONG BUY" and minavg == "STRONG SELL":
        conclusion = "Buy"
    elif houravg == "STRONG BUY" and minavg == "SELL":
        conclusion = "Buy"
    else:
        conclusion = "Not today"
    today = date.today()
    global d1
    d1 = today.strftime("%d/%m/%Y")
    conn = sqlite3.connect("eurusd.db")
    db = conn.cursor() 
    db.execute("INSERT INTO trades ('dateoftrade', 'hour_conclusion', 'min_conclusion', 'global_conclusion', 'priceatsix') VALUES ( ?, ?, ?, ?, ?)", (d1, houravg, minavg, conclusion, priceatsix))
    conn.commit()
def secondtrade():
    url = 'https://www.investing.com/currencies/eur-usd-technical'
    driver.get(url)
    time.sleep(10)
    priceatseven = driver.find_element(By.XPATH,'//*[@id="last_last"]').text
    driver.close()
    global will_repeat
    if(((priceatseven < priceatsix) and conclusion == "Sell") or ((priceatseven > priceatsix) and conclusion == "Buy") or conclusion == "Not today"):
        will_repeat = False
    else:
        will_repeat = True
    conn = sqlite3.connect("eurusd.db")
    db = conn.cursor()
    db.execute("UPDATE trades SET priceatseven = ?, will_repeat = ? WHERE dateoftrade = ?", (priceatseven, will_repeat, d1))
    conn.commit()
    conn.close()
#------------------------------------------------------------------#
get_diff()
#firsttrade()
#secondtrade()
schedule.every().day.at(ls_time).do(firsttrade)
schedule.every().day.at(ll_time).do(secondtrade)
#------------------------------------------------------------------#
while True:
    schedule.run_pending()
    time.sleep(1)
