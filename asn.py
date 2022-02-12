from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import argparse, os, sys
from time import sleep
from selenium.webdriver.firefox.options import Options  

firefox_options = Options()  
firefox_options.add_argument("--headless")

url= "https://bgp.he.net/"

parser = argparse.ArgumentParser()
parser.add_argument("-o","--org", help="Organization to be searched for", required=True)
args = parser.parse_args()
org = args.org
print("Searching for:", org)

browser = webdriver.Firefox(options=firefox_options)
browser.get("https://bgp.he.net/search?search%5Bsearch%5D="+str(org)+"&commit=Search")

sleep(5)

data = BeautifulSoup(browser.page_source, features="lxml")
if data:
	table = data.find('table',{"class":"w100p"})

browser.quit()

try:
	df = pd.read_html(table.prettify())
except Exception as e:
	print(str(e))
	sys.exit()

df_frame = pd.DataFrame(df[0])
df_frame.columns = ['IPs','Name']
df_frame = df_frame[1:]
print(df_frame)	

if not df_frame.empty:
	df_frame.to_csv(str(org)+'.csv')
if os.path.exists(str(org)+'.csv'):
	print('Extracted IPs saved to:',os.path.abspath(str(org)+'.csv'))
