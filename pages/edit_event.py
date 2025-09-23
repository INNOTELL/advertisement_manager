from nicegui import ui
import requests
from urllib.parse import quote
from utils.api import base_url


def show_edit_event_page():
    q = ui.context.client.request.query_params
    original_title = q.get('title')
    if not original_title:
        with ui.element('div').classes('container mx-auto px-4 py-8'):
            with ui.card().classes('p-6 text-center'):
                ui.icon('error').classes('text-4xl text-red-500 mb-4')
                ui.label('Product not found').classes('text-xl font-semibold text-gray-800')
                ui.label('The product you\'re trying to edit doesn\'t exist').classes('text-gray-600 mt-2')
                ui.link('Back to Dashboard', '/dashboard').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold no-underline mt-4')
        return

    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto max-w-4xl px-4'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('Edit Product').classes('text-3xl font-bold text-gray-800')
                ui.label('Update your product information').classes('text-gray-600 mt-2')

            # Main Form Card
            with ui.card().classes('bg-white shadow-lg rounded-xl p-8'):
                # Two-column responsive form
                with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8'):
                    # Left column - Basic Info
                    with ui.element('div').classes('space-y-6'):
                        ui.label('Product Information').classes('text-xl font-semibold text-gray-800 mb-4')
                        
                        title = ui.input('Product Title *').classes('w-full').props('outlined')
                        title.props('placeholder=Enter a clear, descriptive title')
                        
                        price = ui.number('Price (GHS) *').classes('w-full').props('outlined')
                        price.props('placeholder=0.00')
                        
                        categories = [
                            'Electronics', 'Fashion', 'Furniture', 'Vehicles',
                            'Real Estate', 'Services', 'Appliances', 'Other',
                        ]
                        category_select = ui.select(categories, label='Category *').classes('w-full').props('outlined')
                        
                        description = ui.textarea('Product Description *').classes('w-full').props('outlined rows=6')
                        description.props('placeholder=Describe your product in detail...')

                    # Right column - Image Upload
                    with ui.element('div').classes('space-y-6'):
                        ui.label('Product Images').classes('text-xl font-semibold text-gray-800 mb-4')
                        
                        image_content = None

                        def handle_image_upload(e):
                            nonlocal image_content
                            image_content = e.content.read()
                            ui.notify('New image uploaded successfully!', type='positive')
                        
                        # Image Upload Area
                        with ui.element('div').classes('border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-orange-500 transition-colors'):
                            ui.icon('cloud_upload').classes('text-4xl text-gray-400 mb-4')
                            ui.label('Upload New Image').classes('text-lg font-medium text-gray-700 mb-2')
                            ui.label('Drag and drop or click to browse').classes('text-sm text-gray-500 mb-4')
                            ui.upload(on_upload=handle_image_upload).props('flat bordered').classes('w-full')
                            ui.label('Supported formats: JPG, PNG, GIF (Max 5MB)').classes('text-xs text-gray-400 mt-2')

                # AI Features Section
                with ui.element('div').classes('mt-8 p-6 bg-orange-50 rounded-lg border border-orange-200'):
                    ui.label('AI-Powered Features').classes('text-lg font-semibold text-orange-800 mb-4')
                    with ui.row().classes('gap-4 flex-wrap'):
                        def generate_description():
                            if title.value:
                                # Simulate AI description generation
                                generated_desc = f"High-quality {title.value.lower()} in excellent condition. Perfect for anyone looking for {category_select.value.lower() if category_select.value else 'quality products'}. Don't miss out on this great deal!"
                                description.value = generated_desc
                                ui.notify('AI description generated!', type='positive')
                            else:
                                ui.notify('Please enter a product title first', type='warning')
                        
                        def suggest_price():
                            # Simulate AI price suggestion
                            suggested_price = 150.00  # This would be calculated based on category and title
                            price.value = suggested_price
                            ui.notify(f'AI suggested price: GHS {suggested_price:,.2f}', type='positive')
                        
                        ui.button('Generate Description', on_click=generate_description, icon='auto_awesome').classes('bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg')
                        ui.button('Suggest Price', on_click=suggest_price, icon='trending_up').classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg')

                # Actions container (populated after save() is defined)
                action_row = ui.row().classes('mt-8 gap-4 justify-end')

                async def load():
                    try:
                        encoded = quote(str(original_title))
                        resp = requests.get(f"{base_url}/advert_details/{encoded}")
                        js = resp.json()
                        items = js.get('data', [])
                        if not items:
                            ui.notify('Product not found', type='negative')
                            return
                        data = items[0]
                        title.value = data['title']
                        description.value = data['description']
                        price.value = data['price']
                        category_select.value = data['category']
                    except Exception as e:
                        ui.notify(f'Error loading product: {e}', type='negative')

                def validate() -> bool:
                    if not title.value or not description.value or not category_select.value:
                        ui.notify('Please fill in all required fields', type='negative')
                        return False
                    try:
                        if float(price.value) <= 0:
                            ui.notify('Price must be greater than 0', type='negative')
                            return False
                    except Exception:
                        ui.notify('Price must be a valid number', type='negative')
                        return False
                    return True

                async def save():
                    if not validate():
                        return
                    if image_content is None:
                        ui.notify('Please upload a new image', type='negative')
                        return
                    encoded = quote(str(original_title))
                    data_form = {
                        'new_title': title.value,
                        'description': description.value,
                        'price': float(price.value),
                        'category': category_select.value,
                    }
                    files = {
                        'image': ('image', image_content, 'application/octet-stream'),
                    }
                    try:
                        r = requests.put(f"{base_url}/edit_advert/{encoded}", data=data_form, files=files)
                        if r.status_code >= 400:
                            ui.notify(f'Update failed: {r.text}', type='negative')
                            return
                        ui.notify('Product updated successfully!', type='positive')
                        ui.navigate.to(f'/view_event?title={quote(str(title.value))}')
                    except Exception as e:
                        ui.notify(f'Error: {e}', type='negative')

                ui.timer(0.05, load, once=True)
                # Populate the actions row defined above so buttons appear side by side
                with action_row:
                    def go_cancel():
                        ui.navigate.to(f'/view_event?title={quote(str(original_title))}')
                    ui.button('Cancel', on_click=go_cancel).classes('bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold')
                    ui.button('Save Changes', on_click=save, icon='save').classes('bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold')

