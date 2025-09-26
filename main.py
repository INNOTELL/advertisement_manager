from nicegui import ui, app
from theme import setup_theme
import asyncio
from utils.api_client import api_client
from utils.auth import auth_state, initialize_auth, signup, signin, logout
from config import PROTECTED_ROUTES, VENDOR_ROUTES, USER_ROLES

# Expose the assets folder to the nicegui server
app.add_static_files("/assets", "assets")

# Inject Tailwind CDN once for layout utilities
ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
ui.add_head_html('''
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
body { font-family: 'Inter', sans-serif; }
</style>
''')
ui.add_head_html('<link rel="stylesheet" href="/assets/reset.css"/>')
setup_theme()

# ===== Frontend Application =====
# This is now a pure frontend application using NiceGUI
# All backend functionality is handled by the external API

# ===== Authentication Functions =====
# Authentication functions are now in utils.auth
# These are kept for backward compatibility
async def login_user(email: str, password: str) -> bool:
    """Legacy login function - redirects to new auth system"""
    return await signin(email, password)

async def signup_user(email: str, username: str, password: str) -> bool:
    """Legacy signup function - redirects to new auth system"""
    # Default to buyer role for legacy signup
    success, _ = await signup(username, email, password, USER_ROLES["BUYER"])
    return success

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
from pages.order_details import show_order_details_page
from pages.analytics import show_analytics_page
from pages.wishlist import show_wishlist_page
from pages.cart import show_cart_page
from pages.delivery import show_delivery_page
from pages.sell import show_sell_page
from pages.track import show_track_page
from pages.ai_generator import show_ai_generator_page
from pages.ai_text_generator import show_ai_text_generator_page

# Import vendor pages (matching your example structure)
try:
    from pages.vendor.dashboard import show_vendor_dashboard
    from pages.vendor.add_event import show_vendor_add_event
    from pages.vendor.edit_event import show_vendor_edit_event
    from pages.vendor.events import show_vendor_events
    from pages.vendor.signup import show_vendor_signup
    from pages.vendor.signin import show_vendor_signin
except ImportError:
    # Fallback if vendor pages don't exist
    def show_vendor_dashboard():
        ui.label('Vendor Dashboard - Coming Soon')
    def show_vendor_add_event():
        ui.label('Add Event - Coming Soon')
    def show_vendor_edit_event():
        ui.label('Edit Event - Coming Soon')
    def show_vendor_events():
        ui.label('Vendor Events - Coming Soon')
    def show_vendor_signup():
        ui.label('Vendor Signup - Coming Soon')
    def show_vendor_signin():
        ui.label('Vendor Signin - Coming Soon')

# Import additional pages (matching your example)

@ui.page('/')
def home_page():
    # Initialize authentication and API discovery on every page load
    # ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
    
    show_header(auth_state, logout_user)
    show_home_page(auth_state)
    show_footer()

# Initialize authentication on app start
@ui.page('/init')
def init_auth():
    # ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
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
        ui.navigate.to('/login?next=/edit_event')
        return
    # Check if user is vendor
    if not auth_state.is_vendor():
        ui.notify("You don't have access to that page.", type="negative")
        ui.navigate.to('/')
        return
    show_header(auth_state, logout_user)
    show_edit_event_page()
    show_footer()

@ui.page('/view_event')
def add_view_page(id=""):
    show_header(auth_state, logout_user)
    show_view_event_page()
    show_footer()

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

@ui.page('/order_details')
def order_details_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    show_header(auth_state, logout_user)
    show_order_details_page()
    show_footer()

@ui.page('/analytics')
def analytics_page():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/analytics')
        return
    # Check if user is vendor (Insights are vendor-only)
    if not auth_state.is_vendor():
        ui.notify("You don't have access to that page.", type="negative")
        ui.navigate.to('/')
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
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/sell')
        return
    # Check if user is vendor
    if not auth_state.is_vendor():
        ui.notify("You don't have access to that page.", type="negative")
        ui.navigate.to('/')
        return
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
    # ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
    
    show_header(auth_state, logout_user)
    show_ai_generator_page()
    show_footer()

@ui.page('/ai_text_generator')
def ai_text_generator_page():
    # Initialize authentication and API discovery on every page load
    # ui.timer(0.1, lambda: asyncio.create_task(initialize_auth()), once=True)
    
    show_header(auth_state, logout_user)
    show_ai_text_generator_page()
    show_footer()

# Vendor-specific routes (matching your example structure)
@ui.page("/vendor/dashboard")
def vendor_dashboard():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/vendor/dashboard')
        return
    if not auth_state.is_vendor():
        ui.notify("You don't have access to that page.", type="negative")
        ui.navigate.to('/')
        return
    show_vendor_dashboard()

@ui.page("/vendor/add_event")
def vendor_add_event():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/vendor/add_event')
        return
    if not auth_state.is_vendor():
        ui.notify("You don't have access to that page.", type="negative")
        ui.navigate.to('/')
        return
    show_vendor_add_event()

@ui.page("/vendor/edit_event")
def vendor_edit_event():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/vendor/edit_event')
        return
    if not auth_state.is_vendor():
        ui.notify("You don't have access to that page.", type="negative")
        ui.navigate.to('/')
        return
    show_vendor_edit_event()

@ui.page("/vendor/events")
def vendor_events():
    if not auth_state.is_authenticated:
        ui.navigate.to('/login?next=/vendor/events')
        return
    if not auth_state.is_vendor():
        ui.notify("You don't have access to that page.", type="negative")
        ui.navigate.to('/')
        return
    show_vendor_events()

@ui.page("/vendor/signup")
def vendor_signup():
    show_vendor_signup()

@ui.page("/vendor/signin")
def vendor_signin():
    show_vendor_signin()


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(reload=True)
