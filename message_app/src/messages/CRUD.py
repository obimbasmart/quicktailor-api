from fastapi import  HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from message_app.src.messages.dependencies import verify_by_id, get_user_by_id
from message_app.src.messages.models import Message
from message_app.models import User
from message_app.src.messages.schemas import UserInfo, SendMessageData, UpdateMessage
from message_app.models import UserType

def create_new_message(message_data:SendMessageData, from_user_id:str, to_user_id:str, db:Session):

    data = {k: v for k, v in message_data if v is not None and k != 'message_key'}
    
    if message_data.product:
        data['product'] = message_data.product.dict()
    sender = verify_by_id(from_user_id, db)
    reciever = verify_by_id(to_user_id, db)
    if sender.user_type != UserType.ADMIN:
        if sender.user_type == reciever.user_type:
            raise HTTPException(status_code=400, detail="This type of conversation is not allowed")
    if sender.user_type == UserType.TAILOR  and reciever.user_type != UserType.ADMIN:
        check_message = db.query(Message).filter(Message.from_user_id == reciever.user_id, Message.to_user_id ==sender.user_id).all()
        if not check_message:
            raise HTTPException(status_code=401, detail="Unauthorized access")
    
    print("This is the check Message ", sender.user_type)
    if sender.message_key != message_data.message_key:
        raise HTTPException(status_code=422, detail="Invalid Message Key")
    if not data:
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    new_message = Message(**data, from_user_key = message_data.message_key, from_user_id=from_user_id, to_user_id=to_user_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def update_message(update_data: UpdateMessage, from_user_id: str, message_id: str, db: Session):
    
    sender = verify_by_id(from_user_id, db)

    message = db.query(Message).filter(Message.id == message_id).one_or_none()
   
    if update_data.message_key != message.from_user_key or from_user_id != message.from_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    if message:
        time_difference = datetime.utcnow() - message.created_at
        if time_difference > timedelta(minutes=2):
            raise HTTPException(status_code=400, detail="Cannot update message after 1 minute of creation.")

        message.content = update_data.content 
        
        db.commit()
        db.refresh(message)
        
        return message
    else:
        raise HTTPException(status_code=404, detail="Message not found.") 


def is_viewed(message_id: str, to_user_id, db: Session):

   message = db.query(Message).filter(Message.id == message_id).one_or_none()
   if message.to_user_id != to_user_id:
       raise HTTPException(status_code=401, detail="Unauthorized request")
   if message:
       message.is_viewed = True
       db.commit()
       db.refresh(message)
       return message
   else:
       raise HTTPException(status_code=404, detail="Message not found.")


def get_last_messages_list(user_id, db):
    sender = verify_by_id(user_id, db)
    
    message_list = Message.get_last_messages(user_id, db)
    
    return (message_list)


def create_new_user(user_data:UserInfo, db:Session):
    
    check_user = get_user_by_id(user_data.user_id, db)

    if check_user:
        raise HTTPException(status_code=409, detail="user already registered")
    new_user = User(**user_data.model_dump())
 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_message_history(from_user_id:str, to_user_id:str, db:Session):
    
    sender = verify_by_id(from_user_id, db)
    reciever = verify_by_id(to_user_id, db)
    
    if sender.user_type != UserType.ADMIN:
        if sender.user_type == reciever.user_type:
            raise HTTPException(status_code=400, detail="This type of conversation is not allowed")
    
    message1 = db.query(Message).filter(from_user_id == Message.from_user_id, to_user_id == Message.to_user_id).all()
    message2 = db.query(Message).filter(to_user_id == Message.from_user_id, from_user_id == Message.to_user_id).all()
    return message1+message2
