import re

from app.agents.contracts import AdvisorIntent


class DemoIntentPlanner:
    """Deterministic planner used for local development and stable classroom demos."""

    scene_keywords = {
        "面试": "interview",
        "通勤": "commute",
        "上班": "commute",
        "约会": "date",
        "运动": "sport",
        "校园": "campus",
        "聚会": "party",
    }
    style_keywords = {
        "正式": "formal",
        "简约": "minimal",
        "休闲": "casual",
        "活力": "active",
        "韩系": "korean",
    }
    colors = ("黑", "白", "蓝", "绿", "红", "灰")

    def understand(self, message: str) -> AdvisorIntent:
        scene = next(
            (value for keyword, value in self.scene_keywords.items() if keyword in message),
            None,
        )
        style = next(
            (value for keyword, value in self.style_keywords.items() if keyword in message),
            None,
        )
        budget_match = re.search(r"(?:预算|不超过|以内)[^0-9]*(\d{2,5})", message)
        excluded = tuple(
            color
            for color in self.colors
            if f"不要{color}" in message or f"不想穿{color}" in message
        )
        return AdvisorIntent(
            scene=scene,
            style=style,
            budget=int(budget_match.group(1)) if budget_match else None,
            excluded_colors=excluded,
        )
