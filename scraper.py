import requests
import datetime
from bs4 import BeautifulSoup

year = int("2023") # user input
nextyear = False
month = int("05") # user input
currentyear = int(datetime.datetime.now().strftime("%Y"))
if month > 8 and currentyear > year:
    nextyear = True
elif month > 8 and currentyear == year:
    print("We have an inability to get the rates for the requested month. We apologize for the inconvenience.")
if currentyear - 3 > year:
    print("No we will not do that.")
months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
url = f"https://www.gsa.gov/travel/plan-book/per-diem-rates/per-diem-rates-results/?fiscal_year={year if nextyear == False else year + 1}&state=AZ&perdiemSearchVO_city=Tucson&action=perdiems_report&zip=&op=Find+Rates&form_build_id=form-GGHt7ZcnOjh5MtzZ4RJnygTl3DivBQfZf_k071phWGU&form_id=perdiem_form"
html = requests.get(url)
page = BeautifulSoup(html.text, "html.parser")
price = page.find("td", attrs={"headers": f"maxLodging y{year} {months[month]}"}).text
print(months[month] + price)