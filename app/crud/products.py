from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..crud import productlines as productline_crud
from ..model import Product
from ..logger import logger

class ProductLineNotFoundError(ValueError):
    pass

def get_products(db: Session, skip: int = 0, limit: int = 100):
    try:
        logger.info(f"Fetching products with skip={skip}, limit={limit}")
        result = db.query(Product).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(result)} products")
        return result
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise

def get_product_by_id(db: Session, productcode: str):
    try:
        logger.info(f"Fetching product by ID: {productcode}")
        result = db.query(Product).filter(Product.productCode == productcode).first()
        if result:
            logger.info(f"Product found: {productcode}")
        else:
            logger.warning(f"Product not found: {productcode}")
        return result
    except Exception as e:
        logger.error(f"Error fetching product {productcode}: {e}")
        raise

def create_product(db: Session, product: Product):
    try:
        logger.info(f"Creating product: {product.productCode}")
        db.add(product)
        db.commit()
        db.refresh(product)
        logger.info(f"Product created: {product.productCode}")
        return product
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        db.rollback()
        raise

def update_product(db: Session, productcode: str, updates):
    try:
        logger.info(f"Updating product: {productcode} with updates: {updates}")
        if "productLine" in updates:
            product_line = updates["productLine"]
            if product_line is not None:
                existing_line = productline_crud.get_productline_by_id(db, product_line)
                if not existing_line:
                    raise ProductLineNotFoundError(f"ProductLine '{product_line}' does not exist")

        rows = db.query(Product).filter(Product.productCode == productcode).update(updates)
        if rows == 0:
            db.rollback()
            return None
        db.commit()
        result = get_product_by_id(db, productcode)
        logger.info(f"Product updated: {productcode}")
        return result
    except Exception as e:
        logger.error(f"Error updating product {productcode}: {e}")
        db.rollback()
        raise

def delete_product(db: Session, productcode: str):
    try:
        logger.info(f"Deleting product: {productcode}")
        rows = db.query(Product).filter(Product.productCode == productcode).delete()
        if rows == 0:
            db.rollback()
            return None
        db.commit()
        logger.info(f"Product deleted: {productcode}")
        return True
    except IntegrityError as e:
        logger.error(f"Foreign key error deleting product {productcode}: {e}")
        db.rollback()
        raise ValueError(
            f"Cannot delete product '{productcode}' because it is referenced by existing order details"
        )
    except Exception as e:
        logger.error(f"Error deleting product {productcode}: {e}")
        db.rollback()
        raise