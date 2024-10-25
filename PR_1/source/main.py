from linkedin_scraper import LinkedInScraper

if __name__ == "__main__":
    scraper = LinkedInScraper()
    
    # Login
    scraper.login()
    
    # Cerca feines amb el títol 'Data Scientist'
    scraper.search_jobs('Data Scientist')
    
    # Veure tots els resultats
    scraper.view_all_results()
    
    # Extreure la informació de cada oferta
    scraper.scrape_job_info()
    
    # Tancar el navegador
    scraper.close()
