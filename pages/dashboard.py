import json
import asyncio

from nicegui import ui
from utils.api_client import api_client

def show_dashboard_page(auth_state=None):
    if not auth_state or not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    
    ui.run_javascript("""
        if (!window.__advertsChangedBridge) {
            window.__advertsChangedBridge = true;
            window.addEventListener('adverts:changed', (event) => {
                const detail = event.detail || {};
                if (window.nicegui && window.nicegui.emit) {
                    window.nicegui.emit('adverts_changed', detail);
                }
            });
        }
    """)

    adverts_state = {'items': []}

    def resolve_advert_id(advert: dict) -> str:
        if not isinstance(advert, dict):
            return ''
        for key in ('id', 'advert_id', '_id'):
            value = advert.get(key)
            if value:
                return str(value)
        fallback = advert.get('title') if isinstance(advert, dict) else ''
        return str(fallback or '')

    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-7xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('Dashboard').classes('text-3xl font-bold text-gray-800')
                ui.label('Manage your adverts and track performance').classes('text-gray-600 mt-2')
            
            # Quick Stats
            @ui.refreshable
            def dashboard_stats():
                items = adverts_state.get('items') or []
                total = len(items)

                prices = []
                for advert in items:
                    price_value = advert.get('price')
                    try:
                        prices.append(float(price_value))
                    except (TypeError, ValueError):
                        continue

                avg_price = sum(prices) / len(prices) if prices else 0
                highest = max(prices) if prices else None
                lowest = min(prices) if prices else None

                metrics = [
                    {'title': 'Total Listings', 'value': str(total), 'icon': 'inventory', 'color': 'bg-blue-500'},
                    {'title': 'Average Price', 'value': f"GHS {avg_price:,.2f}" if prices else 'GHS 0.00', 'icon': 'attach_money', 'color': 'bg-green-500'},
                    {'title': 'Highest Price', 'value': f"GHS {highest:,.2f}" if highest is not None else 'N/A', 'icon': 'trending_up', 'color': 'bg-purple-500'},
                    {'title': 'Lowest Price', 'value': f"GHS {lowest:,.2f}" if lowest is not None else 'N/A', 'icon': 'trending_down', 'color': 'bg-orange-500'},
                ]

                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-4 gap-6 mb-8'):
                    for metric in metrics:
                        with ui.card().classes('p-6 bg-gray-50 shadow-sm hover:shadow-md transition-shadow'):
                            with ui.element('div').classes('flex items-center justify-between mb-4'):
                                ui.icon(metric['icon']).classes(f"text-white text-2xl {metric['color']} rounded-full p-3")
                                ui.label(metric['value']).classes('text-lg font-semibold text-gray-700')
                            ui.label(metric['title']).classes('text-sm text-gray-600')

            dashboard_stats()

            # Main Dashboard Content
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-3 gap-8'):
                # Left Column - Products Management
                with ui.element('div').classes('lg:col-span-2 space-y-8'):
                    # Recent Products
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        with ui.element('div').classes('flex items-center justify-between mb-6'):
                            ui.label('Recent Products').classes('text-xl font-bold text-gray-800')
                            ui.button('VIEW ALL', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded font-medium')

                        @ui.refreshable
                        def recent_products():
                            items = adverts_state.get('items') or []
                            if not items:
                                with ui.element('div').classes('text-center py-8 text-gray-500'):
                                    ui.icon('inventory').classes('text-4xl text-gray-300 mb-2')
                                    ui.label('No adverts available yet.').classes('text-sm text-gray-500')
                                return

                            def to_float(value):
                                try:
                                    return float(value)
                                except (TypeError, ValueError):
                                    return None

                            for advert in items[:5]:
                                advert_id = resolve_advert_id(advert)
                                title = advert.get('title') or advert.get('name') or 'Advert'
                                price_value = to_float(advert.get('price'))
                                price_text = f"GHS {price_value:,.2f}" if price_value is not None else 'Price not set'
                                category = advert.get('category') or 'Uncategorized'
                                location = advert.get('location') or advert.get('region') or 'Unknown location'

                                def open_details():
                                    ui.navigate.to(f"/view_event?title={advert.get('title', '')}&id={resolve_advert_id(advert)}")

                                with ui.element('div').classes('flex items-center gap-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer').on('click', open_details):
                                    image_data = advert.get('image') or advert.get('image_url')
                                    with ui.element('div'):
                                        if image_data and isinstance(image_data, str):
                                            if image_data.startswith('http'):
                                                ui.image(image_data).classes('w-16 h-16 object-cover rounded-lg')
                                            elif len(image_data) > 50:
                                                ui.image(f"data:image/jpeg;base64,{image_data}").classes('w-16 h-16 object-cover rounded-lg')
                                            else:
                                                ui.icon('image').classes('text-4xl text-gray-400')
                                        else:
                                            ui.icon('image').classes('text-4xl text-gray-400')
                                    with ui.element('div').classes('flex-1'):
                                        ui.label(title).classes('font-semibold text-gray-800')
                                        ui.label(price_text).classes('text-primary font-medium')
                                        ui.label(f"{category} - {location}").classes('text-xs text-gray-500 mt-1')
                                    with ui.element('div').classes('flex flex-col items-end gap-2'):
                                        def handle_edit_click():
                                            ui.navigate.to(f"/edit_event?title={advert.get('title', '')}&id={resolve_advert_id(advert)}")
                                        
                                        def handle_delete_click():
                                            delete_advert(resolve_advert_id(advert), advert.get('title', 'Advert'))
                                        
                                        ui.button('Edit', on_click=handle_edit_click).classes('bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-xs')
                                        ui.button('Delete', on_click=handle_delete_click).classes('bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-xs')

                        recent_products()

                    # Recent Orders
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        with ui.element('div').classes('flex items-center justify-between mb-6'):
                            ui.label('Recent Orders').classes('text-xl font-bold text-gray-800')
                        with ui.element('div').classes('text-center py-8 text-gray-500'):
                            ui.icon('local_shipping').classes('text-4xl text-gray-300 mb-2')
                            ui.label('Orders will appear here once the orders API is connected.').classes('text-sm text-gray-500')

                # Right Column - Analytics & Actions
                with ui.element('div').classes('space-y-8'):
                    # Sales Analytics
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        ui.label('Sales Analytics').classes('text-xl font-bold text-gray-800 mb-6')
                        with ui.element('div').classes('text-center py-8 text-gray-500'):
                            ui.icon('insights').classes('text-4xl text-gray-300 mb-2')
                            ui.label('Analytics will appear once reporting data is available from the backend.').classes('text-sm text-gray-500')

                    # Quick Actions
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        ui.label('Quick Actions').classes('text-xl font-bold text-gray-800 mb-6')
                        with ui.element('div').classes('space-y-4'):
                            ui.button('Add New Product', on_click=lambda: ui.navigate.to('/add_event')).classes('w-full bg-primary hover:bg-orange-600 text-white py-3 rounded-lg font-semibold')
                            ui.button('View All Products', on_click=lambda: ui.navigate.to('/dashboard')).classes('w-full bg-blue-500 hover:bg-blue-600 text-white py-3 rounded-lg font-semibold')
                            ui.button('Analytics', on_click=lambda: ui.navigate.to('/analytics')).classes('w-full bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg font-semibold')

                    # Performance Metrics
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        ui.label('Performance Metrics').classes('text-xl font-bold text-gray-800 mb-6')
                        with ui.element('div').classes('text-center py-8 text-gray-500'):
                            ui.icon('leaderboard').classes('text-4xl text-gray-300 mb-2')
                            ui.label('Performance insights will show here when analytics endpoints are available.').classes('text-sm text-gray-500')

            # My Adverts Section (Enhanced)
            with ui.card().classes('mt-8 p-6 bg-gray-50 shadow-sm'):
                with ui.element('div').classes('flex items-center justify-between mb-6'):
                    ui.label('My Adverts').classes('text-2xl font-bold text-gray-800')
                    with ui.row().classes('gap-4 items-center'):
                        category_filter = ui.select(['All Categories', 'Electronics', 'Fashion', 'Furniture', 'Vehicles', 'Real Estate', 'Services'], value='All Categories').props('outlined')
                        ui.button('Add New', on_click=lambda: ui.navigate.to('/add_event')).classes('bg-primary hover:bg-orange-600 text-white px-4 py-2 rounded-lg')
                
                table_state = {'lookup': {}}

                @ui.refreshable
                def adverts_table():
                    async def load_adverts():
                        try:
                            if not api_client._discovered:
                                await api_client.discover_endpoints()

                            success, response = await api_client.get_ads()

                            if not success:
                                ui.notify('Failed to load adverts', type='negative')
                                return

                            if isinstance(response, dict):
                                adverts = response.get("data", response.get("adverts", response.get("items", [])))
                            elif isinstance(response, list):
                                adverts = response
                            else:
                                adverts = []

                            user_adverts = adverts
                            adverts_state['items'] = user_adverts
                            dashboard_stats.refresh()
                            recent_products.refresh()

                            table_state['lookup'] = {resolve_advert_id(ad): ad for ad in user_adverts}

                            if not user_adverts:
                                with ui.element('div').classes('text-center py-12'):
                                    ui.icon('inventory').classes('text-6xl text-gray-300 mb-4')
                                    ui.label('No adverts found').classes('text-gray-500 text-lg mb-2')
                                    ui.label('Start by posting your first advert').classes('text-gray-400 mb-4')
                                    ui.button('Post Advert', on_click=lambda: ui.navigate.to('/add_event')).classes('bg-primary hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold')
                                return

                            columns = [
                                {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left', 'sortable': False, 'classes': 'hidden', 'headerClasses': 'hidden', 'style': 'display:none'},
                                {'name': 'image', 'label': 'Image', 'field': 'image', 'align': 'left', 'sortable': False},
                                {'name': 'title', 'label': 'Title', 'field': 'title', 'align': 'left'},
                                {'name': 'category', 'label': 'Category', 'field': 'category', 'align': 'left'},
                                {'name': 'price', 'label': 'Price', 'field': 'price', 'align': 'left'},
                                {'name': 'status', 'label': 'Status', 'field': 'status', 'align': 'left'},
                                {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'align': 'right', 'sortable': False},
                            ]

                            rows = []
                            for advert in user_adverts:
                                advert_id = resolve_advert_id(advert)
                                price_value = advert.get('price')
                                try:
                                    price_text = f"GHS {float(price_value):,.2f}"
                                except (TypeError, ValueError):
                                    price_text = 'GHS 0.00'

                                rows.append({
                                    'id': advert_id,
                                    'image': advert.get('image', '') or advert.get('image_url', ''),
                                    'title': advert.get('title', 'N/A'),
                                    'category': advert.get('category', 'N/A'),
                                    'price': price_text,
                                    'status': advert.get('status', 'Active'),
                                    'actions': advert_id,
                                })

                            table = ui.table(columns=columns, rows=rows, row_key='id').classes('w-full')

                            lookup = table_state['lookup']

                            def slot_image(row):
                                advert = lookup.get(row['id'])
                                image_data = row.get('image')
                                with ui.element('div'):
                                    if image_data and isinstance(image_data, str):
                                        if image_data.startswith('http'):
                                            ui.image(image_data).classes('w-16 h-16 object-cover rounded')
                                        elif len(image_data) > 50:
                                            ui.image(f'data:image/jpeg;base64,{image_data}').classes('w-16 h-16 object-cover rounded')
                                        else:
                                            ui.icon('image').classes('text-4xl text-gray-400')
                                    else:
                                        ui.icon('image').classes('text-4xl text-gray-400')

                            def slot_actions(row):
                                advert = lookup.get(row['id'])
                                advert_id = row['id']
                                title = row.get('title', 'Advert')
                                with ui.row().classes('gap-2 justify-end'):
                                    def view_advert():
                                        ui.navigate.to(f"/view_event?title={title}&id={advert_id}")
                                    
                                    def edit_advert():
                                        ui.navigate.to(f"/edit_event?title={title}&id={advert_id}")
                                    
                                    def delete_advert_action():
                                        delete_advert(advert_id, title)
                                    
                                    ui.button('View', on_click=view_advert)\
                                        .classes('bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm')
                                    ui.button('Edit', on_click=edit_advert)\
                                        .classes('bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm')
                                    ui.button('Delete', on_click=delete_advert_action)\
                                        .classes('bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm')
                            
                            table.add_slot('body-cell-image', slot_image)
                            table.add_slot('body-cell-actions', slot_actions)

                        except Exception as e:
                            ui.notify(f"Error loading adverts: {e}", type='negative')
                            print(f"Dashboard error: {e}")

                    ui.timer(0.1, lambda: asyncio.create_task(load_adverts()), once=True)

                adverts_table()

                def handle_adverts_changed(event):
                    detail = getattr(event, 'args', {}) or {}
                    event_type = detail.get('type')
                    if event_type in {'created', 'updated', 'deleted', None}:
                        adverts_table.refresh()

                ui.on('adverts_changed', handle_adverts_changed)

            # Global delete function
            async def delete_advert(advert_id: str, title: str):
                safe_id = str(advert_id or '').strip()
                if not safe_id:
                    ui.notify('Unable to delete this advert: missing identifier.', type='negative')
                    return
                label_title = title or "this advert"
                with ui.dialog() as dialog, ui.card().classes('max-w-md p-6 space-y-4'):
                    ui.label(f"Delete {label_title}?").classes('text-lg font-semibold')
                    ui.label('This action cannot be undone.').classes('text-sm text-gray-600')
                    with ui.row().classes('justify-end gap-3'):
                        ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded')

                        async def confirm_delete():
                            dialog.close()
                            try:
                                if not api_client._discovered:
                                    await api_client.discover_endpoints()
                                success, response = await api_client.delete_ad(safe_id)
                                if success:
                                    previous_items = list(adverts_state.get('items') or [])
                                    filtered_items = [ad for ad in previous_items if resolve_advert_id(ad) != safe_id]
                                    adverts_state['items'] = filtered_items
                                    dashboard_stats.refresh()
                                    recent_products.refresh()
                                    adverts_table.refresh()
                                    payload = {'type': 'deleted', 'id': safe_id}
                                    detail_json = json.dumps(payload)
                                    ui.run_javascript(
                                        f"window.dispatchEvent(new CustomEvent('adverts:changed',{{detail:{detail_json}}}));"
                                    )
                                    ui.notify('Advert deleted successfully', type='positive')
                                else:
                                    ui.notify(f"Delete failed: {response}", type='negative')
                            except Exception as exc:
                                ui.notify(f"Error deleting advert: {exc}", type='negative')

                        ui.button('Delete', on_click=confirm_delete).classes('bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded')
                dialog.open()
