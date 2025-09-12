from nicegui import ui


def show_header():
    # Header bar with subtle blur and sticky positioning
   with ui.element('div').classes('w-full bg-transparent text-white backdrop-blur sticky top-0 z-50 shadow-2xl shadow-blue-400').style('font-family: "Libre Baskerville", serif;'):
        with ui.row().classes('container mx-auto px-4 py-3 flex items-center justify-between'):
            with ui.row():
                ui.image("https://static.vecteezy.com/system/resources/previews/008/515/119/non_2x/online-shop-logo-happy-shop-logo-design-vector.jpg").classes("w-8 rounded-full")
                ui.link('Comfy_Hub', '/').classes('text-lg font-semibold no-underline text-blue-400 text-center')
            with ui.row().classes('gap-3'):
                # Outline-style button
                ui.link('Home', '/').classes(
                    'text-sm px-3 py-1.5 rounded-md border border-blue-600 '
                    'text-blue-400 hover:bg-yellow-50 no-underline')
                # ui.link('Home', '/').classes(
                #   'text-sm px-3 py-1.5 rounded-md border border-blue-600 '
                #   'text-blue-600 hover:bg-blue-50 no-underline'
                
                # Filled primary button
                ui.link('Add Advert', '/add_event').classes(
                    'text-sm px-3 py-1.5 rounded-md bg-blue-600 text-white '
                    'hover:bg-blue-700 no-underline')
 


    # with ui.element('div').classes('w-full bg-blue-100 backdrop-blur sticky top-0 z-50 shadow-sm bg-white/40'):
    #     with ui.row().classes('container mx-auto px-4 py-3 flex items-center justify-between'):
    #         ui.link('Adverts', '/').classes('text-xl font-semibold no-underline text-blue-600')
    #         with ui.row().classes('gap-3'):
    #             # Outline-style button



# def show_header():
#     # Header bar with semantic colors
#     with ui.element('div').classes('w-full sticky top-0 z-50 shadow-sm').style('background:#081107; color:#2CDD0D;'):
#         with ui.row().classes('container mx-auto px-4 py-3 flex items-center justify-between'):
#             # Brand: simple logo + name linking home
#             with ui.row().classes('items-center gap-2'):
#                 ui.icon('shopping_cart')
#                 ui.link('COMFY', '/').classes('text-xl font-semibold no-underline link')
#             with ui.row().classes('gap-3'):
#                 ui.button('Home', on_click=lambda: ui.navigate.to('/')).classes('btn-primary')
#                 ui.button('Add Advert', on_click=lambda: ui.navigate.to('/add_event')).classes('btn-primary')
