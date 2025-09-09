from nicegui import ui

def show_view_event_page():
    q = ui.context.client.request.query_params
    advert_id = q.get('id')
    if not advert_id:
        ui.label('Missing advert id').classes('text-red-600 container mx-auto px-4')
        return

    async def load():
        data = await ui.run_javascript(f'fetch("/api/adverts/{advert_id}").then(r=>r.json())')
        with ui.card().classes('max-w-2xl mx-auto overflow-hidden my-6'):
            if data.get('image_url'):
                ui.image(data['image_url']).classes('w-full h-64 object-cover')
            with ui.element('div').classes('p-4 space-y-2'):
                ui.label(data['title']).classes('text-2xl font-semibold')
                ui.label(f"GHS {data['price']:,.2f}").classes('opacity-80')
                ui.label(data['category']).classes('text-sm opacity-60')
                ui.label(data['description']).classes('pt-2')
                with ui.row().classes('pt-3 gap-3'):
                    ui.link('Edit', f'/edit_event?id={advert_id}').classes('underline')
                    ui.link('Back to list', '/').classes('underline')

    ui.timer(0.05, load, once=True)
