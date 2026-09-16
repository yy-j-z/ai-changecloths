import pytest

from app.services.size_recommendation import recommend_size


@pytest.mark.parametrize(
    ("height_cm", "weight_kg", "expected"),
    [(170, 50, "S"), (170, 65, "M"), (170, 75, "L"), (170, 90, "XL")],
)
def test_size_bands(height_cm: float, weight_kg: float, expected: str) -> None:
    assert recommend_size(height_cm, weight_kg) == expected


def test_invalid_measurement() -> None:
    with pytest.raises(ValueError):
        recommend_size(0, 65)
