import stripe

import os
from dotenv import load_dotenv

load_dotenv(override=True)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_product(product_name, product_description):
    product = stripe.Product.create(
        name=product_name,
        description=product_description,
    )
    return product


def create_stripe_price(amount):
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        recurring={"interval": "month"},
        product_data={"name": "Gold Plan"},
    )
    return price


def create_stripe_checkout_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price.get("id"),
                "quantity": 1,
            }
        ],
        mode="payment",
    )

    return session.get("id"), session.get("url")
