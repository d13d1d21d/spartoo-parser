from enum import Enum
from dataclasses import dataclass, asdict

class Selectors(Enum):
    TOP_BRANDS = "div[id*='topBrand']"
    STYLE_FILTER = "div[id='style']"
    PRODUCT_LIST = "div[class='productsList']"
    PRODUCT_CARD = "div[class='prodcardBase']"
    SCHEMA = "script[type='application/ld+json']"
    DESCRIPTION = "span[id*='products_description']"
    PRODUCT_IMAGES = "div[class*='productView']"
    SIZE_LIST = "ul[id*='display_size']"

class BrandIDType(Enum):
    MARQUE = "marque"
    UNIVERSE = "universe"

@dataclass
class BrandID:
    id_type: BrandIDType
    id: str
    url: str

@dataclass
class ProductFilters:
    type: int
    extended: int

    def as_params(self) -> str:
        params = []
        for x, y in asdict(self).items():
            params.append(f"{x}={y}")

        return "&".join(params)
    
@dataclass
class ProductData:
    url: str
    sku: str
    spu: str
    name: str
    brand: str
    category: str
    price: int
    in_stock: int
    color: str
    color_origin: str
    size: str
    images: str
    description: str

COLORS = {
    "Weiss": "белый",
    "Blau": "голубой",
    "Grau": "серый",
    "Schwarz": "черный",
    "Braun": "коричневый",
    "Rot": "красный",
    "Silber": "серебряный",
    "Marine": "морской",
    "Bunt": "разноцветный",
    "Beige": "бежевый",
    "Kaki": "хаки",
    "Orange": "оранжевый",
    "Rosa": "розовый",
    "Bordeaux": "бордовый",
    "Violett": "фиолетовый",
    "Grün": "зелёный",
    "Gold": "золотой",
    "Creme": "кремовый",
    "Gelb": "желтый",
    "Cognac": "коричневый",
    "Maulwurf": "коричневый",
    "Multicolor": "разноцветный",
    "Other": "другой",
    "Silbern": "серебряный",
    "Leopard": "разноцветный",
    "Camel": "темно-бежевый",
    "Bronze": "бронза",
    "Multifarben": "разноцветный",
    "Malvenfarben": "лиловый",
    "Fuchsienrot": "розовый",
    "Pfirsisch": "светло-желтый",
    "Champagne": "оранжевый",
    "Goldfarben": "золотой",
    "Navy": "темно-синий",
    "Lila": "лиловый",
    "Glitterfarbe": "глиттер",
    "Olive": "оливковый",
    "Flamme": "светло-оранжевый",
    "Mustard": "оранжевый",
    "Senf": "оранжевый",
    "Schattengrau": "серый",
    "Capretto": "бежевый",
    "Elfenbein": "кремовый",
    "Platin": "светло-серый"
}

EXCLUDED_BRANDS = [
    "https://www.spartoo.de/adidas.php",
    "https://www.spartoo.de/Puma-b36.php",
    "https://www.spartoo.de/Nike-b4.php",
    "https://www.spartoo.de/New-Balance-b337.php",
    "https://www.spartoo.de/Converse-b5.php",
    "https://www.spartoo.de/Crocs-b508.php",
    "https://www.spartoo.de/Timberland-b103.php",
    "https://www.spartoo.de/Asics-b63.php",
    "https://www.spartoo.de/Guess-b775.php"
]

LAST_IN_STOCK = "Letzter vorrätiger Artikel"