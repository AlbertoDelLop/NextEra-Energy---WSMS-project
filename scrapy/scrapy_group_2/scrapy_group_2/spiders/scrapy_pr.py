# -*- coding: utf-8 -*-
import scrapy
import time


start = time.perf_counter()





class Overview(scrapy.Item):
    CompanyOverview = scrapy.Field()

#creating spider named crawler and telling it to go to the following webpage
class OverviewSpider(scrapy.Spider):
    name = 'crawler'
    start_urls = ['http://www.investor.nexteraenergy.com/']

#scraping the text from the assigned xpath
    def parse(self, response):
        p = Overview()
        p['CompanyOverview'] = response.xpath('//*[@id="contentwrapperinner"]/div/div[1]/p/span/text()').getall()

        yield p


class StockTable(scrapy.Item):
    Stock_parameter = scrapy.Field()
    Value = scrapy.Field()

#creating spider named stock and telling it to go to the following url
class StockSpider(scrapy.Spider):
    name = 'stock'
    start_urls = ['http://ir.tools.investis.com/Clients/(S(1odes4dttvfhicymklu3tcp3))/us/nextera_energy_inc/SM8/Default.aspx?culture=en-US']
    
    def parse(self, response):
        
#the spider will extract information from the following xpath
        col1_xpath = '//div[re:test(@class, "box share-information")]//div[re:test(@class, "col-one")]//text()'
        selection = response.xpath(col1_xpath)
        col1=[]  #creating an empty vector
        
        for s in selection:                         #removing all empty spaces from the scraped text
            if ('\n' or '\r') in s.getall()[0]:
                continue
            col1.append(s.getall()[0])  #appends to the empty vector every extracted element from the given xpath

         #the vector contains every text element separately, however we need for some elements to be together such as money symbol and value
        #let's fix the first vector

        s=0
        stockp=[]
        while (s<len(col1)):
            
            if (col1[s+1]==' / '):          #appending the elements if there's '/'
                stockp.append([col1[s]+col1[s+1]+col1[s+2]])
                s = s+3
            else:
                stockp.append([col1[s]])    #if no '/' keep iterating
                s = s+1
                
            if s+1 == len(col1):            #stop the while loop once the correct length is reached
                stockp.append([col1[s]])
                break

# the spider will extract information from the following xpath
        
        col2_xpath = '//div[re:test(@class, "box share-information")]//div[re:test(@class, "col-two")]//text()'
        selection = response.xpath(col2_xpath)
        col2=[]   #creating an empty vector
        
        for s in selection:             #appending the scraped text without empty spaces
            if ('\n' or '\r') in s.getall()[0]:
                continue
            col2.append(s.getall()[0])
            
#fixing the second vector

        s=0
        value=[] #empty vector that will contain the fixed data
        while (s<len(col2)):
    
            if (col2[s+1]==' / '):
                value.append([col2[s]+col2[s+1]+col2[s+2]])     #appending the elements if there's '/' and then moving to the next index
                s = s+3
            elif (col2[s]=='$'):                                #appending the elements if there's '$' and then moving to the next index
                value.append([col2[s]+col2[s+1]])
                s = s+2
            else:                                               #keep iterating if none of the symbols are found
                value.append([col2[s]])
                s = s+1
                
            if s+1 >= len(col2):                                 #stop while loop at reached length
                value.append([col2[s]])
                break
        

   #creating a table with two columns from the data
        d = StockTable()
        
        for data in range(14):
            d['Stock_parameter']=stockp[data]
            d['Value']=value[data]
            yield d


print('\nExecution time:',str(round(time.perf_counter() - start , 4))+'s')

#after running the first spider, i saved the output with overview.csv

#the code below serves to read the saved file in order to check the most common words
#uncomment it if this needs to be checked and eneter the path to the saved output


#text = open('C:/Users/Dell/Desktop/pythonProject/scrapy_group_2/scrapy_group_2/overview.csv').read()
#words = text.split() #spliting every word as separate elements
#word_count = {}
#for word in words:
#     count = word_count.get(word, 0)         #counting the number of times the word appears
#                                             # the number is either the number of times we encountered the word, or 0 if we haven’t seen it yet
#     count += 1
#     word_count[word] = count                #store the updated count into the dictionary
# word_count_list = sorted(word_count, key=word_count.get, reverse=True)      #sort the input and return a list
# for word in word_count_list[:20]:
#     print(word, word_count[word]0)

