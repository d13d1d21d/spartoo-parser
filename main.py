import concurrent.futures
import platform

from colorama import Fore, Style, just_fix_windows_console
from proxy_client import *
from utils.structures import *
from webparser import Parser
from math import ceil


PREFIX = "SPT-"
if platform.system() == "Windows":
    just_fix_windows_console()


proxy_client = ProxyClient(
    map_proxies("http", open("proxy_list.txt").read().split("\n")),
    retries=5
)
parser = Parser(proxy_client)

print(f"[{Fore.CYAN + Style.BRIGHT}⧖{Style.RESET_ALL}] Получение брендов...")
brands = list(
    filter(
        lambda x: x not in EXCLUDED_BRANDS,
        parser.get_top_100_urls()
    )
)
brand_ids = dict((i, parser.get_brand_id(i)) for i in brands)
print(f"[{Fore.GREEN + Style.BRIGHT}✓{Style.RESET_ALL}] Получено {len(brand_ids)} брендов\n")

insert_headers = [True, True]
executor = concurrent.futures.ThreadPoolExecutor(50)
nb = 0

for k, v in brand_ids.items():
    nb += 1

    filters = ProductFilters(1, 1)
    n_pages = ceil(parser.get_n_products(v, filters) / Parser.PER_PAGE)
    urls = []
    
    print(f"[{Fore.CYAN + Style.BRIGHT}⧖{Style.RESET_ALL}] Получение URL товаров из {k}...")
    for page in range(n_pages):
        offset = page * Parser.PER_PAGE
        if product_urls := parser.get_product_urls(k, filters, offset):
            urls += product_urls

    if urls:
        print(f"[{Fore.GREEN + Style.BRIGHT}✓{Style.RESET_ALL}] Получено {len(urls)} URLs")

        n = 0
        products = []

        for variations in executor.map(parser.get_product_data, urls):
            if variations:
                products += variations
                n += 1
                if n % 100 == 0:
                    print(f"    > [{Fore.CYAN + Style.BRIGHT}{n}/{len(urls)}{Style.RESET_ALL}] Обработано {len(products)} вариаций")
        
        print(f"    > [{Fore.CYAN + Style.BRIGHT}{n}/{len(urls)}{Style.RESET_ALL}] Обработано {len(products)} вариаций")
        print(f"[{Fore.GREEN + Style.BRIGHT}{k.split("/")[-1].replace(".php", "")}{Style.RESET_ALL}: {Fore.CYAN + Style.BRIGHT}{nb}/{len(brand_ids)}{Style.RESET_ALL}] Запись {len(products)} вариаций\n")
        create_df(products, False, PREFIX).to_csv(
            "output/spartoo-products.csv",
            sep=";",
            index=False,
            encoding="utf-8",
            header=insert_headers[0], 
            mode="w" if insert_headers[0] else "a"
        )
        if insert_headers[0]: insert_headers[0] = False
        
        create_df(products, True, PREFIX).to_csv(
            "output/spartoo.csv",
            sep=";",
            index=False,
            encoding="utf-8",
            header=insert_headers[1], 
            mode="w" if insert_headers[1] else "a"
        )
        if insert_headers[1]: insert_headers[1] = False

    else:
        print(f"[{Fore.RED + Style.BRIGHT}X{Style.RESET_ALL}] Товары не найдены\n")
    
