import asyncio
import csv
from bs4 import BeautifulSoup
from pyppeteer import launch



async def page_to_csv(page_content):
  async with asyncio.Lock():
      soup = BeautifulSoup(page_content, 'lxml')
      try:
        table = soup.select_one("table")
        headers = [th.text for th in table.select("tr th")]
        with open("./csv/daily-attendance.csv", "w") as f:
            wr = csv.writer(f)
            wr.writerow(headers)
            wr.writerows([[td.text for td in row.find_all("td")] for row in table.select("tr + tr")])
      except Exception:
          print('Error')
          print(page_content)
          

        
async def hmm():
    browser = await launch({ 'headless': True,  'args': [
        '--no-sandbox',
        '--single-process',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--no-zygote'
    ] })
    page = await browser.newPage()
    print('await page.goto')
    await page.goto('https://www.nycenet.edu/PublicApps/Attendance.aspx')
    await asyncio.sleep(.5)  

    print('await page.content')
    await page.content()

    print('await page.select')
    await page.select('#ctl00_ContentPlaceHolder1_gvAttendance_ctl23_ddlPageSize', 'ALL')
    await asyncio.sleep(1)

    print('await page.content')
    page_content = await page.content()

    print('await page_to_csv')
    await page_to_csv(page_content)    
    await asyncio.sleep(1)  
    await browser.close()
    return


asyncio.get_event_loop().run_until_complete(hmm())
