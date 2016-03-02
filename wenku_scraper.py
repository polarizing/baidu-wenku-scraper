from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
import StringIO
from PIL import Image
import json
import multiprocessing

from fpdf import FPDF

# driver = webdriver.Chrome('/Users/programming/Desktop/baidu_wenku_scraper/chromedriver')
driver = webdriver.Firefox()
# driver.set_window_size(3000, 3000)
driver.get("http://wenku.baidu.com/link?url=QgHHxpq2UkFW7gZsT8iRnNYTPdeM6f60ShommVtOTT514iM-I-OB6RnkYmklXven9vAmKP9tQKXLqMxGY4iljloepETisP3rdraZB2MnUAm")

# Wait for Reader to load
try:
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.reader-page')))
except TimeoutException:
	print 'could not load reader'

# Find more button
try:
	more = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fc2e')))
	print more.text
	# more_location = more.location
	# driver.execute_script('window.scrollTo(0,' + str(more_location['y']-100) + ')')
	more.click()
except (TimeoutException, NoSuchElementException) as e:
	print e

# Zoom in document
try:
	zoom = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.zoom-add')))
	for x in range(5):
		zoom.click()
except NoSuchElementException as e:
	print e

doc_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#doc-tittle-1'))).text
# try:
# 	more = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fc2e')))
# 	more.click()
# except Exception as e:
# 	print e

# Zoom page
# driver.execute_script("document.body.style.zoom='150%'")

# Hide reader tools
driver.execute_script("document.getElementsByClassName('reader-tools-bar-wrap')[0].style.display = 'none';")
driver.execute_script("document.getElementsByClassName('fix-searchbar-wrap')[0].style.display = 'none';")


driver.save_screenshot('page.png')

# Get all reader pages
pages = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.reader-page')))


print (type(pages))
for idx, page in enumerate(pages):
	location = page.location
	size = page.size
	im = Image.open('page.png')
	left = location['x']
	top = location['y']
	right = location['x'] + size['width']
	bottom = location['y'] + size['height']
	im = im.crop((left, top, right, bottom))
	print ('working')
	im.save('page_' + str(idx)+'_cropped.png')
	print (location, size)
	# print page.text

driver.close()


# pdf = FPDF()
# pdf.add_page()
# pdf.image('page_0_cropped.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
# pdf.set_font('Arial', 'B', 16)
# pdf.cell(40, 10, 'Hello World!')
# pdf.output('tuto1.pdf', 'F')
