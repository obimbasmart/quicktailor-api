from src.products.models.product import Fabric
from sqlalchemy.orm import Session

def _get_list_of_fabrics(db: Session):
    return db.query(Fabric).all()