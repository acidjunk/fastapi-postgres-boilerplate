from server.crud.base import CRUDBase
from server.db.models import ProductTypesTable
from server.schemas.product_type import ProductTypeCreate, ProductTypeUpdate


class CRUDProductType(CRUDBase[ProductTypesTable, ProductTypeCreate, ProductTypeUpdate]):
    pass


product_type_crud = CRUDProductType(ProductTypesTable)
