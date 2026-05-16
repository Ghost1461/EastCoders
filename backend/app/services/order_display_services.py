from sqlalchemy import or_
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from collections import defaultdict
from datetime import datetime

from app.models.order_model import Order
from app.models.order_item import OrderItem



def serialize_order(order: Order):
    order_total_price = sum(
        item.quantity * item.unit_price
        for item in order.items
    )

    return {
        "id": order.id,
        "order_id": order.order_id,
        "owner_user_id": order.owner_user_id,
        "source_user_id": order.source_user_id,
        "platform": order.platform,
        "external_order_id": order.external_order_id,
        "customer_id": order.customer_id,
        "status": order.status,
        "order_date": order.order_date,

        "order_total_price": order_total_price,

        "items": [
            {
                "id": item.id,
                "listing_id": item.listing_id,
                "internal_product_id": item.internal_product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.quantity * item.unit_price
            }
            for item in order.items
        ]
    }


def base_order_query(db, current_user):
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.owner_user_id == current_user.id)
    )


def get_all_orders_service(db, current_user):
    orders = (
        base_order_query(db, current_user)
        .order_by(Order.order_date.desc())
        .all()
    )

    return {
        "total": len(orders),
        "orders": [serialize_order(order) for order in orders]
    }


def get_orders_by_platform_service(platform_key: str, db, current_user):
    platform_key = platform_key.lower()

    orders = (
        base_order_query(db, current_user)
        .filter(Order.platform == platform_key)
        .order_by(Order.order_date.desc())
        .all()
    )

    return {
        "platform": platform_key,
        "total": len(orders),
        "orders": [serialize_order(order) for order in orders]
    }




def get_orders_by_status_service(status: str, db, current_user):
    status = status.lower()

    orders = (
        base_order_query(db, current_user)
        .filter(Order.status == status)
        .order_by(Order.order_date.desc())
        .all()
    )

    return {
        "status": status,
        "total": len(orders),
        "orders": [serialize_order(order) for order in orders]
    }


def get_orders_by_date_range_service(start_date, end_date, db, current_user):
    orders = (
        base_order_query(db, current_user)
        .filter(Order.order_date >= str(start_date))
        .filter(Order.order_date <= str(end_date))
        .order_by(Order.order_date.desc())
        .all()
    )

    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total": len(orders),
        "orders": [serialize_order(order) for order in orders]
    }


def search_orders_service(q: str, db, current_user):
    orders = (
        base_order_query(db, current_user)
        .filter(
            or_(
                Order.order_id.ilike(f"%{q}%"),
                Order.external_order_id.ilike(f"%{q}%")
            )
        )
        .order_by(Order.order_date.desc())
        .all()
    )

    return {
        "query": q,
        "total": len(orders),
        "orders": [serialize_order(order) for order in orders]
    }


def get_order_detail_service(order_id: str, db, current_user):
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(
            Order.owner_user_id == current_user.id,
            Order.order_id == order_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": order.id,
        "order_id": order.order_id,
        "source_user_id": order.source_user_id,
        "platform": order.platform,
        "external_order_id": order.external_order_id,
        "customer_id": order.customer_id,
        "status": order.status,
        "order_date": order.order_date,
        "total_items": len(order.items),
        "total_quantity": sum(item.quantity for item in order.items),
        "total_amount": sum(item.quantity * item.unit_price for item in order.items),
        "items": [
            {
                "id": item.id,
                "listing_id": item.listing_id,
                "internal_product_id": item.internal_product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.quantity * item.unit_price
            }
            for item in order.items
        ]
    }


def get_order_items_service(order_id: str, db, current_user):
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(
            Order.owner_user_id == current_user.id,
            Order.order_id == order_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": order.order_id,
        "total_items": len(order.items),
        "items": [
            {
                "id": item.id,
                "listing_id": item.listing_id,
                "internal_product_id": item.internal_product_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.quantity * item.unit_price
            }
            for item in order.items
        ]
    }


def get_order_summary_service(db, current_user):
    base_query = (
        db.query(Order)
        .filter(Order.owner_user_id == current_user.id)
    )

    total_orders = base_query.count()

    delivered_orders = base_query.filter(Order.status == "delivered").count()
    cancelled_orders = base_query.filter(Order.status == "cancelled").count()
    returned_orders = base_query.filter(Order.status == "returned").count()
    shipped_orders = base_query.filter(Order.status == "shipped").count()

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(OrderItem.quantity * OrderItem.unit_price),
                0
            )
        )
        .join(Order, Order.id == OrderItem.order_id)
        .filter(
            Order.owner_user_id == current_user.id,
            Order.status.in_(["delivered", "shipped"])        
        )
        .scalar()
    )

    average_order_value = 0
    successful_orders = delivered_orders + shipped_orders

    if successful_orders > 0:
        average_order_value = total_revenue / successful_orders

    return {
        "total_orders": total_orders,
        "total_revenue": float(total_revenue),
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
        "returned_orders": returned_orders,
        "shipped_orders": shipped_orders,
        "average_order_value": round(float(average_order_value), 2)
    }


def calculate_order_total(order):
    return sum(
        item.quantity * item.unit_price
        for item in order.items
    )


def get_time_based_analysis(db, current_user, period: str):
    orders = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.owner_user_id == current_user.id)
        .all()
    )

    grouped_data = defaultdict(lambda: {
        "total_orders": 0,
        "total_revenue": 0,
        "delivered_orders": 0,
        "cancelled_orders": 0,
        "returned_orders": 0,
        "shipped_orders": 0
    })

    for order in orders:
        order_date = datetime.strptime(order.order_date, "%Y-%m-%d")

        if period == "daily":
            key = order_date.strftime("%Y-%m-%d")

        elif period == "weekly":
            year, week, _ = order_date.isocalendar()
            key = f"{year}-W{week}"

        elif period == "monthly":
            key = order_date.strftime("%Y-%m")

        else:
            key = "unknown"

        grouped_data[key]["total_orders"] += 1

        if order.status == "delivered":
            grouped_data[key]["delivered_orders"] += 1

        elif order.status == "cancelled":
            grouped_data[key]["cancelled_orders"] += 1

        elif order.status == "returned":
            grouped_data[key]["returned_orders"] += 1

        elif order.status == "shipped":
            grouped_data[key]["shipped_orders"] += 1

        if order.status in ["delivered", "shipped"]:
            grouped_data[key]["total_revenue"] += calculate_order_total(order)

    result = []

    for key, value in grouped_data.items():
        total_revenue = value["total_revenue"]

        successful_orders = (
            value["delivered_orders"] +
            value["shipped_orders"]
        )

        value["successful_orders"] = successful_orders

        value["average_order_value"] = (
            round(total_revenue / successful_orders, 2)
            if successful_orders > 0
            else 0
        )

        result.append({
            "period": key,
            **value
        })

    result.sort(key=lambda x: x["period"])

    return {
        "period_type": period,
        "total_periods": len(result),
        "data": result
    }


def get_daily_order_analysis_service(db, current_user):
    return get_time_based_analysis(
        db=db,
        current_user=current_user,
        period="daily"
    )


def get_weekly_order_analysis_service(db, current_user):
    return get_time_based_analysis(
        db=db,
        current_user=current_user,
        period="weekly"
    )


def get_monthly_order_analysis_service(db, current_user):
    return get_time_based_analysis(
        db=db,
        current_user=current_user,
        period="monthly"
    )



def get_platform_analysis_service(db, current_user):
    orders = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.owner_user_id == current_user.id)
        .all()
    )

    platform_data = {}

    for order in orders:
        platform = order.platform.lower()

        if platform not in platform_data:
            platform_data[platform] = {
                "platform": platform,
                "total_orders": 0,
                "total_revenue": 0,
                "delivered_orders": 0,
                "cancelled_orders": 0,
                "returned_orders": 0,
                "shipped_orders": 0,
            }

        platform_data[platform]["total_orders"] += 1

        if order.status == "delivered":
            platform_data[platform]["delivered_orders"] += 1

        elif order.status == "cancelled":
            platform_data[platform]["cancelled_orders"] += 1

        elif order.status == "returned":
            platform_data[platform]["returned_orders"] += 1

        elif order.status == "shipped":
            platform_data[platform]["shipped_orders"] += 1

        if order.status in ["delivered", "shipped"]:
            revenue = calculate_order_total(order)

            platform_data[platform]["total_revenue"] += revenue

    result = []

    for platform, data in platform_data.items():
        total_orders = data["total_orders"]
        total_revenue = data["total_revenue"]

        data["average_order_value"] = (
            round(total_revenue / total_orders, 2)
            if total_orders > 0
            else 0
        )

        result.append(data)

    result.sort(
        key=lambda x: x["total_revenue"],
        reverse=True
    )

    return {
        "total_platforms": len(result),
        "platforms": result
    }