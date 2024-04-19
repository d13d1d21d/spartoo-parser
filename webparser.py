import re
import json

from colorama import Fore, Style
from html import unescape
from bs4 import BeautifulSoup as bs
from proxy_client import *
from utils.structures import *
from utils.utils import *


class Parser:
    BASE_URL = "https://www.spartoo.de"
    PER_PAGE = 144

    def __init__(self, proxy_client: ProxyClient) -> None:
        self.proxy_client = proxy_client
        self.vues = "ABCDEFG"

    @staticmethod
    def get_product_id(product_url: str) -> str:
        if match := re.search(r"-x(\d+).php", product_url):
            return match.group(1)
        
        return ""

    @debug(f"[{Fore.RED + Style.BRIGHT}X{Style.RESET_ALL}] Ошибка в получении списка брендов" + "\n{debug_exc}", True)
    def get_top_100_urls(self) -> list[str]:
        html = bs(
            self.proxy_client.retry("GET", self.BASE_URL).text,
            "html.parser"
        )
        return list(set(
            f"{self.BASE_URL}/{i.get("href")}"
            for i in html.select_one(Selectors.TOP_BRANDS.value).find_all("a")
        ))
    
    @debug(f"[{Fore.RED + Style.BRIGHT}X{Style.RESET_ALL}] Ошибка в получении ID для " + "{brand_url}\n{debug_exc}", True)
    def get_brand_id(self, brand_url: str) -> str:
        if not (match := re.search(r"-b(\d+)", brand_url)):
            html = bs(
                self.proxy_client.retry("GET", brand_url).text,
                "html.parser"
            )
            return BrandID(
                BrandIDType.UNIVERSE,
                re.search(r"st-(\d+)-", html.select_one(Selectors.STYLE_FILTER.value).find("a").get("href")).group(1),
                brand_url
            )
             
        return BrandID(BrandIDType.MARQUE, match.group(1), brand_url)
    
    @debug(f"[{Fore.RED + Style.BRIGHT}X{Style.RESET_ALL}] Ошибка в получении кол-ва продуктов для бренда " + "{BrandID}\n{debug_exc}", True)
    def get_n_products(self, brand_id: BrandID, filters: ProductFilters) -> int:
        return self.proxy_client.retry(
            "GET",
            f"{self.BASE_URL}/ajax/product_list_filters.php?{filters.as_params()}&{brand_id.id_type.value}={brand_id.id}"
        ).json().get("available_filters").get("count")
    
    @debug(f"[{Fore.RED + Style.BRIGHT}X{Style.RESET_ALL}] Ошибка в получении товаров " + "{url}?&offset={offset}\n{debug_exc}")
    def get_product_urls(self, url: str, filters: ProductFilters, offset: int) -> list[str]:
        html = bs(
            self.proxy_client.retry(
                "GET", 
                f"{url}?{filters.as_params()}&offset={offset}"
            ).text,
            "html.parser"
        )
        if product_list := html.select(Selectors.PRODUCT_LIST.value + "> div > a[onmouseup]"):
            return list(
                f"{self.BASE_URL}/{i.get("href")}"
                for i in product_list
            )
        
        return []
    
    @debug(f"    > [{Fore.RED + Style.BRIGHT}X{Style.RESET_ALL}] Ошибка в парсинге " + "URL: {url}. Похоже, этот товар больше не доступен")
    def get_product_data(self, url: str) -> ProductData:
        spu = self.get_product_id(url)
        products = []

        if req := self.proxy_client.retry("GET", url):
            if html := bs(req.text, "html.parser"):
                max_img_size = re.search(r"_(\d+)_", html.select_one(Selectors.MAIN_PHOTO.value).get("src")).group(1)
                images = list(i.get("src").replace("_40_", f"_{max_img_size}_") for i in html.select(Selectors.PRODUCT_IMAGES.value + ">a>img[id]"))
                product_card = html.select_one(Selectors.PRODUCT_CARD.value)
                name_color = product_card.find("div", { "class": "productNameColor" })

                price = float(html.select_one("span[itemprop='price']").get("content"))
                brand = product_card.find("div", { "itemprop": "brand" }).get("content")
                color_origin = name_color.find("span", { "itemprop": "color" }).text.strip().replace(" ", "")
                color = "/".join(COLORS.get(i.title(), "не определено") for i in color_origin.split("/"))
                if not (name := name_color.find("span", { "itemprop": "name" }).text.strip().replace("_", " ")):
                    name = json.loads(html.select_one(Selectors.SCHEMA.value).text).get("itemListElement")[-1].get("item").get("name").strip()
                
                category = ">".join(
                    i.get("item").get("name").strip()
                    for i in json.loads(html.select_one(Selectors.SCHEMA.value).text).get("itemListElement")[:4]
                )

                if description := html.select_one(Selectors.DESCRIPTION.value):
                    description= unescape(description.text.strip().replace("\n", ""))
                else: description = ""

                if size_info := html.select(Selectors.SIZE_LIST.value + ">li"):
                    for i in size_info:
                        if LAST_IN_STOCK in i.text: in_stock = 1
                        else: in_stock = 2

                        size = i.select_one("div[class*='size_name']").text.strip()
                        size_id = i.select_one("input").get("value")

                        products.append(
                            ProductData(
                                url + f"?size_id={size_id}",
                                spu + size_id,
                                spu,
                                name,
                                brand,
                                category,
                                price,
                                in_stock,
                                color,
                                color_origin,
                                size,
                                images,
                                description
                            )
                        )

            return products
