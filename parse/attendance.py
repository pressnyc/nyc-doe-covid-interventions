import asyncio
import csv
from bs4 import BeautifulSoup
from pyppeteer import launch



async def page_to_csv(page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    table = soup.select_one("table")
    headers = [th.text for th in table.select("tr th")]
    with open("./csv/attendance.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow(headers)
        wr.writerows([[td.text for td in row.find_all("td")] for row in table.select("tr + tr")])    
    return
        
        
async def hmm():
    browser = await launch({ 'headless': True,  'args': [
        '--no-sandbox',
        '--single-process',
        '--disable-dev-shm-usage',
        '--disable-gpu',
        '--no-zygote'
    ] })
    page = await browser.newPage()
    await page.goto('https://www.nycenet.edu/PublicApps/Attendance.aspx')
    await asyncio.sleep(.5)  
    await page.select('#ContentPlaceHolder1_gvAttendance_ddlPageSize', 'ALL')
    await asyncio.sleep(.5)  
    page_content = await page.content()
    await page_to_csv(page_content)    
    await asyncio.sleep(.3)  
    await browser.close()
    return


asyncio.get_event_loop().run_until_complete(hmm())
