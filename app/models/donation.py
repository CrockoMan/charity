from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import PreBaseCommonDonationCharity


class Donation(PreBaseCommonDonationCharity):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Донат "{self.name}" {super().__repr__()}'
        )
