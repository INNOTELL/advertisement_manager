from nicegui import ui
import requests
from utils.api import base_url

def show_wishlist_page(auth_state=None):
    if not auth_state or not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('My Wishlist').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Save items you love for later').classes('text-gray-600')
            
            # Wishlist Statistics
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6 mb-8'):
                stats = [
                    {'title': 'Total Items', 'value': '12', 'icon': 'favorite', 'color': 'bg-red-500'},
                    {'title': 'In Stock', 'value': '8', 'icon': 'check_circle', 'color': 'bg-green-500'},
                    {'title': 'Price Drops', 'value': '3', 'icon': 'trending_down', 'color': 'bg-blue-500'},
                ]
                
                for stat in stats:
                    with ui.card().classes('p-6 bg-white shadow-sm'):
                        with ui.element('div').classes('flex items-center gap-4'):
                            ui.icon(stat['icon']).classes(f'text-white text-2xl {stat["color"]} rounded-full p-3')
                            with ui.element('div'):
                                ui.label(stat['value']).classes('text-2xl font-bold text-gray-800')
                                ui.label(stat['title']).classes('text-sm text-gray-600')
            
            # Wishlist Actions
            with ui.card().classes('p-6 bg-white shadow-sm mb-8'):
                with ui.row().classes('items-center justify-between w-full'):
                    with ui.row().classes('items-center gap-4'):
                        ui.button('Select All', icon='check_box').classes('bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg')
                        ui.button('Clear All', icon='clear_all').classes('bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg')
                        ui.button('Share Wishlist', icon='share').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.label('Sort by:').classes('text-gray-600')
                        sort_select = ui.select(['Recently Added', 'Price: Low to High', 'Price: High to Low', 'Name A-Z'], 
                                              value='Recently Added').classes('w-48').props('outlined')
            
            # Wishlist Items
            # Demo wishlist data
            wishlist_items = [
                {
                    'id': 1,
                    'name': 'iPhone 15 Pro Max',
                    'price': 4500.00,
                    'original_price': 4800.00,
                    'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=300&h=300&fit=crop',
                    'category': 'Electronics',
                    'added_date': '2024-01-15',
                    'in_stock': True,
                    'rating': 4.8,
                    'reviews': 1247
                },
                {
                    'id': 2,
                    'name': 'MacBook Pro M3',
                    'price': 8500.00,
                    'original_price': 9000.00,
                    'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop',
                    'category': 'Computing',
                    'added_date': '2024-01-12',
                    'in_stock': True,
                    'rating': 4.9,
                    'reviews': 892
                },
                {
                    'id': 3,
                    'name': 'Samsung Galaxy S24 Ultra',
                    'price': 4200.00,
                    'original_price': 4200.00,
                    'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop',
                    'category': 'Electronics',
                    'added_date': '2024-01-10',
                    'in_stock': False,
                    'rating': 4.7,
                    'reviews': 2156
                },
                {
                    'id': 4,
                    'name': 'AirPods Pro 2nd Gen',
                    'price': 1200.00,
                    'original_price': 1500.00,
                    'image': 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=300&h=300&fit=crop',
                    'category': 'Electronics',
                    'added_date': '2024-01-08',
                    'in_stock': True,
                    'rating': 4.6,
                    'reviews': 3421
                },
                {
                    'id': 5,
                    'name': 'Nike Air Max 270',
                    'price': 450.00,
                    'original_price': 500.00,
                    'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop',
                    'category': 'Fashion',
                    'added_date': '2024-01-05',
                    'in_stock': True,
                    'rating': 4.5,
                    'reviews': 1876
                },
                {
                    'id': 6,
                    'name': 'Sony WH-1000XM5 Headphones',
                    'price': 1800.00,
                    'original_price': 2000.00,
                    'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop',
                    'category': 'Electronics',
                    'added_date': '2024-01-03',
                    'in_stock': True,
                    'rating': 4.8,
                    'reviews': 2934
                }
            ]
            
            if not wishlist_items:
                # Empty wishlist state
                with ui.card().classes('p-12 bg-white shadow-sm text-center'):
                    ui.icon('favorite_border').classes('text-8xl text-gray-300 mb-6')
                    ui.label('Your wishlist is empty').classes('text-2xl font-semibold text-gray-600 mb-4')
                    ui.label('Start adding items you love to your wishlist').classes('text-gray-500 mb-6')
                    ui.button('Start Shopping', on_click=lambda: ui.navigate.to('/')).classes('bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold')
            else:
                # Wishlist items grid
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'):
                    for item in wishlist_items:
                        with ui.card().classes('bg-white shadow-sm hover:shadow-lg transition-shadow overflow-hidden group'):
                            # Product Image
                            with ui.element('div').classes('relative overflow-hidden bg-gray-50 h-64'):
                                ui.image(item['image']).classes('w-full h-full object-cover group-hover:scale-110 transition-transform duration-300')
                                
                                # Stock status badge
                                if not item['in_stock']:
                                    with ui.element('div').classes('absolute top-3 left-3 bg-red-500 text-white px-2 py-1 rounded text-xs font-medium'):
                                        ui.label('Out of Stock')
                                
                                # Remove from wishlist button
                                with ui.element('div').classes('absolute top-3 right-3'):
                                    ui.button(icon='favorite', on_click=lambda i=item['id']: remove_from_wishlist(i)).classes('bg-white/80 hover:bg-white text-red-500 rounded-full p-2 shadow-lg').props('flat round')
                                
                                # Quick actions overlay
                                with ui.element('div').classes('absolute bottom-3 left-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity'):
                                    with ui.row().classes('gap-2'):
                                        ui.button('Quick View', icon='visibility').classes('flex-1 bg-white/90 hover:bg-white text-gray-800 px-3 py-2 rounded text-sm font-medium')
                                        ui.button('Add to Cart', icon='shopping_cart').classes('flex-1 bg-orange-500 hover:bg-orange-600 text-white px-3 py-2 rounded text-sm font-medium')
                            
                            # Product Details
                            with ui.element('div').classes('p-4'):
                                # Category
                                ui.label(item['category']).classes('text-xs text-gray-500 uppercase tracking-wide mb-1')
                                
                                # Product Name
                                ui.label(item['name']).classes('text-lg font-semibold text-gray-800 mb-2 line-clamp-2')
                                
                                # Rating
                                with ui.row().classes('items-center gap-2 mb-2'):
                                    with ui.row().classes('items-center gap-1'):
                                        for i in range(5):
                                            ui.icon('star').classes('text-yellow-400 text-sm')
                                    ui.label(f'{item["rating"]} ({item["reviews"]} reviews)').classes('text-xs text-gray-600')
                                
                                # Price
                                with ui.row().classes('items-baseline gap-2 mb-3'):
                                    ui.label(f'GHS {item["price"]:,.2f}').classes('text-xl font-bold text-orange-500')
                                    if item['original_price'] > item['price']:
                                        ui.label(f'GHS {item["original_price"]:,.2f}').classes('text-sm text-gray-400 line-through')
                                
                                # Added date
                                ui.label(f'Added on {item["added_date"]}').classes('text-xs text-gray-500 mb-4')
                                
                                # Actions
                                with ui.row().classes('gap-2'):
                                    if item['in_stock']:
                                        ui.button('Add to Cart', icon='shopping_cart').classes('flex-1 bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium')
                                    else:
                                        ui.button('Notify When Available', icon='notifications').classes('flex-1 bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg font-medium')
                                    
                                    ui.button('View Details', icon='visibility').classes('bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium')
            
            # Price Drop Notifications
            with ui.card().classes('mt-8 p-6 bg-white shadow-sm'):
                ui.label('Price Drop Alerts').classes('text-xl font-bold text-gray-800 mb-4')
                ui.label('Get notified when items in your wishlist go on sale').classes('text-gray-600 mb-4')
                
                with ui.row().classes('items-center gap-4'):
                    ui.switch('Enable price drop notifications').classes('text-gray-700')
                    ui.button('Manage Alerts', icon='notifications').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg')

def remove_from_wishlist(item_id):
    """Remove item from wishlist"""
    ui.notify(f'Item removed from wishlist', type='info')
    # In a real implementation, this would make an API call to remove the item
