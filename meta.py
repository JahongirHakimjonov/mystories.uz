from pprint import pprint

import requests
from bs4 import BeautifulSoup


def get_meta_data(url):
    try:
        # URL'dan sahifani yuklash
        response = requests.get(url)
        response.raise_for_status()  # Agar muammo bo'lsa, xato beradi

        # HTMLni tahlil qilish
        soup = BeautifulSoup(response.text, "html.parser")

        # Meta teglarni olish
        meta_tags = soup.find_all("meta")
        meta_data = {}

        for tag in meta_tags:
            # Agar meta teglarda "name" yoki "property" bo'lsa, uni saqlash
            if "name" in tag.attrs:
                meta_data[tag.attrs["name"]] = tag.attrs.get("content", "")
            elif "property" in tag.attrs:
                meta_data[tag.attrs["property"]] = tag.attrs.get("content", "")

        return meta_data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch URL: {e}"}


# Sinov uchun URL
url = "https://api.mystories.uz"
meta_data = get_meta_data(url)
pprint(meta_data)
