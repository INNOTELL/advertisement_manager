from nicegui import ui

def show_header():
    with ui.element('div').classes('w-full bg-white/80 backdrop-blur sticky top-0 z-50 shadow-sm'):
        with ui.row().classes('container mx-auto px-4 py-3 flex items-center justify-between'):
            ui.link('Adverts', '/').classes('text-xl font-semibold')
            with ui.row().classes('gap-4'):
                ui.link('Home', '/').classes('text-sm hover:underline')
                ui.link('Add Advert', '/add_event').classes('text-sm hover:underline')
