from nicegui import ui
import asyncio
import requests
import json
import time
from urllib.parse import quote
from utils.api import base_url


def show_home_page():
    # Data is fetched inside the grid renderer to ensure freshness
    deleted_titles = set()

    q_params = ui.context.client.request.query_params
    q = (q_params.get('q') or '').lower()
    cat = q_params.get('cat') or ''

    # Full screen background wrapper (surface)
    with ui.element("div").classes("container mx-auto w-full px-4 sm:px-6 ig:px-8 bg-[url('https://img.freepik.com/free-photo/black-friday-sales-sign-neon-light_23-2151833076.jpg?semt=ais_hybrid&w=740&q=80')] bg-cover bg-center h-screen w-full text-center flex justify-center items-center").style('font-family: "Libre_Baskerville" , Serif;'):
        with ui.element('div').classes('container mx-auto max-w-7xl h-full w-full'):
            # Hero section (alternating palette via .section)
            with ui.element('div').classes('section min-h-screen rounded-xl p-6 mb-6'):
                with ui.element('div').classes('grid md:grid-cols-2 gap-6 items-center'):
                    with ui.element('div').classes('space-y-3'):
                        ui.label('Welcome to Comfy_Hub!').classes('text-2xl md:text-4xl text-blue-100 font-bold')
                        ui.label('Find, Post, Sell.').classes('text-blue-100 text-4xl font-bold')
                        
                        ui.label('At Comfy_hub, we make advertising simple, smart, and seamless.').classes('text-blue-100 text-4xl font-bold')
                        # with ui.row().classes('gap-3'):
                        #     ui.link('Browse Adverts', '/#adverts_list').classes('btn-secondary no-underline')

                            # def go_add():
                            #     ui.navigate.to('/add_event')
                            # ui.button('Post an Advert', on_click=go_add).classes('btn-primary')

                    # ui.image('https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1600&auto=format&fit=crop').classes('w-full h-64 md:h-80 object-cover rounded-xl shadow-lg')

            # Filters section
            with ui.element('div').classes('section rounded-2xl p-4 mb-4 bg-blue-200'):
                with ui.row().classes('items-end justify-between gap-4'):
                    ui.label('All Adverts').classes('text-2xl font-semibold text-blue-600')
                    with ui.row().classes('gap-3'):
                        q_input = ui.input('Search title...').classes('input w-48 sm:w-64 text-blue-100')
                        cat_select = ui.select(['All', 'Electronics', 'Furniture', 'Vehicles', 'Real Estate', 'Services'], value='All').classes('input').props('outlined')
                        if cat:
                            try:
                                cat_select.value = cat
                            except Exception:
                                pass

                        def apply_filters():
                            qv = q_input.value or ''
                            cv = '' if cat_select.value in (None, 'All') else cat_select.value
                            ui.navigate.to(f'/?q={qv}&cat={cv}')

                        q_input.on('blur', apply_filters)
                        cat_select.on('change', apply_filters)

            @ui.refreshable
            def grid():
                with ui.element('div').classes('section rounded-2xl p-4 bg-blue-300').props('id=adverts_list'):

                    async def render():
                        try:
                            # Bypass any intermediate caching using a timestamp param
                            resp = await asyncio.to_thread(requests.get, f"{base_url}/adverts", params={"_ts": time.time()})
                            js = resp.json()
                            items = js.get("data", [])
                        except Exception as e:
                            ui.notify(f"Failed to load adverts: {e}")
                            items = []

                        # Optimistically exclude items deleted this session
                        if deleted_titles:
                            items = [ad for ad in items if ad.get('title') not in deleted_titles]

                        def matches(ad):
                            ok_q = (q in ad['title'].lower()) if q else True
                            ok_cat = (ad['category'] == cat) if cat else True
                            return ok_q and ok_cat

                        items = [ad for ad in items if matches(ad)]

                        if not items:
                            with ui.element('div').classes('card mx-auto max-w-3xl my-10 p-10 text-center'):
                                ui.label('No adverts yet').classes('text-xl font-semibold')
                                ui.label('Post your first advert').classes('opacity-80')
                                ui.link('Add Advert', '/add_event').classes('link mt-4')
                            return

                        with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6'):
                            for ad in items:
                                card = ui.card().classes('card hover:shadow-md transition p-0 overflow-hidden')
                                with card:
                                    if ad.get('image'):
                                        ui.image(ad['image']).classes('w-full h-50 object-cover')
                                    with ui.element('div').classes('p-4 space-y-2'):
                                        ui.label(ad['title']).classes('font-semibold')
                                        ui.label(f"GHS {ad['price']:,.2f}").classes('text-md opacity-80')
                                        ui.label(ad['category']).classes('text-xs opacity-60')
                                        with ui.row().classes('gap-3 mt-2 flex-wrap items-center'):

                                            def on_view(e, title=ad['title']):
                                                ui.navigate.to(f"/view_event?title={quote(str(title))}")
                                            ui.button('View', on_click=on_view).classes('btn-secondary').props('title=View advert')

                                            def on_edit(e, title=ad['title']):
                                                ui.navigate.to(f"/edit_event?title={quote(str(title))}")
                                            ui.button('Edit', on_click=on_edit).classes('btn-secondary').props('title=Edit advert')

                                            btn_delete = ui.button('Delete').classes('btn-primary').props('title=Delete advert')

                                            async def on_delete(e, title=ad['title'], btn=btn_delete, ad_card=card):
                                                # Visual feedback: disable button while deleting
                                                btn.classes('opacity-50 pointer-events-none')
                                                ok = await delete_ad(title)
                                                if ok:
                                                    # Hide the card immediately
                                                    ad_card.classes('hidden')
                                                else:
                                                    # Re-enable on failure
                                                    btn.classes(remove='opacity-50 pointer-events-none')
                                            btn_delete.on('click', on_delete)

                    ui.timer(0.05, render, once=True)

                async def delete_ad(title: str) -> bool:
                    try:
                        safe_title = (title or "").strip()
                        encoded = quote(str(safe_title))
                        # Run blocking HTTP call off the event loop
                        r = await asyncio.to_thread(requests.delete, f"{base_url}/adverts/{encoded}")
                        if r.status_code >= 400:
                            ui.notify(f"Delete failed: {r.status_code}: {r.text}")
                            return False
                        else:
                            # API returns a plain JSON string like "Advert successfully deleted!"
                            try:
                                body = r.json()
                                msg = body if isinstance(body, str) else 'Deleted'
                            except Exception:
                                # Fallback to raw text
                                msg = (r.text or 'Deleted').strip().strip('"')
                            ui.notify(msg or 'Deleted')
                            # Optimistically remove from current view
                            deleted_titles.add(safe_title)
                            grid.refresh()
                            return True
                    except Exception as e:
                        ui.notify(f"Error: {e}")
                        return False

            grid()
