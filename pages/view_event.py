from nicegui import ui
import requests
from urllib.parse import quote
from utils.api import base_url

def show_view_event_page():
    q = ui.context.client.request.query_params
    title = q.get('title')
    if not title:
        with ui.element('div').classes('container mx-auto px-4'):
            ui.element('div').classes('alert-dark rounded-md p-3').slot('')
            ui.label('Missing advert title')
        return

    async def load():
        encoded = quote(str(title))
        response = requests.get(f"{base_url}/advert_details/{encoded}")
        json_data = response.json()
        items = json_data.get("data", [])
        if not items:
            with ui.element('div').classes('container mx-auto px-4'):
                with ui.element('div').classes('alert-dark rounded-md p-3'):
                    ui.label('Advert not found')
            return
        data = items[0]
        with ui.element('div').classes('container mx-auto my-8 px-4 section min-h-screen rounded-2xl p-4'):
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 gap-6 items-start'):
                # Left column: image
                with ui.card().classes('card p-0 overflow-hidden'):
                    if data.get('image'):
                        ui.image(data['image']).classes('w-full').style('display:block; width:100%; height:auto; max-height:80vh; object-fit:contain;')
                # Right column: details
                with ui.card().classes('card p-6 space-y-4'):
                    ui.label(data['title']).classes('text-3xl font-semibold')
                    ui.label(f"GHS {data['price']:,.2f}").classes('text-lg opacity-80')
                    ui.label(data['category']).classes('text-sm opacity-60')
                    ui.label(data['description']).classes('pt-2 text-base').style('white-space: pre-line;')
                    with ui.row().classes('pt-4 gap-3'):
                        def go_edit():
                            ui.navigate.to(f'/edit_event?title={quote(str(data.get("title","")))}')
                        def go_back():
                            ui.navigate.to('/')
                        ui.button('Edit', on_click=go_edit).classes('btn-primary')
                        ui.button('Back to list', on_click=go_back).classes('btn-secondary')
                # Remove duplicated bottom buttons; actions live in right column only

    ui.timer(0.05, load, once=True)
