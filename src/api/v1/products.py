from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Optional, List
from src.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from src.services import product_service
from src.api.deps import get_current_user
from prisma.models import User
import math

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new product (protected endpoint)."""
    try:
        product = await product_service.create_product(product_data)
        return ProductResponse(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price,
            category=product.category,
            imageUrl=product.imageUrl,
            createdAt=product.createdAt,
            updatedAt=product.updatedAt
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating product"
        )


@router.get("", response_model=dict)
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    sort: Optional[str] = Query(None, regex="^(price_asc|price_desc)$")
):
    """Get all products with pagination, search, filter, and sort."""
    skip = (page - 1) * page_size
    
    try:
        products, total = await product_service.get_products(
            skip=skip,
            limit=page_size,
            search=search,
            category=category,
            sort=sort
        )
        
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        
        return {
            "data": [
                ProductResponse(
                    id=p.id,
                    title=p.title,
                    description=p.description,
                    price=p.price,
                    category=p.category,
                    imageUrl=p.imageUrl,
                    createdAt=p.createdAt,
                    updatedAt=p.updatedAt
                ) for p in products
            ],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching products"
        )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get a single product by ID."""
    try:
        product = await product_service.get_product_by_id(product_id)
        return ProductResponse(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price,
            category=product.category,
            imageUrl=product.imageUrl,
            createdAt=product.createdAt,
            updatedAt=product.updatedAt
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching product"
        )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a product (protected endpoint)."""
    try:
        product = await product_service.update_product(product_id, product_data)
        return ProductResponse(
            id=product.id,
            title=product.title,
            description=product.description,
            price=product.price,
            category=product.category,
            imageUrl=product.imageUrl,
            createdAt=product.createdAt,
            updatedAt=product.updatedAt
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating product"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a product (protected endpoint)."""
    try:
        await product_service.delete_product(product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting product"
        )
