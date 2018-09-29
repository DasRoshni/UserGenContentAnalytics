from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import re

COMMENTS_AMOUNT = 120

forumUrl = 'https://forums.edmunds.com/discussion/2864/general/x/entry-level-luxury-performance-sedans/p{}'

def get_first_comments(amount=COMMENTS_AMOUNT):
	messages = []
	driver = webdriver.Chrome("C:\Users\Tomer\Documents\Studies\UT\User Generated Content Analytics\Ex1\chromedriver.exe")
	for pageNum in range(700):
		driver.get(forumUrl.format(pageNum))
		rawPageContents = driver.page_source
		soup = BeautifulSoup(rawPageContents, 'html.parser')
		messages.extend(map(lambda msgElement: msgElement.text.strip(),soup.find_all('div',{'class':'Message'})))
		if len(messages) >= COMMENTS_AMOUNT:
			break
	return messages
	
def replace_models_with_brands(messages):
	replace_map = get_models_replace_map()
			
			
def get_models_replace_map():
	replace_map = {}
	with open("C:\Users\Tomer\Documents\Studies\UT\User Generated Content Analytics\Ex1\models.csv") as f:
		replace_map = {row['model'].replace('\xa0', ''): row['brand'].replace('\xa0', '') for row in csv.DictReader(f,fieldnames=['brand','model'])}
	return replace_map

def apply_model_brand_replacements(messages,replace_map):
	manipulated_messages = []
	for message in messages:
		manipulated_message = message
		for model,brand in replace_map.iteritems():
			re_expression = re.compile(r'\b{}\b'.format(re.escape(model)), re.IGNORECASE)
			manipulated_message = re_expression.sub(brand, manipulated_message)
		manipulated_messages.append(manipulated_message)
	return manipulated_messages

replace_map = get_models_replace_map()
messages = get_first_comments()
manipulated_messages = apply_model_brand_replacements(messages,replace_map)
		
