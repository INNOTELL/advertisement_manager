from nicegui import ui
import requests
from urllib.parse import quote
from utils.api import base_url


def show_edit_event_page():
    q = ui.context.client.request.query_params
    original_title = q.get('title')
    if not original_title:
        with ui.element('div').classes('container mx-auto px-4'):
            with ui.element('div').classes('alert-dark'):
                ui.label('Missing advert title')
        return

    ui.label('Edit Advert').classes('text-2xl font-semibold my-4 container mx-auto px-4')

    with ui.element('div').classes('container mx-auto max-w-4xl px-4 bg-gray-100 min-h-screen rounded-2xl p-4'):
        with ui.element('div').classes('card p-6'):
            # Two-column responsive form
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-4'):
                # Left column
                with ui.element('div').classes('space-y-3'):
                    title = ui.input('Title').classes('input w-full')
                    price = ui.number('Price (GHS)').classes('input w-full')
                    categories = [
                        'Electronics', 'Fashion', 'Furniture', 'Vehicles',
                        'Real Estate', 'Services', 'Appliances', 'Other',
                    ]
                    category_select = ui.select(categories, label='Category').classes('input w-full').props('outlined')

                # Right column
                with ui.element('div').classes('space-y-3'):
                    description = ui.textarea('Description').classes('input w-full h-48')

                    image_content = None

                    def handle_image_upload(e):
                        nonlocal image_content
                        image_content = e.content.read()

                    ui.upload(on_upload=handle_image_upload).props('flat bordered').classes('w-full').style('border:2px dashed var(--color-accent); padding:20px; background:var(--color-charcoal); color:var(--color-accent); border-radius:12px;')

            # Actions container (populated after save() is defined)
            action_row = ui.row().classes('mt-4 gap-3 justify-end')

        async def load():
            try:
                encoded = quote(str(original_title))
                resp = requests.get(f"{base_url}/advert_details/{encoded}")
                js = resp.json()
                items = js.get('data', [])
                if not items:
                    ui.notify('Advert not found')
                    return
                data = items[0]
                title.value = data['title']
                description.value = data['description']
                price.value = data['price']
                category_select.value = data['category']
            except Exception as e:
                ui.notify(f'Error loading advert: {e}')

        def validate() -> bool:
            if not title.value or not description.value or not category_select.value:
                ui.notify('Please fill in all required fields')
                return False
            try:
                if float(price.value) <= 0:
                    ui.notify('Price must be greater than 0')
                    return False
            except Exception:
                ui.notify('Price must be a valid number')
                return False
            return True

        async def save():
            if not validate():
                return
            if image_content is None:
                ui.notify('Please upload an image')
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
                    ui.notify(f'Update failed: {r.text}')
                    return
                ui.notify('Advert updated')
                ui.navigate.to(f'/view_event?title={quote(str(title.value))}')
            except Exception as e:
                ui.notify(f'Error: {e}')

        ui.timer(0.05, load, once=True)
        # Populate the actions row defined above so buttons appear side by side
        with action_row:
            def go_cancel():
                ui.navigate.to(f'/view_event?title={quote(str(original_title))}')
            ui.button('Cancel', on_click=go_cancel).classes('btn-secondary')
            ui.button('Save Changes', on_click=save).classes('btn-primary')

