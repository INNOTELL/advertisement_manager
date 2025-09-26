from nicegui import ui
import asyncio
from utils.api_client import api_client

@ui.page('/order_details')
def show_order_details_page():
    q = ui.context.client.request.query_params
    order_id = q.get('id', 'ORD-2024-001')  # Default order ID for demo
    
    # Header is handled by main.py
    
    async def load_order_details():
        try:
            # For now, we'll use mock data since the backend doesn't have order endpoints yet
            # In the future, this would fetch from: /orders/{order_id}
            
            # Mock order data - replace with actual API call when available
            order_data = {
                'id': order_id,
                'placed_date': '2024-01-15',
                'status': 'Delivered',
                'total_amount': 1250.00,
                'expected_delivery': '2024-01-18',
                'items': [
                    {
                        'id': 'item1',
                        'name': 'iPhone 14 Pro',
                        'quantity': 1,
                        'price': 800.00,
                        'image': 'https://res.cloudinary.com/dyhqmkyfc/image/upload/v1758640412/ghlr3noblhotzlk1lvyx.avif'  # Using existing image from backend
                    },
                    {
                        'id': 'item2', 
                        'name': 'AirPods Pro',
                        'quantity': 1,
                        'price': 450.00,
                        'image': 'https://res.cloudinary.com/dyhqmkyfc/image/upload/v1758636628/zrbjlrdd0w4mvfmslsmz.png'  # Using existing image from backend
                    }
                ]
            }
            
            # Display order details
            with ui.element('div').classes('min-h-screen bg-gray-50 py-8'):
                with ui.element('div').classes('max-w-4xl mx-auto px-4'):
                    # Order Summary Section
                    with ui.card().classes('bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6'):
                        with ui.element('div').classes('flex justify-between items-start mb-4'):
                            with ui.element('div'):
                                ui.label(f'Order #{order_data["id"]}').classes('text-2xl font-bold text-gray-800')
                                ui.label(f'Placed on {order_data["placed_date"]}').classes('text-gray-600 mt-1')
                            
                            with ui.element('div').classes('text-right'):
                                ui.label(f'GHS {order_data["total_amount"]:,.2f}').classes('text-3xl font-bold text-orange-500')
                                with ui.element('div').classes('mt-2'):
                                    status_color = 'bg-green-100 text-green-600' if order_data['status'] == 'Delivered' else 'bg-yellow-100 text-yellow-600'
                                    ui.label(order_data['status']).classes(f'px-3 py-1 rounded-full text-sm font-medium {status_color}')
                    
                    # Ordered Items Section
                    with ui.card().classes('bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6'):
                        ui.label('Ordered Items').classes('text-xl font-bold text-gray-800 mb-4')
                        
                        for item in order_data['items']:
                            with ui.element('div').classes('flex items-center gap-4 p-4 border border-gray-200 rounded-lg mb-3'):
                                # Product Image - fetched from backend
                                if item.get('image'):
                                    ui.image(item['image']).classes('w-16 h-16 object-cover rounded-lg')
                                else:
                                    with ui.element('div').classes('w-16 h-16 bg-gray-200 rounded-lg flex items-center justify-center'):
                                        ui.icon('image').classes('text-gray-400')
                                
                                # Product Details
                                with ui.element('div').classes('flex-1'):
                                    ui.label(item['name']).classes('font-semibold text-gray-800')
                                    ui.label(f'Quantity: {item["quantity"]}').classes('text-gray-600 text-sm')
                                
                                # Price
                                ui.label(f'GHS {item["price"]:,.2f}').classes('font-bold text-gray-800')
                    
                    # Action Buttons and Delivery Info
                    with ui.card().classes('bg-white rounded-xl shadow-lg border border-gray-200 p-6'):
                        with ui.element('div').classes('flex justify-between items-center'):
                            # Action Buttons
                            with ui.element('div').classes('flex gap-4'):
                                def track_package():
                                    ui.notify('Tracking information will be available soon!', type='info')
                                    # In the future: ui.navigate.to(f'/track_package?id={order_id}')
                                
                                def reorder():
                                    ui.notify('Redirecting to reorder...', type='info')
                                    ui.navigate.to('/dashboard')  # Navigate to products page
                                
                                def write_review():
                                    ui.notify('Review system coming soon!', type='info')
                                    # In the future: ui.navigate.to(f'/write_review?order_id={order_id}')
                                
                                ui.button('TRACK PACKAGE', on_click=track_package, icon='local_shipping').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium')
                                ui.button('REORDER', on_click=reorder, icon='refresh').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium')
                                ui.button('WRITE REVIEW', on_click=write_review, icon='rate_review').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium')
                            
                            # Expected Delivery
                            with ui.element('div').classes('text-right'):
                                ui.label(f'Expected delivery: {order_data["expected_delivery"]}').classes('text-gray-600')
                    
                    # Back to Orders Button
                    with ui.element('div').classes('mt-6 text-center'):
                        def back_to_orders():
                            ui.navigate.to('/orders')  # Navigate to orders list page
                        
                        ui.button('Back to Orders', on_click=back_to_orders, icon='arrow_back').classes('bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-medium')
            
            # Add bottom spacing for footer
            with ui.element('div').classes('h-16'):
                pass
                
        except Exception as e:
            ui.notify(f'Error loading order details: {e}', type='negative')
            print(f"Order details error: {e}")
    
    # Load order details
    ui.timer(0.1, load_order_details, once=True)
