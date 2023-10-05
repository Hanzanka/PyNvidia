from ui.app import App
from scraper.scraper import NvidiaWebScraper
from gpu.gpu import GPU


driver_downloader = NvidiaWebScraper(gpu=GPU())
app = App(driver_downloader=driver_downloader)
app.mainloop()
