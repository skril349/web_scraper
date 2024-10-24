import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from credentials import username as linkedin_username, password as linkedin_password

# Configurem l'User-Agent i desactivem la pantalla de selecció de motor de cerca per defecte
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
opts.add_argument("--disable-search-engine-choice-screen")
opts.add_argument('--disable-gpu')

# Instanciem el driver de selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

# Anem a la pàgina de LinkedIn
driver.get('https://www.linkedin.com/login')
sleep(8)

# Email linkedin
username_input = driver.find_element(By.ID, 'username')
username_input.send_keys(linkedin_username)

# password de linkedin
password_input = driver.find_element(By.ID, 'password')
password_input.send_keys(linkedin_password)

# login
login_button = driver.find_element(By.XPATH, '//*[@type="submit"]')
login_button.click()

sleep(10)

# Buscador
search_bar = driver.find_element(By.XPATH, '//input[@aria-label="Buscar"]')

# Escrivim data scientist
search_bar.send_keys('Data Scientist')

sleep(8)

#Intro per buscar
search_bar.send_keys(Keys.ENTER)

sleep(4)

# ver todos los resultados
login_button = driver.find_element(By.XPATH, '//div[@class="search-results__cluster-bottom-banner artdeco-button artdeco-button--tertiary artdeco-button--muted"]')
login_button.click()

sleep(3)


jobs = driver.find_elements(By.XPATH, '//li[contains(@id,"ember")]')


for job in jobs:
    try:
        # Click a cada oferta
        job.click()
        sleep(5)  # Esperem que es carregui la informació

        # Títol
        title = driver.find_element(By.XPATH, '//h1[contains(@class, "t-24 t-bold inline")]').text
        print(f"Títol: {title}")

    except Exception as e:
        print ('No hi ha títol')


