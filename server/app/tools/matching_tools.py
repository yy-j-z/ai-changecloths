from app.tools.catalog import Product


def check_outfit_compatibility(product: Product, scene: str, color: str) -> str:
    if scene not in product.scenes:
        return "场景匹配度不足"
    if scene == "interview" and color == "红":
        return "面试场景建议降低高饱和色面积"
    return "场景、风格和配色检查通过"
