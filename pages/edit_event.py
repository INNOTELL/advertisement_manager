from nicegui import ui

def show_edit_event_page():
    q = ui.context.client.request.query_params
    advert_id = q.get('id')
    if not advert_id:
        ui.label('Missing advert id').classes('text-red-600 container mx-auto px-4')
        return

    ui.label('Edit Advert').classes('text-2xl font-semibold my-4 container mx-auto px-4')

    with ui.element('div').classes('container mx-auto max-w-xl px-4 space-y-3'):
        title = ui.input('Title').classes('w-full')
        description = ui.textarea('Description').classes('w-full')
        price = ui.number('Price (GHS)').classes('w-full')
        category = ui.input('Category').classes('w-full')
        image_url = ui.input('Image URL (optional)').classes('w-full')

        async def load():
            data = await ui.run_javascript(f'fetch("/api/adverts/{advert_id}").then(r=>r.json())')
            title.value = data['title']
            description.value = data['description']
            price.value = data['price']
            category.value = data['category']
            image_url.value = data.get('image_url') or ''

        def validate() -> bool:
            if not title.value or not description.value or not category.value:
                ui.notify('Please fill in all required fields', color='red')
                return False
            try:
                if float(price.value) <= 0:
                    ui.notify('Price must be greater than 0', color='red')
                    return False
            except:
                ui.notify('Price must be a valid number', color='red')
                return False
            return True

        async def save():
            if not validate():
                return
            payload = {
                'title': title.value,
                'description': description.value,
                'price': float(price.value),
                'category': category.value,
                'image_url': image_url.value or None,
            }
            await ui.run_javascript(
                f'fetch("/api/adverts/{advert_id}", {{method:"PUT", headers:{{"Content-Type":"application/json"}}, body: JSON.stringify({payload})}}).then(r=>r.json())'
            )
            ui.notify('Advert updated')
            ui.navigate.to(f'/view_event?id={advert_id}')

        ui.timer(0.05, load, once=True)
        ui.button('Save Changes', on_click=save).classes('w-full')
