from nicegui import ui
import asyncio
import json
from urllib.parse import quote
from utils.api_client import api_client


def show_home_page(auth_state=None):
    # Data is fetched inside the grid renderer to ensure freshness
    deleted_titles = set()

    q_params = ui.context.client.request.query_params
    q = (q_params.get('q') or '').lower()
    cat = q_params.get('cat') or ''
    scroll_to = q_params.get('scroll') or ''
    instant_scroll = q_params.get('instant') == 'true'

    ui.run_javascript("""
        if (!window.__advertsChangedBridge) {
            window.__advertsChangedBridge = true;
            window.addEventListener('adverts:changed', (event) => {
                const detail = event.detail || {};
                if (window.nicegui && window.nicegui.emit) {
                    window.nicegui.emit('adverts_changed', detail);
                }
            });
        }
    """)

    def handle_adverts_changed(event):
        detail = getattr(event, 'args', {}) or {}
        if detail.get('type') in {'created', 'updated', 'deleted', None}:
            ui.navigate.reload()

    ui.on('adverts_changed', handle_adverts_changed)

    # Jumia-style homepage layout
    with ui.element("div").classes("min-h-screen bg-white overflow-x-hidden w-full max-w-full pb-20 md:pb-0"):
        
        # Hero Slideshow Section
        with ui.element('div').classes('w-full h-96 mb-6 overflow-hidden relative'):
            # Slideshow images with Product Categories and Items
            slideshow_images = [
                {
                    'url': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1200&h=600&fit=crop&crop=center',
                    'title': 'Electronics & Gadgets',
                    'subtitle': 'Smartphones, laptops, tablets, and tech accessories'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=1200&h=600&fit=crop&crop=center',
                    'title': 'Fashion & Clothing',
                    'subtitle': 'Men\'s and women\'s clothing, shoes, and accessories'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=1200&h=600&fit=crop&crop=center',
                    'title': 'Home & Furniture',
                    'subtitle': 'Furniture, home decor, kitchen items, and appliances'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&h=600&fit=crop&crop=center',
                    'title': 'Health & Beauty',
                    'subtitle': 'Skincare, cosmetics, health products, and wellness items'
                },
                {
                    'url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=1200&h=600&fit=crop&crop=center',
                    'title': 'Sports & Fitness',
                    'subtitle': 'Sports equipment, fitness gear, and outdoor activities'
                }
            ]
            
            # Create slideshow container
            slideshow_container = ui.element('div').classes('relative w-full h-full')
            current_slide = {'index': 0}
            slide_elements = []
            
            # Create all slide elements (initially hidden)
            for i, slide in enumerate(slideshow_images):
                slide_div = ui.element('div').classes('absolute inset-0 w-full h-full transition-opacity duration-1000')
                slide_div.style(f"background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{slide['url']}')")
                slide_div.classes('bg-cover bg-center bg-no-repeat')
                
                with slide_div:
                    with ui.element('div').classes('absolute inset-0 flex flex-col justify-center items-center text-white text-center px-4'):
                        # Main brand logo with star
                        with ui.element('div').classes('flex items-center justify-center gap-3 mb-4 flex-wrap'):
                            ui.label('INNO').classes('text-4xl sm:text-6xl font-bold text-white drop-shadow-lg')
                            ui.icon('star').classes('text-yellow-400 text-3xl sm:text-5xl drop-shadow-lg')
                            ui.label('HUB').classes('text-4xl sm:text-6xl font-bold text-white drop-shadow-lg')
                        
                        # Location
                        ui.label('Ghana').classes('text-lg sm:text-xl text-yellow-200 mb-4 font-medium drop-shadow-md')
                        
                        # Dynamic title and subtitle
                        ui.label(slide['title']).classes('text-lg sm:text-2xl font-semibold text-white mb-2 break-words px-4 drop-shadow-md max-w-4xl mx-auto')
                        ui.label(slide['subtitle']).classes('text-base sm:text-lg text-yellow-100 break-words px-4 drop-shadow-md mb-6')
                        
                        # Call to action buttons
                        with ui.element('div').classes('flex flex-col sm:flex-row gap-4 justify-center items-center'):
                            ui.button('Browse Ads', on_click=lambda: ui.navigate.to('/?cat=all')).classes('bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300')
                            ui.button('Post Ad', on_click=lambda: ui.navigate.to('/add_event')).classes('bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300')
                
                slide_elements.append(slide_div)
                if i == 0:
                    slide_div.classes('opacity-100')
                else:
                    slide_div.classes('opacity-0')
            
            
            
            def change_slide(index):
                current_slide['index'] = index
                
                # Hide all slides
                for slide in slide_elements:
                    slide.classes('opacity-0', remove='opacity-100')
                
                # Show current slide
                slide_elements[index].classes('opacity-100', remove='opacity-0')
                
            
            # Auto-advance slideshow every 5 seconds
            def auto_advance():
                next_index = (current_slide['index'] + 1) % len(slideshow_images)
                change_slide(next_index)
            
            # Start auto-advance timer
            ui.timer(5.0, auto_advance, active=True)
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
                            'bg_color': 'from-orange-600 to-red-600',
                            'accent_color': 'orange',
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
                        with ui.card().classes('p-4 bg-blue-600 text-white shadow-sm flex-1 flex items-center justify-center min-h-0'):
                            with ui.element('div').classes('text-center'):
                                ui.icon('home').classes('text-white text-2xl mb-2')
                                ui.label('HOME MAKEOVER').classes('text-sm font-bold mb-1')
                                ui.label('UP TO 45% OFF').classes('text-xs opacity-90')

        # Platform Analytics & Insights Section
        with ui.element('div').classes('container mx-auto px-4 py-8 max-w-7xl mb-8'):
            with ui.card().classes('p-6 bg-white shadow-sm w-full overflow-hidden rounded-lg border border-gray-200'):
                
                # Platform Analytics & Insights Section
                with ui.element('div').classes('text-center mb-6'):
                    with ui.row().classes('items-center justify-center gap-3 mb-2'):
                        # Light blue vertical bar
                        ui.element('div').classes('w-1 h-8 bg-blue-300 rounded')
                        # "Analytics" text in light blue
                        ui.label('Analytics').classes('text-blue-400 font-semibold text-sm')
                    # "Platform Insights" text in dark blue - centered
                    ui.label('Platform Insights').classes('text-2xl font-bold text-blue-600')
                
                # Live Stats and Tips Row - More Functional
                with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-5 gap-4 mb-6'):
                    # Live Stats Cards (4 columns)
                    with ui.element('div').classes('lg:col-span-4 grid grid-cols-2 sm:grid-cols-4 gap-4'):
                        # Total Adverts Card - Live Data
                        with ui.card().classes('bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-lg p-4 text-center hover:shadow-md transition-all duration-300'):
                            ui.icon('inventory').classes('text-2xl text-blue-600 mb-2')
                            ui.label('Total Adverts').classes('text-sm font-medium text-blue-700')
                            # Live count will be updated by the stats_refresh function
                            total_adverts_label = ui.label('Loading...').classes('text-xl font-bold text-blue-800')
                        
                        # Active Users Card - Live Data
                        with ui.card().classes('bg-gradient-to-br from-green-50 to-green-100 border border-green-200 rounded-lg p-4 text-center hover:shadow-md transition-all duration-300'):
                            ui.icon('people').classes('text-2xl text-green-600 mb-2')
                            ui.label('Active Users').classes('text-sm font-medium text-green-700')
                            # Live count will be updated by the stats_refresh function
                            active_users_label = ui.label('Loading...').classes('text-xl font-bold text-green-800')
                        
                        # Categories Card - Live Data
                        with ui.card().classes('bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-lg p-4 text-center hover:shadow-md transition-all duration-300'):
                            ui.icon('category').classes('text-2xl text-purple-600 mb-2')
                            ui.label('Categories').classes('text-sm font-medium text-purple-700')
                            # Live count will be updated by the stats_refresh function
                            categories_label = ui.label('Loading...').classes('text-xl font-bold text-purple-800')
                        
                        # Success Rate Card - Live Data
                        with ui.card().classes('bg-gradient-to-br from-orange-50 to-orange-100 border border-orange-200 rounded-lg p-4 text-center hover:shadow-md transition-all duration-300'):
                            ui.icon('trending_up').classes('text-2xl text-orange-600 mb-2')
                            ui.label('Success Rate').classes('text-sm font-medium text-orange-700')
                            # Live rate will be updated by the stats_refresh function
                            success_rate_label = ui.label('Loading...').classes('text-xl font-bold text-orange-800')
                    
                    # Search Tips Card (1 column) - Compact version
                    with ui.card().classes('lg:col-span-1 bg-gradient-to-br from-gray-50 to-blue-50 border border-gray-200 rounded-lg p-4 hover:shadow-md transition-all duration-300'):
                        with ui.column().classes('gap-3 h-full justify-center'):
                            with ui.row().classes('items-center gap-2 mb-2'):
                                ui.icon('lightbulb').classes('text-xl text-yellow-500')
                                ui.label('Search Tips').classes('text-sm font-semibold text-gray-800')
                            
                            with ui.column().classes('gap-1 text-xs text-gray-600'):
                                ui.label('Use specific keywords').classes('text-xs')
                                ui.label('Filter by location').classes('text-xs')
                                ui.label('Set price range').classes('text-xs')
                                ui.label('Contact sellers directly').classes('text-xs')
                
                # Function to animate counter values
                async def animate_counter(label, target_value, suffix=""):
                    """Animate counter from current value to target value"""
                    try:
                        current_text = label.text.replace(suffix, "").replace("Loading...", "0")
                        current_value = int(current_text) if current_text.isdigit() else 0
                        
                        if current_value == target_value:
                            return
                        
                        # Animate from current to target
                        steps = min(abs(target_value - current_value), 20)  # Max 20 steps
                        if steps == 0:
                            return
                            
                        step_size = (target_value - current_value) / steps
                        
                        for i in range(steps + 1):
                            value = int(current_value + (step_size * i))
                            label.text = f"{value}{suffix}"
                            await asyncio.sleep(0.05)  # 50ms delay between steps
                            
                    except Exception as e:
                        # Fallback to direct update
                        label.text = f"{target_value}{suffix}"
                
                # Function to refresh live stats
                async def refresh_live_stats():
                    try:
                        print("🔄 Refreshing live stats...")
                        
                        # Show loading state with spinner
                        total_adverts_label.text = "⏳"
                        active_users_label.text = "⏳"
                        categories_label.text = "⏳"
                        success_rate_label.text = "⏳"
                        
                        # Ensure API client is initialized
                        if not api_client.routes:
                            print("🔧 Initializing API client...")
                            await api_client.discover_endpoints()
                        
                        # Get live data from API
                        success, response = await api_client.get_ads()
                        print(f"📡 API Response - Success: {success}")
                        
                        if success and response:
                            # Count total adverts
                            if isinstance(response, dict):
                                adverts = response.get("data", response.get("adverts", response.get("items", [])))
                            elif isinstance(response, list):
                                adverts = response
                            else:
                                adverts = []
                            
                            total_count = len(adverts) if adverts else 0
                            print(f"📊 Total adverts found: {total_count}")
                            
                            # Count unique categories
                            categories_set = set()
                            for ad in adverts:
                                if isinstance(ad, dict) and 'category' in ad:
                                    categories_set.add(ad['category'].lower())
                            categories_count = len(categories_set)
                            
                            # Estimate active users (vendors who posted ads)
                            active_users_set = set()
                            for ad in adverts:
                                if isinstance(ad, dict) and 'advertiser_id' in ad:
                                    active_users_set.add(ad['advertiser_id'])
                            active_users_count = len(active_users_set)
                            
                            # Calculate success rate (ads with complete info - title, description, price, image)
                            ads_with_complete_info = sum(1 for ad in adverts if isinstance(ad, dict) and 
                                                       ad.get('title') and ad.get('description') and 
                                                       ad.get('price') and ad.get('image'))
                            success_rate = int((ads_with_complete_info / total_count * 100)) if total_count > 0 else 0
                            
                            # Update labels with animation
                            await animate_counter(total_adverts_label, total_count)
                            await animate_counter(active_users_label, active_users_count)
                            await animate_counter(categories_label, categories_count)
                            await animate_counter(success_rate_label, success_rate, suffix="%")
                            
                            # Update status indicator
                            try:
                                from datetime import datetime
                                current_time = datetime.now().strftime("%H:%M:%S")
                                last_updated_label.text = f"Updated {current_time}"
                            except:
                                pass
                            
                            print(f"✅ Stats updated: {total_count} adverts, {active_users_count} users, {categories_count} categories, {success_rate}% success")
                            
                        else:
                            # Fallback to default values if API fails
                            total_adverts_label.text = "0"
                            active_users_label.text = "0"
                            categories_label.text = "0"
                            success_rate_label.text = "0%"
                            
                            # Update status to show error
                            try:
                                last_updated_label.text = "Error - Retrying..."
                            except:
                                pass
                            
                    except Exception as e:
                        print(f"Error refreshing stats: {e}")
                        # Fallback to default values
                        total_adverts_label.text = "0"
                        active_users_label.text = "0"
                        categories_label.text = "0"
                        success_rate_label.text = "0%"
                
                # Refresh stats on page load - use ui.timer for proper execution
                def start_refresh():
                    async def delayed_refresh():
                        await asyncio.sleep(0.5)
                        await refresh_live_stats()
                    asyncio.create_task(delayed_refresh())
                
                ui.timer(0.1, start_refresh, once=True)
                
                # Also try immediate refresh
                ui.timer(1.0, lambda: asyncio.create_task(refresh_live_stats()), once=True)
                
                # Auto-refresh every 15 seconds for live analytics (more responsive)
                ui.timer(15.0, lambda: asyncio.create_task(refresh_live_stats()), active=True)
                
                # Listen for custom refresh events (e.g., when new ads are added)
                ui.run_javascript('''
                    window.addEventListener('refreshStats', function() {
                        // Trigger stats refresh when new content is added
                        setTimeout(() => {
                            // This will be handled by the auto-refresh timer
                        }, 1000);
                    });
                ''')
                
                # Add refresh button and live status indicator
                with ui.row().classes('justify-center items-center gap-4 mt-4'):
                    # Live status indicator
                    status_indicator = ui.element('div').classes('flex items-center gap-2 text-sm text-gray-600')
                    with status_indicator:
                        ui.icon('fiber_manual_record').classes('text-green-500 text-xs animate-pulse')
                        last_updated_label = ui.label('Live').classes('text-green-600 font-medium')
                    
                    # Refresh button
                    ui.button('Refresh Stats', on_click=refresh_live_stats, icon='refresh').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 text-sm font-medium rounded-lg shadow-sm hover:shadow-md transition-all duration-300')

        # Search and Filter Section
        with ui.element('div').classes('container mx-auto px-4 py-4 max-w-8xl'):
            with ui.card().classes('p-6 bg-gray-50 shadow-sm w-full overflow-hidden'):
                with ui.row().classes('items-end justify-between gap-4 mb-6'):
                    ui.label('All Adverts').classes('text-2xl font-bold text-gray-800')
                    with ui.row().classes('gap-3 flex-wrap items-center'):
                        q_input = ui.input('Search adverts...').classes('w-48 sm:w-64').props('outlined')
                        
                        # Browse All Ads button - moved here for better functionality
                        def browse_all_ads():
                            ui.navigate.to('/?cat=all&refresh=true')
                            products_grid.refresh()
                            ui.notify('Loading all adverts...', type='info')
                        
                        ui.button('Browse All Ads', on_click=browse_all_ads, icon='refresh').classes('bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 text-sm font-medium transition-all duration-300 shadow-lg hover:shadow-xl')

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
                            # Use the centralized API client to fetch all adverts
                            from utils.api_client import api_client
                            
                            # Ensure API client is initialized
                            if not api_client._discovered:
                                print("🔧 API client not discovered, initializing...")
                                await api_client.discover_endpoints()
                            
                            print("🌐 Fetching all adverts from backend...")
                            # Try to fetch more results with parameters
                            params = {
                                "limit": 100,  # Try to get more results
                                "offset": 0,   # Start from beginning
                                "all": "true"  # Try to get all results
                            }
                            success, response = await api_client.get_ads(params)
                            
                            # If we get few results, try without parameters
                            if success and isinstance(response, (dict, list)):
                                if isinstance(response, dict):
                                    items_count = len(response.get("data", response.get("adverts", response.get("items", []))))
                                else:
                                    items_count = len(response)
                                if items_count < 5:
                                    print(f"⚠️ Only {items_count} items found, trying without parameters...")
                                    success, response = await api_client.get_ads()
                                    print(f"📡 Retry response: {response}")
                            
                            print(f"📡 API Response - Success: {success}, Response type: {type(response)}")
                            
                            # Initialize items variable
                            items = []
                            
                            if success:
                                print(f"📥 Raw response: {response}")
                                
                                # Handle different response formats
                                if isinstance(response, dict):
                                    items = response.get("data", response.get("adverts", response.get("items", [])))
                                    print(f"📋 Extracted items from dict: {len(items)} items")
                                    # Check if there are more fields that might contain the data
                                    for key in response.keys():
                                        if isinstance(response[key], list) and len(response[key]) > len(items):
                                            items = response[key]
                                            print(f"📋 Found more items in '{key}': {len(items)} items")
                                elif isinstance(response, list):
                                    items = response
                                    print(f"📋 Direct list response: {len(items)} items")
                                else:
                                    items = []
                                    print(f"⚠️ Unexpected response format: {type(response)}")
                                
                                # Log successful data loading
                                if items:
                                    print(f"✓ Loaded {len(items)} adverts from backend")
                                    # Show first few titles for verification
                                    titles = [item.get('title', 'N/A') for item in items[:3]]
                                    print(f"  Recent adverts: {', '.join(titles)}")
                                else:
                                    print("⚠ No adverts found in backend response")
                            else:
                                print(f"❌ Failed to fetch adverts: {response}")
                                items = []
                        except Exception as e:
                            print(f"❌ Error loading adverts: {e}")
                            ui.notify(f"Failed to load products: {e}")
                            items = []

                        # Optimistically exclude items deleted this session
                        if deleted_titles:
                            items = [ad for ad in items if ad.get('title') not in deleted_titles]

                        def matches(ad):
                            ok_q = (q in ad['title'].lower()) if q else True
                            ok_cat = (ad['category'] == cat) if cat else True
                            return ok_q and ok_cat

                        print(f"🔍 Filtering - Query: '{q}', Category: '{cat}', Total items before filter: {len(items)}")
                        items = [ad for ad in items if matches(ad)]
                        print(f"🔍 After filtering: {len(items)} items")

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
                                    # Product Image Container - Portrait Frame
                                    with ui.element('div').classes('relative overflow-hidden bg-gray-50 h-80 w-full border border-gray-200 rounded-t-lg'):
                                        # Get image data from the advert
                                        image_data = ad.get('image', '')
                                        
                                        # Check if we have valid image data
                                        has_image = False
                                        image_url = None
                                        
                                        # Debug: Print image data info
                                        print(f"🔍 Image data for '{ad.get('title', 'N/A')}': {type(image_data)}, length: {len(str(image_data)) if image_data else 0}")
                                        
                                        if image_data and isinstance(image_data, str) and image_data.strip():
                                            if image_data.startswith('http'):
                                                # Direct URL (like Cloudinary)
                                                image_url = image_data
                                                has_image = True
                                                print(f"✅ Using direct URL: {image_data[:50]}...")
                                            elif image_data.startswith('data:'):
                                                # Base64 data URL
                                                image_url = image_data
                                                has_image = True
                                                print(f"✅ Using data URL: {image_data[:50]}...")
                                            elif len(image_data) > 100 and not image_data.startswith('http'):
                                                # Assume it's base64 data without prefix
                                                image_url = f'data:image/jpeg;base64,{image_data}'
                                                has_image = True
                                                print(f"✅ Using base64: {image_data[:50]}...")
                                            else:
                                                print(f"❌ Image data too short or invalid: {image_data[:100]}...")
                                        else:
                                            print(f"❌ No image data for '{ad.get('title', 'N/A')}'")
                                        
                                        if has_image and image_url:
                                            # Display the actual image with proper error handling
                                            try:
                                                # Create image element with error handling
                                                img_element = ui.image(image_url).classes('w-full h-full object-cover group-hover:scale-110 transition-transform duration-500')
                                                
                                                # Add error handler to fallback to placeholder
                                                def handle_image_error():
                                                    print(f"Image failed to load: {image_url[:50]}...")
                                                    # Replace with placeholder
                                                    img_element.clear()
                                                    with img_element:
                                                        with ui.element('div').classes('w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center p-4'):
                                                            category = ad.get('category', '').lower()
                                                            category_icons = {
                                                                'electronics': 'phone_android',
                                                                'fashion': 'checkroom', 
                                                                'home': 'home',
                                                                'vehicles': 'directions_car',
                                                                'real estate': 'home_work',
                                                                'services': 'build',
                                                                'furniture': 'chair',
                                                                'appliances': 'kitchen'
                                                            }
                                                            icon = 'image'
                                                            for cat_key, cat_icon in category_icons.items():
                                                                if cat_key in category:
                                                                    icon = cat_icon
                                                                    break
                                                            ui.icon(icon).classes('text-6xl text-gray-400 mb-3')
                                                            ui.label('Image Failed').classes('text-lg text-gray-500 font-medium mb-1')
                                                            ui.label(f'Category: {ad.get("category", "N/A")}').classes('text-sm text-gray-400')
                                                
                                                # Note: NiceGUI doesn't have direct on('error') support, so we'll rely on the try-catch
                                                
                                            except Exception as e:
                                                print(f"Image display error: {e}")
                                                # Fallback to placeholder if image fails
                                                has_image = False
                                        
                                        if not has_image:
                                            # Show a clean placeholder with product info
                                            with ui.element('div').classes('w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center p-4'):
                                                # Category icon
                                                category = ad.get('category', '').lower()
                                                category_icons = {
                                                    'electronics': 'phone_android',
                                                    'fashion': 'checkroom', 
                                                    'home': 'home',
                                                    'vehicles': 'directions_car',
                                                    'real estate': 'home_work',
                                                    'services': 'build',
                                                    'furniture': 'chair',
                                                    'appliances': 'kitchen'
                                                }
                                                
                                                icon = 'image'
                                                for cat_key, cat_icon in category_icons.items():
                                                    if cat_key in category:
                                                        icon = cat_icon
                                                        break
                                            
                                                ui.icon(icon).classes('text-6xl text-gray-400 mb-3')
                                                ui.label('No Image Available').classes('text-lg text-gray-500 font-medium mb-1')
                                                ui.label(f'{ad.get("category", "Product")}').classes('text-sm text-gray-400')
                                                
                                                # Add a subtle border to make it look like a frame
                                                ui.element('div').classes('absolute inset-0 border-2 border-dashed border-gray-300 rounded-lg')
                                        
                                        # Product Badge (New, Sale, etc.)
                                        with ui.element('div').classes('absolute top-3 left-3'):
                                            ui.label('NEW').classes('bg-green-500 text-white text-xs px-2 py-1 rounded-full font-semibold')
                                        
                                        # Wishlist button
                                        ui.button(icon='favorite_border').classes('absolute top-3 right-3 bg-white/90 backdrop-blur-sm rounded-full p-2 shadow-lg hover:bg-white hover:scale-110 transition-all duration-200').props('flat round')
                                        
                                        # Quick view overlay removed for cleaner UX
                                    
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

                                            # Secondary actions - All buttons with uniform height
                                            with ui.row().classes('gap-2 items-stretch h-12'):
                                                # Add to Cart Button
                                                def add_to_cart_action(title):
                                                    ui.notify(f'Added {title} to cart', type='positive')
                                                    ui.navigate.to('/cart')
                                                
                                                ui.button('Add to Cart', 
                                                    on_click=lambda e, t=ad['title']: add_to_cart_action(t), 
                                                    icon='shopping_cart'
                                                ).classes('btn-secondary flex-1 h-12 text-sm font-medium flex items-center justify-center')
                                                
                                                # Edit Button (only for vendors)
                                                if auth_state and auth_state.is_vendor():
                                                    ui.button('Edit', 
                                                        on_click=lambda e, advert=ad: ui.navigate.to(f"/edit_event?title={quote(str(advert['title']))}&id={advert.get('id', '')}"), 
                                                        icon='edit'
                                                        ).classes('btn-outline flex-1 h-12 text-sm font-medium flex items-center justify-center')
                                                
                                                # Delete Button (only for vendors)
                                                if auth_state and auth_state.is_vendor():
                                                    ui.button('Delete', 
                                                        on_click=lambda e, ad_id=ad.get('id', ad['title']): delete_ad(ad_id), 
                                                        icon='delete'
                                                    ).classes('bg-red-500 hover:bg-red-600 text-white flex-1 h-12 text-sm font-medium flex items-center justify-center')
                                                
                                                # Wishlist Button - Square button with same height
                                                ui.button('', 
                                                    on_click=lambda e, t=ad['title']: ui.notify(f'Added {t} to wishlist', type='positive'), 
                                                    icon='favorite_border'
                                                ).classes('bg-error text-white hover:bg-error w-12 h-12 flex items-center justify-center rounded-lg')

                    ui.timer(0.05, render, once=True)

                async def delete_ad(title: str) -> bool:
                    # Show confirmation dialog
                    with ui.dialog() as dialog, ui.card():
                        ui.label(f'Are you sure you want to delete "{title}"?').classes('text-lg font-semibold mb-4')
                        ui.label('This action cannot be undone.').classes('text-gray-600 mb-6')
                        
                        with ui.row().classes('gap-4 justify-end'):
                            ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded')
                            
                            async def confirm_delete():
                                dialog.close()
                                try:
                                    safe_title = (title or "").strip()
                                    # Use the API client's delete method with authentication
                                    success, response = await api_client.delete_ad(safe_title)
                                    
                                    if success:
                                        ui.notify('Advert deleted successfully', type='positive')
                                        # Optimistically remove from current view
                                        deleted_titles.add(safe_title)
                                        products_grid.refresh()
                                        return True
                                    else:
                                        ui.notify(f"Delete failed: {response}", type='negative')
                                        return False
                                except Exception as e:
                                    ui.notify(f"Error: {e}", type='negative')
                                    return False
                            
                            ui.button('Delete', on_click=confirm_delete).classes('bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded')
                    
                    dialog.open()
                    return False

            products_grid()
            
            # Load More Button
            with ui.element('div').classes('text-center mt-8 mb-4'):
                def load_more_ads():
                    ui.notify('Loading more adverts...', type='info')
                    products_grid.refresh()
                
                ui.button('Load More Ads', on_click=load_more_ads, icon='expand_more').classes('bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg text-sm font-medium transition-all duration-300 shadow-lg hover:shadow-xl')

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
        
        # Add immediate scroll functionality for returning from product view
        if scroll_to == 'products':
            # Use immediate scroll to prevent jarring behavior
            ui.timer(0.05, lambda: ui.run_javascript('''
                // Immediately scroll to products section
                const productsElement = document.getElementById("products");
                if (productsElement) {
                    // Use instant scroll for immediate positioning
                    productsElement.scrollIntoView({behavior: "instant", block: "start"});
                    
                    // Then apply smooth scroll for better UX
                    setTimeout(() => {
                        productsElement.scrollIntoView({behavior: "smooth", block: "start"});
                    }, 100);
                }
            '''), once=True)
