import json

from nicegui import ui
from urllib.parse import quote
from utils.api_client import api_client
from config import CATEGORIES, LOCATIONS


def show_edit_event_page():
    q = ui.context.client.request.query_params
    original_title = q.get('title')
    advert_id = q.get('id')  # Also check for ID parameter
    
    if not original_title and not advert_id:
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
                        
                        category_select = ui.select(CATEGORIES, value=None, label='Category *').classes('w-full').props('outlined')

                        location_select = ui.select(LOCATIONS, value=LOCATIONS[0], label='Location *').classes('w-full').props('outlined')
                        
                        description = ui.textarea('Product Description *').classes('w-full').props('outlined rows=6')
                        description.props('placeholder=Describe your product in detail...')

                    # Right column - Image Upload
                    with ui.element('div').classes('space-y-6'):
                        ui.label('Product Images').classes('text-xl font-semibold text-gray-800 mb-4')
                        
                        image_content = None
                        
                        # Image Preview Area
                        image_preview = ui.element('div').classes('mb-4')

                        def handle_image_upload(e):
                            nonlocal image_content
                            image_content = e.content.read()
                            ui.notify('New image uploaded successfully!', type='positive')
                            
                            # Show preview of new image
                            if image_content:
                                import base64
                                image_base64 = base64.b64encode(image_content).decode('utf-8')
                                image_preview.clear()
                                with image_preview:
                                    with ui.card().classes('p-4 bg-white border border-gray-200 rounded-lg'):
                                        ui.label('New Image Preview').classes('text-sm font-semibold text-gray-700 mb-2')
                                        ui.image(f'data:image/jpeg;base64,{image_base64}').classes('w-full h-48 object-cover rounded-lg')
                                        ui.label('This will replace the current image').classes('text-xs text-green-600 mt-2')
                        
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
                        # Use the API client for consistent authentication and error handling
                        
                        # Ensure API client is initialized
                        if not api_client._discovered:
                            await api_client.discover_endpoints()
                        
                        # Get all adverts and find the specific one
                        success, response = await api_client.get_ads()
                        
                        if not success:
                            ui.notify('Failed to load product data', type='negative')
                            return
                        
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
                        elif original_title:
                            target_advert = next((ad for ad in all_adverts if ad.get('title') == original_title), None)
                        
                        if not target_advert:
                            ui.notify('Product not found', type='negative')
                            return
                        
                        # Populate the form with existing data
                        title.value = target_advert.get('title', '')
                        description.value = target_advert.get('description', '')
                        price.value = target_advert.get('price', 0)
                        category_value = target_advert.get('category')
                        category_select.value = category_value if category_value in CATEGORIES else None

                        location_value = target_advert.get('location') or LOCATIONS[0]
                        if location_value not in LOCATIONS:
                            location_value = LOCATIONS[0]
                        location_select.value = location_value
                        
                        # Show current image if available
                        current_image = target_advert.get('image', '')
                        if current_image:
                            image_preview.clear()
                            with image_preview:
                                with ui.card().classes('p-4 bg-white border border-gray-200 rounded-lg'):
                                    ui.label('Current Image').classes('text-sm font-semibold text-gray-700 mb-2')
                                    if current_image.startswith('http'):
                                        ui.image(current_image).classes('w-full h-48 object-cover rounded-lg')
                                    else:
                                        ui.label('Image available but format not supported for preview').classes('text-xs text-gray-500')
                                    ui.label('Upload a new image below to replace this one').classes('text-xs text-blue-600 mt-2')
                        
                    except Exception as e:
                        ui.notify(f'Error loading product: {e}', type='negative')

                def validate() -> bool:
                    if not title.value or not description.value or not category_select.value or not location_select.value:
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

                save_button_ref = {}
                async def save():
                    if not validate():
                        return

                    btn = save_button_ref.get('button')
                    if btn:
                        btn.disable()
                        btn.props('loading')
                    try:
                        if not api_client._discovered:
                            await api_client.discover_endpoints()

                        update_data = {
                            'new_title': title.value,
                            'description': description.value,
                            'price': float(price.value),
                            'category': category_select.value
                        }

                        if image_content:
                            update_data['image'] = image_content

                        identifier = advert_id or original_title

                        print(f" Updating advert with ID: {identifier}")
                        print(f"⚙️ Update data: {update_data}")
                        print(f"⚙️ Location: {location_select.value}")

                        success, response = await api_client.update_ad_with_location(
                            str(identifier),
                            update_data,
                            location_select.value
                        )

                        if success:
                            ui.notify('Product updated successfully!', type='positive')
                            payload = json.dumps({'type': 'updated', 'id': str(identifier)})
                            ui.timer(
                                0.2,
                                lambda payload=payload: ui.run_javascript(
                                    f"window.dispatchEvent(new CustomEvent('adverts:changed',{{detail:{payload}}}));"
                                ),
                                once=True,
                            )
                            ui.navigate.to(f'/view_event?title={quote(str(title.value))}&id={advert_id or ""}')
                        else:
                            ui.notify(f'Update failed: {response}', type='negative')
                            print(f"❌ Update failed: {response}")
                    except Exception as e:
                        ui.notify(f'Error: {e}', type='negative')
                        print(f"❌ Update error: {e}")
                    finally:
                        if btn:
                            btn.enable()
                            btn.props(remove='loading')
                ui.timer(0.05, load, once=True)
                # Populate the actions row defined above so buttons appear side by side
                with action_row:
                    def go_cancel():
                        ui.navigate.to(f'/view_event?title={quote(str(original_title))}')
                    ui.button('Cancel', on_click=go_cancel).classes('bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold')
                    save_button_ref['button'] = ui.button('Save Changes', on_click=save, icon='save').classes('bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold')
            
            # Add bottom spacing to push footer down
            with ui.element('div').classes('h-16'):
                pass

