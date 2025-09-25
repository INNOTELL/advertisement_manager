from nicegui import ui
import asyncio
from utils.api_client import api_client

def show_cart_page(auth_state=None):
    # Allow access for testing - no authentication required
    
    # Cart state management
    cart_items = []
    removed_items = set()  # Track removed items
    
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('Shopping Cart').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Review your items before checkout').classes('text-gray-600')
            
            # Cart items container - will be populated with backend data
            cart_container = ui.element('div')
            
            async def load_cart_items():
                """Load cart items from backend"""
                try:
                    # Use the centralized API client to fetch all adverts
                    if not api_client._discovered:
                        print("🔧 API client not discovered, initializing...")
                        await api_client.discover_endpoints()
                    
                    print("🌐 Fetching adverts for cart from backend...")
                    success, response = await api_client.get_ads()
                    
                    if success and response:
                        # Handle different response formats
                        if isinstance(response, dict):
                            items = response.get("data", response.get("adverts", response.get("items", [])))
                        elif isinstance(response, list):
                            items = response
                        else:
                            items = []
                        
                        # Convert backend adverts to cart format
                        all_cart_items = []
                        for i, advert in enumerate(items[:3]):  # Show first 3 adverts as cart items
                            # Extract image URL
                            image_url = None
                            if advert.get('image'):
                                if advert['image'].startswith('http'):
                                    image_url = advert['image']
                                elif advert['image'].startswith('data:image'):
                                    image_url = advert['image']
                                else:
                                    # Assume it's base64 data
                                    image_url = f"data:image/jpeg;base64,{advert['image']}"
                            
                            # Create cart item from advert
                            cart_item = {
                                'id': advert.get('id', i + 1),
                                'name': advert.get('title', 'Unknown Product'),
                                'price': float(advert.get('price', 0)),
                                'original_price': float(advert.get('price', 0)) * 1.1,  # 10% markup for original price
                                'image': image_url or 'https://via.placeholder.com/200x200?text=No+Image',
                                'category': advert.get('category', 'General'),
                                'quantity': 1,  # Default quantity
                                'in_stock': True,  # Assume in stock
                                'seller': advert.get('seller', 'InnoHub Seller'),
                                'description': advert.get('description', ''),
                                'location': advert.get('location', 'Ghana')
                            }
                            all_cart_items.append(cart_item)
                        
                        # Filter out removed items
                        cart_items.clear()
                        cart_items.extend([item for item in all_cart_items if item['id'] not in removed_items])
                        
                        print(f"✅ Loaded {len(cart_items)} items for cart (filtered from {len(all_cart_items)} total)")
                        render_cart_items(cart_items)
                        
                    else:
                        print(f"❌ Failed to fetch adverts: {response}")
                        # Show empty cart
                        render_empty_cart()
                        
                except Exception as e:
                    print(f"❌ Error loading cart items: {e}")
                    ui.notify(f"Failed to load cart items: {e}", type='negative')
                    # Show empty cart
                    render_empty_cart()
            
            def render_cart_items(cart_items):
                """Render cart items"""
                cart_container.clear()
                with cart_container:
                    if not cart_items:
                        render_empty_cart()
                    else:
                        with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-3 gap-8'):
                            # Cart Items
                            with ui.element('div').classes('lg:col-span-2'):
                                with ui.card().classes('bg-white shadow-sm'):
                                    # Cart Header
                                    with ui.element('div').classes('p-6 border-b border-gray-200'):
                                        with ui.row().classes('items-center justify-between'):
                                            ui.label(f'Cart ({len(cart_items)} items)').classes('text-xl font-bold text-gray-800')
                                            
                                            def clear_cart():
                                                """Clear all items from cart"""
                                                if cart_items:
                                                    # Add all current items to removed_items
                                                    for item in cart_items:
                                                        removed_items.add(item['id'])
                                                    
                                                    # Clear the cart
                                                    cart_items.clear()
                                                    
                                                    ui.notify('Cart cleared', type='positive')
                                                    
                                                    # Refresh the cart display
                                                    render_cart_items(cart_items)
                                                else:
                                                    ui.notify('Cart is already empty', type='info')
                                            
                                            ui.button('Clear Cart', on_click=clear_cart, icon='clear_all').classes('text-red-500 hover:text-red-600 font-medium')
                                    
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
            
            def render_empty_cart():
                """Render empty cart state"""
                cart_container.clear()
                with cart_container:
                    # Empty cart state
                    with ui.card().classes('p-12 bg-white shadow-sm text-center'):
                        ui.icon('shopping_cart').classes('text-8xl text-gray-300 mb-6')
                        ui.label('Your cart is empty').classes('text-2xl font-semibold text-gray-600 mb-4')
                        ui.label('Add some items to get started').classes('text-gray-500 mb-6')
                        ui.button('Continue Shopping', on_click=lambda: ui.navigate.to('/')).classes('bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold')
            
            # Load cart items from backend
            ui.timer(0.1, lambda: asyncio.create_task(load_cart_items()), once=True)
            
            # Recommended Products - Load from backend
            recommended_container = ui.element('div')
            
            async def load_recommended_products():
                """Load recommended products from backend"""
                try:
                    if not api_client._discovered:
                        await api_client.discover_endpoints()
                    
                    print("🌐 Fetching recommended products from backend...")
                    success, response = await api_client.get_ads()
                    
                    if success and response:
                        # Handle different response formats
                        if isinstance(response, dict):
                            items = response.get("data", response.get("adverts", response.get("items", [])))
                        elif isinstance(response, list):
                            items = response
                        else:
                            items = []
                        
                        # Take items 3-6 for recommendations (skip first 3 used in cart)
                        recommended_items = items[3:6] if len(items) > 3 else items
                        
                        render_recommended_products(recommended_items)
                        
                    else:
                        print(f"❌ Failed to fetch recommended products: {response}")
                        render_recommended_products([])
                        
                except Exception as e:
                    print(f"❌ Error loading recommended products: {e}")
                    render_recommended_products([])
            
            def render_recommended_products(recommended_items):
                """Render recommended products"""
                recommended_container.clear()
                with recommended_container:
                    with ui.card().classes('mt-8 p-6 bg-white shadow-sm'):
                        ui.label('You might also like').classes('text-xl font-bold text-gray-800 mb-6')
                        
                        if recommended_items:
                            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6'):
                                for item in recommended_items:
                                    # Extract image URL
                                    image_url = None
                                    if item.get('image'):
                                        if item['image'].startswith('http'):
                                            image_url = item['image']
                                        elif item['image'].startswith('data:image'):
                                            image_url = item['image']
                                        else:
                                            image_url = f"data:image/jpeg;base64,{item['image']}"
                                    
                                    with ui.card().classes('p-4 hover:shadow-lg transition-shadow cursor-pointer').on('click', lambda i=item: add_to_cart(i)):
                                        ui.image(image_url or 'https://via.placeholder.com/200x200?text=No+Image').classes('w-full h-32 object-cover rounded-lg mb-3')
                                        ui.label(item.get('title', 'Unknown Product')).classes('font-medium text-gray-800 mb-2')
                                        with ui.row().classes('items-center justify-between'):
                                            ui.label(f'GHS {float(item.get("price", 0)):,.2f}').classes('font-bold text-orange-500')
                                            with ui.row().classes('items-center gap-1'):
                                                ui.icon('star').classes('text-yellow-400 text-sm')
                                                ui.label('4.5').classes('text-sm text-gray-600')  # Default rating
                        else:
                            ui.label('No recommended products available').classes('text-gray-500 text-center py-8')
            
            # Load recommended products from backend
            ui.timer(0.2, lambda: asyncio.create_task(load_recommended_products()), once=True)
            
            def update_quantity(item_id, change):
                """Update item quantity in cart"""
                # Find the item in cart_items and update quantity
                for item in cart_items:
                    if item['id'] == item_id:
                        new_quantity = max(1, item['quantity'] + change)  # Minimum quantity is 1
                        item['quantity'] = new_quantity
                        ui.notify(f'Quantity updated to {new_quantity}', type='info')
                        # Refresh the cart display
                        render_cart_items(cart_items)
                        return
                ui.notify(f'Item {item_id} not found in cart', type='negative')

            def remove_from_cart(item_id):
                """Remove item from cart"""
                # Add to removed items set
                removed_items.add(item_id)
                
                # Find item name for notification before removing
                item_name = "Item"
                for item in cart_items:
                    if item['id'] == item_id:
                        item_name = item['name']
                        break
                
                # Remove from current cart_items list
                cart_items[:] = [item for item in cart_items if item['id'] != item_id]
                
                ui.notify(f'{item_name} removed from cart', type='positive')
                
                # Refresh the cart display
                render_cart_items(cart_items)

            def add_to_cart(item):
                """Add item to cart"""
                # Check if item is already in cart
                for cart_item in cart_items:
                    if cart_item['id'] == item.get('id'):
                        cart_item['quantity'] += 1
                        ui.notify(f'{item.get("title", item.get("name", "Item"))} quantity increased', type='positive')
                        render_cart_items(cart_items)
                        return
                
                # Add new item to cart
                cart_item = {
                    'id': item.get('id', len(cart_items) + 1),
                    'name': item.get('title', item.get('name', 'Unknown Product')),
                    'price': float(item.get('price', 0)),
                    'original_price': float(item.get('price', 0)) * 1.1,
                    'image': item.get('image', 'https://via.placeholder.com/200x200?text=No+Image'),
                    'category': item.get('category', 'General'),
                    'quantity': 1,
                    'in_stock': True,
                    'seller': item.get('seller', 'InnoHub Seller'),
                    'description': item.get('description', ''),
                    'location': item.get('location', 'Ghana')
                }
                
                cart_items.append(cart_item)
                ui.notify(f'{cart_item["name"]} added to cart', type='positive')
                
                # Refresh the cart display
                render_cart_items(cart_items)
