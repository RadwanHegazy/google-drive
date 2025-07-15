import stripe
from core.settings import STRIPE_SECRET_KEY

def create_stripe_checkout_link(line_items, success_url, cancel_url) -> str :
    """Creating TransactionTable and generating stripe url for checkout""" 
    try : 
        
        stripe.api_key = STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            success_url=success_url,
            cancel_url=cancel_url,
            line_items=line_items,
            mode='payment'
        )
    
        return session.url
    
    except Exception as error :
        raise Exception(f"stripe checkout error : {error}")