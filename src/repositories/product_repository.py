from typing import List, Optional
from prisma.models import Product
from src.core.database import get_db


async def create_product(
    title: str,
    description: str,
    price: float,
    category: str,
    image_url: str
) -> Product:
    """Create a new product."""
    db = get_db()
    product = await db.product.create(
        data={
            "title": title,
            "description": description,
            "price": price,
            "category": category,
            "imageUrl": image_url
        }
    )
    return product


async def get_products(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    category: Optional[str] = None,
    sort_by: Optional[str] = None
) -> List[Product]:
    """Get products with pagination, search, filter, and sort."""
    db = get_db()
    
    where = {}
    
    # Search by title
    if search:
        where["title"] = {"contains": search, "mode": "insensitive"}
    
    # Filter by category
    if category:
        where["category"] = category
    
    # Sort configuration
    order = {}
    if sort_by == "price_asc":
        order = {"price": "asc"}
    elif sort_by == "price_desc":
        order = {"price": "desc"}
    else:
        order = {"createdAt": "desc"}
    
    products = await db.product.find_many(
        where=where,
        skip=skip,
        take=limit,
        order=order
    )
    
    return products


async def get_product_by_id(product_id: str) -> Optional[Product]:
    """Get product by ID."""
    db = get_db()
    product = await db.product.find_unique(where={"id": product_id})
    return product


async def update_product(
    product_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    category: Optional[str] = None,
    image_url: Optional[str] = None
) -> Optional[Product]:
    """Update a product."""
    db = get_db()
    
    data = {}
    if title is not None:
        data["title"] = title
    if description is not None:
        data["description"] = description
    if price is not None:
        data["price"] = price
    if category is not None:
        data["category"] = category
    if image_url is not None:
        data["imageUrl"] = image_url
    
    if not data:
        return await get_product_by_id(product_id)
    
    product = await db.product.update(
        where={"id": product_id},
        data=data
    )
    return product


async def delete_product(product_id: str) -> bool:
    """Delete a product."""
    db = get_db()
    try:
        await db.product.delete(where={"id": product_id})
        return True
    except:
        return False


async def count_products(
    search: Optional[str] = None,
    category: Optional[str] = None
) -> int:
    """Count total products matching filters."""
    db = get_db()
    
    where = {}
    if search:
        where["title"] = {"contains": search, "mode": "insensitive"}
    if category:
        where["category"] = category
    
    count = await db.product.count(where=where)
    return count
