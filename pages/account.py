from nicegui import ui
import requests
from utils.api import base_url

def show_account_page(auth_state=None):
    if not auth_state or not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('My Account').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label(f'Welcome back, {auth_state.name}!').classes('text-gray-600')
            
            # Account Overview Cards
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6 mb-8'):
                # Profile Card
                with ui.card().classes('p-6 bg-white shadow-sm'):
                    with ui.element('div').classes('text-center'):
                        ui.icon('account_circle').classes('text-6xl text-orange-500 mb-4')
                        ui.label(auth_state.name).classes('text-xl font-semibold text-gray-800 mb-2')
                        ui.label(auth_state.email).classes('text-gray-600 mb-4')
                        ui.label(f'Account Type: {auth_state.role.title()}').classes('text-sm text-orange-500 font-medium')
                
                # Orders Card
                with ui.card().classes('p-6 bg-white shadow-sm'):
                    with ui.element('div').classes('text-center'):
                        ui.icon('shopping_bag').classes('text-6xl text-blue-500 mb-4')
                        ui.label('12').classes('text-3xl font-bold text-gray-800 mb-2')
                        ui.label('Total Orders').classes('text-gray-600 mb-4')
                        ui.button('View Orders', on_click=lambda: ui.navigate.to('/orders')).classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg')
                
                # Wishlist Card
                with ui.card().classes('p-6 bg-white shadow-sm'):
                    with ui.element('div').classes('text-center'):
                        ui.icon('favorite').classes('text-6xl text-red-500 mb-4')
                        ui.label('8').classes('text-3xl font-bold text-gray-800 mb-2')
                        ui.label('Wishlist Items').classes('text-gray-600 mb-4')
                        ui.button('View Wishlist', on_click=lambda: ui.navigate.to('/wishlist')).classes('bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg')
            
            # Main Content Tabs
            with ui.card().classes('bg-white shadow-sm'):
                with ui.element('div').classes('border-b border-gray-200'):
                    with ui.row().classes('px-6 py-4'):
                        ui.button('Profile Settings', icon='person').classes('px-4 py-2 text-orange-500 font-semibold border-b-2 border-orange-500')
                        ui.button('Order History', icon='history').classes('px-4 py-2 text-gray-600 hover:text-orange-500')
                        ui.button('Addresses', icon='location_on').classes('px-4 py-2 text-gray-600 hover:text-orange-500')
                        ui.button('Payment Methods', icon='credit_card').classes('px-4 py-2 text-gray-600 hover:text-orange-500')
                        ui.button('Notifications', icon='notifications').classes('px-4 py-2 text-gray-600 hover:text-orange-500')
                
                # Profile Settings Content
                with ui.element('div').classes('p-6'):
                    ui.label('Profile Information').classes('text-xl font-bold text-gray-800 mb-6')
                    
                    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-6'):
                        # Personal Information
                        with ui.element('div'):
                            ui.label('Personal Information').classes('text-lg font-semibold text-gray-700 mb-4')
                            
                            username_input = ui.input('Username').classes('w-full mb-4').props('outlined')
                            username_input.value = auth_state.name
                            
                            email_input = ui.input('Email Address').classes('w-full mb-4').props('outlined')
                            email_input.value = auth_state.email
                            
                            phone_input = ui.input('Phone Number').classes('w-full mb-4').props('outlined')
                            phone_input.value = '+233 24 123 4567'  # Demo data
                            
                            birthdate_input = ui.input('Date of Birth').classes('w-full mb-4').props('outlined')
                            birthdate_input.value = '1990-01-15'  # Demo data
                            
                            ui.button('Update Profile', icon='save').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold')
                        
                        # Account Security
                        with ui.element('div'):
                            ui.label('Account Security').classes('text-lg font-semibold text-gray-700 mb-4')
                            
                            current_password = ui.input('Current Password').classes('w-full mb-4').props('outlined type=password')
                            new_password = ui.input('New Password').classes('w-full mb-4').props('outlined type=password')
                            confirm_password = ui.input('Confirm New Password').classes('w-full mb-4').props('outlined type=password')
                            
                            async def update_password():
                                if not all([current_password.value, new_password.value, confirm_password.value]):
                                    ui.notify('Please fill in all password fields', type='negative')
                                    return
                                
                                if new_password.value != confirm_password.value:
                                    ui.notify('New passwords do not match', type='negative')
                                    return
                                
                                if len(new_password.value) < 8:
                                    ui.notify('Password must be at least 8 characters', type='negative')
                                    return
                                
                                ui.notify('Password updated successfully!', type='positive')
                                current_password.value = ''
                                new_password.value = ''
                                confirm_password.value = ''
                            
                            ui.button('Update Password', on_click=update_password, icon='lock').classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold')
                            
                            # Two-Factor Authentication
                            with ui.element('div').classes('mt-6 p-4 bg-gray-50 rounded-lg'):
                                ui.label('Two-Factor Authentication').classes('text-md font-semibold text-gray-700 mb-2')
                                ui.label('Add an extra layer of security to your account').classes('text-sm text-gray-600 mb-3')
                                ui.button('Enable 2FA', icon='security').classes('bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm')
            
            # Recent Activity
            with ui.card().classes('mt-8 p-6 bg-white shadow-sm'):
                ui.label('Recent Activity').classes('text-xl font-bold text-gray-800 mb-6')
                
                activities = [
                    {'action': 'Order Placed', 'item': 'iPhone 14 Pro', 'time': '2 hours ago', 'icon': 'shopping_cart', 'color': 'text-green-500'},
                    {'action': 'Product Added', 'item': 'Samsung Galaxy S23', 'time': '1 day ago', 'icon': 'add_shopping_cart', 'color': 'text-blue-500'},
                    {'action': 'Review Posted', 'item': 'MacBook Pro M2', 'time': '3 days ago', 'icon': 'rate_review', 'color': 'text-yellow-500'},
                    {'action': 'Wishlist Added', 'item': 'AirPods Pro', 'time': '1 week ago', 'icon': 'favorite', 'color': 'text-red-500'},
                ]
                
                for activity in activities:
                    with ui.element('div').classes('flex items-center gap-4 py-3 border-b border-gray-100 last:border-b-0'):
                        ui.icon(activity['icon']).classes(f'{activity["color"]} text-xl')
                        with ui.element('div').classes('flex-1'):
                            ui.label(activity['action']).classes('font-medium text-gray-800')
                            ui.label(activity['item']).classes('text-sm text-gray-600')
                        ui.label(activity['time']).classes('text-sm text-gray-500')
            
            # Quick Actions - Enhanced with Real Functionality
            with ui.element('div').classes('mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'):
                
                # Track Order Button
                def track_order():
                    ui.notify('Opening order tracking...', type='info')
                    ui.navigate.to('/track')
                
                with ui.card().classes('p-4 bg-white shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer border border-gray-200 hover:border-blue-300').on('click', track_order):
                    with ui.element('div').classes('text-center'):
                        ui.icon('local_shipping').classes('text-white text-2xl bg-blue-500 rounded-full p-3 mx-auto mb-3')
                        ui.label('Track Order').classes('font-medium text-gray-800')
                        ui.label('Monitor your deliveries').classes('text-xs text-gray-500 mt-1')
                
                # Support Button
                def open_support():
                    ui.notify('Opening customer support...', type='info')
                    # Create support dialog
                    with ui.dialog() as support_dialog:
                        with ui.card().classes('p-6 w-full max-w-md'):
                            ui.label('Customer Support').classes('text-xl font-bold text-gray-800 mb-4')
                            
                            # Support options
                            with ui.element('div').classes('space-y-3'):
                                def live_chat():
                                    ui.notify('Starting live chat...', type='positive')
                                    support_dialog.close()
                                
                                def email_support():
                                    ui.notify('Opening email support...', type='positive')
                                    support_dialog.close()
                                
                                def phone_support():
                                    ui.notify('Calling support: +233 24 123 4567', type='positive')
                                    support_dialog.close()
                                
                                ui.button('💬 Live Chat', on_click=live_chat).classes('w-full bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg font-medium')
                                ui.button('📧 Email Support', on_click=email_support).classes('w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg font-medium')
                                ui.button('📞 Phone Support', on_click=phone_support).classes('w-full bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-lg font-medium')
                            
                            ui.button('Close', on_click=support_dialog.close).classes('w-full bg-gray-500 hover:bg-gray-600 text-white py-2 rounded-lg mt-4')
                    
                    support_dialog.open()
                
                with ui.card().classes('p-4 bg-white shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer border border-gray-200 hover:border-green-300').on('click', open_support):
                    with ui.element('div').classes('text-center'):
                        ui.icon('help').classes('text-white text-2xl bg-green-500 rounded-full p-3 mx-auto mb-3')
                        ui.label('Support').classes('font-medium text-gray-800')
                        ui.label('Get help & assistance').classes('text-xs text-gray-500 mt-1')
                
                # Settings Button
                def open_settings():
                    ui.notify('Opening account settings...', type='info')
                    # Create settings dialog
                    with ui.dialog() as settings_dialog:
                        with ui.card().classes('p-6 w-full max-w-lg'):
                            ui.label('Account Settings').classes('text-xl font-bold text-gray-800 mb-4')
                            
                            # Settings tabs
                            with ui.element('div').classes('space-y-4'):
                                # Notification Settings
                                with ui.element('div').classes('p-4 bg-gray-50 rounded-lg'):
                                    ui.label('🔔 Notifications').classes('font-semibold text-gray-800 mb-2')
                                    with ui.element('div').classes('space-y-2'):
                                        ui.checkbox('Email notifications', value=True).classes('text-sm')
                                        ui.checkbox('SMS notifications', value=False).classes('text-sm')
                                        ui.checkbox('Push notifications', value=True).classes('text-sm')
                                
                                # Privacy Settings
                                with ui.element('div').classes('p-4 bg-gray-50 rounded-lg'):
                                    ui.label('🔒 Privacy').classes('font-semibold text-gray-800 mb-2')
                                    with ui.element('div').classes('space-y-2'):
                                        ui.checkbox('Profile visibility', value=True).classes('text-sm')
                                        ui.checkbox('Order history privacy', value=False).classes('text-sm')
                                
                                # Language Settings
                                with ui.element('div').classes('p-4 bg-gray-50 rounded-lg'):
                                    ui.label('🌐 Language').classes('font-semibold text-gray-800 mb-2')
                                    ui.select(['English', 'Twi', 'Ga', 'Ewe'], value='English').classes('w-full')
                            
                            def save_settings():
                                ui.notify('Settings saved successfully!', type='positive')
                                settings_dialog.close()
                            
                            ui.button('Save Settings', on_click=save_settings).classes('w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg mt-4')
                            ui.button('Close', on_click=settings_dialog.close).classes('w-full bg-gray-500 hover:bg-gray-600 text-white py-2 rounded-lg mt-2')
                    
                    settings_dialog.open()
                
                with ui.card().classes('p-4 bg-white shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer border border-gray-200 hover:border-gray-400').on('click', open_settings):
                    with ui.element('div').classes('text-center'):
                        ui.icon('settings').classes('text-white text-2xl bg-gray-500 rounded-full p-3 mx-auto mb-3')
                        ui.label('Settings').classes('font-medium text-gray-800')
                        ui.label('Manage preferences').classes('text-xs text-gray-500 mt-1')
                
                # Logout Button
                def confirm_logout():
                    # Create logout confirmation dialog
                    with ui.dialog() as logout_dialog:
                        with ui.card().classes('p-6 w-full max-w-sm'):
                            ui.label('Confirm Logout').classes('text-xl font-bold text-gray-800 mb-4')
                            ui.label('Are you sure you want to logout?').classes('text-gray-600 mb-6')
                            
                            with ui.element('div').classes('flex gap-3'):
                                def perform_logout():
                                    ui.notify('Logging out...', type='info')
                                    # Import logout function from main
                                    from main import logout_user
                                    logout_user()
                                    logout_dialog.close()
                                
                                ui.button('Yes, Logout', on_click=perform_logout).classes('flex-1 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg font-medium')
                                ui.button('Cancel', on_click=logout_dialog.close).classes('flex-1 bg-gray-500 hover:bg-gray-600 text-white py-2 rounded-lg font-medium')
                    
                    logout_dialog.open()
                
                with ui.card().classes('p-4 bg-white shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer border border-gray-200 hover:border-red-300').on('click', confirm_logout):
                    with ui.element('div').classes('text-center'):
                        ui.icon('logout').classes('text-white text-2xl bg-red-500 rounded-full p-3 mx-auto mb-3')
                        ui.label('Logout').classes('font-medium text-gray-800')
                        ui.label('Sign out of account').classes('text-xs text-gray-500 mt-1')
