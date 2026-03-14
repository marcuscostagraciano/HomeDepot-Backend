"""Products package.

Exports:
    router (APIRouter): FastAPI router for product endpoints.

        Endpoints:
        - GET /products/ - List products with filtering, searching, and sorting
        - POST /products/ - Create a new product
        - GET /products/{product_id} - Retrieve a specific product
        - PUT /products/{product_id} - Update an existing product
        - DELETE /products/{product_id} - Delete a product

        Supports filtering by brand, price range, and full-text search.
        Prefix: /products | Tags: ['products']
"""

from .routers import router

__all__ = ["router"]
