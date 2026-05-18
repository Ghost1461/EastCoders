from fastapi import HTTPException

from app.services.prompt_builder import (
    build_report_summary_prompt,
    build_ai_recommendations_prompt,
    build_stock_analysis_prompt,
    build_review_analysis_prompt,
    build_period_summary_prompt,
)

from app.services.gemini_llm_service import generate_gemini_response

from app.services.order_display_services import (
    get_order_summary_service,
    get_platform_analysis_service,
    get_daily_order_analysis_service,
    get_weekly_order_analysis_service,
    get_monthly_order_analysis_service,
)

from app.services.review_display_service import (
    get_review_summary_service,
    get_rating_distribution_service,
    get_topic_summary_service,
)

from app.services.product_display_service import (
    get_top_rated_products,
    get_lowest_rated_products,
    get_most_reviewed_products,
    get_low_stock_products,
    get_category_item_counts,
    get_gender_distribution,
    get_gender_item_counts,
    get_low_stock_products_by_gender
)


def get_dashboard_report_service(db, current_user):
    return {
        "orders": {
            "summary": get_order_summary_service(
                db=db,
                current_user=current_user
            ),
            "platform_analysis": get_platform_analysis_service(
                db=db,
                current_user=current_user
            ),
            "daily_analysis": get_daily_order_analysis_service(
                db=db,
                current_user=current_user
            ),
            "weekly_analysis": get_weekly_order_analysis_service(
                db=db,
                current_user=current_user
            ),
            "monthly_analysis": get_monthly_order_analysis_service(
                db=db,
                current_user=current_user
            ),
        },
        "reviews": {
            "summary": get_review_summary_service(
                db=db,
                current_user=current_user
            ),
            "rating_distribution": get_rating_distribution_service(
                db=db,
                current_user=current_user
            ),
            "topic_summary": get_topic_summary_service(
                db=db,
                current_user=current_user
            ),
        },
        "products": {
            "top_rated": get_top_rated_products(
                db=db,
                user_id=current_user.id,
                limit=5
            ),
            "lowest_rated": get_lowest_rated_products(
                db=db,
                user_id=current_user.id,
                limit=5
            ),
            "most_reviewed": get_most_reviewed_products(
                db=db,
                user_id=current_user.id,
                limit=5
            ),
            "low_stock": get_low_stock_products(
                db=db,
                user_id=current_user.id,
                threshold=20
            ),
            "category_counts": get_category_item_counts(
                db=db,
                user_id=current_user.id
            ),
            "gender_distribution": get_gender_distribution(
                db=db,
                user_id=current_user.id
            ),

            "gender_item_counts": get_gender_item_counts(
                db=db,
                user_id=current_user.id
            )
        }
    }


#genel özet raporu
def get_ai_report_summary_service(db, current_user):
    report_data = get_dashboard_report_service(
        db=db,
        current_user=current_user
    )

    prompt = build_report_summary_prompt(report_data)

    ai_response = generate_gemini_response(prompt)

    return {
        "type": "summary",
        "ai": ai_response
    }


#aksiyon, recomendation verme
def get_ai_recommendations_service(db, current_user):
    report_data = get_dashboard_report_service(
        db=db,
        current_user=current_user
    )

    prompt = build_ai_recommendations_prompt(report_data)

    ai_response = generate_gemini_response(prompt)

    return {
        "type": "recommendations",
        "ai": ai_response
    }


#stok(ürün adedi ağırlıklı)
def get_ai_stock_analysis_service(db, current_user):
    product_data = {
        "top_rated": get_top_rated_products(
            db=db,
            user_id=current_user.id,
            limit=5
        ),
        "lowest_rated": get_lowest_rated_products(
            db=db,
            user_id=current_user.id,
            limit=5
        ),
        "most_reviewed": get_most_reviewed_products(
            db=db,
            user_id=current_user.id,
            limit=5
        ),
        "low_stock": get_low_stock_products(
            db=db,
            user_id=current_user.id,
            threshold=10
        ),
        "category_counts": get_category_item_counts(
            db=db,
            user_id=current_user.id
        ),
        "women_low_stock": get_low_stock_products_by_gender(
            db=db,
            user_id=current_user.id,
            gender="women",
            threshold=10
        ),
        "men_low_stock": get_low_stock_products_by_gender(
            db=db,
            user_id=current_user.id,
            gender="men",
            threshold=10
        )
    }

    prompt = build_stock_analysis_prompt(product_data)

    ai_response = generate_gemini_response(prompt)

    return {
        "type": "stock_analysis",
        "ai": ai_response
    }

#review ağırlıklı
def get_ai_review_analysis_service(db, current_user):
    review_data = {
        "summary": get_review_summary_service(
            db=db,
            current_user=current_user
        ),
        "rating_distribution": get_rating_distribution_service(
            db=db,
            current_user=current_user
        ),
        "topic_summary": get_topic_summary_service(
            db=db,
            current_user=current_user
        )
    }

    prompt = build_review_analysis_prompt(review_data)

    ai_response = generate_gemini_response(prompt)

    return {
        "type": "review_analysis",
        "ai": ai_response
    }




#hesabın period bazlı özeti
def get_ai_period_summary_service(db, current_user, period: str, value: str):
    period = period.lower().strip()

    SUPPORTED_PERIODS = ["daily", "weekly", "monthly"]

    #daily   -> 2026-05-17 şeklinde girilmeli
    #weekly  -> 2026-W20 şeklinde girilmeli
    #monthly -> 2026-05 şeklinde girilmeli

    if period not in SUPPORTED_PERIODS:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unsupported period. Supported values: daily, weekly, monthly",
                "supported_periods": SUPPORTED_PERIODS
            }
        )

    if period == "daily":
        all_data = get_daily_order_analysis_service(db, current_user)

    elif period == "weekly":
        all_data = get_weekly_order_analysis_service(db, current_user)

    elif period == "monthly":
        all_data = get_monthly_order_analysis_service(db, current_user)

    #tüm gün/ay/yıl verisini llm'e gönderip yormamak için
    selected_data = next(
        (item for item in all_data["data"] if item["period"] == value),
        None
    )

    if not selected_data:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for period={period}, value={value}"
        )

    prompt = build_period_summary_prompt(
        period=period,
        value=value,
        data=selected_data
    )

    ai_response = generate_gemini_response(prompt)

    return {
        "type": "period_summary",
        "period": period,
        "value": value,
        "data": selected_data,
        "ai": ai_response
    }