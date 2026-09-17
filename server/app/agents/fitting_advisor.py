from uuid import uuid4

from app.agents.contracts import AdvisorIntent, IntentPlanner
from app.agents.factory import create_intent_planner
from app.schemas.assistant import AdvisorRequest, AdvisorResponse, ToolEvent
from app.tools.avatar_tools import apply_outfit
from app.tools.matching_tools import check_outfit_compatibility
from app.tools.product_tools import choose_available_color, search_products
from app.tools.size_tools import recommend_size


class FittingAdvisor:
    """Coordinates a constrained tool-calling workflow for outfit recommendations."""

    def __init__(self, planner: IntentPlanner | None = None) -> None:
        self.planner = planner or create_intent_planner()

    def _search_with_fallback(
        self, intent: AdvisorIntent
    ) -> tuple[list, list[ToolEvent], int]:
        """Search products with up to three relaxed attempts.

        Returns (products, events, fallback_level) where fallback_level is:
        0 = matched on first attempt, 1 = budget relaxed, 2 = style relaxed.
        """
        events: list[ToolEvent] = []

        products = search_products(
            scene=intent.scene,
            style=intent.style,
            budget=intent.budget,
            excluded_colors=intent.excluded_colors,
        )
        events.append(
            ToolEvent(
                tool="search_products",
                label="查询商品库",
                summary=f"找到 {len(products)} 件符合场景、预算和库存条件的商品",
            )
        )
        if products:
            return products, events, 0

        relaxed_budget = intent.budget * 2 if intent.budget else None
        products = search_products(
            scene=intent.scene,
            style=intent.style,
            budget=relaxed_budget,
            excluded_colors=intent.excluded_colors,
        )
        events.append(
            ToolEvent(
                tool="search_products",
                label="放宽预算重新查询",
                summary=(
                    f"预算放宽至 ¥{relaxed_budget} 后找到 {len(products)} 件"
                    if products
                    else "放宽预算后仍无合适商品"
                ),
            )
        )
        if products:
            return products, events, 1

        products = search_products(
            scene=intent.scene,
            style=None,
            budget=None,
            excluded_colors=intent.excluded_colors,
        )
        events.append(
            ToolEvent(
                tool="search_products",
                label="放宽风格限制重新查询",
                summary=(
                    f"仅按场景查询找到 {len(products)} 件替代款"
                    if products
                    else "当前场景下无可用商品"
                ),
            )
        )
        return products, events, 2

    def respond(self, request: AdvisorRequest) -> AdvisorResponse:
        conversation_id = request.conversation_id or str(uuid4())
        context = " ".join(message.content for message in request.history[-6:])
        intent = self.planner.understand(f"{context} {request.message}")

        if intent.scene is None:
            return AdvisorResponse(
                conversation_id=conversation_id,
                state="needs_input",
                reply="你准备在什么场合穿？例如面试、通勤、约会、运动或校园。",
            )

        products, events, fallback_level = self._search_with_fallback(intent)

        if not products:
            return AdvisorResponse(
                conversation_id=conversation_id,
                state="needs_input",
                reply="当前条件下没有合适且有库存的商品。可以提高预算或放宽风格要求吗？",
                tool_events=events,
            )

        product = products[0]
        size = recommend_size(request.user_height_cm, request.user_weight_kg, product.sizes)
        events.append(
            ToolEvent(
                tool="recommend_size",
                label="计算推荐尺码",
                summary=f"根据身高和体重建议 {size} 码",
            )
        )

        color, color_hex = choose_available_color(product, intent.excluded_colors)
        compatibility = check_outfit_compatibility(product, intent.scene, color)
        events.append(
            ToolEvent(
                tool="check_outfit_compatibility",
                label="检查搭配规则",
                summary=compatibility,
            )
        )

        action = apply_outfit(product, size, color, color_hex)
        events.append(
            ToolEvent(
                tool="apply_outfit",
                label="应用到 3D 数字人",
                summary=f"已换上{product.name}，{color}，{size} 码",
            )
        )
        budget_text = f"，价格 ¥{product.price}" if intent.budget is not None else ""
        fallback_note = ""
        if fallback_level == 1:
            fallback_note = "原预算内没有完全合适的，已为你放宽预算找到替代款。"
        elif fallback_level == 2:
            fallback_note = "原条件下没有完全合适的，已为你放宽风格和预算找到替代款。"
        return AdvisorResponse(
            conversation_id=conversation_id,
            state="completed",
            reply=(
                f"{fallback_note}我为你选择了{color}{product.name}{budget_text}，推荐 {size} 码。"
                "已经穿到数字人上了；要不要再换一种颜色？"
            ),
            tool_events=events,
            outfit_action=action,
        )


fitting_advisor = FittingAdvisor()
