from app.tools.catalog import PRODUCTS, Product


def search_products(
    scene: str,
    style: str | None,
    budget: int | None,
    excluded_colors: tuple[str, ...],
) -> list[Product]:
    candidates = [
        product
        for product in PRODUCTS
        if scene in product.scenes
        and product.stock > 0
        and (style is None or style in product.styles)
        and (budget is None or product.price <= budget)
        and any(color not in excluded_colors for color in product.colors)
    ]
    return sorted(candidates, key=lambda product: product.price, reverse=True)


def choose_available_color(product: Product, excluded_colors: tuple[str, ...]) -> tuple[str, str]:
    return next(
        (item for item in product.colors.items() if item[0] not in excluded_colors),
        next(iter(product.colors.items())),
    )
