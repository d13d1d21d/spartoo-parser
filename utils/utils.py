from __future__ import annotations
import pandas as pd

from functools import wraps
from inspect import signature
from collections.abc import Callable


def debug(info: str, raise_exc: bool = False, **d_kwargs) -> any:
    def debug_wrapper(f: Callable[..., any]) -> any:
        @wraps(f)
        def debug_wrapped(*args, **kwargs) -> any:
            try: return f(*args, **kwargs)
            except Exception as debug_exc:
                sig = signature(f)
                ba = sig.bind(*args, **kwargs)
                print(info.format(debug_exc=debug_exc, **d_kwargs, **ba.arguments))
                if raise_exc: raise debug_exc

        return debug_wrapped
    
    return debug_wrapper

def create_df(products: list[ProductData], stocks: bool, prefix: str):
    if stocks:
        data = {
            "url": [],
            "brand": [],
            "shop_sku": [],
            "newmen_sku": [],
            "in_stock": [],
            "price": []
        }
    else:
        data = {
            "url": [],
            "artikul": [],
            "shop_sku": [],
            "newmen_sku": [],
            "bundle_id": [],
            "product_name": [],
            "producer_size": [],
            "price": [],
            "price_before_discount": [],
            "base_type": [],
            "commercial_type": [],
            "brand": [],
            "origin_color": [],
            "color_rgb": [],
            "color": [],
            "manufacturer": [],
            "main_photo": [],
            "additional_photos": [],
            "number": [],
            "vat": [],
            "ozon_id": [],
            "gtin": [],
            "weight_in_pack": [],
            "pack_width": [],
            "pack_length": [],
            "pack_height": [],
            "images_360": [],
            "note": [],
            "keywords": [],
            "in_stock": [],
            "card_num": [],
            "error": [],
            "warning": [],
            "num_packs": [],
            "origin_name": [],
            "category": [],
            "content_unit": [],
            "net_quantity_content": [],
            "instruction": [],
            "info_sheet": [],
            "product_description": [],
            "non_food_ingredients_description": [],
            "application_description": [],
            "company_address_description": [],
            "care_label_description": [],
            "country_of_origin_description": [],
            "warning_label_description": [],
            "sustainability_description": [],
            "required_fields_description": [],
            "additional_information_description": [],
            "hazard_warnings_description": [],
            "leaflet_description": []
        }

    for i in products:
        if stocks:
            data["url"].append(i.url)
            data["brand"].append(i.brand)
            data["shop_sku"].append(i.sku)
            data["newmen_sku"].append(prefix + i.sku)
            data["in_stock"].append(i.in_stock)
            data["price"].append(i.price)
        else:
            if not i.images: i.images = [""]

            data["url"].append(i.url)
            data["artikul"].append(i.sku)
            data["shop_sku"].append(i.sku)
            data["newmen_sku"].append(prefix + i.sku)
            data["bundle_id"].append(i.spu)
            data["product_name"].append(i.name)
            data["producer_size"].append(i.size)
            data["price"].append(i.price)
            data["price_before_discount"].append("")
            data["base_type"].append("")
            data["commercial_type"].append("")
            data["brand"].append(i.brand)
            data["origin_color"].append(i.color_origin)
            data["color_rgb"].append("")
            data["color"].append(i.color)
            data["manufacturer"].append("")
            data["main_photo"].append(i.images[0])
            data["additional_photos"].append(",".join(i.images[1:]))
            data["number"].append("")
            data["vat"].append("")
            data["ozon_id"].append("")
            data["gtin"].append("")
            data["weight_in_pack"].append("")
            data["pack_width"].append("")
            data["pack_length"].append("")
            data["pack_height"].append("")
            data["images_360"].append("")
            data["note"].append("")
            data["keywords"].append("")
            data["in_stock"].append(i.in_stock)
            data["card_num"].append("")
            data["error"].append("")
            data["warning"].append("")
            data["num_packs"].append("")
            data["origin_name"].append(i.name)
            data["category"].append(i.category)
            data["content_unit"].append("")
            data["net_quantity_content"].append("")
            data["instruction"].append("")
            data["info_sheet"].append("")
            data["product_description"].append(i.description)
            data["non_food_ingredients_description"].append("")
            data["application_description"].append("")
            data["company_address_description"].append("")
            data["care_label_description"].append("")
            data["country_of_origin_description"].append("")
            data["warning_label_description"].append("")
            data["sustainability_description"].append("")
            data["required_fields_description"].append("")
            data["additional_information_description"].append("")
            data["hazard_warnings_description"].append("")
            data["leaflet_description"].append("")

    return pd.DataFrame(data)