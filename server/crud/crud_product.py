from server.crud.base import CRUDBase
from server.db.models import ProductsTable
from server.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[ProductsTable, ProductCreate, ProductUpdate]):
    pass


product_crud = CRUDProduct(ProductsTable)
