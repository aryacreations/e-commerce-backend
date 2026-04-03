import math
from typing import Tuple
from src.core.config import settings


def calculate_total_pages(total_items: int, page_size: int) -> int:
    """Calculate total number of pages."""
    if total_items == 0:
        return 0
    return math.ceil(total_items / page_size)


def validate_pagination_params(page: int, page_size: int) -> Tuple[int, int]:
    """Validate and normalize pagination parameters."""
    # Ensure page is at least 1
    if page < 1:
        page = 1
    
    # Ensure page_size is within allowed range
    if page_size < 1:
        page_size = settings.DEFAULT_PAGE_SIZE
    elif page_size > settings.MAX_PAGE_SIZE:
        page_size = settings.MAX_PAGE_SIZE
    
    return page, page_size


def calculate_skip(page: int, page_size: int) -> int:
    """Calculate skip value for database query."""
    return (page - 1) * page_size
