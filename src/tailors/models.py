from sqlalchemy import Boolean, Column, String, DATETIME, TEXT, Enum, ForeignKey
from sqlalchemy_json import NestedMutableJson
from models import BaseUser, BaseModel, Gender, TailorType
from sqlalchemy.orm import relationship, Session

class Tailor(BaseUser):
    __tablename__ = "tailors"
    
    first_name = Column(String(60), nullable=True)
    last_name = Column(String(60), nullable=True)
    DOB = Column(DATETIME, nullable=True)
    brand_name = Column(String(60), nullable=True)
    about = Column(String(400), nullable=True)
    nin = Column(String(11), nullable=True, unique=True)
    cac_number = Column(String(20), nullable=True)
    bank_details = Column(NestedMutableJson, nullable=True)
    photo = Column(TEXT, nullable=True)
    nin_photo = Column(TEXT, nullable=True)
    is_available = Column(Boolean, default=False)
    is_enabled = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_suspended = Column(Boolean, default=False)
    nin_is_verified = Column(Boolean, default=False)
    last_active = Column(DATETIME, nullable=True)
    language = Column(NestedMutableJson, nullable=True)
    type = Column(Enum(TailorType), nullable=False, default=TailorType.tailor)

    products = relationship('Product', back_populates="tailor")
    orders = relationship("Order", back_populates="tailor")
    reviews = relationship("Review", backref="tailor", cascade="all, delete-orphan")

    def check_and_activate(self, db: Session):
        if all([
            self.first_name, self.last_name,
            self.nin_is_verified, self.about,
            self.brand_name, self.photo
        ]):
            self.is_enabled = True
            db.commit()


class Verification(BaseModel):
    __tablename__ = "verifications"
    
    tailor_id = Column(String(60), ForeignKey('tailors.id'), nullable=False)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    DOB = Column(DATETIME, nullable=False)
    vNIN = Column(String(60), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    photo = Column(TEXT, nullable=True)
    is_api_verified = Column(Boolean, default=False)
    status = Column(String(128), nullable=True)
    message = Column(TEXT, nullable=True)