import sys
from linkedin_scraper import LinkedInScraper

if __name__ == "__main__":
    # Llegeix els paràmetres des de la línia de comandes
    if len(sys.argv) < 3:
        print("Ús: python main.py 'Títol del treball' 'Número de cerques'")
        sys.exit(1)

    job_title = sys.argv[1]
    num_searches = int(sys.argv[2])

    scraper = LinkedInScraper(num_searches)

    # Login
    scraper.login()
    
    # Cerca feines amb el títol especificat
    scraper.search_jobs(job_title)
    
    # Veure tots els resultats
    scraper.view_all_results()
    
    # Extreure la informació de cada oferta
    scraper.scrape_job_info()
    
    # Tancar el navegador
    scraper.close()
