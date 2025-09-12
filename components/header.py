from nicegui import ui


def show_header():
    # Header bar with semantic colors
    with ui.element('div').classes('w-full sticky top-0 z-50 shadow-sm').style('background:#081107; color:#2CDD0D;'):
        with ui.row().classes('container mx-auto px-4 py-3 flex items-center justify-between'):
            # Brand: simple logo + name linking home
            with ui.row().classes('items-center gap-2'):
                ui.icon('shopping_cart')
                ui.link('COMFY', '/').classes('text-xl font-semibold no-underline link')
            with ui.row().classes('gap-3'):
                ui.button('Home', on_click=lambda: ui.navigate.to('/')).classes('btn-primary')
                ui.button('Add Advert', on_click=lambda: ui.navigate.to('/add_event')).classes('btn-primary')
