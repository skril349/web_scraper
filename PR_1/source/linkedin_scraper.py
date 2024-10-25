import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from credentials import username as linkedin_username, password as linkedin_password

class LinkedInScraper:
    def __init__(self):
        # Configurem l'User-Agent i desactivem la pantalla de selecció de motor de cerca per defecte
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        opts.add_argument("--disable-search-engine-choice-screen")
        opts.add_argument('--disable-gpu')
        
        # Instanciem el driver de selenium
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    def login(self):
        # Anem a la pàgina de LinkedIn
        self.driver.get('https://www.linkedin.com/login')
        sleep(8)

        # Email linkedin
        username_input = self.driver.find_element(By.ID, 'username')
        username_input.send_keys(linkedin_username)

        # password de linkedin
        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys(linkedin_password)

        # login
        login_button = self.driver.find_element(By.XPATH, '//*[@type="submit"]')
        login_button.click()

        sleep(10)

    def search_jobs(self, job_title):
        # Buscador
        search_bar = self.driver.find_element(By.XPATH, '//input[@aria-label="Buscar"]')
        search_bar.send_keys(job_title)

        sleep(8)

        # Intro per buscar
        search_bar.send_keys(Keys.ENTER)

        sleep(4)

    def view_all_results(self):
        try:
            all_results_button = self.driver.find_element(By.XPATH, '//div[@class="search-results__cluster-bottom-banner artdeco-button artdeco-button--tertiary artdeco-button--muted"]')
            all_results_button.click()
            sleep(3)
        except Exception as e:
            print("No s'han trobat més resultats:", e)

    def scrape_job_info(self):
        jobs = self.driver.find_elements(By.XPATH, '//li[contains(@id,"ember")]')

        for job in jobs:
            try:
                # Click a cada oferta
                job.click()
                sleep(random.uniform(2.0, 5.0))

                # Empresa
                try:
                    bussiness = self.driver.find_element(By.XPATH, '//div[@class="job-details-jobs-unified-top-card__company-name"]').text
                    print(f"Empresa: {bussiness}")
                except Exception:
                    print("No s'ha trobat el nom de l'empresa")

                # Títol
                try:
                    title = self.driver.find_element(By.XPATH, '//h1[contains(@class, "t-24 t-bold inline")]').text
                    print(f"Títol: {title}")
                except Exception:
                    print("No s'ha trobat el títol")   

                # Remot
                try:
                    remote = self.driver.find_element(By.XPATH, '//ul/li/span/span/span/span[1]').text
                    print(f"Remot: {remote}")
                except Exception:
                    print("No s'ha trobat informació de treball remot")

            except Exception as e:
                print(f"Error al processar l'oferta: {e}")

    def close(self):
        # Tancar el navegador
        self.driver.quit()
