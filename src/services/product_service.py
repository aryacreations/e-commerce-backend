from typing import List, Optional, Tuple
from prisma.models import Product
from src.repositories import product_repository
from src.schemas.product import ProductCreate, ProductUpdate


async def create_product(product_data: ProductCreate) -> Product:
    """Create a new product with validation."""
    if product_data.price <= 0:
        raise ValueError("Price must be greater than 0")
    
    product = await product_repository.create_product(
        title=product_data.title,
        description=product_data.description,
        price=product_data.price,
        category=product_data.category,
        image_url=product_data.imageUrl
    )
    
    return product


async def get_products(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    category: Optional[str] = None,
    sort: Optional[str] = None
) -> Tuple[List[Product], int]:
    """Get products with search, filter, sort, and pagination."""
    products = await product_repository.get_products(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        sort_by=sort
    )
    
    total = await product_repository.count_products(search=search, category=category)
    
    return products, total


async def get_product_by_id(product_id: str) -> Optional[Product]:
    """Get product by ID."""
    product = await product_repository.get_product_by_id(product_id)
    
    if not product:
        raise ValueError("Product not found")
    
    return product


async def update_product(product_id: str, product_data: ProductUpdate) -> Product:
    """Update a product with validation."""
    # Check if product exists
    existing_product = await product_repository.get_product_by_id(product_id)
    if not existing_product:
        raise ValueError("Product not found")
    
    # Validate price if provided
    if product_data.price is not None and product_data.price <= 0:
        raise ValueError("Price must be greater than 0")
    
    product = await product_repository.update_product(
        product_id=product_id,
        title=product_data.title,
        description=product_data.description,
        price=product_data.price,
        category=product_data.category,
        image_url=product_data.imageUrl
    )
    
    return product


async def delete_product(product_id: str) -> bool:
    """Delete a product."""
    # Check if product exists
    existing_product = await product_repository.get_product_by_id(product_id)
    if not existing_product:
        raise ValueError("Product not found")
    
    success = await product_repository.delete_product(product_id)
    return success
