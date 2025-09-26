from nicegui import ui
from utils.auth import auth_state, logout
from config import USER_ROLES

def show_header(auth_state=None, logout_user=None):
    # Top Header Bar (Dark Grey - Jumia style) - Fixed at top
    with ui.element('div').classes('w-full bg-blue-500 text-white py-2 text-sm sticky top-0 z-50'):
        with ui.element('div').classes('container mx-auto px-4 flex items-center justify-between'):
            with ui.row().classes('items-center gap-6'):
                ui.label('Free delivery on orders over GHS 200').classes('text-white')
                ui.label('•').classes('text-gray-400')
                ui.label('24/7 Customer Support').classes('text-gray-300')
            with ui.row().classes('items-center gap-4'):
                if auth_state and auth_state.is_authenticated:
                    ui.label(f'Welcome, {auth_state.name}').classes('text-gray-300')
                else:
                    ui.link('Login', '/login').classes('text-gray-300 hover:text-white no-underline')
                    ui.link('Signup', '/signup').classes('text-gray-300 hover:text-white no-underline')
    
    # Main Header (White background)
    with ui.element('div').classes('w-full bg-white shadow-sm sticky top-8 z-40 border-b border-gray-200'):
        with ui.element('div').classes('container mx-auto px-4 py-4'):
            with ui.row().classes('items-center justify-between w-full'):
                # Creative Logo and Brand (Clickable)
                with ui.row().classes('items-center gap-3 cursor-pointer').on('click', lambda: ui.navigate.to('/')):
                    # Custom InnoHub Logo with star
                    with ui.element('div').classes('flex items-center gap-2 hover:scale-105 transition-transform duration-200'):
                        ui.label('INNO').classes('text-2xl font-bold text-primary')
                        ui.icon('star').classes('text-primary text-xl')
                        ui.label('HUB').classes('text-2xl font-bold text-primary')
                    ui.label('Ghana').classes('text-xs text-gray-500 -mt-2')
                
                # Search Bar (Jumia-style)
                with ui.element('div').classes('flex-1 max-w-2xl mx-8 hidden md:block'):
                    with ui.row().classes('w-full bg-gray-100 rounded-lg overflow-hidden border border-gray-200'):
                        ui.icon('search').classes('text-gray-400 ml-4')
                        search_input = ui.input('Search adverts, brands and categories').classes('flex-1 bg-transparent border-0 px-3 py-3 text-sm').props('outlined=false')
                        
                        def perform_search():
                            query = search_input.value.strip()
                            if query:
                                ui.navigate.to(f'/?q={query}')
                            else:
                                ui.navigate.to('/')
                        
                        ui.button('Search', on_click=perform_search).classes('btn-primary px-6 py-3 font-medium')
                        search_input.on('keydown.enter', perform_search)
                
                # Navigation and Auth
                with ui.row().classes('items-center gap-2'):
                    # Theme Toggle Button
                    def toggle_theme():
                        ui.run_javascript('''
                            const isDark = document.body.classList.contains('dark-mode');
                            if (isDark) {
                                // Switch to light mode
                                document.body.classList.remove('dark-mode');
                                document.body.style.backgroundColor = '#ffffff';
                                document.body.style.color = '#111827';
                                localStorage.setItem('theme', 'light');
                                
                                // Reset all elements
                                const allElements = document.querySelectorAll('*');
                                allElements.forEach(el => {
                                    el.style.backgroundColor = '';
                                    el.style.color = '';
                                    el.style.borderColor = '';
                                });
                            } else {
                                // Switch to dark mode
                                document.body.classList.add('dark-mode');
                                document.body.style.backgroundColor = '#1a1a1a';
                                document.body.style.color = '#ffffff';
                                localStorage.setItem('theme', 'dark');
                                
                                // Apply dark mode to elements
                                const bgElements = document.querySelectorAll('.bg-white, .bg-gray-50, .bg-gray-100');
                                bgElements.forEach(el => {
                                    if (el.classList.contains('bg-white')) {
                                        el.style.backgroundColor = '#2d2d2d';
                                        el.style.color = '#ffffff';
                                    }
                                    if (el.classList.contains('bg-gray-50')) {
                                        el.style.backgroundColor = '#2d2d2d';
                                        el.style.color = '#ffffff';
                                    }
                                    if (el.classList.contains('bg-gray-100')) {
                                        el.style.backgroundColor = '#404040';
                                        el.style.color = '#ffffff';
                                    }
                                });
                                
                                const textElements = document.querySelectorAll('.text-gray-800, .text-gray-700, .text-gray-600, .text-gray-500');
                                textElements.forEach(el => {
                                    if (el.classList.contains('text-gray-800') || el.classList.contains('text-gray-700')) {
                                        el.style.color = '#ffffff';
                                    }
                                    if (el.classList.contains('text-gray-600')) {
                                        el.style.color = '#b0b0b0';
                                    }
                                    if (el.classList.contains('text-gray-500')) {
                                        el.style.color = '#888888';
                                    }
                                });
                            }
                        ''')
                    
                    ui.button(icon='dark_mode', on_click=toggle_theme).classes('text-gray-700 hover:text-gray-900 hover:bg-gray-100 p-2 rounded-full transition-all').props('flat round').tooltip('Toggle Dark Mode')
                    
                    # Context-aware navigation based on authentication and role
                    if auth_state and auth_state.is_authenticated:
                        # Authenticated user navigation
                        def nav_wishlist():
                            ui.navigate.to('/wishlist')
                        
                        def nav_cart():
                            ui.navigate.to('/cart')
                        
                        def nav_dashboard():
                            ui.navigate.to('/dashboard')
                        
                        def nav_messages():
                            ui.navigate.to('/messages')
                        
                        def nav_notifications():
                            ui.navigate.to('/notifications')
                        
                        # Show different icons based on role
                        if auth_state.is_buyer():
                            ui.button(icon='favorite_border', on_click=nav_wishlist).classes('text-gray-700 hover:text-red-500 hover:bg-red-50 p-2 rounded-full transition-all').props('flat round').tooltip('Wishlist')
                            # Cart button with counter
                            with ui.element('div').classes('relative'):
                                ui.button(icon='shopping_cart', on_click=nav_cart).classes('text-gray-700 hover:text-green-500 hover:bg-green-50 p-3 rounded-full transition-all border border-gray-200 hover:border-green-300').props('flat round').tooltip('Cart')
                                # Cart counter badge
                                with ui.element('div').classes('absolute -top-1 -right-1 bg-orange-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold'):
                                    ui.label('3').classes('text-xs')
                        
                        ui.button(icon='chat_bubble_outline', on_click=nav_messages).classes('text-gray-700 hover:text-blue-500 hover:bg-blue-50 p-2 rounded-full transition-all').props('flat round').tooltip('Messages')
                        ui.button(icon='notifications_none', on_click=nav_notifications).classes('text-gray-700 hover:text-purple-500 hover:bg-purple-50 p-2 rounded-full transition-all').props('flat round').tooltip('Notifications')
                        ui.button(icon='dashboard', on_click=nav_dashboard).classes('text-gray-700 hover:text-orange-500 hover:bg-orange-50 p-2 rounded-full transition-all').props('flat round').tooltip('Dashboard')
                        
                        # AI Tools dropdown (for all authenticated users)
                        with ui.dropdown_button('AI Tools', icon='auto_awesome').classes('bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white px-4 py-2 font-bold text-sm shadow-lg hover:shadow-xl transition-all rounded-lg'):
                            ui.item('AI Image Generator', on_click=lambda: ui.navigate.to('/ai_generator'))
                            ui.item('AI Text Generator', on_click=lambda: ui.navigate.to('/ai_text_generator'))
                        
                        # Vendor-specific buttons
                        if auth_state.is_vendor():
                            def nav_sell():
                                ui.navigate.to('/add_event')
                            
                            ui.button('SELL', on_click=nav_sell, icon='add').classes('btn-primary px-4 py-2 font-bold text-sm shadow-primary')
                    else:
                        # Non-authenticated user - show limited navigation
                        def nav_sell():
                            ui.navigate.to('/signup')
                        
                        ui.button('SELL', on_click=nav_sell, icon='add').classes('btn-primary px-4 py-2 font-bold text-sm shadow-primary')
                    
                    if auth_state and auth_state.is_authenticated:
                        # User Profile Icon (highlighted when authenticated)
                        def nav_account():
                            ui.notify('Navigating to account...', type='info')
                            ui.navigate.to('/account')
                        
                        ui.button(icon='account_circle', on_click=nav_account).classes('text-primary hover:text-primary-dark p-2 bg-primary-light rounded-full transition-all').props('flat round').tooltip('My Account')
                        
                        # Prominent Logout Button - Easy to see and access
                        def handle_logout():
                            if logout_user:
                                logout_user()
                            else:
                                ui.notify('Logout function not available', type='negative')
                        
                        ui.button('Logout', on_click=handle_logout, icon='logout').classes('text-red-600 hover:text-red-700 hover:bg-red-50 px-3 py-2 border border-red-200 rounded-lg hover:border-red-300 font-medium transition-all').tooltip('Sign out of your account')
                        
                        # Account dropdown (hidden, using profile icon instead)
                        with ui.dropdown_button('', icon='').classes('hidden'):
                            ui.item('My Account', on_click=lambda: ui.navigate.to('/account'))
                            ui.item('My Orders', on_click=lambda: ui.navigate.to('/orders'))
                            ui.item('Wishlist', on_click=lambda: ui.navigate.to('/wishlist'))
                            ui.item('My Adverts', on_click=lambda: ui.navigate.to('/dashboard'))
                    else:
                        # Guest user - show login button with icon
                        def nav_login():
                            ui.notify('Navigating to login...', type='info')
                            ui.navigate.to('/login')
                        
                        ui.button('Login', on_click=nav_login, icon='login').classes('text-gray-700 hover:text-orange-500 font-medium px-3 py-2 border border-gray-300 rounded-lg hover:border-orange-500')