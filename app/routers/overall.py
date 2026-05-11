import asyncio
import time
from fastapi import APIRouter
from ..database import SessionLocal
from ..crud import counts as crud
from ..schemas import overall as schemas
from ..logger import logger

router = APIRouter()

@router.get("/overall_counts", response_model=schemas.OverallCounts)
async def read_overall_counts():
    start_time = time.time()
    logger.info("Starting concurrent count aggregation")

    # Internal function to handle its own database session life cycle
    def get_count_with_own_session(count_func):
        db = SessionLocal()
        try:
            return count_func(db)
        finally:
            db.close()

    # Run all 8 queries simultaneously using their own private sessions
    results = await asyncio.gather(
        asyncio.to_thread(get_count_with_own_session, crud.count_customers),
        asyncio.to_thread(get_count_with_own_session, crud.count_orders),
        asyncio.to_thread(get_count_with_own_session, crud.count_products),
        asyncio.to_thread(get_count_with_own_session, crud.count_employees),
        asyncio.to_thread(get_count_with_own_session, crud.count_offices),
        asyncio.to_thread(get_count_with_own_session, crud.count_payments),
        asyncio.to_thread(get_count_with_own_session, crud.count_orderdetails),
        asyncio.to_thread(get_count_with_own_session, crud.count_productlines),
    )

    duration = time.time() - start_time
    logger.info(f"Aggregation completed in {duration:.4f} seconds")

    return {
        "customers": results[0], "orders": results[1], "products": results[2],
        "employees": results[3], "offices": results[4], "payments": results[5],
        "orderdetails": results[6], "productlines": results[7]
    }