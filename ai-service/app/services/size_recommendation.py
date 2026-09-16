def recommend_size(height_cm: float, weight_kg: float) -> str:
    """Return a demo size until brand-specific measurement tables are available."""
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("height and weight must be positive")

    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        return "S"
    if bmi < 24:
        return "M"
    if bmi < 28:
        return "L"
    return "XL"
