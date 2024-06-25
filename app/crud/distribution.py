from datetime import datetime

from app.schemas.charity_project import CharityDB


def donate_distribution(
        new_rec: CharityDB,
        unclosed: list[CharityDB],
):
    changed_records = set()
    if new_rec.invested_amount is None:
        new_rec.invested_amount = 0
    for one_unclosed in unclosed:
        investment_amount = min(
            one_unclosed.full_amount - one_unclosed.invested_amount,
            new_rec.full_amount - new_rec.invested_amount
        )
        for changed_object in (one_unclosed, new_rec):
            changed_object.invested_amount += investment_amount
            if changed_object.full_amount == changed_object.invested_amount:
                changed_object.fully_invested = True
                changed_object.close_date = datetime.now()
        changed_records.add(one_unclosed)
        if new_rec.fully_invested is True:
            break
    return changed_records
