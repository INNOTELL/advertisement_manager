from nicegui import ui
import asyncio
from utils.api_client import api_client

@ui.page('/orders')
def show_orders_page(auth_state=None):
    # Header is handled by main.py
    
    async def load_orders():
        try:
            # For now, we'll use mock data since the backend doesn't have order endpoints yet
            # In the future, this would fetch from: /orders
            
            # Mock orders data - replace with actual API call when available
            orders_data = [
                {
                    'id': 'ORD-2024-001',
                    'placed_date': '2024-01-15',
                    'status': 'Delivered',
                    'total_amount': 1250.00,
                    'item_count': 2,
                    'items': [
                        {'name': 'iPhone 14 Pro', 'image': 'https://res.cloudinary.com/dyhqmkyfc/image/upload/v1758640412/ghlr3noblhotzlk1lvyx.avif'},
                        {'name': 'AirPods Pro', 'image': 'https://res.cloudinary.com/dyhqmkyfc/image/upload/v1758636628/zrbjlrdd0w4mvfmslsmz.png'}
                    ]
                },
                {
                    'id': 'ORD-2024-002',
                    'placed_date': '2024-01-10',
                    'status': 'Shipped',
                    'total_amount': 750.00,
                    'item_count': 1,
                    'items': [
                        {'name': 'Dell Laptop', 'image': 'https://res.cloudinary.com/dyhqmkyfc/image/upload/v1758640412/ghlr3noblhotzlk1lvyx.avif'}
                    ]
                },
                {
                    'id': 'ORD-2024-003',
                    'placed_date': '2024-01-05',
                    'status': 'Processing',
                    'total_amount': 300.00,
                    'item_count': 3,
                    'items': [
                        {'name': 'Fashion Item', 'image': 'https://res.cloudinary.com/dyhqmkyfc/image/upload/v1758638410/xbt0acxjhsmlf8pgcs1m.png'}
                    ]
                }
            ]
            
            # Display orders list
            with ui.element('div').classes('min-h-screen bg-gray-50 py-8'):
                with ui.element('div').classes('max-w-6xl mx-auto px-4'):
                    # Page Header
                    with ui.element('div').classes('mb-8'):
                        ui.label('My Orders').classes('text-3xl font-bold text-gray-800')
                        ui.label('Track and manage your orders').classes('text-gray-600 mt-2')
                    
                    # Orders List
                    for order in orders_data:
                        with ui.card().classes('bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-4 hover:shadow-xl transition-shadow'):
                            with ui.element('div').classes('flex justify-between items-start mb-4'):
                                with ui.element('div'):
                                    ui.label(f'Order #{order["id"]}').classes('text-xl font-bold text-gray-800')
                                    ui.label(f'Placed on {order["placed_date"]}').classes('text-gray-600')
                                    ui.label(f'{order["item_count"]} item(s)').classes('text-gray-500 text-sm')
                                
                                with ui.element('div').classes('text-right'):
                                    ui.label(f'GHS {order["total_amount"]:,.2f}').classes('text-2xl font-bold text-orange-500')
                                    with ui.element('div').classes('mt-2'):
                                        status_colors = {
                                            'Delivered': 'bg-green-100 text-green-600',
                                            'Shipped': 'bg-blue-100 text-blue-600',
                                            'Processing': 'bg-yellow-100 text-yellow-600',
                                            'Cancelled': 'bg-red-100 text-red-600'
                                        }
                                        status_color = status_colors.get(order['status'], 'bg-gray-100 text-gray-600')
                                        ui.label(order['status']).classes(f'px-3 py-1 rounded-full text-sm font-medium {status_color}')
                            
                            # Order Items Preview
                            with ui.element('div').classes('flex items-center gap-3 mb-4'):
                                ui.label('Items:').classes('text-gray-600 font-medium')
                                for item in order['items'][:3]:  # Show first 3 items
                                    if item.get('image'):
                                        ui.image(item['image']).classes('w-12 h-12 object-cover rounded-lg')
                                    else:
                                        with ui.element('div').classes('w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center'):
                                            ui.icon('image').classes('text-gray-400')
                                
                                if len(order['items']) > 3:
                                    with ui.element('div').classes('w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center'):
                                        ui.label(f'+{len(order["items"]) - 3}').classes('text-gray-600 text-sm font-medium')
                            
                            # Action Buttons
                            with ui.element('div').classes('flex gap-3'):
                                def view_order_details(order_id=order['id']):
                                    ui.navigate.to(f'/order_details?id={order_id}')
                                
                                def track_order(order_id=order['id']):
                                    ui.notify(f'Tracking for order {order_id} will be available soon!', type='info')
                                
                                def reorder_items(order_id=order['id']):
                                    ui.notify(f'Reorder for order {order_id} - redirecting to products...', type='info')
                                    ui.navigate.to('/dashboard')
                                
                                ui.button('View Details', on_click=view_order_details).classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium')
                                ui.button('Track', on_click=track_order).classes('bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg font-medium')
                                ui.button('Reorder', on_click=reorder_items).classes('bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium')
                    
                    # Empty state if no orders
                    if not orders_data:
                        with ui.card().classes('bg-white rounded-xl shadow-lg border border-gray-200 p-12 text-center'):
                            ui.icon('shopping_bag').classes('text-6xl text-gray-300 mb-4')
                            ui.label('No orders yet').classes('text-2xl font-bold text-gray-800 mb-2')
                            ui.label('Start shopping to see your orders here').classes('text-gray-600 mb-6')
                            ui.button('Start Shopping', on_click=lambda: ui.navigate.to('/dashboard')).classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold')
            
            # Add bottom spacing for footer
            with ui.element('div').classes('h-16'):
                pass
                
        except Exception as e:
            ui.notify(f'Error loading orders: {e}', type='negative')
            print(f"Orders error: {e}")
    
    # Load orders
    ui.timer(0.1, load_orders, once=True)