from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    category: str
    scenes: tuple[str, ...]
    styles: tuple[str, ...]
    price: int
    colors: dict[str, str]
    sizes: tuple[str, ...]
    stock: int


PRODUCTS = (
    Product(
        id="garment-shirt-001",
        name="清爽通勤衬衫",
        category="top",
        scenes=("interview", "commute"),
        styles=("formal", "minimal"),
        price=299,
        colors={"白": "#f4f3ee", "蓝": "#54728c"},
        sizes=("S", "M", "L", "XL"),
        stock=18,
    ),
    Product(
        id="garment-jacket-001",
        name="轻量都市夹克",
        category="outerwear",
        scenes=("interview", "commute", "date"),
        styles=("formal", "minimal", "casual"),
        price=499,
        colors={"灰": "#626a6d", "绿": "#27695c"},
        sizes=("S", "M", "L", "XL"),
        stock=9,
    ),
    Product(
        id="garment-tee-001",
        name="舒适基础上衣",
        category="top",
        scenes=("sport", "campus", "date", "party"),
        styles=("casual", "active", "minimal"),
        price=159,
        colors={"绿": "#27695c", "红": "#c8553d", "白": "#f4f3ee"},
        sizes=("S", "M", "L", "XL"),
        stock=32,
    ),
)
