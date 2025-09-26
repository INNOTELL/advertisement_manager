from nicegui import ui

# Backend API base URL
from utils.api_client import api_client
from config import CATEGORIES, LOCATIONS


def show_add_event_page():
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto max-w-4xl px-4'):
            # Page Header
            with ui.element('div').classes('mb-8 text-center'):
                with ui.element('div').classes('flex items-center justify-center gap-3 mb-4'):
                    ui.icon('add_circle').classes('text-orange-500 text-4xl')
                    ui.label('Post Your Advert').classes('text-3xl font-bold text-gray-800')
                ui.label('Reach thousands of potential buyers across Ghana').classes('text-gray-600 text-lg')
                ui.label('Create an engaging advert and start selling today!').classes('text-orange-500 font-medium mt-2')

            # Main Form Card
            with ui.card().classes('bg-gray-50 shadow-lg rounded-xl p-8'):
                image_content = None

                def handle_image_upload(e):
                    nonlocal image_content
                    image_content = e.content.read()
                    ui.notify('Image uploaded successfully!', type='positive')
                    
                    # Show image preview
                    if image_content:
                        # Create a preview of the uploaded image
                        import base64
                        image_base64 = base64.b64encode(image_content).decode('utf-8')
                        image_preview.clear()
                        with image_preview:
                            with ui.card().classes('p-4 bg-white border border-gray-200 rounded-lg'):
                                ui.label('Image Preview').classes('text-sm font-semibold text-gray-700 mb-2')
                                ui.image(f'data:image/jpeg;base64,{image_base64}').classes('w-full h-48 object-cover rounded-lg')
                                ui.label('Image ready for upload').classes('text-xs text-green-600 mt-2')

                # Image Upload Section - At the Top
                with ui.element('div').classes('mb-8'):
                    ui.label('Advert Image').classes('text-xl font-semibold text-gray-800 mb-4')
                    
                    # Image Preview Area
                    image_preview = ui.element('div').classes('mb-4')
                    
                    # Image Upload Area
                    with ui.element('div').classes('border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-orange-500 transition-colors bg-white'):
                        ui.icon('cloud_upload').classes('text-4xl text-gray-400 mb-4')
                        ui.label('Upload Advert Image *').classes('text-lg font-medium text-gray-700 mb-2')
                        ui.label('Drag and drop or click to browse').classes('text-sm text-gray-500 mb-4')
                        ui.upload(on_upload=handle_image_upload).props('flat bordered').classes('w-full')
                        ui.label('Supported formats: JPG, PNG, GIF (Max 5MB)').classes('text-xs text-gray-400 mt-2')
                        ui.label('Image is required to create an advert').classes('text-xs text-red-500 mt-2 font-medium')
                    
                    # Image Upload Tips
                    with ui.card().classes('p-4 bg-blue-50 border border-blue-200 mt-4'):
                        ui.label('Image Tips').classes('text-sm font-semibold text-blue-800 mb-2')
                        with ui.element('div').classes('text-xs text-blue-700 space-y-1'):
                            ui.label('• Use high-quality images (at least 800x800px)')
                            ui.label('• Show the product from multiple angles')
                            ui.label('• Use good lighting and clear backgrounds')
                            ui.label('• Images help increase sales by up to 30%')

                # Two-column responsive form
                with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8'):
                    # Left column - Basic Info
                    with ui.element('div').classes('space-y-6'):
                        ui.label('Advert Information').classes('text-xl font-semibold text-gray-800 mb-4')
                        
                        title = ui.input('Advert Title *').classes('w-full').props('outlined')
                        title.props('placeholder=Enter a clear, descriptive title for your advert')
                        
                        price = ui.number('Price (GHS) *').classes('w-full').props('outlined')
                        price.props('placeholder=0.00')
                        
                        category_select = ui.select(CATEGORIES, value=None, label='Category *').classes('w-full').props('outlined')
                        
                        location_select = ui.select(LOCATIONS, value=LOCATIONS[0], label='Location *').classes('w-full').props('outlined')
                        
                        description = ui.textarea('Advert Description *').classes('w-full').props('outlined rows=6')
                        description.props('placeholder=Describe your product or service in detail...')

                    # Right column - Additional Details
                    with ui.element('div').classes('space-y-6'):
                        ui.label('Additional Details').classes('text-xl font-semibold text-gray-800 mb-4')
                        
                        # Contact Information
                        contact_name = ui.input('Contact Name').classes('w-full').props('outlined')
                        contact_name.props('placeholder=Your name for contact')
                        
                        contact_phone = ui.input('Contact Phone').classes('w-full').props('outlined')
                        contact_phone.props('placeholder=+233 XX XXX XXXX')
                        
                        # Additional Options
                        with ui.card().classes('p-4 bg-green-50 border border-green-200'):
                            ui.label('Selling Tips').classes('text-sm font-semibold text-green-800 mb-2')
                            with ui.element('div').classes('text-xs text-green-700 space-y-1'):
                                ui.label('• Be honest about the condition of your item')
                                ui.label('• Respond to inquiries quickly')
                                ui.label('• Set a competitive price')
                                ui.label('• Include all relevant details')

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

                # Actions row
                with ui.row().classes('mt-8 gap-4 justify-end'):
                    def go_cancel():
                        ui.navigate.to('/dashboard')
                    ui.button('Cancel', on_click=go_cancel).classes('bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold')

                    post_button_ref = {}
                    async def create():
                        nonlocal image_content
                        btn = post_button_ref.get('button')
                        if btn:
                            btn.disable()
                            btn.props('loading')
                        try:
                            if not title.value or not description.value or not category_select.value or not location_select.value:
                                ui.notify('Please fill in all required fields', type='negative')
                                return

                            if image_content is None:
                                ui.notify('Please upload an image - it is required to create an advert', type='negative')
                                return

                            try:
                                if float(price.value) <= 0:
                                    ui.notify('Price must be greater than 0', type='negative')
                                    return
                            except Exception:
                                ui.notify('Price must be a valid number', type='negative')
                                return

                            if not api_client._discovered:
                                await api_client.discover_endpoints()

                            ad_data = {
                                'title': title.value,
                                'description': description.value,
                                'price': float(price.value),
                                'category': category_select.value,
                                'location': location_select.value
                            }

                            if contact_name.value:
                                ad_data['contact_name'] = contact_name.value
                            if contact_phone.value:
                                ad_data['contact_phone'] = contact_phone.value
                            if image_content:
                                ad_data['image'] = image_content

                            print(f"Creating advert with data: {ad_data}")
                            success, response = await api_client.create_ad(ad_data)

                            if success:
                                ui.notify('Advert posted successfully!', type='positive')
                                ui.notify('Your advert is now live and visible to buyers across Ghana!', type='info')

                                title.value = ''
                                description.value = ''
                                price.value = ''
                                category_select.value = None
                                location_select.value = LOCATIONS[0]
                                contact_name.value = ''
                                contact_phone.value = ''
                                image_content = None
                                image_preview.clear()

                                ui.timer(1.0, lambda: ui.navigate.to('/'), once=True)
                                ui.timer(0.2, lambda: ui.run_javascript("window.dispatchEvent(new CustomEvent('adverts:changed',{detail:{type:'created'}}));"), once=True)
                            else:
                                ui.notify(f'Failed to create advert: {response}', type='negative')
                                print(f"Create advert failed: {response}")
                        except Exception as e:
                            ui.notify(f'Error creating advert: {str(e)}', type='negative')
                            print(f"Create advert error: {e}")
                        finally:
                            if btn:
                                btn.enable()
                                btn.props(remove='loading')
                    post_button_ref['button'] = ui.button('Post Advert', on_click=create, icon='publish').classes('bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold text-lg')


