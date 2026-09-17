from app.schemas.assistant import OutfitAction
from app.tools.catalog import Product


def apply_outfit(product: Product, size: str, color: str, color_hex: str) -> OutfitAction:
    """Create a validated command for the frontend 3D avatar."""
    return OutfitAction(
        garment_id=product.id,
        garment_name=product.name,
        size=size,
        color=color,
        color_hex=color_hex,
    )
