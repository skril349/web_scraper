import random
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from credentials import username as linkedin_username, password as linkedin_password

class LinkedInScraper:
    def __init__(self, num_searches):
        # Configurem el User-Agent i desactivem la pantalla de selecció de motor de cerca per defecte
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        opts.add_argument("--disable-search-engine-choice-screen")
        opts.add_argument('--disable-gpu')

        self.num_searches = num_searches
        self.current_search_count = 0
        
        # Instanciem el driver de selenium
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

        # Inicialitzem el DataFrame de pandas
        self.jobs_data = pd.DataFrame(columns=['business', 'title', 'where', 'when', 'apply', 'remote', 'requisits', 'requisits_compleixes', 'requisits_no_compleixes'])

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

        # Avegades demana captcha (fer manualment en 20 segons de marge)
        sleep(20)

    def search_jobs(self, job_title):
        # Buscador
        search_bar = self.driver.find_element(By.XPATH, '//input[@aria-label="Buscar"]')
        search_bar.send_keys(job_title)
        sleep(8)
        search_bar.send_keys(Keys.ENTER)
        sleep(8)
        
        

    def view_all_results(self):
        try:
            filter_button = self.driver.find_element(By.XPATH, '//nav//ul/li/button[text()="Empleos"]')
            filter_button.click()
            sleep(3)
            print("Filtre 'Empleos' aplicat correctament.")

        except Exception as e:
            print("No s'ha pogut aplicar el filtre 'Empleos':", e)
            
    def scrape_job_info(self):
        while self.current_search_count < self.num_searches:
            try:
                jobs = self.driver.find_elements(By.XPATH, '//li[contains(@id,"ember")]')
            except Exception as e:
                print("No s'han trobat els elements de treballs:", e)
                break
            
            if not jobs:  
                print("No s'han trobat més ofertes a la pàgina actual.")
                break
            
            for idx, job in enumerate(jobs):
                if self.current_search_count >= self.num_searches:
                    break
                
                # Desplaçament cada 5 elements
                if idx % 5 == 0 and idx != 0:
                    self.driver.execute_script("arguments[0].scrollIntoView();", job)
                    sleep(2)

                try:
                    job.click()
                    self.current_search_count += 1
                    sleep(random.uniform(2, 5.0))

                    business, title, where, when, apply, remote = '', '', '', '', '', ''
                    r_text, compleix_requisits, no_compleix_requisits = [], [], []

                    # Business
                    try:
                        business = self.driver.find_element(By.XPATH, '//div[@class="job-details-jobs-unified-top-card__company-name"]').text
                    except Exception:
                        business = "NA"
                        print("No s'ha trobat el nom de l'empresa")
                    
                    # Title
                    try:
                        title = self.driver.find_element(By.XPATH, '//h1[contains(@class, "t-24 t-bold inline")]').text
                    except Exception:
                        title = "NA"
                        print("No s'ha trobat el títol")
                    
                    # Where
                    try:
                        where = self.driver.find_element(By.XPATH, '//div[contains(@class, "mt2")]/span[1]').text
                    except Exception:
                        where = "NA"
                        print("No s'ha trobat el lloc")
                    
                    # When
                    try:
                        when = self.driver.find_element(By.XPATH, '//div[contains(@class, "mt2")]/span[3]').text
                    except Exception:
                        when = "NA"
                        print("No s'ha trobat quan s'ha publicat")
                    
                    # Apply
                    try:
                        apply = self.driver.find_element(By.XPATH, '//div[contains(@class, "mt2")]/span[5]').text
                    except Exception:
                        apply = "NA"
                        print("No s'han trobat les sol·licituds")
                    
                    # Remote
                    try:
                        remote = self.driver.find_element(By.XPATH, '//ul/li/span/span/span/span[1]').text
                    except Exception:
                        remote = "NA"
                        print("No s'ha trobat informació de treball remot")
                    
                    # Requisits
                    try:
                        container_div = self.driver.find_element(By.XPATH, '//div[@id="how-you-match-card-container"]')
                        self.driver.execute_script("arguments[0].scrollIntoView();", container_div)
                        sleep(2)
                        requisits_button = container_div.find_element(By.XPATH, './/button')
                        requisits_button.click()
                        sleep(2)
                        requisits_list = self.driver.find_element(By.XPATH, '//ul[@class="job-details-skill-match-status-list"]')
                        requisits = requisits_list.find_elements(By.TAG_NAME, 'li')
                        
                        for requisit in requisits:
                            r_text.append(requisit.text)
                            if requisit.find_elements(By.XPATH, './/button[contains(@aria-label, "Añade")]'):
                                no_compleix_requisits.append(requisit.text)
                            else:
                                compleix_requisits.append(requisit.text)
                                
                        close_modal = self.driver.find_element(By.XPATH, '//button[@aria-label="Descartar"]')
                        close_modal.click()
                        sleep(1)

                    except Exception:
                        r_text = "NA"
                        compleix_requisits = "NA"
                        no_compleix_requisits = "NA"
                        print("No s'ha trobat informació dels requisits")

                    # Afegeix les dades al DataFrame
                    new_row = pd.DataFrame([{
                        'business': business,
                        'title': title,
                        'where': where,
                        'when': when,
                        'apply': apply,
                        'remote': remote,
                        'requisits': r_text,
                        'requisits_compleixes': compleix_requisits,
                        'requisits_no_compleixes': no_compleix_requisits,
                        'numero_requisits': len(r_text),
                        'numero_requisits_compleixes': len(compleix_requisits),
                        'numero_requisits_no_compleixes': len(no_compleix_requisits)
                    }])
                    self.jobs_data = pd.concat([self.jobs_data, new_row], ignore_index=True)
                    print(title)
                    
                    # Si és l'últim <li> presiona siguiente
                    if idx == 24:
                        try:
                            next_button = self.driver.find_element(By.XPATH, '//button[@aria-label="Ver siguiente página"]')
                            next_button.click()
                            sleep(5)
                            break  
                        except Exception:
                            print("No s'ha trobat el botó 'Siguiente', o no hi ha més pàgines.")
                            return 
                except Exception as e:
                    print(f"Error al processar l'oferta: {e}")

        
    def close(self):
        self.jobs_data.to_csv('../dataset/linkedin_jobs.csv', index=False, encoding='utf-8')
        print("Dades guardades a 'linkedin_jobs.csv'")

        # Tanca el navegador
        self.driver.quit()
