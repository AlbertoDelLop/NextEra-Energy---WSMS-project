                                                            #NextEra energy
#Extracting Company Overview
#First of all, upload necessary packages
import time
from urllib import request as re
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
# Then, open the page below in a browser of your choice.
url = 'http://www.investor.nexteraenergy.com'
html = re.urlopen(url)
bs = BS(html.read(), 'html.parser')


# Beautiful Soup 'find' method allows to create list of tags by class:
intro = bs.find('div', {'class': 'home-intro'}).get_text()
print(intro)

intro=intro.split(sep='\n')
print(type(intro))
print(intro[3])

# Instead of displaying it one by one we might use list comprehension to put them into new list and pandas data frame:
# The data can be put into data frame, later into .csv file.
overview = {'Title': [intro[1]], 'Text': [intro[3]]}

d = pd.DataFrame(overview)

print(d)
# ################################################################################
# # This part saves data to csv.
# ################################################################################
d.to_csv('overview.csv')

                                           # Extraction of Stock Chart Table


# We download the code as before:
#Changing the link for getting stock chart information
url = 'http://ir.tools.investis.com/Clients/(S(i350sggxfguad3cfd2icvazs))/us/nextera_energy_inc/SM8/Default.aspx?culture=en-US'
html = re.urlopen(url)
bs = BS(html.read(), 'html.parser')
# Variables created is a list to store quotes
ISIN = []
Symbol = []
Number_of_shares_Tota=[]
Market_Cap_Mn=[]
Best_Bid=[]
Best_offer=[]
Day_Volume=[]
Dividend=[]
Last_Close=[]
Open=[]
Day_High=[]
Day_Low=[]
_52_Week_High=[]
_52_Week_Low=[]
Dividend_yield=[]


# Agent is any software that retrieves and presents Web content for end users.
# it can be web browsers, media players, and plug-ins that help in retrieving, rendering and interacting with web content.
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

rqst_html= requests.get(url, headers=agent)
html=rqst_html.text
data=BS(html, 'html.parser')

#Here with find_all method using span and its attributes via indexes [0] I am getting the information.
#Span id's are unique for each information this is why it is the best way to extract information with those id's.
#There are some classes that are the same and I can't use it for getting the information I needed.
#And this information that I get is appending to the quotes that I created to store
ISIN.append(data.find_all('span', attrs={'id':'snapShotBox_Instrument4'})[0].text)
Symbol.append(data.find_all('span', attrs={'id':'snapShotBox_inst1'})[0].text)
Number_of_shares_Tota.append(data.find_all('span', attrs={'id':'snapShotBox_Instrument9'})[0].text)
Market_Cap_Mn.append(data.find_all('span', attrs={'id':'snapShotBox_marketcap2'})[0].text)
Best_Bid.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot1'})[0].text)
Best_offer.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot16'})[0].text)
Day_Volume.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot11'})[0].text)
Dividend.append(data.find_all('span', attrs={'id':'snapShotBox_Dividend1'})[0].text)
Last_Close.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot10'})[0].text)
Open.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot9'})[0].text)
Day_High.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot13'})[0].text)
Day_Low.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot14'})[0].text)
_52_Week_High.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot17'})[0].text)
_52_Week_Low.append(data.find_all('span', attrs={'id':'snapShotBox_Snapshot18'})[0].text)
Dividend_yield.append(data.find_all('span', attrs={'id':'snapShotBox_Dividend2'})[0].text)



# Dataframe
# I am creating dataframe with the main names in the table and giving them titles to make it clearer.
# These names can be found in
DF = pd.DataFrame({"ISIN": ISIN, "Symbol": Symbol, "Number of shares - Total": Number_of_shares_Tota,
	"Market Cap": Market_Cap_Mn, "Best Bid": Best_Bid, "Best Offer": Best_offer, "Day Volume": Day_Volume,
 			"Dividend": Dividend,"Last Close":Last_Close, "Open": Open,
 			"Day High": Day_High, "Day Low": Day_Low,
 			"52 Week High": _52_Week_High, "52 Week Low": _52_Week_Low, "Dividend Yield": Dividend_yield})

# save to StockChart
DF.to_csv('StockChart.csv', header = True)

start = time.perf_counter()
print('\nExecution time:',str(round(time.perf_counter() - start , 4))+'s') #execution time is 0 second
