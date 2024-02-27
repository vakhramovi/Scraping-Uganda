import requests
from bs4 import BeautifulSoup as BS

def get_data():
    url = "https://www.yellow.ug/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    response = requests.get(url, headers=headers).text
    soup = BS(response, "lxml")


    page_link = soup.find("div", class_="iholder").find_all("a")[-1].get("href")
    url = f"https://www.yellow.ug{page_link}"
    response = requests.get(url, headers=headers).text
    soup = BS(response, "lxml")

    ul_s = soup.find_all("ul", class_="cat_list")
    all_elements = []
    with open("result.json", "w", encoding="utf-8") as file_json:
        for lis in ul_s:
            li_s = lis.find_all("li")
            for li in li_s:
                link = li.find("a").get("href")
                url = f"https://www.yellow.ug{link}"
                response = requests.get(url, headers=headers).text
                soup = BS(response, "lxml")
                try:
                    page_count = int(soup.find("div", class_="pages_container").find_all("a")[-2].text)
                except:
                    page_count = 1
                    
                for page in range(1, page_count + 1):
                    url = f"https://www.yellow.ug{link}/{str(page)}"
                    response = requests.get(url, headers=headers).text
                    soup = BS(response, "lxml")
                    block = soup.find("div", id="listings")

                    element_block = block.find_all("div", class_="company")
                    for element_a in element_block:
                        try:
                            element = element_a.find("a").get("href")
                        except:
                            continue
                        url = f"https://www.yellow.ug{element}"
                        response = requests.get(url, headers=headers).text
                        soup = BS(response, "lxml")
                        try:
                            company_name = soup.find("div", id="company_item").find("b", id="company_name").text
                        except:
                            company_name = "None"
                        try:
                            # phone_num = soup.find_all("div", class_="info")
                            # for ph_num in phone_num:
                            phone_number = soup.find("div", class_="cmp_details_in").find_all("div", class_="text")[1].text
                        except:
                            phone_number = "None"
                        try:
                            mobile_phone = soup.find("div", class_="cmp_details_in").find_all("div", class_="text")[2].text
                        except:
                            mobile_phone = "None"
                        try:
                            website = soup.find("div", class_="text weblinks").find("a").text
                        except:
                            website = "None"
                        try:
                            rating = soup.find("div", class_="info noreviews").find("div", class_="rate rate_5 rate_big").text
                        except:
                            rating = "None"
                        try:
                            address = soup.find("div", class_="cmp_details_in").find_all("div", class_="text")[0].text.replace(", UgandaView Map", "")
                        except:
                            address = "None"
                        # print (f"{company_name}\n{phone_number}\n{mobile_phone}\n{website}\n{rating}\n\n")
                        
                        element_list={
                            "Company_name": company_name,
                            "Phone_number": phone_number,
                            "Mobile_phone": mobile_phone,
                            "Website": website,
                            "Address": address,
                            "Rating": rating
                        }
                        all_elements.append(element_list) 
                        print("In Process")
                        # print(f"{company_name}\n{phone_number}\n{mobile_phone}\n{adress}\n{website}\n{rating}\n\n")

def main():
    get_data()

if __name__ == "__main__":
    main()
