from datetime import datetime

from app.models.abstract import CommonFieldsModel


def invest(
        target: CommonFieldsModel,
        sources: list[CommonFieldsModel],
) -> list[CommonFieldsModel]:
    modified_sources = []
    target.invested_amount = (
        0 if not target.invested_amount else target.invested_amount
    )
    for source in sources:
        amount = min(
            (source.full_amount - source.invested_amount),
            (target.full_amount - target.invested_amount)
        )
        if amount == 0:
            break
        for obj in [target, source]:
            obj.invested_amount += amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = 1
                obj.close_date = datetime.now()
                if obj.create_date is None:
                    obj.create_date = obj.close_date
        modified_sources.append(source)
    return modified_sources
