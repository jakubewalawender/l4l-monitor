from typing import List

from pydantic import BaseModel


class Product(BaseModel):
    products_id: str
    name: str
    name_pl: str
    pr_name: str
    net_price: str
    products_price_brutto: str
    promotions_price_brutto: str
    quantity: int
    products_model: str
    ean: str
    currency: str
    main_category_path: str
    main_category_path_pl: str
    gross_price: str
    promotions_gross_price: str
    payment_gross_price: str
    url: str
    images: List[str]
    main_image: str


class SearchResult(BaseModel):
    query_test: str
    products: List[Product]
    currency: str


class LuxuryForLessAPIResponse(BaseModel):
    search: List[SearchResult]
