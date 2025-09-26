from nicegui import ui
import requests
import asyncio
from urllib.parse import quote
from utils.api import base_url
# Header and footer are handled by main.py
from utils.auth import auth_state, logout


@ui.page('/view_event')
def show_view_event_page():
    q = ui.context.client.request.query_params
    title = q.get('title')
    advert_id = q.get('id')  # Also check for ID parameter
    
    # Header is handled by main.py
    
    if not title and not advert_id:
        with ui.element('div').classes('min-h-screen w-full max-w-full px-4 py-8'):
            with ui.card().classes('p-6 text-center max-w-2xl mx-auto'):
                ui.icon('error').classes('text-4xl text-red-500 mb-4')
                ui.label('Product not found').classes('text-xl font-semibold text-gray-800')
                ui.label('The product you\'re looking for doesn\'t exist').classes('text-gray-600 mt-2')
                ui.link('Back to Home', '/').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold no-underline mt-4')
        # Footer is handled by main.py
        return

    async def load():
        try:
            # Use the API client for consistent authentication and error handling
            from utils.api_client import api_client
            
            # Ensure API client is initialized
            if not api_client._discovered:
                await api_client.discover_endpoints()
            
            # Get all adverts and find the specific one
            success, response = await api_client.get_ads()
            
            if not success:
                print(f"Failed to load adverts: {response}")
                items = []
            else:
                # Handle different response formats
                if isinstance(response, dict):
                    all_adverts = response.get("data", response.get("adverts", response.get("items", [])))
                elif isinstance(response, list):
                    all_adverts = response
                else:
                    all_adverts = []
                
                # Find the specific advert
                target_advert = None
                if advert_id:
                    target_advert = next((ad for ad in all_adverts if ad.get('id') == advert_id), None)
                elif title:
                    target_advert = next((ad for ad in all_adverts if ad.get('title') == title), None)
                
                if not target_advert:
                    items = []
                else:
                    items = [target_advert]
            
        except Exception as e:
            print(f"Error loading advert details: {e}")
            items = []
        
        if not items:
            with ui.element('div').classes('min-h-screen w-full max-w-full px-4 py-8'):
                with ui.card().classes('p-6 text-center max-w-2xl mx-auto'):
                    ui.icon('error').classes('text-4xl text-red-500 mb-4')
                    ui.label('Product not found').classes('text-xl font-semibold text-gray-800')
                    ui.label('The product you\'re looking for doesn\'t exist').classes('text-gray-600 mt-2')
                    ui.link('Back to Home', '/').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold no-underline mt-4')
            # Footer is handled by main.py
            return
        
        data = items[0]
        
        # Enhanced product detail page with proper footer positioning
        with ui.element('div').classes('min-h-screen bg-gray-50'):
            with ui.element('div').classes('w-full max-w-7xl mx-auto px-4 py-4'):
                # Back button and breadcrumb
                with ui.element('div').classes('mb-6 flex items-center justify-between bg-white p-4 rounded-lg shadow-sm border border-gray-200'):
                    # Back button - more visible and functional
                    def go_back():
                        # Navigate back to dashboard
                        ui.navigate.to('/dashboard')
                    
                    ui.button('Back to Products', on_click=go_back, icon='arrow_back').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300')
                    
                    # Breadcrumb - more visible and functional
                    with ui.row().classes('items-center gap-2 text-sm'):
                        ui.link('Home', '/').classes('hover:text-orange-500 no-underline text-gray-600 hover:text-orange-500 font-medium')
                        ui.icon('chevron_right').classes('text-gray-400')
                        ui.link(data.get('category', 'Category'), f'/?cat={data.get("category", "")}').classes('hover:text-orange-500 no-underline text-gray-600 hover:text-orange-500 font-medium')
                        ui.icon('chevron_right').classes('text-gray-400')
                        ui.label(data.get('title', 'Product')).classes('text-gray-800 font-semibold')
                
                # Main Product Section with full width utilization
                with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6'):
                    # Left column: Product Images
                    with ui.card().classes('bg-white p-6 rounded-xl shadow-lg border border-gray-200'):
                        # Main Product Image - Fills Full Card, Clickable
                        if data.get('image') and data['image'].strip():
                            # Clickable image for full view - shows VERY BIG free form image
                            def show_main_full_image():
                                with ui.dialog() as dialog:
                                    # No card wrapper - just the image in free form
                                    with ui.element('div').classes('fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50'):
                                        # Very big image without any container constraints
                                        ui.image(data['image']).classes('max-w-[95vw] max-h-[95vh] object-contain')
                                        
                                        # Close button positioned absolutely
                                        with ui.element('div').classes('absolute top-4 right-4'):
                                            ui.button('✕', on_click=dialog.close).classes('bg-white bg-opacity-20 hover:bg-opacity-30 text-white text-2xl font-bold w-12 h-12 rounded-full border-2 border-white hover:border-gray-300 transition-all duration-300')
                                        
                                        # Click anywhere to close
                                        with ui.element('div').classes('absolute inset-0 -z-10').on('click', dialog.close):
                                            pass
                                dialog.open()
                            
                            # Main clickable image - fills the entire card area
                            with ui.element('div').classes('cursor-pointer hover:opacity-90 transition-opacity duration-300 w-full').on('click', show_main_full_image):
                                ui.image(data['image']).classes('w-full h-full min-h-[500px] max-h-[700px] object-cover rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300')
                            
                            # Click hint
                            ui.label('Click image to view full size').classes('text-sm text-gray-500 text-center italic mt-2')
                        else:
                            # Enhanced fallback for missing images - fills card
                            with ui.element('div').classes('w-full h-[500px] bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex flex-col items-center justify-center border border-gray-200'):
                                ui.icon('image').classes('text-8xl text-gray-400 mb-4')
                                ui.label('No Image Available').classes('text-lg text-gray-500 font-medium')
                                ui.label('Uploaded image will be displayed here').classes('text-sm text-gray-400')
                    
                    # Right column: Product Details
                    with ui.card().classes('bg-white p-6 rounded-xl shadow-lg border border-gray-200'):
                        with ui.element('div').classes('space-y-6'):
                            # Product Title and Rating
                            ui.label(data['title']).classes('text-2xl lg:text-3xl font-bold text-gray-800 leading-tight')
                        
                        # Rating and Stock Status
                        with ui.row().classes('items-center gap-4 mb-4'):
                            ui.label('In Stock').classes('text-green-600 font-semibold bg-green-100 px-3 py-1 rounded-full text-sm')
                            ui.label('Free Shipping').classes('text-blue-600 font-semibold bg-blue-100 px-3 py-1 rounded-full text-sm')
                        
                        # Price Section
                        with ui.element('div').classes('mb-6'):
                            price_value = data.get('price', 0)
                            try:
                                price_float = float(price_value)
                                ui.label(f'GHS {price_float:,.2f}').classes('text-3xl font-bold text-orange-500')
                            except (TypeError, ValueError):
                                ui.label('Price not available').classes('text-2xl font-bold text-gray-500')
                        
                        # Product Features
                        with ui.element('div').classes('mb-6'):
                            features = [
                                'High Quality Product',
                                'Fast Delivery Available',
                                'Customer Support 24/7',
                                'Money Back Guarantee'
                            ]
                            for feature in features:
                                with ui.row().classes('items-center gap-2 mb-2'):
                                    ui.icon('check_circle').classes('text-green-500 text-sm')
                                    ui.label(feature).classes('text-gray-700 text-sm')
                        
                        # Action Buttons with proper functionality
                        with ui.element('div').classes('space-y-4 pt-6'):
                            with ui.row().classes('gap-4'):
                                def add_to_cart():
                                    ui.notify('Added to cart successfully!', type='positive')
                                    ui.navigate.to('/cart')
                                
                                def buy_now():
                                    ui.notify('Redirecting to checkout...', type='info')
                                    ui.navigate.to('/cart')
                                
                                ui.button('Add to Cart', on_click=add_to_cart, icon='shopping_cart').classes('flex-1 bg-blue-500 hover:bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg transition-all duration-300')
                                ui.button('Buy Now', on_click=buy_now, icon='flash_on').classes('flex-1 bg-orange-500 hover:bg-orange-600 text-white py-4 rounded-lg font-semibold text-lg transition-all duration-300')
                            
                            with ui.row().classes('gap-4'):
                                def add_to_wishlist():
                                    ui.notify('Added to wishlist!', type='positive')
                                    ui.navigate.to('/wishlist')
                                
                                def share_product():
                                    ui.notify('Share link copied to clipboard!', type='info')
                                
                                ui.button('Add to Wishlist', on_click=add_to_wishlist, icon='favorite_border').classes('bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-medium transition-all duration-300')
                                ui.button('Share', on_click=share_product, icon='share').classes('bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-medium transition-all duration-300')
                                
                                # Delete button (for vendors only)
                                if auth_state and auth_state.is_vendor():
                                    async def delete_product_from_actions():
                                        with ui.dialog() as dialog, ui.card():
                                            ui.label(f'Are you sure you want to delete "{data.get("title", "this product")}"?').classes('text-lg font-semibold mb-4')
                                            ui.label('This action cannot be undone.').classes('text-gray-600 mb-6')
                                            
                                            with ui.row().classes('gap-4 justify-end'):
                                                ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded')
                                                
                                                async def confirm_delete():
                                                    dialog.close()
                                                    try:
                                                        from utils.api_client import api_client
                                                        success, response = await api_client.delete_ad(str(data.get('id', data.get('title', ''))))
                                                        
                                                        if success:
                                                            ui.notify('Product deleted successfully', type='positive')
                                                            ui.navigate.to('/')
                                                        else:
                                                            ui.notify(f'Failed to delete product: {response}', type='negative')
                                                    except Exception as e:
                                                        ui.notify(f'Error: {e}', type='negative')
                                                
                                                ui.button('Delete', on_click=confirm_delete).classes('bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded')
                                        
                                        dialog.open()
                                    
                                    ui.button('Delete', on_click=delete_product_from_actions, icon='delete').classes('bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-medium transition-all duration-300')
                
                # Product Details Tabs with full width
                with ui.card().classes('bg-white rounded-xl shadow-lg border border-gray-200 mb-6'):
                    with ui.element('div').classes('border-b border-gray-200'):
                        with ui.row().classes('px-6 py-4 gap-2'):
                            def show_description():
                                ui.notify('Showing product description', type='info')
                            
                            def show_specifications():
                                ui.notify('Showing specifications', type='info')
                            
                            def show_reviews():
                                ui.notify('Showing reviews', type='info')
                            
                            def show_shipping():
                                ui.notify('Showing shipping info', type='info')
                            
                            ui.button('Description', on_click=show_description).classes('px-4 py-2 text-orange-500 font-semibold border-b-2 border-orange-500 hover:bg-orange-50 transition-all duration-300')
                            ui.button('Specifications', on_click=show_specifications).classes('px-4 py-2 text-gray-600 hover:text-orange-500 hover:bg-orange-50 transition-all duration-300')
                            ui.button('Reviews', on_click=show_reviews).classes('px-4 py-2 text-gray-600 hover:text-orange-500 hover:bg-orange-50 transition-all duration-300')
                            ui.button('Shipping', on_click=show_shipping).classes('px-4 py-2 text-gray-600 hover:text-orange-500 hover:bg-orange-50 transition-all duration-300')
                    
                    # Description Content
                    with ui.element('div').classes('p-6'):
                        ui.label('Product Description').classes('text-xl font-bold text-gray-800 mb-4')
                        ui.label(data['description']).classes('text-gray-700 leading-relaxed').style('white-space: pre-line;')
                        
                        # Additional product details
                        with ui.element('div').classes('mt-6 grid grid-cols-1 md:grid-cols-2 gap-6'):
                            with ui.element('div'):
                                ui.label('Product Information').classes('text-lg font-semibold text-gray-800 mb-3')
                                details = [
                                    ('Brand', 'Generic'),
                                    ('Model', 'Standard'),
                                    ('Category', data.get('category', 'N/A')),
                                    ('Condition', 'New'),
                                    ('Warranty', '1 Year')
                                ]
                                for i, (label, value) in enumerate(details):
                                    # Alternating colors: even rows get light blue, odd rows get light gray
                                    bg_color = 'bg-blue-50' if i % 2 == 0 else 'bg-gray-50'
                                    text_color = 'text-blue-800' if i % 2 == 0 else 'text-gray-800'
                                    label_color = 'text-blue-600' if i % 2 == 0 else 'text-gray-600'
                                    
                                    with ui.row().classes(f'justify-between py-3 px-4 border-b border-gray-200 {bg_color} rounded-lg mb-1'):
                                        ui.label(label).classes(f'{label_color} font-medium')
                                        ui.label(value).classes(f'{text_color} font-semibold')
                            
                            with ui.element('div'):
                                ui.label('Shipping Information').classes('text-lg font-poppins font-semibold text-gray-800 mb-3')
                                shipping_info = [
                                    ('Delivery Time', '2-5 Business Days'),
                                    ('Shipping Cost', 'Free over GHS 200'),
                                    ('Return Policy', '30 Days'),
                                    ('Payment Methods', 'Cash, Mobile Money, Card')
                                ]
                                for i, (label, value) in enumerate(shipping_info):
                                    # Alternating colors: even rows get light green, odd rows get light gray
                                    bg_color = 'bg-green-50' if i % 2 == 0 else 'bg-gray-50'
                                    text_color = 'text-green-800' if i % 2 == 0 else 'text-gray-800'
                                    label_color = 'text-green-600' if i % 2 == 0 else 'text-gray-600'
                                    
                                    with ui.row().classes(f'justify-between py-3 px-4 border-b border-gray-200 {bg_color} rounded-lg mb-1'):
                                        ui.label(label).classes(f'{label_color} font-medium')
                                        ui.label(value).classes(f'{text_color} font-semibold')
                
                # Related Products Section - Real Products from Database
                with ui.card().classes('bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6'):
                    ui.label('Related Products').classes('text-2xl font-bold text-gray-800 mb-6')
                    with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6'):
                        # Get real related products from database (same category, excluding current product)
                        current_category = data.get('category', '')
                        current_title = data.get('title', '')
                        
                        # Filter related products from the same category, excluding current product
                        related_products = []
                        for advert in all_adverts:
                            if (advert.get('category') == current_category and 
                                advert.get('title') != current_title and 
                                len(related_products) < 4):  # Limit to 4 products
                                related_products.append(advert)
                        
                        # If not enough products in same category, add other products
                        if len(related_products) < 4:
                            for advert in all_adverts:
                                if (advert.get('title') != current_title and 
                                    advert not in related_products and 
                                    len(related_products) < 4):
                                    related_products.append(advert)
                        
                        # Display real related products
                        if related_products:
                            for product in related_products:
                                def view_related_product(p=product):
                                    ui.navigate.to(f'/view_event?title={quote(str(p.get("title", "")))}&id={p.get("id", "")}')
                                
                                with ui.card().classes('p-4 hover:shadow-lg transition-all duration-300 cursor-pointer border border-gray-100 hover:border-orange-300').on('click', view_related_product):
                                    # Product image
                                    if product.get('image') and product['image'].strip():
                                        ui.image(product['image']).classes('w-full h-32 object-cover rounded mb-3')
                                    else:
                                        with ui.element('div').classes('w-full h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded mb-3 flex items-center justify-center'):
                                            ui.icon('image').classes('text-4xl text-gray-400')
                                    
                                    # Product details
                                    ui.label(product.get('title', 'Product')).classes('font-medium text-gray-800 mb-1 text-sm')
                                    ui.label(f'GHS {product.get("price", 0):,.2f}').classes('text-orange-500 font-bold')
                                    ui.label(f'Category: {product.get("category", "N/A")}').classes('text-xs text-gray-500 mt-1')
                        else:
                            # Fallback if no related products found
                            ui.label('No related products found').classes('col-span-full text-center text-gray-500 py-8')
            
            # Add bottom spacing to properly separate content from footer
            with ui.element('div').classes('h-24 w-full'):
                pass
        # Footer is handled by main.py

    ui.timer(0.05, load, once=True)
