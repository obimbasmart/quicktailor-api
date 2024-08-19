
from src.auth.schemas import TailorRegIn
from src.tailors.schemas import UpdateTailor, VerificationInfo
from .models import Tailor, Verification
from sqlalchemy.orm import Session
from fastapi import File
from utils import generate_uuid
from exceptions import bad_request_exception
from src.storage.aws_s3_storage import s3_client


def create_tailor(tailor: TailorRegIn, db: Session):
    new_tailor = Tailor(**tailor.model_dump(exclude="password"))

    new_tailor.set_password(tailor.password)
    new_tailor.message_key = generate_uuid()

    # TODO: sychronize tailor to message service

    db.add(new_tailor)
    db.commit()
    db.refresh(new_tailor)
    return new_tailor


def get_tailors(db: Session, filters: dict = None):
    return db.query(Tailor).all()


def _update_tailor(tailor: Tailor, req_body: UpdateTailor, db: Session):
    update_data = req_body.model_dump(exclude_unset=True)

    [
        setattr(tailor, attr, value)
        for attr, value in update_data.items()
        if attr not in ['first_name', 'last_name']
    ]

    if not tailor.nin_is_verified:
        [
            setattr(tailor, attr, value)
            for attr, value in update_data.items()
            if attr in ['first_name', 'last_name']
        ]

    tailor.check_and_activate(db)

    db.commit()
    db.refresh(tailor)
    return tailor


def _upload_verification_details(tailor: Tailor,
                                 details: VerificationInfo,
                                 db: Session):

    if tailor.nin_is_verified:
        raise bad_request_exception('NIN is already verfied for this tailor')

    verification_item = db.query(Verification).filter(
        Verification.tailor_id == tailor.id).one_or_none()

    if verification_item:
        tailor_details = _update_verification_details(verification_item, details, db)
    else:
        tailor_details = Verification(**details.model_dump(), tailor_id=tailor.id)
        db.add(tailor_details)

    # TODO: run api verifcation background task and save info to db
    # ..........

    db.commit()
    db.refresh(tailor_details)
    return tailor_details


def _upload_verification_photo(tailor: Tailor,
                               photo: File,
                               db: Session):

    if tailor.nin_is_verified:
        raise bad_request_exception('NIN is already verfied for this tailor')

    details = db.query(Verification).filter(
        Verification.tailor_id == tailor.id).one_or_none()

    if details:
        key_name = s3_client.upload_file(photo, tailor.id, "verfication-photos")
        details.photo = key_name
        # TODO: upload photo to s3 client, return url save to database


    db.commit()
    db.refresh(details)
    return details


def _update_verification_details(verification_item: Verification,
                                 req_body: VerificationInfo,
                                 db: Session):

    update_data = req_body.model_dump()

    print(update_data)

    [
        setattr(verification_item, attr, val)
        for attr, val in update_data.items()
    ]

    return verification_item
