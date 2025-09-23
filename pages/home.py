from nicegui import ui
import asyncio
import requests
import json
import time
from urllib.parse import quote
from utils.api import base_url


def show_home_page():
    # Data is fetched inside the grid renderer to ensure freshness
    deleted_titles = set()

    q_params = ui.context.client.request.query_params
    q = (q_params.get('q') or '').lower()
    cat = q_params.get('cat') or ''

    # Jumia-style homepage layout
    with ui.element("div").classes("min-h-screen bg-white overflow-x-hidden w-full max-w-full pb-20 md:pb-0"):
        
        # Welcome Banner at the top
        with ui.element('div').classes('w-full bg-gradient-to-r from-orange-500 via-orange-600 to-orange-700 text-white py-6 sm:py-8 mb-6 overflow-hidden'):
            with ui.element('div').classes('container mx-auto px-4 text-center max-w-full'):
                with ui.element('div').classes('flex items-center justify-center gap-2 sm:gap-3 mb-3 sm:mb-4 flex-wrap'):
                    ui.label('INNO').classes('text-2xl sm:text-4xl font-bold text-white')
                    ui.icon('star').classes('text-yellow-300 text-xl sm:text-3xl')
                    ui.label('HUB').classes('text-2xl sm:text-4xl font-bold text-white')
                ui.label('Ghana').classes('text-sm sm:text-lg text-orange-100 mb-2')
                ui.label('🛒 Buy and Sell all your products from the comfort of your home').classes('text-sm sm:text-xl font-semibold text-white mb-3 sm:mb-4 break-words px-2')
                ui.label('Welcome to InnoHub - Your Ultimate Marketplace!').classes('text-sm sm:text-lg text-orange-100 break-words px-2')
        # Main Content Area - Jumia Style Hero Section
        with ui.element('div').classes('container mx-auto px-4 py-8 max-w-8xl mb-8'):
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-4 gap-6 w-full'):
                
                # Left Sidebar - Categories
                with ui.element('div').classes('lg:col-span-1'):
                    with ui.card().classes('bg-gray-100 p-4 shadow-sm h-fit max-h-96 overflow-y-auto'):
                        ui.label('Categories').classes('text-lg font-semibold text-gray-800 mb-4')
                        categories = [
                            {'name': 'Supermarket', 'icon': 'local_grocery_store'},
                            {'name': 'Phones & Tablets', 'icon': 'phone_android'},
                            {'name': 'Health & Beauty', 'icon': 'face'},
                            {'name': 'Home & Office', 'icon': 'home'},
                            {'name': 'Appliances', 'icon': 'kitchen'},
                            {'name': 'Electronics', 'icon': 'tv'},
                            {'name': 'Computing', 'icon': 'computer'},
                            {'name': 'Fashion', 'icon': 'checkroom'},
                            {'name': 'Sporting Goods', 'icon': 'sports_soccer'},
                            {'name': 'Baby Products', 'icon': 'child_care'},
                            {'name': 'Gaming', 'icon': 'sports_esports'},
                            {'name': 'Other', 'icon': 'more_horiz'}
                        ]
                        for category in categories:
                            with ui.element('div').classes('flex items-center gap-3 py-2 px-2 hover:bg-gray-200 rounded cursor-pointer').on('click', lambda c=category['name']: ui.navigate.to(f'/?cat={c}')):
                                ui.icon(category['icon']).classes('text-gray-600 text-lg')
                                ui.label(category['name']).classes('text-gray-700 font-medium')
                
                # Center - Main Promotional Banner
                with ui.element('div').classes('lg:col-span-2'):
                    with ui.element('div').classes('bg-gradient-to-r from-teal-600 to-teal-700 text-white rounded-lg overflow-hidden relative h-96 w-full shadow-lg'):
                        # Background decorative elements
                        with ui.element('div').classes('absolute top-4 right-4 w-16 h-16 bg-teal-500 rounded-full opacity-20'):
                            pass
                        with ui.element('div').classes('absolute top-8 right-12 w-8 h-8 bg-teal-400 rounded-full opacity-30'):
                            pass
                        
                        # Main content
                        with ui.element('div').classes('relative z-10 h-full flex items-center justify-between p-8'):
                            # Left side - Text and products
                            with ui.element('div').classes('flex-1 z-10'):
                                ui.label('HOME MAKEOVER').classes('text-4xl lg:text-5xl font-bold mb-2')
                                ui.label('UP TO 45% OFF').classes('text-2xl lg:text-3xl font-bold mb-4')
                                ui.label('T & C\'s Apply').classes('text-sm opacity-75 mb-6')
                                
                                # Product showcase (clothing rack and shoes)
                                with ui.element('div').classes('flex items-end gap-4 mb-4'):
                                    # Clothing rack
                                    with ui.element('div').classes('w-20 h-24 bg-white/20 rounded-lg flex flex-col items-center justify-end p-2'):
                                        ui.icon('checkroom').classes('text-white text-2xl mb-1')
                                        ui.label('Clothes').classes('text-white text-xs')
                                    
                                    # Shoes
                                    with ui.element('div').classes('w-16 h-16 bg-white/20 rounded-lg flex items-center justify-center'):
                                        ui.icon('sports').classes('text-white text-xl')
                                
                                # Shop Now button
                                ui.button('SHOP NOW').classes('bg-black hover:bg-gray-800 text-white px-6 py-3 rounded font-semibold text-lg')
                            
                            # Right side - People
                            with ui.element('div').classes('flex-1 flex justify-end items-center relative hidden lg:flex'):
                                # People illustration
                                with ui.element('div').classes('flex items-end gap-4'):
                                    # Woman
                                    with ui.element('div').classes('w-16 h-20 bg-white/20 rounded-lg flex flex-col items-center justify-end p-2'):
                                        ui.icon('person').classes('text-white text-2xl mb-1')
                                        ui.label('Woman').classes('text-white text-xs')
                                    
                                    # Man
                                    with ui.element('div').classes('w-16 h-24 bg-white/20 rounded-lg flex flex-col items-center justify-end p-2'):
                                        ui.icon('person').classes('text-white text-2xl mb-1')
                                        ui.label('Man').classes('text-white text-xs')
                                
                                # Plant
                                with ui.element('div').classes('absolute -bottom-2 -right-2 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center'):
                                    ui.icon('eco').classes('text-white text-sm')
                        
                        # Carousel dots
                        with ui.element('div').classes('absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2 z-20'):
                            for i in range(3):
                                ui.element('div').classes(f'w-2 h-2 rounded-full {"bg-orange-500" if i == 0 else "bg-white opacity-50"} cursor-pointer hover:bg-white')
                
                # Right Sidebar - Services and Secondary Banner
                with ui.element('div').classes('lg:col-span-1 h-96'):
                    with ui.element('div').classes('h-full flex flex-col gap-4'):
                        # Service Cards - All same height
                        services = [
                            {'title': 'INNO HUB DELIVERY', 'subtitle': 'Send parcels easily', 'icon': 'local_shipping', 'color': 'bg-orange-500', 'route': '/delivery'},
                            {'title': 'SELL ON INNO HUB', 'subtitle': 'Make more money', 'icon': 'store', 'color': 'bg-orange-500', 'route': '/sell'},
                            {'title': 'TRACK YOUR ORDER', 'subtitle': 'Stay up to date', 'icon': 'track_changes', 'color': 'bg-orange-500', 'route': '/track'}
                        ]
                        for service in services:
                            with ui.card().classes('p-4 bg-white shadow-sm flex-1 flex items-center min-h-0 cursor-pointer hover:shadow-md transition-all').on('click', lambda s=service: ui.navigate.to(s['route'])):
                                with ui.row().classes('items-center gap-3 w-full h-full'):
                                    ui.icon(service['icon']).classes(f'text-white text-lg {service["color"]} rounded-full p-2 flex-shrink-0')
                                    with ui.element('div').classes('flex-1 flex flex-col justify-center'):
                                        ui.label(service['title']).classes('text-sm font-semibold text-gray-800 leading-tight')
                                        ui.label(service['subtitle']).classes('text-xs text-gray-600 leading-tight')
                        
                        # Secondary Banner - Fixed height to fill remaining space
                        with ui.card().classes('p-4 bg-teal-600 text-white shadow-sm flex-1 flex items-center justify-center min-h-0'):
                            with ui.element('div').classes('text-center'):
                                ui.icon('home').classes('text-white text-2xl mb-2')
                                ui.label('HOME MAKEOVER').classes('text-sm font-bold mb-1')
                                ui.label('UP TO 45% OFF').classes('text-xs opacity-90')

        # Browse By Category Section
        with ui.element('div').classes('container mx-auto px-4 py-8 max-w-8xl mb-8'):
            with ui.card().classes('p-6 bg-white shadow-sm w-full overflow-hidden'):
                # Define categories list outside functions for shared access
                categories = [
                    {'name': 'Electronics', 'icon': 'phone_android', 'selected': False},
                    {'name': 'Fashion', 'icon': 'checkroom', 'selected': False},
                    {'name': 'Home & Garden', 'icon': 'home', 'selected': False},
                    {'name': 'Vehicles', 'icon': 'directions_car', 'selected': True},
                    {'name': 'Real Estate', 'icon': 'home_work', 'selected': False},
                    {'name': 'Services', 'icon': 'handyman', 'selected': False}
                ]
                
                # Category Header
                with ui.row().classes('items-center justify-between mb-6'):
                    with ui.row().classes('items-center gap-3'):
                        ui.element('div').classes('w-1 h-8 bg-primary rounded')
                        ui.label('Categories').classes('text-primary font-semibold text-sm')
                    ui.label('Browse By Category').classes('text-2xl font-bold text-primary')
                    
                    # Arrow buttons with functionality
                    with ui.row().classes('gap-2'):
                        def prev_category():
                            # Find current selected category and select the previous one
                            current_index = next((i for i, cat in enumerate(categories) if cat['selected']), 0)
                            categories[current_index]['selected'] = False
                            prev_index = (current_index - 1) % len(categories)
                            categories[prev_index]['selected'] = True
                            category_grid.refresh()
                        
                        def next_category():
                            # Find current selected category and select the next one
                            current_index = next((i for i, cat in enumerate(categories) if cat['selected']), 0)
                            categories[current_index]['selected'] = False
                            next_index = (current_index + 1) % len(categories)
                            categories[next_index]['selected'] = True
                            category_grid.refresh()
                        
                        ui.button(icon='chevron_left', on_click=prev_category).classes('w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full').props('flat round')
                        ui.button(icon='chevron_right', on_click=next_category).classes('w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full').props('flat round')
                
                # Category Cards Grid
                @ui.refreshable
                def category_grid():
                    with ui.element('div').classes('grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-6 w-full overflow-hidden'):
                        for category in categories:
                            if category['selected']:
                                # Selected category with primary background
                                with ui.card().classes('card-primary p-4 text-center cursor-pointer transition-all').on('click', lambda c=category['name']: ui.navigate.to(f'/?cat={c}')):
                                    ui.icon(category['icon']).classes('text-4xl mb-2')
                                    ui.label(category['name']).classes('text-sm font-medium')
                            else:
                                # Regular category with surface background
                                with ui.card().classes('card p-4 text-center cursor-pointer hover:border-primary hover:shadow-primary transition-all').on('click', lambda c=category['name']: ui.navigate.to(f'/?cat={c}')):
                                    ui.icon(category['icon']).classes('text-4xl mb-2 text-secondary')
                                    ui.label(category['name']).classes('text-sm font-medium text-secondary')
                
                # Render the category grid
                category_grid()

        # Search and Filter Section
        with ui.element('div').classes('container mx-auto px-4 py-4 max-w-8xl'):
            with ui.card().classes('p-6 bg-gray-50 shadow-sm w-full overflow-hidden'):
                with ui.row().classes('items-end justify-between gap-4 mb-6'):
                    ui.label('All Adverts').classes('text-2xl font-bold text-gray-800')
                    with ui.row().classes('gap-3 flex-wrap items-center'):
                        q_input = ui.input('Search adverts...').classes('w-48 sm:w-64').props('outlined')

                        def apply_filters():
                            qv = q_input.value or ''
                            ui.navigate.to(f'/?q={qv}')

                        def post_advert():
                            ui.navigate.to('/add_event')

                        q_input.on('blur', apply_filters)
                        
                        # Post Advert Button
                        ui.button('Post Advert', on_click=post_advert, icon='add').classes('btn-primary px-4 py-2 text-sm shadow-primary hover:shadow-lg transition-all duration-200')

            # Products Grid Section
            @ui.refreshable
            def products_grid():
                with ui.element('div').classes('mt-8 bg-white p-6 rounded-lg').props('id=products'):

                    async def render():
                        try:
                            # Bypass any intermediate caching using a timestamp param
                            resp = await asyncio.to_thread(requests.get, f"{base_url}/adverts", params={"_ts": time.time()})
                            js = resp.json()
                            items = js.get("data", [])
                            
                            # Debug: Log first item to see image data structure
                            if items:
                                first_item = items[0]
                                print(f"Debug - First item keys: {list(first_item.keys())}")
                                print(f"Debug - Image field: {first_item.get('image', 'NO_IMAGE_FIELD')}")
                        except Exception as e:
                            ui.notify(f"Failed to load products: {e}")
                            items = []

                        # Optimistically exclude items deleted this session
                        if deleted_titles:
                            items = [ad for ad in items if ad.get('title') not in deleted_titles]

                        def matches(ad):
                            ok_q = (q in ad['title'].lower()) if q else True
                            ok_cat = (ad['category'] == cat) if cat else True
                            return ok_q and ok_cat

                        items = [ad for ad in items if matches(ad)]

                        if not items:
                            with ui.element('div').classes('text-center py-16'):
                                ui.icon('shopping_bag').classes('text-6xl text-gray-300 mb-4')
                                ui.label('No products found').classes('text-2xl font-semibold text-gray-600 mb-2')
                                ui.label('Try adjusting your search or browse all categories').classes('text-gray-500 mb-6')
                                ui.link('Browse All Products', '/').classes('btn-primary px-6 py-3 font-semibold no-underline')
                            return

                        # Enhanced Jumia-style product grid - 3 cards per row
                        with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full overflow-hidden'):
                            for ad in items:
                                with ui.card().classes('card hover:shadow-xl transition-all duration-300 overflow-hidden group w-full h-full fade-in'):
                                    # Product Image Container
                                    with ui.element('div').classes('relative overflow-hidden bg-gray-50 h-80'):
                                        image_url = ad.get('image', '').strip() if ad.get('image') else ''
                                        
                                        if image_url and (image_url.startswith('http') or image_url.startswith('data:') or image_url.startswith('/')):
                                            # Display image from backend database with error handling
                                            try:
                                                ui.image(image_url).classes('w-full h-full object-cover group-hover:scale-110 transition-transform duration-500').on('error', lambda: ui.notify('Image failed to load', type='warning'))
                                            except Exception as e:
                                                # Fallback if image fails to load
                                                with ui.element('div').classes('w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center'):
                                                    ui.icon('image').classes('text-6xl text-gray-400 mb-2')
                                                    ui.label('Image Error').classes('text-sm text-gray-500')
                                        else:
                                            # Fallback for missing or invalid images - show sample image based on category
                                            category = ad.get('category', '').lower()
                                            sample_images = {
                                                'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
                                                'fashion': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop',
                                                'home': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop',
                                                'vehicles': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop',
                                                'real estate': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop',
                                                'services': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop'
                                            }
                                            
                                            # Try to find a matching category or use default
                                            sample_url = None
                                            for cat_key, url in sample_images.items():
                                                if cat_key in category:
                                                    sample_url = url
                                                    break
                                            
                                            if sample_url:
                                                # Show sample image
                                                ui.image(sample_url).classes('w-full h-full object-cover group-hover:scale-110 transition-transform duration-500')
                                            else:
                                                # Show placeholder
                                                with ui.element('div').classes('w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center'):
                                                    ui.icon('image').classes('text-6xl text-gray-400 mb-2')
                                                    ui.label('No Image').classes('text-sm text-gray-500')
                                                    if image_url:
                                                        ui.label(f'URL: {image_url[:30]}...').classes('text-xs text-gray-400 mt-1')
                                        
                                        # Product Badge (New, Sale, etc.)
                                        with ui.element('div').classes('absolute top-3 left-3'):
                                            ui.label('NEW').classes('bg-green-500 text-white text-xs px-2 py-1 rounded-full font-semibold')
                                        
                                        # Wishlist button
                                        ui.button(icon='favorite_border').classes('absolute top-3 right-3 bg-white/90 backdrop-blur-sm rounded-full p-2 shadow-lg hover:bg-white hover:scale-110 transition-all duration-200').props('flat round')
                                        
                                        # Quick view overlay
                                        with ui.element('div').classes('absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100'):
                                            def on_quick_view(e, title=ad['title']):
                                                ui.navigate.to(f"/view_event?title={quote(str(title))}")
                                            ui.button('Quick View', on_click=on_quick_view, icon='visibility').classes('bg-white text-gray-800 px-4 py-2 rounded-lg font-medium shadow-lg hover:bg-gray-100')
                                    
                                    # Product Details
                                    with ui.element('div').classes('p-4 space-y-3'):
                                        # Product Title
                                        ui.label(ad['title']).classes('font-semibold text-gray-800 text-sm line-clamp-2 hover:text-orange-500 cursor-pointer leading-tight').on('click', lambda t=ad['title']: ui.navigate.to(f"/view_event?title={quote(str(t))}"))
                                        
                                        # Price Section
                                        with ui.element('div').classes('space-y-1'):
                                            with ui.row().classes('items-baseline gap-2'):
                                                ui.label(f"GHS {ad['price']:,.2f}").classes('text-xl font-bold text-primary')
                                                # Original price (if on sale)
                                                ui.label(f"GHS {(ad['price'] * 1.2):,.2f}").classes('text-sm text-gray-400 line-through')
                                            
                                            # Shipping info
                                            with ui.row().classes('items-center gap-2'):
                                                ui.icon('local_shipping').classes('text-green-500 text-sm')
                                                ui.label('Free shipping').classes('text-xs text-green-600 font-medium')
                                        
                                        # Category and Rating
                                        with ui.row().classes('items-center justify-between'):
                                            ui.label(ad['category']).classes('text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full')
                                            with ui.row().classes('items-center gap-1'):
                                                for i in range(5):
                                                    ui.icon('star').classes('text-yellow-400 text-xs')
                                                ui.label('4.5 (128)').classes('text-xs text-gray-600')
                                        
                                        # Action Buttons
                                        with ui.element('div').classes('space-y-2 mt-4'):
                                            # View Details Button
                                            ui.button('View Details', 
                                                on_click=lambda e, t=ad['title']: ui.navigate.to(f"/view_event?title={quote(str(t))}"), 
                                                icon='visibility'
                                            ).classes('btn-primary w-full py-2.5 text-sm font-semibold transition-all duration-200')

                                            # Secondary actions
                                            with ui.row().classes('gap-2'):
                                                # Add to Cart Button
                                                ui.button('Add to Cart', 
                                                    on_click=lambda e, t=ad['title']: (ui.notify(f'Added {t} to cart', type='positive'), ui.navigate.to('/cart')), 
                                                    icon='shopping_cart'
                                                ).classes('btn-secondary flex-1 py-2 text-sm font-medium')
                                                
                                                # Edit Button
                                                ui.button('Edit', 
                                                    on_click=lambda e, t=ad['title']: ui.navigate.to(f"/edit_event?title={quote(str(t))}"), 
                                                    icon='edit'
                                                ).classes('btn-outline flex-1 py-2 text-sm font-medium')
                                                
                                                # Wishlist Button
                                                ui.button('', 
                                                    on_click=lambda e, t=ad['title']: ui.notify(f'Added {t} to wishlist', type='positive'), 
                                                    icon='favorite_border'
                                                ).classes('bg-error text-white hover:bg-error p-2 rounded-lg')

                    ui.timer(0.05, render, once=True)

                async def delete_ad(title: str) -> bool:
                    try:
                        safe_title = (title or "").strip()
                        encoded = quote(str(safe_title))
                        # Run blocking HTTP call off the event loop
                        r = await asyncio.to_thread(requests.delete, f"{base_url}/adverts/{encoded}")
                        if r.status_code >= 400:
                            ui.notify(f"Delete failed: {r.status_code}: {r.text}")
                            return False
                        else:
                            # API returns a plain JSON string like "Advert successfully deleted!"
                            try:
                                body = r.json()
                                msg = body if isinstance(body, str) else 'Deleted'
                            except Exception:
                                # Fallback to raw text
                                msg = (r.text or 'Deleted').strip().strip('"')
                            ui.notify(msg or 'Deleted')
                            # Optimistically remove from current view
                            deleted_titles.add(safe_title)
                            products_grid.refresh()
                            return True
                    except Exception as e:
                        ui.notify(f"Error: {e}")
                        return False

            products_grid()

        # Add spacing before bottom navigation
        with ui.element('div').classes('h-8'):
            pass

        # Bottom Navigation Bar (Mobile-style)
        with ui.element('div').classes('fixed bottom-0 left-0 right-0 bg-green-500 px-4 py-3 z-50 md:hidden'):
            with ui.row().classes('items-center justify-between w-full'):
                # Bookmark Icon
                ui.button(icon='bookmark_border').classes('w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg').props('flat round')
                
                # Chat Icon
                ui.button(icon='chat_bubble_outline').classes('w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg').props('flat round')
                
                # Notification Bell Icon
                ui.button(icon='notifications_none').classes('w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg').props('flat round')
                
                # Document/Page Icon
                ui.button(icon='description').classes('w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg').props('flat round')
                
                # User Profile Icon
                ui.button(icon='account_circle').classes('w-12 h-12 bg-green-100 border-2 border-green-300 rounded-full flex items-center justify-center shadow-lg').props('flat round')
                
                # SELL Button
                ui.button('SELL', on_click=lambda: ui.navigate.to('/add_event')).classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-bold text-sm shadow-lg')
