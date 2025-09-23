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
        with ui.element('div').classes('w-full bg-gradient-to-r from-blue-300 via-blue-500 to-blue-700 text-white py-6 sm:py-8 mb-6 overflow-hidden'):
            with ui.element('div').classes('container mx-auto px-4 text-center max-w-full'):
                with ui.element('div').classes('flex items-center justify-center gap-2 sm:gap-3 mb-3 sm:mb-4 flex-wrap'):
                    ui.label('INNO').classes('text-2xl sm:text-4xl font-bold text-white')
                    ui.icon('star').classes('text-orange-300 text-xl sm:text-3xl')
                    ui.label('HUB').classes('text-2xl sm:text-4xl font-bold text-white')
                ui.label('Ghana').classes('text-sm sm:text-lg text-orange-100 mb-2')
                ui.label('Buy and Sell all your products from the comfort of your home').classes('text-sm sm:text-xl font-semibold text-white mb-3 sm:mb-4 break-words px-2')
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
                
                # Center - Main Promotional Banner Slideshow
                with ui.element('div').classes('lg:col-span-2'):
                    # Slideshow container
                    slideshow_container = ui.element('div').classes('relative h-96 w-full rounded-lg overflow-hidden shadow-lg')
                    
                    # Define slides data
                    slides_data = [
                        {
                            'title': 'HOME MAKEOVER',
                            'subtitle': 'UP TO 45% OFF',
                            'disclaimer': 'T & C\'s Apply',
                            'bg_color': 'from-teal-600 to-teal-700',
                            'accent_color': 'teal',
                            'products': [
                                {'icon': 'checkroom', 'label': 'Clothes'},
                                {'icon': 'sports', 'label': 'Shoes'}
                            ],
                            'people': [
                                {'icon': 'person', 'label': 'Woman'},
                                {'icon': 'person', 'label': 'Man'}
                            ],
                            'cta': 'SHOP NOW'
                        },
                        {
                            'title': 'ELECTRONICS SALE',
                            'subtitle': 'UP TO 60% OFF',
                            'disclaimer': 'Limited Time Offer',
                            'bg_color': 'from-blue-600 to-blue-700',
                            'accent_color': 'blue',
                            'products': [
                                {'icon': 'phone_android', 'label': 'Phones'},
                                {'icon': 'computer', 'label': 'Laptops'}
                            ],
                            'people': [
                                {'icon': 'headset', 'label': 'Gaming'},
                                {'icon': 'tv', 'label': 'TVs'}
                            ],
                            'cta': 'SHOP ELECTRONICS'
                        },
                        {
                            'title': 'FASHION WEEK',
                            'subtitle': 'UP TO 50% OFF',
                            'disclaimer': 'New Arrivals',
                            'bg_color': 'from-pink-600 to-pink-700',
                            'accent_color': 'pink',
                            'products': [
                                {'icon': 'checkroom', 'label': 'Dresses'},
                                {'icon': 'watch', 'label': 'Accessories'}
                            ],
                            'people': [
                                {'icon': 'star', 'label': 'Trending'},
                                {'icon': 'favorite', 'label': 'Favorites'}
                            ],
                            'cta': 'SHOP FASHION'
                        },
                        {
                            'title': 'VEHICLE DEALS',
                            'subtitle': 'UP TO 30% OFF',
                            'disclaimer': 'Best Prices',
                            'bg_color': 'from-gray-600 to-gray-700',
                            'accent_color': 'gray',
                            'products': [
                                {'icon': 'directions_car', 'label': 'Cars'},
                                {'icon': 'motorcycle', 'label': 'Bikes'}
                            ],
                            'people': [
                                {'icon': 'local_gas_station', 'label': 'Fuel'},
                                {'icon': 'build', 'label': 'Parts'}
                            ],
                            'cta': 'BROWSE VEHICLES'
                        },
                        {
                            'title': 'REAL ESTATE',
                            'subtitle': 'PRIME LOCATIONS',
                            'disclaimer': 'Limited Offers',
                            'bg_color': 'from-green-600 to-green-700',
                            'accent_color': 'green',
                            'products': [
                                {'icon': 'home_work', 'label': 'Houses'},
                                {'icon': 'apartment', 'label': 'Apartments'}
                            ],
                            'people': [
                                {'icon': 'location_on', 'label': 'Location'},
                                {'icon': 'trending_up', 'label': 'Investment'}
                            ],
                            'cta': 'VIEW PROPERTIES'
                        }
                    ]
                    
                    # Current slide index
                    current_slide = {'index': 0}
                    
                    @ui.refreshable
                    def render_slide():
                        slide = slides_data[current_slide['index']]
                        
                        with slideshow_container:
                            slideshow_container.clear()
                            with slideshow_container:
                                with ui.element('div').classes(f'bg-gradient-to-r {slide["bg_color"]} text-white rounded-lg overflow-hidden relative h-96 w-full shadow-lg transition-all duration-500'):
                                    # Background decorative elements
                                    with ui.element('div').classes(f'absolute top-4 right-4 w-16 h-16 bg-{slide["accent_color"]}-500 rounded-full opacity-20'):
                                        pass
                                    with ui.element('div').classes(f'absolute top-8 right-12 w-8 h-8 bg-{slide["accent_color"]}-400 rounded-full opacity-30'):
                                        pass
                                    
                                    # Main content
                                    with ui.element('div').classes('relative z-10 h-full flex items-center justify-between p-8'):
                                        # Left side - Text and products
                                        with ui.element('div').classes('flex-1 z-10'):
                                            ui.label(slide['title']).classes('text-4xl lg:text-5xl font-bold mb-2')
                                            ui.label(slide['subtitle']).classes('text-2xl lg:text-3xl font-bold mb-4')
                                            ui.label(slide['disclaimer']).classes('text-sm opacity-75 mb-6')
                                            
                                            # Product showcase
                                            with ui.element('div').classes('flex items-end gap-4 mb-4'):
                                                for i, product in enumerate(slide['products']):
                                                    size_class = 'w-20 h-24' if i == 0 else 'w-16 h-16'
                                                    with ui.element('div').classes(f'{size_class} bg-white/20 rounded-lg flex flex-col items-center justify-end p-2'):
                                                        ui.icon(product['icon']).classes('text-white text-2xl mb-1')
                                                        ui.label(product['label']).classes('text-white text-xs')
                                            
                                            # Shop Now button
                                            def shop_now_action():
                                                if slide['title'] == 'HOME MAKEOVER':
                                                    ui.navigate.to('/?cat=Fashion')
                                                elif slide['title'] == 'ELECTRONICS SALE':
                                                    ui.navigate.to('/?cat=Electronics')
                                                elif slide['title'] == 'FASHION WEEK':
                                                    ui.navigate.to('/?cat=Fashion')
                                                elif slide['title'] == 'VEHICLE DEALS':
                                                    ui.navigate.to('/?cat=Vehicles')
                                                elif slide['title'] == 'REAL ESTATE':
                                                    ui.navigate.to('/?cat=Real Estate')
                                                else:
                                                    ui.navigate.to('/')
                                            
                                            ui.button(slide['cta'], on_click=shop_now_action).classes('bg-black hover:bg-gray-800 text-white px-6 py-3 rounded font-semibold text-lg')
                                        
                                        # Right side - People/Features
                                        with ui.element('div').classes('flex-1 flex justify-end items-center relative hidden lg:flex'):
                                            # Features illustration
                                            with ui.element('div').classes('flex items-end gap-4'):
                                                for i, person in enumerate(slide['people']):
                                                    size_class = 'w-16 h-20' if i == 0 else 'w-16 h-24'
                                                    with ui.element('div').classes(f'{size_class} bg-white/20 rounded-lg flex flex-col items-center justify-end p-2'):
                                                        ui.icon(person['icon']).classes('text-white text-2xl mb-1')
                                                        ui.label(person['label']).classes('text-white text-xs')
                                            
                                            # Decorative element
                                            with ui.element('div').classes(f'absolute -bottom-2 -right-2 w-8 h-8 bg-{slide["accent_color"]}-500 rounded-full flex items-center justify-center'):
                                                ui.icon('eco').classes('text-white text-sm')
                    
                    # Navigation functions
                    def next_slide():
                        current_slide['index'] = (current_slide['index'] + 1) % len(slides_data)
                        render_slide()
                    
                    def prev_slide():
                        current_slide['index'] = (current_slide['index'] - 1) % len(slides_data)
                        render_slide()
                    
                    def go_to_slide(index):
                        current_slide['index'] = index
                        render_slide()
                    
                    # Render initial slide
                    render_slide()
                    
                    # Navigation arrows
                    with ui.element('div').classes('absolute left-4 top-1/2 transform -translate-y-1/2 z-30'):
                        ui.button(icon='chevron_left', on_click=prev_slide).classes('w-10 h-10 bg-white/20 hover:bg-white/30 text-white rounded-full flex items-center justify-center transition-all')
                    
                    with ui.element('div').classes('absolute right-4 top-1/2 transform -translate-y-1/2 z-30'):
                        ui.button(icon='chevron_right', on_click=next_slide).classes('w-10 h-10 bg-white/20 hover:bg-white/30 text-white rounded-full flex items-center justify-center transition-all')
                    
                    # Carousel dots
                    with ui.element('div').classes('absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2 z-20'):
                        for i in range(len(slides_data)):
                            is_active = i == current_slide['index']
                            ui.button('', on_click=lambda idx=i: go_to_slide(idx)).classes(f'w-3 h-3 rounded-full {"bg-orange-500" if is_active else "bg-white opacity-50"} hover:bg-white transition-all')
                    
                    # Auto-advance slideshow
                    def auto_advance():
                        next_slide()
                    
                    ui.timer(5.0, auto_advance)  # Auto-advance every 5 seconds
                
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
                        
                        # Refresh Button
                        def refresh_products():
                            products_grid.refresh()
                            ui.notify('Products refreshed!', type='positive')
                        
                        ui.button('Refresh', on_click=refresh_products, icon='refresh').classes('bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 text-sm rounded-lg')

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
                            
                            # Log successful data loading
                            if items:
                                print(f"✓ Loaded {len(items)} adverts from backend")
                                # Show first few titles for verification
                                titles = [item.get('title', 'N/A') for item in items[:3]]
                                print(f"  Recent adverts: {', '.join(titles)}")
                            else:
                                print("⚠ No adverts found in backend")
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
                                        # Get image data from the advert
                                        image_data = ad.get('image', '')
                                        
                                        # Check if we have valid image data
                                        has_image = False
                                        image_url = None
                                        
                                        if image_data and isinstance(image_data, str):
                                            if image_data.startswith('http'):
                                                # Direct URL (like Cloudinary)
                                                image_url = image_data
                                                has_image = True
                                            elif image_data.startswith('data:'):
                                                # Base64 data URL
                                                image_url = image_data
                                                has_image = True
                                            elif len(image_data) > 100 and not image_data.startswith('http'):
                                                # Assume it's base64 data without prefix
                                                image_url = f'data:image/jpeg;base64,{image_data}'
                                                has_image = True
                                        
                                        if has_image and image_url:
                                            # Display the actual image
                                            try:
                                                ui.image(image_url).classes('w-full h-full object-cover group-hover:scale-110 transition-transform duration-500')
                                            except Exception as e:
                                                print(f"Image display error: {e}")
                                                # Fallback to placeholder if image fails
                                                has_image = False
                                        
                                        if not has_image:
                                            # Show category-based placeholder image
                                            category = ad.get('category', '').lower()
                                            sample_images = {
                                                'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
                                                'fashion': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=300&fit=crop',
                                                'home': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop',
                                                'vehicles': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400&h=300&fit=crop',
                                                'real estate': 'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&h=300&fit=crop',
                                                'services': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300&fit=crop',
                                                'furniture': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop',
                                                'appliances': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400&h=300&fit=crop'
                                            }
                                            
                                            # Find matching category or use default
                                            sample_url = None
                                            for cat_key, url in sample_images.items():
                                                if cat_key in category:
                                                    sample_url = url
                                                    break
                                            
                                            if sample_url:
                                                ui.image(sample_url).classes('w-full h-full object-cover group-hover:scale-110 transition-transform duration-500')
                                            else:
                                                # Default placeholder
                                                with ui.element('div').classes('w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center'):
                                                    ui.icon('image').classes('text-6xl text-gray-400 mb-2')
                                                    ui.label('No Image').classes('text-sm text-gray-500')
                                                    ui.label(f'Category: {category}').classes('text-xs text-gray-400 mt-1')
                                        
                                        # Product Badge (New, Sale, etc.)
                                        with ui.element('div').classes('absolute top-3 left-3'):
                                            ui.label('NEW').classes('bg-green-500 text-white text-xs px-2 py-1 rounded-full font-semibold')
                                        
                                        # Wishlist button
                                        ui.button(icon='favorite_border').classes('absolute top-3 right-3 bg-white/90 backdrop-blur-sm rounded-full p-2 shadow-lg hover:bg-white hover:scale-110 transition-all duration-200').props('flat round')
                                        
                                        # Quick view overlay
                                        with ui.element('div').classes('absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100'):
                                            def on_quick_view(e, advert=ad):
                                                ui.navigate.to(f"/view_event?title={quote(str(advert['title']))}&id={advert.get('id', '')}")
                                            ui.button('Quick View', on_click=on_quick_view, icon='visibility').classes('bg-white text-gray-800 px-4 py-2 rounded-lg font-medium shadow-lg hover:bg-gray-100')
                                    
                                    # Product Details
                                    with ui.element('div').classes('p-4 space-y-3'):
                                        # Product Title
                                        ui.label(ad['title']).classes('font-semibold text-gray-800 text-sm line-clamp-2 hover:text-orange-500 cursor-pointer leading-tight').on('click', lambda advert=ad: ui.navigate.to(f"/view_event?title={quote(str(advert['title']))}&id={advert.get('id', '')}"))
                                        
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
                                                on_click=lambda e, advert=ad: ui.navigate.to(f"/view_event?title={quote(str(advert['title']))}&id={advert.get('id', '')}"), 
                                                icon='visibility'
                                            ).classes('btn-primary w-full py-2.5 text-sm font-semibold transition-all duration-200')

                                            # Secondary actions
                                            with ui.row().classes('gap-2'):
                                                # Add to Cart Button
                                                def add_to_cart_action(title):
                                                    ui.notify(f'Added {title} to cart', type='positive')
                                                    ui.navigate.to('/cart')
                                                
                                                ui.button('Add to Cart', 
                                                    on_click=lambda e, t=ad['title']: add_to_cart_action(t), 
                                                    icon='shopping_cart'
                                                ).classes('btn-secondary flex-1 py-2 text-sm font-medium')
                                                
                                                # Edit Button
                                                ui.button('Edit', 
                                                    on_click=lambda e, advert=ad: ui.navigate.to(f"/edit_event?title={quote(str(advert['title']))}&id={advert.get('id', '')}"), 
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
