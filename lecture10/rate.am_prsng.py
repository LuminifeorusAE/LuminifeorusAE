import requests
from bs4 import BeautifulSoup
 
def parse_rate_am():
    response = requests.get("https://rate.am/")
 
    soup = BeautifulSoup(response.text, 'html.parser')  


    all_trs = soup.find_all('tr') 
    bank_currencies = []

    for tr in all_trs:
        if "id" in tr.attrs:
            bank_name = tr.find('td', class_='bank').text
            all_tds = tr.find_all('td', class_="")
            currencies = {}
            my_keys = ["usd_buy", "usd_sell", "eur_buy", "eur_sell", "rub_buy", "rub_sell", "gbp_buy", "gbp_sell"]
            
            for i in range(3,len(all_tds)):
                span_check = all_tds[i].find("span")
                my_currency_value = None

                if not span_check:
                    my_currency_value = all_tds[i].text
                else:
                    my_currency_value = span_check.text
                    currencies[my_keys[i-3]] = my_currency_value

            currencies["bank_name"] = bank_name.replace("\n","")
            bank_currencies.append(currencies)

    print(bank_currencies)
parse_rate_am()
 