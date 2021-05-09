from selenium import webdriver
import time
import pandas as pd

start = time.perf_counter()

gecko_path = '/usr/local/bin/geckodriver'
url = 'http://www.investor.nexteraenergy.com/'

options = webdriver.firefox.options.Options()
options.headless = False

driver = webdriver.Firefox(options = options, executable_path = gecko_path)

# Actual program:
driver.get(url)
time.sleep(2)


#Extract the information from overview site
intro = driver.find_element_by_xpath('/html/body/form/div[3]/div[5]/div/div/div/div[1]').text
intro = intro.split(sep='\n') #divides the elements in a vector

print("************************************")

d = pd.DataFrame({'Title':[intro[0]],'Text':[intro[2]]}) #Adds the title and the main text in a dataframe from the vector intro
print(d)
d.to_csv('overview.csv') #Saves it in a .csv file

print("************************************")
time.sleep(2)


#click and change to the Stock Information section
stock = driver.find_element_by_xpath('//*[@id="secondnav-nav-stock-information-level1"]')
stock.click()

time.sleep(2)


# It's necessary to switch to the iframe because the next information we want to extract is in there
driver.switch_to.frame(driver.find_element_by_id("ExternalWebContentExternalIFrame"))

#The information is hidden so it is necessary to click the button 'Show more' in order to extract it
showmore = driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div/a')
showmore.click()

time.sleep(2)


#Etract the data from the two columns of the data
stockp = driver.find_elements_by_xpath('//*[@id="upSnapshot"]//*[@class="col-one" or @class="col-one share_in_issue"]')
values = driver.find_elements_by_xpath('//*[@id="upSnapshot"]//*[@class="col-two"]')

print("************************************")

print('Stock parameters\n')
print(len(stockp))
#print(stockp)
Stockp=[]
for data in stockp:
    print(data.text)
    Stockp.append(data.text) #Creates a vector with the names of the stock parameters from column 1

print('Values\n')
print(len(values))
#print(values)
Values=[]
for data in values:
    print(data.text)
    Values.append(data.text) #Creates a vector with the values of the stock parameters from column 2

d = pd.DataFrame({'Stock parameter':Stockp,'Value':Values}) #Creates a dataframe with the table
print('\n',d)
d.to_csv('Stock output.csv') #Saves it in a .csv file

print("************************************")


time.sleep(5)

# Close browser:
driver.quit()

print('\nExecution time:',str(round(time.perf_counter() - start - 13, 4))+'s')

