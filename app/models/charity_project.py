from sqlalchemy import Column, String, Text

from app.constants import NAME_MAX_LEN
from app.models.base import PreBaseCommonDonationCharity


class CharityProject(PreBaseCommonDonationCharity):
    name = Column(String(NAME_MAX_LEN), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Сбор "{self.name}" {super().__repr__()}'
        )
