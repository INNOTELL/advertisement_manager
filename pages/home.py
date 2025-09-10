from nicegui import ui
import asyncio

def show_home_page():
    q_params = ui.context.client.request.query_params
    q = (q_params.get('q') or '').lower()
    cat = q_params.get('cat') or ''

    with ui.element('div').classes('container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 bg-blue-100 h-full w-full'):
        with ui.row().classes('items-end justify-between gap-4 py-4 text-white'):
            ui.label('All Adverts').classes('text-2xl font-semibold text-blue-700')
            with ui.row().classes('gap-3'):
                q_input = ui.input('Search title...').classes('w-48 sm:w-64 text-blue text-2xl')
                cat_select = ui.select(['All','Electronics','Furniture','Vehicles','Real Estate','Services'], value='All').props('outlined')
                if cat:
                    try:
                        cat_select.value = cat
                    except:
                        pass

                def apply_filters():
                    qv = q_input.value or ''
                    cv = '' if cat_select.value in (None, 'All') else cat_select.value
                    ui.navigate.to(f'/?q={qv}&cat={cv}')
                q_input.on('blur', apply_filters)
                cat_select.on('change', apply_filters)

        @ui.refreshable
        def grid():
            with ui.element('div').classes('py-2'):
                async def load():
                    return await ui.run_javascript('fetch("/api/adverts").then(r => r.json())')

                async def render():
                    items = await load()

                    def matches(ad):
                        ok_q = (q in ad['title'].lower()) if q else True
                        ok_cat = (ad['category'] == cat) if cat else True
                        return ok_q and ok_cat

                    items = [ad for ad in items if matches(ad)]

                    if not items:
                        with ui.card().classes('mx-auto max-w-3xl my-10 p-10 text-center'):
                            ui.label('No adverts yet').classes('text-xl text-blue-200 font-semibold')
                            ui.label('Post your first advert').classes('opacity-70')
                            ui.link('Add Advert', '/add_event').classes('underline mt-4')
                        return

                    with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6'):
                        for ad in items:
                            with ui.card().classes('rounded-2xl shadow hover:shadow-md transition p-0 overflow-hidden'):
                                if ad.get('image_url'):
                                    ui.image(ad['image_url']).classes('w-full h-48 object-cover')
                                with ui.element('div').classes('p-4 space-y-2'):
                                    ui.label(ad['title']).classes('font-semibold')
                                    ui.label(f"GHS {ad['price']:,.2f}").classes('text-md opacity-80')
                                    ui.label(ad['category']).classes('text-xs opacity-60')
                                    # Actions row: View, Edit, Delete as consistent buttons
                                    with ui.row().classes('gap-3 mt-2 flex-wrap items-center'):
                                        base_btn = 'px-3 py-1.5 rounded-md text-sm font-medium shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2'

                                        # View button (neutral)
                                        def on_view(ad_id=ad['id']):
                                            ui.navigate.to(f"/view_event?id={ad_id}")
                                        ui.button('View', on_click=on_view).classes(f"{base_btn} bg-gray-800 text-white hover:bg-gray-900 focus:ring-gray-400").props('title=View advert')

                                        # Edit button (primary)
                                        def on_edit(ad_id=ad['id']):
                                            ui.navigate.to(f"/edit_event?id={ad_id}")
                                        ui.button('Edit', on_click=on_edit).classes(f"{base_btn} bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-400").props('title=Edit advert')

                                        # Delete button (danger)
                                        def on_delete(ad_id=ad['id']):
                                            ui.run(delete_ad(ad_id))
                                        ui.button('Delete', on_click=on_delete).classes(f"{base_btn} bg-red-600 text-white hover:bg-red-700 focus:ring-red-400").props('title=Delete advert')

                ui.timer(0.05, render, once=True)

            async def delete_ad(ad_id: str):
                await ui.run_javascript(f'fetch("/api/adverts/{ad_id}", {{method:"DELETE"}})')
                ui.notify('Deleted')
                grid.refresh()

        grid()
