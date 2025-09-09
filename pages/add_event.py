from nicegui import ui

def show_add_event_page():
    ui.label('Post an Advert').classes('text-2xl font-semibold my-4 container mx-auto px-4')

    with ui.element('div').classes('container mx-auto max-w-xl px-4 space-y-3'):
        title = ui.input('Title').classes('w-full')
        description = ui.textarea('Description').classes('w-full')
        price = ui.number('Price (GHS)').classes('w-full')
        category = ui.input('Category').classes('w-full')
        image_url = ui.input('Image URL (optional)').classes('w-full')

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

        async def submit():
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
                f'fetch("/api/adverts", {{method:"POST", headers:{{"Content-Type":"application/json"}}, body: JSON.stringify({payload})}}).then(r=>r.json())'
            )
            ui.notify('Advert created')
            ui.navigate.to('/')

        ui.button('Create Advert', on_click=submit).classes('w-full')
