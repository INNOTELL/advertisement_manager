from nicegui import ui, events
import requests
from utils.api import base_url

def create_advert(data):
    response = requests.post(f"{base_url}/advert", data)
    print(response.json())
    

def show_add_event_page():

    image_content = None

    def handle_image_upload(e):
        nonlocal image_content
        image_content = e.content.read()

    ui.label('Post an Advert').classes('text-2xl font-semibold my-4 container mx-auto px-4')

    with ui.element('div').classes('container mx-auto max-w-xl px-4 space-y-3'):
        title = ui.input('Title').classes('w-full')
        description = ui.textarea('Description').classes('w-full')
        price = ui.number('Price (GHS)').classes('w-full')
        category = ui.input('Category').classes('w-full')
        image = ui.upload(on_upload=handle_image_upload).props('flat bordered').classes('w-full').style('border:2px dashed #ccc; padding:20px;')

        ui.button('Create Advert', on_click=lambda:create_advert({
            "title": title.value, 
            "description": description.value,
            "price": price.value,
            "category": category.value,
            "image": image_content
        })).classes('w-full')
