from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from database import Base
import enum

class PushNotificationEnum(str, enum.Enum):
    everything = "everything"
    email = "email"
    none = "none"

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    about = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    country = Column(String)
    street_address = Column(String)
    city = Column(String)
    region = Column(String)
    postal_code = Column(String)
    notify_comments = Column(Boolean, default=True)
    notify_candidates = Column(Boolean, default=False)
    notify_offers = Column(Boolean, default=False)
    push_notifications = Column(String)

    # store actual files
    photo = Column(LargeBinary, nullable=True)
    cover_photo = Column(LargeBinary, nullable=True)
