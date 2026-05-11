import time
from fastapi import FastAPI, Request
from .routers import customers as router_customers, employees as router_employees, offices as router_offices, orders as router_orders, payments as router_payments, products as router_products, productlines as router_productlines, orderdetails as router_orderdetails, overall as router_overall
from .logger import logger

app = FastAPI(title="Customer API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request start: {request.method} {request.url.path}")
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000
    logger.info(
        f"Request complete: {request.method} {request.url.path} status={response.status_code} duration_ms={duration_ms:.2f}"
    )
    return response

app.include_router(router_overall.router)
app.include_router(router_customers.router)
app.include_router(router_products.router)
app.include_router(router_productlines.router)
app.include_router(router_offices.router)
app.include_router(router_employees.router)
app.include_router(router_orders.router)
app.include_router(router_orderdetails.router)
app.include_router(router_payments.router)


@app.get("/")
def root():
    return {"message": "API is online"}