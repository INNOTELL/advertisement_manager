from nicegui import ui, app
from theme import setup_theme
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import uuid
import requests
from utils.api import base_url

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

# ===== Authentication State =====
class AuthState:
    def __init__(self):
        self.is_authenticated = False
        self.user_type = None  # 'vendor' or 'user'
        self.user_email = None
        self.username = None
        self.user_id = None
        self.token = None

auth_state = AuthState()

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
async def login_user(email: str, password: str) -> bool:
    try:
        print(f"Login attempt: email={email}, password={password}")  # Debug
        # Demo login for testing - accept any email/password combination
        if email and password and len(email) >= 3 and len(password) >= 3:
            # Set authentication state
            auth_state.is_authenticated = True
            auth_state.user_email = email
            # Use email prefix as username, or just the email if no @
            auth_state.username = email.split('@')[0] if '@' in email else email
            auth_state.token = "demo_token_123"
            # Determine user type based on email content
            auth_state.user_type = 'vendor' if any(word in email.lower() for word in ['vendor', 'seller', 'admin', 'shop']) else 'user'
            print(f"Login successful: {auth_state.username}, type: {auth_state.user_type}")  # Debug
            print(f"Auth state: authenticated={auth_state.is_authenticated}, email={auth_state.user_email}")  # Debug
            return True
        else:
            print(f"Login failed: email={email}, password={password}")  # Debug
        
        # Try real API login as fallback
        response = requests.post(f"{base_url}/Login", params={"email": email, "password": password})
        if response.status_code == 200:
            auth_state.is_authenticated = True
            auth_state.user_email = email
            auth_state.token = response.text.strip('"')
            auth_state.user_type = 'vendor' if 'vendor' in email.lower() else 'user'
            return True
    except Exception as e:
        ui.notify(f"Login failed: {e}")
    return False

async def signup_user(email: str, username: str, password: str) -> bool:
    try:
        print(f"Signup attempt: email={email}, username={username}, password={password}")  # Debug
        # Demo signup for testing - always succeed with minimal validation
        if email and username and password and len(email) >= 3 and len(username) >= 2 and len(password) >= 3:
            ui.notify("Account created successfully! Please login.")
            print(f"Signup successful: {username}")  # Debug
            return True
        else:
            print(f"Signup failed: email={email}, username={username}, password={password}")  # Debug
        
        # Try real API signup as fallback
        response = requests.post(f"{base_url}/Sign up", params={"email": email}, 
                               data={"username": username, "password": password})
        if response.status_code == 200:
            ui.notify("Account created successfully! Please login.")
            return True
    except Exception as e:
        ui.notify(f"Signup failed: {e}")
    return False

def logout_user():
    auth_state.is_authenticated = False
    auth_state.user_type = None
    auth_state.user_email = None
    auth_state.username = None
    auth_state.user_id = None
    auth_state.token = None
    ui.navigate.to('/')

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

@ui.page('/')
def index():
    show_header(auth_state, logout_user)
    show_home_page()
    show_footer()

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
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    show_dashboard_page(auth_state)
    show_footer()

@ui.page('/add_event')
def add_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
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

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(reload=True)
