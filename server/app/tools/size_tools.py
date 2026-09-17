def recommend_size(height_cm: float, weight_kg: float, available_sizes: tuple[str, ...]) -> str:
    bmi = weight_kg / ((height_cm / 100) ** 2)
    recommended = "S" if bmi < 18.5 else "M" if bmi < 24 else "L" if bmi < 28 else "XL"
    return recommended if recommended in available_sizes else available_sizes[0]
