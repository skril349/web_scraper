import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurem l'User-Agent i desactivem la pantalla de selecció de motor de cerca per defecte
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")

# Instanciem el driver de selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# Anem a la pàgina d'Indeed
driver.get('https://es.indeed.com/?r=us')
sleep(4)

# Identifiquem el camp de cerca pel seu id i escrivim "data scientist" , (això ho faig de moment, la idea es que introduïm un array per params)

search_box = driver.find_element(By.ID, "text-input-what")
search_box.clear()  # Esborrem contingut previ
search_box.send_keys("data scientist")

sleep(2)

# Identifiquem el botó de buscar oferta
search_button = driver.find_element(By.CSS_SELECTOR, "button.yosegi-InlineWhatWhere-primaryButton")
search_button.click()

sleep(5)

