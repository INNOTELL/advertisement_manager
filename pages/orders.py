from nicegui import ui
import requests
from utils.api import base_url
from datetime import datetime, timedelta

def show_orders_page(auth_state=None):
    if not auth_state or not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('Order History').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Track and manage your orders').classes('text-gray-600')
            
            # Order Statistics
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-4 gap-6 mb-8'):
                stats = [
                    {'title': 'Total Orders', 'value': '24', 'icon': 'shopping_bag', 'color': 'bg-blue-500'},
                    {'title': 'Pending', 'value': '3', 'icon': 'schedule', 'color': 'bg-yellow-500'},
                    {'title': 'Delivered', 'value': '18', 'icon': 'check_circle', 'color': 'bg-green-500'},
                    {'title': 'Cancelled', 'value': '3', 'icon': 'cancel', 'color': 'bg-red-500'},
                ]
                
                for stat in stats:
                    with ui.card().classes('p-6 bg-white shadow-sm'):
                        with ui.element('div').classes('flex items-center gap-4'):
                            ui.icon(stat['icon']).classes(f'text-white text-2xl {stat["color"]} rounded-full p-3')
                            with ui.element('div'):
                                ui.label(stat['value']).classes('text-2xl font-bold text-gray-800')
                                ui.label(stat['title']).classes('text-sm text-gray-600')
            
            # Filter and Search
            with ui.card().classes('p-6 bg-white shadow-sm mb-8'):
                with ui.row().classes('items-center gap-4 w-full'):
                    # Search
                    search_input = ui.input('Search orders...').classes('flex-1').props('outlined')
                    
                    # Status Filter
                    status_select = ui.select(['All Orders', 'Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled'], 
                                            value='All Orders').classes('w-48').props('outlined')
                    
                    # Date Filter
                    date_select = ui.select(['All Time', 'Last 7 days', 'Last 30 days', 'Last 3 months'], 
                                          value='All Time').classes('w-48').props('outlined')
                    
                    ui.button('Filter', icon='filter_list').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg')
            
            # Orders List
            with ui.card().classes('bg-white shadow-sm'):
                # Demo orders data
                orders = [
                    {
                        'id': 'ORD-2024-001',
                        'date': '2024-01-15',
                        'status': 'Delivered',
                        'total': 1250.00,
                        'items': [
                            {'name': 'iPhone 14 Pro', 'price': 800.00, 'quantity': 1, 'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=100&h=100&fit=crop'},
                            {'name': 'AirPods Pro', 'price': 450.00, 'quantity': 1, 'image': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=100&h=100&fit=crop'}
                        ],
                        'tracking': 'GH123456789',
                        'delivery_date': '2024-01-18'
                    },
                    {
                        'id': 'ORD-2024-002',
                        'date': '2024-01-20',
                        'status': 'Shipped',
                        'total': 350.00,
                        'items': [
                            {'name': 'Samsung Galaxy Buds', 'price': 350.00, 'quantity': 1, 'image': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=100&h=100&fit=crop'}
                        ],
                        'tracking': 'GH987654321',
                        'delivery_date': '2024-01-25'
                    },
                    {
                        'id': 'ORD-2024-003',
                        'date': '2024-01-22',
                        'status': 'Processing',
                        'total': 120.00,
                        'items': [
                            {'name': 'Phone Case', 'price': 60.00, 'quantity': 2, 'image': 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=100&h=100&fit=crop'}
                        ],
                        'tracking': None,
                        'delivery_date': None
                    }
                ]
                
                for order in orders:
                    with ui.element('div').classes('border-b border-gray-200 last:border-b-0 p-6'):
                        # Order Header
                        with ui.row().classes('items-center justify-between mb-4'):
                            with ui.element('div'):
                                ui.label(f'Order #{order["id"]}').classes('text-lg font-semibold text-gray-800')
                                ui.label(f'Placed on {order["date"]}').classes('text-sm text-gray-600')
                            
                            with ui.element('div').classes('text-right'):
                                ui.label(f'GHS {order["total"]:,.2f}').classes('text-xl font-bold text-orange-500')
                                # Status badge
                                status_colors = {
                                    'Delivered': 'bg-green-100 text-green-800',
                                    'Shipped': 'bg-blue-100 text-blue-800',
                                    'Processing': 'bg-yellow-100 text-yellow-800',
                                    'Pending': 'bg-gray-100 text-gray-800',
                                    'Cancelled': 'bg-red-100 text-red-800'
                                }
                                ui.label(order['status']).classes(f'px-3 py-1 rounded-full text-sm font-medium {status_colors.get(order["status"], "bg-gray-100 text-gray-800")}')
                        
                        # Order Items
                        with ui.element('div').classes('mb-4'):
                            for item in order['items']:
                                with ui.row().classes('items-center gap-4 py-2'):
                                    ui.image(item['image']).classes('w-16 h-16 object-cover rounded-lg')
                                    with ui.element('div').classes('flex-1'):
                                        ui.label(item['name']).classes('font-medium text-gray-800')
                                        ui.label(f'Quantity: {item["quantity"]}').classes('text-sm text-gray-600')
                                    ui.label(f'GHS {item["price"]:,.2f}').classes('font-semibold text-gray-800')
                        
                        # Order Actions
                        with ui.row().classes('items-center justify-between'):
                            with ui.row().classes('gap-3'):
                                if order['tracking']:
                                    ui.button('Track Package', icon='local_shipping').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm')
                                
                                if order['status'] == 'Delivered':
                                    ui.button('Reorder', icon='refresh').classes('bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm')
                                    ui.button('Write Review', icon='rate_review').classes('bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg text-sm')
                                
                                if order['status'] in ['Pending', 'Processing']:
                                    ui.button('Cancel Order', icon='cancel').classes('bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm')
                            
                            # Delivery Info
                            if order['delivery_date']:
                                ui.label(f'Expected delivery: {order["delivery_date"]}').classes('text-sm text-gray-600')
            
            # Order Tracking Modal (would be triggered by Track Package button)
            with ui.dialog() as track_dialog:
                with ui.card().classes('p-6 w-full max-w-2xl'):
                    ui.label('Track Your Package').classes('text-2xl font-bold text-gray-800 mb-6')
                    
                    # Tracking Timeline
                    tracking_steps = [
                        {'status': 'Order Placed', 'date': '2024-01-15', 'time': '10:30 AM', 'completed': True},
                        {'status': 'Processing', 'date': '2024-01-15', 'time': '2:15 PM', 'completed': True},
                        {'status': 'Shipped', 'date': '2024-01-16', 'time': '9:00 AM', 'completed': True},
                        {'status': 'In Transit', 'date': '2024-01-17', 'time': '3:45 PM', 'completed': True},
                        {'status': 'Out for Delivery', 'date': '2024-01-18', 'time': '8:00 AM', 'completed': False},
                        {'status': 'Delivered', 'date': '', 'time': '', 'completed': False},
                    ]
                    
                    for i, step in enumerate(tracking_steps):
                        with ui.row().classes('items-center gap-4 py-3'):
                            # Status icon
                            if step['completed']:
                                ui.icon('check_circle').classes('text-green-500 text-xl')
                            else:
                                ui.icon('radio_button_unchecked').classes('text-gray-400 text-xl')
                            
                            with ui.element('div').classes('flex-1'):
                                ui.label(step['status']).classes('font-medium text-gray-800')
                                if step['completed']:
                                    ui.label(f'{step["date"]} at {step["time"]}').classes('text-sm text-gray-600')
                                else:
                                    ui.label('Pending').classes('text-sm text-gray-400')
                            
                            # Connector line (except for last item)
                            if i < len(tracking_steps) - 1:
                                ui.element('div').classes('w-px h-8 bg-gray-300 ml-2')
                    
                    ui.button('Close', on_click=track_dialog.close).classes('bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg mt-6')
