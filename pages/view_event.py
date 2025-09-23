from nicegui import ui
import requests
import asyncio
from urllib.parse import quote
from utils.api import base_url
from components.footer import show_footer


@ui.page('/view_event')

def show_view_event_page():
    q = ui.context.client.request.query_params
    title = q.get('title')
    advert_id = q.get('id')  # Also check for ID parameter
    
    if not title and not advert_id:
        with ui.element('div').classes('container mx-auto px-4 py-8'):
            with ui.card().classes('p-6 text-center'):
                ui.icon('error').classes('text-4xl text-red-500 mb-4')
                ui.label('Product not found').classes('text-xl font-semibold text-gray-800')
                ui.label('The product you\'re looking for doesn\'t exist').classes('text-gray-600 mt-2')
                ui.link('Back to Home', '/').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold no-underline mt-4')
        return

    async def load():
        try:
            # First try to get all adverts and find the one we want
            response = await asyncio.to_thread(requests.get, f"{base_url}/adverts")
            json_data = response.json()
            all_adverts = json_data.get("data", [])
            
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
            with ui.element('div').classes('container mx-auto px-4 py-8'):
                with ui.card().classes('p-6 text-center'):
                    ui.icon('error').classes('text-4xl text-red-500 mb-4')
                    ui.label('Product not found').classes('text-xl font-semibold text-gray-800')
                    ui.label('The product you\'re looking for doesn\'t exist').classes('text-gray-600 mt-2')
                    ui.link('Back to Home', '/').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold no-underline mt-4')
            return
        
        data = items[0]
        
        # Jumia-style product detail page
        with ui.element('div').classes('min-h-screen bg-white py-8'):
            with ui.element('div').classes('container mx-auto px-4 max-w-7xl'):
                # Breadcrumb
                with ui.element('div').classes('mb-6'):
                    with ui.row().classes('items-center gap-2 text-sm text-gray-600'):
                        ui.link('Home', '/').classes('hover:text-orange-500 no-underline')
                        ui.icon('chevron_right').classes('text-gray-400')
                        ui.link(data.get('category', 'Category'), f'/?cat={data.get("category", "")}').classes('hover:text-orange-500 no-underline')
                        ui.icon('chevron_right').classes('text-gray-400')
                        ui.label(data.get('title', 'Product')).classes('text-gray-800 font-medium')
                
                # Main Product Section
                with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'):
                    # Left column: Product Images
                    with ui.card().classes('bg-gray-50 p-6 rounded-xl shadow-sm'):
                        # Main Product Image
                        with ui.element('div').classes('relative overflow-hidden bg-gray-50 rounded-lg mb-4 aspect-square'):
                            if data.get('image') and data['image'].strip():
                                # Display image from backend database
                                ui.image(data['image']).classes('w-full h-full object-contain rounded-lg hover:scale-105 transition-transform duration-300')
                            else:
                                # Enhanced fallback for missing images
                                with ui.element('div').classes('w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex flex-col items-center justify-center'):
                                    ui.icon('image').classes('text-8xl text-gray-400 mb-4')
                                    ui.label('No Image Available').classes('text-lg text-gray-500 font-medium')
                                    ui.label('Image will be displayed here').classes('text-sm text-gray-400')
                        
                        # Image thumbnails and gallery
                        with ui.element('div').classes('space-y-3'):
                            ui.label('Product Gallery').classes('text-sm font-semibold text-gray-700')
                            with ui.row().classes('gap-2 flex-wrap'):
                                # Main image thumbnail
                                if data.get('image') and data['image'].strip():
                                    with ui.element('div').classes('w-16 h-16 bg-gray-200 rounded-lg cursor-pointer hover:border-2 hover:border-orange-500 overflow-hidden border-2 border-orange-500'):
                                        ui.image(data['image']).classes('w-full h-full object-cover')
                                else:
                                    with ui.element('div').classes('w-16 h-16 bg-gray-200 rounded-lg cursor-pointer hover:border-2 hover:border-orange-500 flex items-center justify-center border-2 border-orange-500'):
                                        ui.icon('image').classes('text-gray-400')
                                
                                # Additional placeholder thumbnails
                                for i in range(3):
                                    with ui.element('div').classes('w-16 h-16 bg-gray-200 rounded-lg cursor-pointer hover:border-2 hover:border-orange-500 flex items-center justify-center'):
                                        ui.icon('add_photo_alternate').classes('text-gray-400 text-sm')
                    
                    # Right column: Product Details
                    with ui.element('div').classes('space-y-6'):
                        # Product Title and Rating
                        ui.label(data['title']).classes('text-2xl lg:text-3xl font-bold text-gray-800 leading-tight')
                        
                        # Rating and Stock Status
                        with ui.row().classes('items-center gap-4 mb-4'):
                            with ui.row().classes('items-center gap-1'):
                                for i in range(5):
                                    ui.icon('star').classes('text-yellow-400 text-sm')
                                ui.label('4.5 (128 reviews)').classes('text-sm text-gray-600')
                            ui.label('•').classes('text-gray-400')
                            ui.label('In Stock').classes('text-sm text-green-600 font-medium')
                        
                        # Price Section
                        with ui.element('div').classes('py-4 border-b border-gray-200'):
                            with ui.row().classes('items-baseline gap-3'):
                                ui.label(f"GHS {data['price']:,.2f}").classes('text-3xl lg:text-4xl font-bold text-orange-500')
                                ui.label(f"GHS {(data['price'] * 1.2):,.2f}").classes('text-lg text-gray-400 line-through')
                            ui.label('Free shipping on orders over GHS 200').classes('text-sm text-green-600 mt-2')
                        
                        # Key Features
                        with ui.element('div').classes('py-4 border-b border-gray-200'):
                            ui.label('Key Features').classes('text-lg font-semibold text-gray-800 mb-3')
                            features = [
                                'High Quality Materials',
                                'Easy to Use',
                                'Durable Construction',
                                '1 Year Warranty'
                            ]
                            for feature in features:
                                with ui.row().classes('items-center gap-2 mb-2'):
                                    ui.icon('check_circle').classes('text-green-500 text-sm')
                                    ui.label(feature).classes('text-gray-700 text-sm')
                        
                        # Action Buttons
                        with ui.element('div').classes('space-y-4 pt-6'):
                            with ui.row().classes('gap-4'):
                                ui.button('Add to Cart', icon='shopping_cart').classes('flex-1 bg-blue-300 hover:bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg')
                                ui.button('Buy Now', icon='flash_on').classes('flex-1 bg-red-500 hover:bg-red-600 text-white py-4 rounded-lg font-semibold text-lg')
                            
                            with ui.row().classes('gap-4'):
                                ui.button('Add to Wishlist', icon='favorite_border').classes('bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-medium')
                                ui.button('Share', icon='share').classes('bg-gray-100 hover:bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-medium')
                        
                        # Vendor Actions (only for authenticated vendors)
                        if True:  # Simplified for demo
                            with ui.element('div').classes('pt-6 border-t border-gray-200'):
                                ui.label('Vendor Actions').classes('text-lg font-semibold text-gray-800 mb-4')
                                with ui.row().classes('gap-4'):
                                    def go_edit():
                                        ui.navigate.to(f'/edit_event?title={quote(str(data.get("title","")))}')
                                    ui.button('Edit Product', on_click=go_edit, icon='edit').classes('bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium')
                                    
                                    async def delete_product():
                                        try:
                                            response = requests.delete(f"{base_url}/adverts/{quote(str(data.get('title', '')))}")
                                            if response.status_code == 200:
                                                ui.notify('Product deleted successfully', type='positive')
                                                ui.navigate.to('/dashboard')
                                            else:
                                                ui.notify('Failed to delete product', type='negative')
                                        except Exception as e:
                                            ui.notify(f'Error: {e}', type='negative')
                                    
                                    ui.button('Delete Product', on_click=delete_product, icon='delete').classes('bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg font-medium')
                
                # Product Details Tabs
                with ui.element('div').classes('bg-gray-50 rounded-xl shadow-sm mb-8'):
                    with ui.element('div').classes('border-b border-gray-200'):
                        with ui.row().classes('px-6 py-4'):
                            ui.button('Description').classes('px-4 py-2 text-orange-500 font-semibold border-b-2 border-orange-500')
                            ui.button('Specifications').classes('px-4 py-2 text-gray-600 hover:text-orange-500')
                            ui.button('Reviews').classes('px-4 py-2 text-gray-600 hover:text-orange-500')
                            ui.button('Shipping').classes('px-4 py-2 text-gray-600 hover:text-orange-500')
                    
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
                                for label, value in details:
                                    with ui.row().classes('justify-between py-2 border-b border-gray-100'):
                                        ui.label(label).classes('text-gray-600')
                                        ui.label(value).classes('text-gray-800 font-medium')
                            
                            with ui.element('div'):
                                ui.label('Shipping Information').classes('text-lg font-poppins font-semibold text-gray-800 mb-3')
                                shipping_info = [
                                    ('Delivery Time', '2-5 Business Days'),
                                    ('Shipping Cost', 'Free over GHS 200'),
                                    ('Return Policy', '30 Days'),
                                    ('Payment Methods', 'Cash, Mobile Money, Card')
                                ]
                                for label, value in shipping_info:
                                    with ui.row().classes('justify-between py-2 border-b border-gray-100'):
                                        ui.label(label).classes('text-gray-600')
                                        ui.label(value).classes('text-gray-800 font-medium')
                
                # Related Products Section
                with ui.element('div').classes('bg-gray-50 rounded-xl shadow-sm p-6'):
                    ui.label('Related Products').classes('text-2xl font-bold text-gray-800 mb-6')
                    with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6'):
                        # Placeholder for related products
                        for i in range(4):
                            with ui.card().classes('p-4 hover:shadow-lg transition-shadow cursor-pointer border border-gray-100'):
                                with ui.element('div').classes('w-full h-32 bg-gray-200 rounded mb-3 flex items-center justify-center'):
                                    ui.icon('image').classes('text-4xl text-gray-400')
                                ui.label(f'Related Product {i+1}').classes('font-medium text-gray-800 mb-1')
                                ui.label(f'GHS {(i+1)*50:,.2f}').classes('text-orange-500 font-bold')
        show_footer()

    ui.timer(0.05, load, once=True)
