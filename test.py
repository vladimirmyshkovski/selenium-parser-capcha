from selenium import webdriver
from PIL import Image
from capcha import resolve
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
from bs4 import BeautifulSoup
import datetime 
import os 
import time


url = ""
login_url = ""
main_url = ""

username = ""
password = ""
security_code = ""

browser = webdriver.Firefox()#PhantomJS()


def get_image():
	
	capcha = browser.find_element_by_id('image')
	location = capcha.location
	
	size = capcha.size
	browser.save_screenshot('capcha.png')
	
	image = Image.open('capcha.png')

	left = location['x'] + 1.7
	top = location['y'] + 1.6
	right = location['x'] + (size['width'] - 1.5)
	bottom = location['y'] + (size['height'] - 1.4)

	image = image.crop((left, top, right, bottom))
	image.save('capcha.png')


def get_code():
	image = resolve('capcha.png')
	os.remove('capcha.png')
	return image


def login():

	browser.get(url + login_url)
	get_image()

	code = get_code()
	
	button = browser.find_element_by_xpath('//button[@id="btnSubmit"]') 

	browser.find_element_by_xpath('//input[@id="code"]').send_keys(code)
	browser.find_element_by_xpath('//input[@id="txtUsername"]').send_keys(username)
	browser.find_element_by_xpath('//input[@id="txtPassword"]').send_keys(password)

	button.click()

	error = get_error()

	if error:
		login()


def get_security_code():

	frame = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.XPATH, "//iframe[@id='main']"))
	)

	browser.switch_to.frame('main')

	form = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.XPATH, "//form[@id='form1']"))
	)

	security_code_input = browser.find_element_by_xpath('//input[@id="txtNewPwd1"]')

	if security_code_input:
		print(security_code_input)
		security_code_input.send_keys(security_code)
	
	button = browser.find_element_by_xpath('//button[@id="btnSubmit"]') 

	button.click()


def close_popup():
	
	button = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.XPATH, "//button[@class='esc']"))
	)

	button.click()

def parse_table():
	
	html = browser.page_source
	soup = BeautifulSoup(html, "html.parser")

	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	with open(str(now) + '.csv', "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for tr in soup.find('table').findAll('tr')[1:]:
			th = tr.find('th').get_text()
			td = tr.find('td').get_text()
			writer.writerow([th, td])


def get_error():
	
	error = None
	
	try:
		error = WebDriverWait(browser, 10).until(
			EC.presence_of_element_located((By.XPATH, '//div[@id="litErr"]'))
		)
		error = browser.find_element_by_xpath('//div[@id="litErr"]') 
	except:
		pass

	return error


def main():
	
	login()

	get_security_code()
	
	close_popup()
	
	parse_table()
	
	browser.quit()



if __name__ == '__main__':
	main()


