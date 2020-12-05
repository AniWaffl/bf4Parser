import requests
from bs4 import BeautifulSoup as BS

url = "https://www.royalgreenwich.gov.uk/directory/53/greenwich_one_card_discounts?fbclid=IwAR2masBdXNYaF8YCXb65En95GAiqbw7Hqn5Vtq212zLo7Cu8hF0wDJQc0_o"
# url = "https://www.allthingsgreenwich.co.uk/directory/"


def get_html(url: str) -> str:
    html_text = requests.get(url)
    if html_text.status_code != 200:
        print("Connection error")
        exit()
    return html_text.text


def get_category_links(html_text) -> list:
    directory_href_list = []

    soap: BS = BS(html_text, 'html.parser')
    ul_dir = soap.find('ul', class_="list list--arrows list--arrows-2up")
    all_a = ul_dir.find_all("a", class_="list__link")

    for i in all_a:
        directory_href_list.append(i.get("href"))

    return directory_href_list


def get_sub_category_links(html_text) -> list:
    directory_href_list = []

    soap: BS = BS(html_text, 'html.parser')
    ul_dir = soap.find('ul', class_="list list--arrows")
    try:
        all_a = ul_dir.find_all("a", class_="list__link")
    except:
        print("1 empty category")
        return

    for i in all_a:
        directory_href_list.append(i.get("href"))

    return directory_href_list


def get_data_from_link(html_text, href) -> dict:
    soap: BS = BS(html_text, 'html.parser')
    ul_dir = soap.find('dl', class_="list list--definition")
    heading = ul_dir.find_all("dt", class_="list--definition__heading")
    content = ul_dir.find_all("dd", class_="list--definition__content")

    keys = []
    values = []

    for key in heading:
        keys.append(key.get_text(strip=True))

    for value in content:
        values.append(value.get_text(strip=True))

    data = dict(zip(keys, values))

    Category = href.split("/")[-1].title()
    data.update({"Category":Category})

    return data


def royalgreenwich_parser(url):
    text = get_html(url)
    category_hrefs = get_category_links(text)

    domen = "https://www.royalgreenwich.gov.uk"
    all_sub_calegory_links = []
    for href in category_hrefs:
        html = get_html(href)
        sublinks = get_sub_category_links(html)

        if sublinks is None:
            continue

        for i in sublinks:
            sublink = domen+i
            all_sub_calegory_links.append(sublink)

    data_list = []
    for href in all_sub_calegory_links:
        html = get_html(href)
        data = get_data_from_link(html, href)
        data_list.append(data)

    print(data_list)
    return data_list

def allthingsgreenwich_parser(url):
    print("Not complite")
    return

if __name__ == "__main__":
    url = url

    url = "https://www.royalgreenwich.gov.uk/directory_record/173454/clocktower_market/category/150/venues"
    a = get_html(url)
    a = get_data_from_link(a, url)
    print(a)
    exit()

    # if "royalgreenwich.gov.uk" in url:
    #     royalgreenwich_parser(url)

    # elif "allthingsgreenwich.co.uk" in url:
    #     allthingsgreenwich_parser(url)

