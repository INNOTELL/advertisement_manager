from nicegui import ui
import requests
from utils.api import base_url

def show_cart_page(auth_state=None):
    # Allow access for testing - no authentication required
    
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('Shopping Cart').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Review your items before checkout').classes('text-gray-600')
            
            # Demo cart data
            cart_items = [
                {
                    'id': 1,
                    'name': 'iPhone 15 Pro Max',
                    'price': 4500.00,
                    'original_price': 4800.00,
                    'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=200&h=200&fit=crop',
                    'category': 'Electronics',
                    'quantity': 1,
                    'in_stock': True,
                    'seller': 'TechStore Ghana'
                },
                {
                    'id': 2,
                    'name': 'AirPods Pro 2nd Gen',
                    'price': 1200.00,
                    'original_price': 1500.00,
                    'image': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=200&h=200&fit=crop',
                    'category': 'Electronics',
                    'quantity': 2,
                    'in_stock': True,
                    'seller': 'AudioHub'
                },
                {
                    'id': 3,
                    'name': 'Nike Air Max 270',
                    'price': 450.00,
                    'original_price': 500.00,
                    'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200&h=200&fit=crop',
                    'category': 'Fashion',
                    'quantity': 1,
                    'in_stock': True,
                    'seller': 'ShoeWorld'
                }
            ]
            
            if not cart_items:
                # Empty cart state
                with ui.card().classes('p-12 bg-white shadow-sm text-center'):
                    ui.icon('shopping_cart').classes('text-8xl text-gray-300 mb-6')
                    ui.label('Your cart is empty').classes('text-2xl font-semibold text-gray-600 mb-4')
                    ui.label('Add some items to get started').classes('text-gray-500 mb-6')
                    ui.button('Continue Shopping', on_click=lambda: ui.navigate.to('/')).classes('bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold')
            else:
                with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-3 gap-8'):
                    # Cart Items
                    with ui.element('div').classes('lg:col-span-2'):
                        with ui.card().classes('bg-white shadow-sm'):
                            # Cart Header
                            with ui.element('div').classes('p-6 border-b border-gray-200'):
                                with ui.row().classes('items-center justify-between'):
                                    ui.label(f'Cart ({len(cart_items)} items)').classes('text-xl font-bold text-gray-800')
                                    ui.button('Clear Cart', icon='clear_all').classes('text-red-500 hover:text-red-600 font-medium')
                            
                            # Cart Items List
                            with ui.element('div').classes('divide-y divide-gray-200'):
                                for item in cart_items:
                                    with ui.element('div').classes('p-6'):
                                        with ui.row().classes('items-center gap-4'):
                                            # Product Image
                                            ui.image(item['image']).classes('w-20 h-20 object-cover rounded-lg')
                                            
                                            # Product Details
                                            with ui.element('div').classes('flex-1'):
                                                ui.label(item['name']).classes('text-lg font-semibold text-gray-800 mb-1')
                                                ui.label(f'Sold by {item["seller"]}').classes('text-sm text-gray-600 mb-2')
                                                
                                                # Price
                                                with ui.row().classes('items-baseline gap-2'):
                                                    ui.label(f'GHS {item["price"]:,.2f}').classes('text-lg font-bold text-orange-500')
                                                    if item['original_price'] > item['price']:
                                                        ui.label(f'GHS {item["original_price"]:,.2f}').classes('text-sm text-gray-400 line-through')
                                                
                                                # Stock status
                                                if item['in_stock']:
                                                    with ui.row().classes('items-center gap-1 mt-1'):
                                                        ui.icon('check_circle').classes('text-green-600 text-sm')
                                                        ui.label('In Stock').classes('text-green-600 text-sm')
                                                else:
                                                    with ui.row().classes('items-center gap-1 mt-1'):
                                                        ui.icon('cancel').classes('text-red-600 text-sm')
                                                        ui.label('Out of Stock').classes('text-red-600 text-sm')
                                            
                                            # Quantity Controls
                                            with ui.element('div').classes('flex items-center gap-2'):
                                                ui.button('-', on_click=lambda i=item['id']: update_quantity(i, -1)).classes('w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full').props('flat round')
                                                ui.label(str(item['quantity'])).classes('w-12 text-center font-medium')
                                                ui.button('+', on_click=lambda i=item['id']: update_quantity(i, 1)).classes('w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full').props('flat round')
                                            
                                            # Item Total
                                            with ui.element('div').classes('text-right min-w-24'):
                                                ui.label(f'GHS {(item["price"] * item["quantity"]):,.2f}').classes('text-lg font-bold text-gray-800')
                                            
                                            # Remove button
                                            ui.button(icon='delete', on_click=lambda i=item['id']: remove_from_cart(i)).classes('text-red-500 hover:text-red-600 p-2').props('flat round')
                    
                    # Order Summary
                    with ui.element('div').classes('lg:col-span-1'):
                        with ui.card().classes('bg-white shadow-sm sticky top-8'):
                            ui.label('Order Summary').classes('text-xl font-bold text-gray-800 mb-6 p-6 border-b border-gray-200')
                            
                            with ui.element('div').classes('p-6 space-y-4'):
                                # Subtotal
                                subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
                                with ui.row().classes('justify-between'):
                                    ui.label('Subtotal').classes('text-gray-600')
                                    ui.label(f'GHS {subtotal:,.2f}').classes('font-medium')
                                
                                # Shipping
                                shipping = 0 if subtotal >= 200 else 50
                                with ui.row().classes('justify-between'):
                                    ui.label('Shipping').classes('text-gray-600')
                                    ui.label(f'GHS {shipping:,.2f}').classes('font-medium')
                                
                                # Tax
                                tax = subtotal * 0.15  # 15% VAT
                                with ui.row().classes('justify-between'):
                                    ui.label('Tax (15% VAT)').classes('text-gray-600')
                                    ui.label(f'GHS {tax:,.2f}').classes('font-medium')
                                
                                # Total
                                total = subtotal + shipping + tax
                                with ui.row().classes('justify-between border-t border-gray-200 pt-4'):
                                    ui.label('Total').classes('text-lg font-bold text-gray-800')
                                    ui.label(f'GHS {total:,.2f}').classes('text-lg font-bold text-orange-500')
                                
                                # Free shipping notice
                                if subtotal < 200:
                                    with ui.element('div').classes('bg-blue-50 border border-blue-200 rounded-lg p-3 mt-4'):
                                        ui.label('Add GHS 50 more for free shipping!').classes('text-blue-700 text-sm font-medium')
                                
                                # Checkout Button
                                ui.button('Proceed to Checkout', icon='shopping_cart').classes('w-full bg-orange-500 hover:bg-orange-600 text-white py-4 rounded-lg font-semibold text-lg mt-6')
                                
                                # Payment Methods
                                with ui.element('div').classes('mt-6 pt-6 border-t border-gray-200'):
                                    ui.label('We Accept').classes('text-sm text-gray-600 mb-3')
                                    with ui.row().classes('gap-2'):
                                        ui.button('Mobile Money').classes('bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded text-sm')
                                        ui.button('Card').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded text-sm')
                                        ui.button('Cash on Delivery').classes('bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded text-sm')
                                
                                # Security badges
                                with ui.element('div').classes('mt-6 pt-6 border-t border-gray-200 text-center'):
                                    ui.label('Secure Checkout').classes('text-sm text-gray-600 mb-2')
                                    with ui.row().classes('justify-center gap-4'):
                                        ui.icon('security').classes('text-green-500 text-xl')
                                        ui.icon('lock').classes('text-green-500 text-xl')
                                        ui.icon('verified').classes('text-green-500 text-xl')
            
            # Recommended Products
            with ui.card().classes('mt-8 p-6 bg-white shadow-sm'):
                ui.label('You might also like').classes('text-xl font-bold text-gray-800 mb-6')
                
                recommended_items = [
                    {
                        'name': 'iPhone 15 Pro Case',
                        'price': 120.00,
                        'image': 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=200&h=200&fit=crop',
                        'rating': 4.5
                    },
                    {
                        'name': 'Wireless Charger',
                        'price': 80.00,
                        'image': 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=200&h=200&fit=crop',
                        'rating': 4.3
                    },
                    {
                        'name': 'Screen Protector',
                        'price': 25.00,
                        'image': 'https://images.unsplash.com/photo-1556656793-08538906a9f8?w=200&h=200&fit=crop',
                        'rating': 4.7
                    }
                ]
                
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6'):
                    for item in recommended_items:
                        with ui.card().classes('p-4 hover:shadow-lg transition-shadow cursor-pointer').on('click', lambda i=item: add_to_cart(i)):
                            ui.image(item['image']).classes('w-full h-32 object-cover rounded-lg mb-3')
                            ui.label(item['name']).classes('font-medium text-gray-800 mb-2')
                            with ui.row().classes('items-center justify-between'):
                                ui.label(f'GHS {item["price"]:,.2f}').classes('font-bold text-orange-500')
                                with ui.row().classes('items-center gap-1'):
                                    ui.icon('star').classes('text-yellow-400 text-sm')
                                    ui.label(str(item['rating'])).classes('text-sm text-gray-600')

def update_quantity(item_id, change):
    """Update item quantity in cart"""
    ui.notify(f'Quantity updated for item {item_id}', type='info')
    # In a real implementation, this would update the cart state
    # For now, just show a notification

def remove_from_cart(item_id):
    """Remove item from cart"""
    ui.notify(f'Item {item_id} removed from cart', type='positive')
    # In a real implementation, this would remove the item from cart
    # For now, just show a notification

def add_to_cart(item):
    """Add item to cart"""
    ui.notify(f'{item["name"]} added to cart', type='positive')
    # In a real implementation, this would add the item to cart
    # For now, just show a notification
