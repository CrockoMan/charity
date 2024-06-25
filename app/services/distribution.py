from datetime import datetime

from app.schemas.charity_project import CharityDB


def donate_distribution(
        new_rec: CharityDB,
        unclosed: list[CharityDB],
):
    changed_records = set()
    if new_rec.invested_amount is None:
        new_rec.invested_amount = 0
    for unclosed_item in unclosed:
        investment_amount = min(
            unclosed_item.full_amount - unclosed_item.invested_amount,
            new_rec.full_amount - new_rec.invested_amount
        )
        for changed_object in (unclosed_item, new_rec):
            changed_object.invested_amount += investment_amount
            if changed_object.full_amount == changed_object.invested_amount:
                changed_object.fully_invested = True
                changed_object.close_date = datetime.now()
        changed_records.add(unclosed_item)
        if new_rec.fully_invested is True:
            break
    return changed_records
