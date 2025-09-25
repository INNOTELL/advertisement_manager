from nicegui import ui, app
from theme import setup_theme
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import uuid
import requests
import asyncio
from utils.api import base_url
from utils.api_client import api_client
from utils.auth import auth_state, initialize_auth, signup, signin, logout
from config import PROTECTED_ROUTES, VENDOR_ROUTES, USER_ROLES

app.add_static_files("/assets", "assets")

# Inject Tailwind CDN once for layout utilities
ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
ui.add_head_html('''
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Inter', sans-serif; }
</style>
''')
setup_theme()

# ===== Models =====
class AdvertIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=80)
    image_url: Optional[str] = None

class AdvertOut(AdvertIn):
    id: str

# ===== In-memory DB =====
DB: Dict[str, AdvertOut] = {}

# ===== Authentication State (using utils.auth) =====
# AuthState is now imported from utils.auth

def ghsc(amount: float) -> str:
    return f"GHS {amount:,.2f}"

# ===== REST API (FastAPI via NiceGUI) =====
@app.post('/api/adverts', response_model=AdvertOut)
def create_advert(ad: AdvertIn):
    advert_id = str(uuid.uuid4())
    out = AdvertOut(id=advert_id, **ad.dict())
    DB[advert_id] = out
    return out

@app.get('/api/adverts', response_model=List[AdvertOut])
def list_adverts():
    return list(DB.values())

@app.get('/api/adverts/{advert_id}', response_model=AdvertOut)
def get_advert(advert_id: str):
    if advert_id not in DB:
        raise HTTPException(status_code=404, detail='Advert not found')
    return DB[advert_id]

@app.put('/api/adverts/{advert_id}', response_model=AdvertOut)
def update_advert(advert_id: str, ad: AdvertIn):
    if advert_id not in DB:
        raise HTTPException(status_code=404, detail='Advert not found')
    updated = AdvertOut(id=advert_id, **ad.dict())
    DB[advert_id] = updated
    return updated

@app.delete('/api/adverts/{advert_id}')
def delete_advert(advert_id: str):
    if advert_id not in DB:
        raise HTTPException(status_code=404, detail='Advert not found')
    del DB[advert_id]
    return {'ok': True}

# ===== Authentication Functions =====
# Authentication functions are now in utils.auth
# These are kept for backward compatibility
async def login_user(email: str, password: str) -> bool:
    """Legacy login function - redirects to new auth system"""
    return await signin(email, password)

async def signup_user(email: str, username: str, password: str) -> bool:
    """Legacy signup function - redirects to new auth system"""
    # Default to buyer role for legacy signup
    return await signup(username, email, password, USER_ROLES["BUYER"])

def logout_user():
    """Legacy logout function - redirects to new auth system"""
    logout()

# ===== Pages =====
from components.header import show_header
from components.footer import show_footer
from pages.home import show_home_page
from pages.add_event import show_add_event_page
from pages.edit_event import show_edit_event_page
from pages.view_event import show_view_event_page
from pages.auth import show_login_page, show_signup_page
from pages.dashboard import show_dashboard_page
from pages.account import show_account_page
from pages.orders import show_orders_page
from pages.analytics import show_analytics_page
from pages.wishlist import show_wishlist_page
from pages.cart import show_cart_page
from pages.delivery import show_delivery_page
from pages.sell import show_sell_page
from pages.track import show_track_page
from pages.ai_generator import show_ai_generator_page
from pages.ai_text_generator import show_ai_text_generator_page

@ui.page('/')
def index():
    # Initialize authentication and API discovery on every page load
    ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
    
    show_header(auth_state, logout_user)
    show_home_page(auth_state)
    show_footer()

# Initialize authentication on app start
@ui.page('/init')
def init_auth():
    ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
    ui.navigate.to('/')

@ui.page('/login')
def login_page():
    show_header(auth_state, logout_user)
    show_login_page(login_user, auth_state)
    show_footer()

@ui.page('/signup')
def signup_page():
    show_header(auth_state, logout_user)
    show_signup_page(signup_user)
    show_footer()

@ui.page('/dashboard')
def dashboard_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/dashboard')
        return
    show_header(auth_state, logout_user)
    show_dashboard_page(auth_state)
    show_footer()

@ui.page('/add_event')
def add_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/add_event')
        return
    # Check if user is vendor
    if not auth_state.is_vendor():
        ui.notify("Insufficient permissions. Only vendors can create ads.", type="negative")
        ui.navigate.to('/dashboard')
        return
    show_header(auth_state, logout_user)
    show_add_event_page()
    show_footer()

@ui.page('/edit_event')
def edit_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    show_edit_event_page()
    show_footer()

# @ui.page('/view_event')
# def view_page():
#     show_header(auth_state, logout_user)
#     show_view_event_page()
#     show_footer()

@ui.page('/account')
def account_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    show_account_page(auth_state)
    show_footer()

@ui.page('/orders')
def orders_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    show_orders_page(auth_state)
    show_footer()

@ui.page('/analytics')
def analytics_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    show_analytics_page(auth_state)
    show_footer()

@ui.page('/wishlist')
def wishlist_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    show_wishlist_page(auth_state)
    show_footer()

@ui.page('/cart')
def cart_page():
    # Allow access to cart page for testing
    show_header(auth_state, logout_user)
    show_cart_page(auth_state)
    show_footer()

@ui.page('/messages')
def messages_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    with ui.element('div').classes('min-h-screen bg-gray-50 py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-4xl'):
            with ui.card().classes('p-8 text-center'):
                ui.icon('chat_bubble_outline').classes('text-6xl text-blue-500 mb-4')
                ui.label('Messages').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Your messages will appear here').classes('text-gray-600 mb-6')
                ui.label('This feature is coming soon!').classes('text-orange-500 font-semibold')
    show_footer()

@ui.page('/notifications')
def notifications_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    with ui.element('div').classes('min-h-screen bg-gray-50 py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-4xl'):
            with ui.card().classes('p-8 text-center'):
                ui.icon('notifications_none').classes('text-6xl text-purple-500 mb-4')
                ui.label('Notifications').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Your notifications will appear here').classes('text-gray-600 mb-6')
                ui.label('This feature is coming soon!').classes('text-orange-500 font-semibold')
    show_footer()

@ui.page('/delivery')
def delivery_page():
    show_header(auth_state, logout_user)
    show_delivery_page(auth_state)
    show_footer()

@ui.page('/sell')
def sell_page():
    show_header(auth_state, logout_user)
    show_sell_page(auth_state)
    show_footer()

@ui.page('/track')
def track_page():
    show_header(auth_state, logout_user)
    show_track_page(auth_state)
    show_footer()

@ui.page('/ai_generator')
def ai_generator_page():
    # Initialize authentication and API discovery on every page load
    ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
    
    show_header(auth_state, logout_user)
    show_ai_generator_page()
    show_footer()

@ui.page('/ai_text_generator')
def ai_text_generator_page():
    # Initialize authentication and API discovery on every page load
    ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
    
    show_header(auth_state, logout_user)
    show_ai_text_generator_page()
    show_footer()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(reload=True)
