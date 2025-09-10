from nicegui import ui


def show_header():
    # Header bar with subtle blur and sticky positioning
    with ui.element('div').classes('w-full bg-gray-100 backdrop-blur sticky top-0 z-50 shadow-sm'):
        with ui.row().classes('container mx-auto px-4 py-3 flex items-center justify-between'):
            ui.link('Adverts', '/').classes('text-xl font-semibold no-underline text-blue-600')
            with ui.row().classes('gap-3'):
                # Outline-style button
                ui.link('Home', '/').classes(
                    'text-sm px-3 py-1.5 rounded-md border border-blue-600 '
                    'text-blue-600 hover:bg-blue-50 no-underline'
                )
                # Filled primary button
                ui.link('Add Advert', '/add_event').classes(
                    'text-sm px-3 py-1.5 rounded-md bg-blue-600 text-white '
                    'hover:bg-blue-700 no-underline'
                )
