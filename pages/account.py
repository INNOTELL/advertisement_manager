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
                ui.label(f'Welcome back, {auth_state.username}!').classes('text-gray-600')
            
            # Account Overview Cards
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6 mb-8'):
                # Profile Card
                with ui.card().classes('p-6 bg-white shadow-sm'):
                    with ui.element('div').classes('text-center'):
                        ui.icon('account_circle').classes('text-6xl text-orange-500 mb-4')
                        ui.label(auth_state.username).classes('text-xl font-semibold text-gray-800 mb-2')
                        ui.label(auth_state.user_email).classes('text-gray-600 mb-4')
                        ui.label(f'Account Type: {auth_state.user_type.title()}').classes('text-sm text-orange-500 font-medium')
                
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
                            
                            username_input = ui.input('Full Name').classes('w-full mb-4').props('outlined')
                            username_input.value = auth_state.username
                            
                            email_input = ui.input('Email Address').classes('w-full mb-4').props('outlined')
                            email_input.value = auth_state.user_email
                            
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
            
            # Quick Actions
            with ui.element('div').classes('mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4'):
                quick_actions = [
                    {'title': 'Track Order', 'icon': 'local_shipping', 'color': 'bg-blue-500', 'action': lambda: ui.navigate.to('/track-order')},
                    {'title': 'Support', 'icon': 'help', 'color': 'bg-green-500', 'action': lambda: ui.navigate.to('/support')},
                    {'title': 'Settings', 'icon': 'settings', 'color': 'bg-gray-500', 'action': lambda: ui.navigate.to('/settings')},
                    {'title': 'Logout', 'icon': 'logout', 'color': 'bg-red-500', 'action': lambda: ui.navigate.to('/logout')},
                ]
                
                for action in quick_actions:
                    with ui.card().classes('p-4 bg-white shadow-sm hover:shadow-md transition-shadow cursor-pointer').on('click', action['action']):
                        with ui.element('div').classes('text-center'):
                            ui.icon(action['icon']).classes(f'text-white text-2xl {action["color"]} rounded-full p-3 mx-auto mb-3')
                            ui.label(action['title']).classes('font-medium text-gray-800')
