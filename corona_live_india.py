"""Just press RUN."""

# Live status of Corona Virus in India.
# Data sorce: 'https://mohfw.gov.in/'

import os
import re
from urllib import request as req
from urllib import error as err

# Install 3rd part module 'bs4'
os.system("pip -q install bs4")
from bs4 import BeautifulSoup as bs
    

url = "https://www.mohfw.gov.in/"

try:
    # Fetch raw html web page.
    raw = req.urlopen(url).read()
except err.URLError: 
    print("Data Error! Failed to fetch the data.")
else:
    # Get data date.
    
    # 2020/03/22 - Note:
    # This regex is not working due to a 
    # slight change in page's html.
    # update = re.search(r"\bas on (.+)\)", raw.decode())
    
    # 2020/03/22 - Quick Fix:
    # New regex to get the date.
    update = re.search(r"\(\*including foreign nationals, as on (.+)\)", raw.decode())
    
    # 2020/03/24 - Quick Fix:
    # Unable to properly find table.
    # Dynamic table location
    # update according to update regex's 
    # location.
    table_at = update.span()[0]
    
    # 2020/03/23 - Quick Fix:
    # Get only the info table.
    tablepart = raw[table_at:]
    
    soup = bs(tablepart, features="html.parser")
    table = soup.find("table")
    
    # Save all the data in a 2d list.
    alldata = []
    data = []

    tds = table.find_all_next("td")
    for n, td in enumerate(tds, start=1):
        text = td.text.replace("\n", "")
        data.append(text)
        
        if n % 6 == 0:
            alldata.append(data)
            data = []
            
    # Add rest of the data
    alldata.append(data)
    # print(alldata)
    datalen = len(alldata)
    
    # Note: Might not work all the time.
    # Checking data structure
    if len(alldata[0]) != 6:
         quit("Data Format Error! Data structure might have changed at source.")
         
    # Print data in tabular format
    print("🇮🇳 ┃ Foreigners 🌐 ┃"
          "Cured 💊 ┃Deaths 💀\n"
          f"{'━' * 34}")
    
    for n, data in enumerate(alldata[1:], start=1):
        if n != datalen - 1:
            region, india, foreign, cured, death = data[1:]
        else:
            region, india, foreign, cured, death = data
        # Minor beautification.
        total = region.startswith("Total")
        region = "Total" if total else region
        hmark = "➖" if total else "━"
        size = 19 if total else 34
        
        print(f"{region:^40}\n"
              f"{hmark * size}"
              f"\n{india:^6}┃{foreign:^10}┃"
              f"{cured:^12}┃ {death:^5}\n"
              f"{hmark * size}")
    
    print(f"\n🌟 Last Update: "
          f"{update.group(1)}\n\n"
          f"📜 Source: " 
          f"'https://mohfw.gov.in/'")
    
    print("\n📞 Helpline Number: "         
          "+91-11-23978046\n\n"
          "✉️ Helpline Email: "
          "ncov2019@gmail.com")
