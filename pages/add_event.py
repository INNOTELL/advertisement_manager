from nicegui import ui
import requests
from urllib.parse import quote
from utils.api import base_url


def show_add_event_page():
    ui.label('Post an Advert').classes('text-2xl font-semibold my-4 container mx-auto px-4')

    image_content = None

    def handle_image_upload(e):
        nonlocal image_content
        image_content = e.content.read()

    with ui.element('div').classes('container mx-auto max-w-4xl px-4 bg-primary min-h-screen rounded-2xl p-6'):
        with ui.element('div').classes('card card-charcoal p-6'):
            # Two-column responsive form matching Edit layout
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
                    ui.upload(on_upload=handle_image_upload).props('flat bordered').classes('w-full').style('border:2px dashed var(--color-accent); padding:20px; background:var(--color-charcoal); color:var(--color-accent); border-radius:12px;')

            # Actions row
            with ui.row().classes('mt-4 gap-3 justify-end'):
                def go_cancel():
                    ui.navigate.to('/')
                ui.button('Cancel', on_click=go_cancel).classes('btn-secondary')

                async def create():
                    # Validation similar to Edit
                    if not title.value or not description.value or not category_select.value:
                        ui.notify('Please fill in all required fields')
                        return
                    try:
                        if float(price.value) <= 0:
                            ui.notify('Price must be greater than 0')
                            return
                    except Exception:
                        ui.notify('Price must be a valid number')
                        return
                    if image_content is None:
                        ui.notify('Please upload an image')
                        return

                    data_form = {
                        'title': title.value,
                        'description': description.value,
                        'price': float(price.value),
                        'category': category_select.value,
                    }
                    files = {
                        'image': ('image', image_content, 'application/octet-stream'),
                    }
                    try:
                        r = requests.post(f"{base_url}/advert", data=data_form, files=files)
                        if r.status_code >= 400:
                            ui.notify(f'Create failed: {r.text}')
                            return
                        ui.notify('Advert created')
                        ui.navigate.to(f"/view_event?title={quote(str(title.value))}")
                    except Exception as e:
                        ui.notify(f'Error: {e}')

                ui.button('Create Advert', on_click=create).classes('btn-primary')


