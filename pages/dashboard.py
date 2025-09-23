from nicegui import ui
import requests
import asyncio
from utils.api import base_url
from datetime import datetime, timedelta

def show_dashboard_page(auth_state=None):
    if not auth_state or not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-7xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('Vendor Dashboard').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label(f'Welcome back, {auth_state.user_email}!').classes('text-gray-600')
            
            # Quick Stats
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-4 gap-6 mb-8'):
                stats = [
                    {'title': 'Total Products', 'value': '24', 'icon': 'inventory', 'color': 'bg-blue-500', 'change': '+12%'},
                    {'title': 'Active Listings', 'value': '18', 'icon': 'visibility', 'color': 'bg-green-500', 'change': '+5%'},
                    {'title': 'Total Sales', 'value': 'GHS 12,450', 'icon': 'attach_money', 'color': 'bg-primary', 'change': '+23%'},
                    {'title': 'Pending Orders', 'value': '5', 'icon': 'pending', 'color': 'bg-yellow-500', 'change': '-2%'},
                ]
                
                for stat in stats:
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm hover:shadow-md transition-shadow'):
                        with ui.element('div').classes('flex items-center justify-between mb-4'):
                            ui.icon(stat['icon']).classes(f'text-white text-2xl {stat["color"]} rounded-full p-3')
                            ui.label(stat['change']).classes('text-sm font-medium text-green-600')
                        with ui.element('div'):
                            ui.label(stat['value']).classes('text-2xl font-bold text-gray-800')
                            ui.label(stat['title']).classes('text-sm text-gray-600')
            
            # Main Dashboard Content
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-3 gap-8'):
                # Left Column - Products Management
                with ui.element('div').classes('lg:col-span-2 space-y-8'):
                    # Recent Products
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        with ui.element('div').classes('flex items-center justify-between mb-6'):
                            ui.label('Recent Products').classes('text-xl font-bold text-gray-800')
                            ui.button('View All', on_click=lambda: ui.navigate.to('/products')).classes('text-primary hover:text-primary-dark font-medium')
                        
                        # Demo products data
                        products = [
                            {'title': 'iPhone 14 Pro', 'price': 4500, 'status': 'Active', 'views': 1247, 'sales': 8, 'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=100&h=100&fit=crop'},
                            {'title': 'Samsung Galaxy S23', 'price': 3800, 'status': 'Active', 'views': 892, 'sales': 5, 'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=100&h=100&fit=crop'},
                            {'title': 'MacBook Pro M2', 'price': 8500, 'status': 'Sold', 'views': 2156, 'sales': 3, 'image': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=100&h=100&fit=crop'},
                        ]
                        
                        with ui.element('div').classes('space-y-4'):
                            for product in products:
                                with ui.element('div').classes('flex items-center gap-4 p-4 border border-gray-200 rounded-lg hover:bg-gray-50'):
                                    ui.image(product['image']).classes('w-16 h-16 object-cover rounded-lg')
                                    with ui.element('div').classes('flex-1'):
                                        ui.label(product['title']).classes('font-semibold text-gray-800')
                                        ui.label(f'GHS {product["price"]:,.2f}').classes('text-primary font-medium')
                                        with ui.row().classes('items-center gap-4 mt-1'):
                                            ui.label(f'{product["views"]} views').classes('text-xs text-gray-500')
                                            ui.label(f'{product["sales"]} sales').classes('text-xs text-green-600')
                                    with ui.element('div').classes('text-right'):
                                        status_colors = {'Active': 'bg-green-100 text-green-800', 'Sold': 'bg-blue-100 text-blue-800', 'Draft': 'bg-gray-100 text-gray-800'}
                                        ui.label(product['status']).classes(f'px-2 py-1 rounded-full text-xs font-medium {status_colors.get(product["status"], "bg-gray-100 text-gray-800")}')
                                        with ui.row().classes('gap-1 mt-2'):
                                            ui.button(icon='edit').classes('text-blue-500 hover:text-blue-600 p-1').props('flat round')
                                            ui.button(icon='delete').classes('text-red-500 hover:text-red-600 p-1').props('flat round')
                    
                    # Recent Orders
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        with ui.element('div').classes('flex items-center justify-between mb-6'):
                            ui.label('Recent Orders').classes('text-xl font-bold text-gray-800')
                            ui.button('View All', on_click=lambda: ui.navigate.to('/orders')).classes('text-primary hover:text-primary-dark font-medium')
                        
                        orders = [
                            {'id': 'ORD-001', 'customer': 'John Doe', 'product': 'iPhone 14 Pro', 'amount': 4500, 'status': 'Pending', 'date': '2024-01-20'},
                            {'id': 'ORD-002', 'customer': 'Jane Smith', 'product': 'Samsung Galaxy S23', 'amount': 3800, 'status': 'Shipped', 'date': '2024-01-19'},
                            {'id': 'ORD-003', 'customer': 'Mike Johnson', 'product': 'MacBook Pro M2', 'amount': 8500, 'status': 'Delivered', 'date': '2024-01-18'},
                        ]
                        
                        with ui.element('div').classes('space-y-3'):
                            for order in orders:
                                with ui.element('div').classes('flex items-center justify-between p-3 border border-gray-200 rounded-lg'):
                                    with ui.element('div'):
                                        ui.label(f'#{order["id"]}').classes('font-semibold text-gray-800')
                                        ui.label(f'{order["customer"]} - {order["product"]}').classes('text-sm text-gray-600')
                                        ui.label(f'GHS {order["amount"]:,.2f}').classes('text-primary font-medium')
                                    with ui.element('div').classes('text-right'):
                                        status_colors = {'Pending': 'bg-yellow-100 text-yellow-800', 'Shipped': 'bg-blue-100 text-blue-800', 'Delivered': 'bg-green-100 text-green-800'}
                                        ui.label(order['status']).classes(f'px-2 py-1 rounded-full text-xs font-medium {status_colors.get(order["status"], "bg-gray-100 text-gray-800")}')
                                        ui.label(order['date']).classes('text-xs text-gray-500')
                
                # Right Column - Analytics & Actions
                with ui.element('div').classes('space-y-8'):
                    # Sales Analytics
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        ui.label('Sales Analytics').classes('text-xl font-bold text-gray-800 mb-6')
                        
                        # Weekly sales chart (simplified)
                        with ui.element('div').classes('space-y-4'):
                            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                            sales = [1200, 1800, 1500, 2200, 1900, 2500, 2100]
                            
                            for day, amount in zip(days, sales):
                                with ui.element('div').classes('flex items-center justify-between'):
                                    ui.label(day).classes('text-sm text-gray-600 w-8')
                                    with ui.element('div').classes('flex-1 mx-3'):
                                        ui.element('div').classes('bg-gray-200 rounded-full h-2').style(f'width: {(amount/2500)*100}%')
                                    ui.label(f'GHS {amount:,}').classes('text-sm font-medium text-gray-800 w-16 text-right')
                    
                    # Quick Actions
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        ui.label('Quick Actions').classes('text-xl font-bold text-gray-800 mb-6')
                        
                        actions = [
                            {'title': 'Add New Product', 'icon': 'add', 'color': 'bg-primary', 'action': lambda: ui.navigate.to('/add_event')},
                            {'title': 'View Analytics', 'icon': 'analytics', 'color': 'bg-blue-500', 'action': lambda: ui.navigate.to('/analytics')},
                            {'title': 'Manage Orders', 'icon': 'shopping_bag', 'color': 'bg-green-500', 'action': lambda: ui.navigate.to('/orders')},
                            {'title': 'Update Profile', 'icon': 'person', 'color': 'bg-purple-500', 'action': lambda: ui.navigate.to('/account')},
                        ]
                        
                        with ui.element('div').classes('grid grid-cols-2 gap-4'):
                            for action in actions:
                                with ui.card().classes('p-4 bg-gray-50 shadow-sm hover:shadow-md transition-shadow cursor-pointer').on('click', action['action']):
                                    with ui.element('div').classes('text-center'):
                                        ui.icon(action['icon']).classes(f'text-white text-2xl {action["color"]} rounded-full p-3 mx-auto mb-3')
                                        ui.label(action['title']).classes('font-medium text-gray-800 text-sm')
                    
                    # Performance Metrics
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                        ui.label('Performance Metrics').classes('text-xl font-bold text-gray-800 mb-6')
                        
                        metrics = [
                            {'label': 'Conversion Rate', 'value': '12.5%', 'trend': '+2.1%'},
                            {'label': 'Average Order Value', 'value': 'GHS 1,250', 'trend': '+5.3%'},
                            {'label': 'Customer Satisfaction', 'value': '4.8/5', 'trend': '+0.2'},
                            {'label': 'Return Rate', 'value': '3.2%', 'trend': '-0.5%'},
                        ]
                        
                        for metric in metrics:
                            with ui.element('div').classes('flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0'):
                                with ui.element('div'):
                                    ui.label(metric['label']).classes('text-sm text-gray-600')
                                    ui.label(metric['value']).classes('font-semibold text-gray-800')
                                ui.label(metric['trend']).classes('text-sm font-medium text-green-600')
            
            # My Adverts Section (Enhanced)
            with ui.card().classes('mt-8 p-6 bg-gray-50 shadow-sm'):
                with ui.element('div').classes('flex items-center justify-between mb-6'):
                    ui.label('My Adverts').classes('text-2xl font-bold text-gray-800')
                    with ui.row().classes('gap-3'):
                        search_input = ui.input('Search adverts...').classes('w-64').props('outlined')
                        category_filter = ui.select(['All Categories', 'Electronics', 'Fashion', 'Furniture', 'Vehicles', 'Real Estate', 'Services'], value='All Categories').props('outlined')
                        ui.button('Add New', on_click=lambda: ui.navigate.to('/add_event')).classes('bg-primary hover:bg-orange-600 text-white px-4 py-2 rounded-lg')
                
                @ui.refreshable
                def adverts_table():
                    async def load_adverts():
                        try:
                            response = await asyncio.to_thread(requests.get, f"{base_url}/adverts")
                            data = response.json()
                            adverts = data.get('data', [])
                            
                            # Filter adverts by current user (in real app, this would be done by backend)
                            if auth_state and auth_state.user_email:
                                user_adverts = [ad for ad in adverts if ad.get('vendor_email') == auth_state.user_email]
                            else:
                                user_adverts = adverts  # Show all if no auth state
                            
                            if not user_adverts:
                                with ui.element('div').classes('text-center py-12'):
                                    ui.icon('inventory').classes('text-6xl text-gray-300 mb-4')
                                    ui.label('No adverts found').classes('text-gray-500 text-lg mb-2')
                                    ui.label('Start by posting your first advert').classes('text-gray-400 mb-4')
                                    ui.button('Post Advert', on_click=lambda: ui.navigate.to('/add_event')).classes('bg-primary hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold')
                                return
                            
                            # Create enhanced table
                            with ui.table(columns=[
                                {'name': 'title', 'label': 'Title', 'field': 'title'},
                                {'name': 'category', 'label': 'Category', 'field': 'category'},
                                {'name': 'price', 'label': 'Price', 'field': 'price'},
                                {'name': 'views', 'label': 'Views', 'field': 'views'},
                                {'name': 'status', 'label': 'Status', 'field': 'status'},
                                {'name': 'actions', 'label': 'Actions', 'field': 'actions'}
                            ], rows=[]).classes('w-full'):
                                for advert in user_adverts:
                                    with ui.table_row():
                                        ui.table_cell(advert.get('title', 'N/A'))
                                        ui.table_cell(advert.get('category', 'N/A'))
                                        ui.table_cell(f"GHS {advert.get('price', 0):,.2f}")
                                        ui.table_cell(f"{advert.get('views', 0)}")
                                        ui.table_cell('Active')
                                        with ui.table_cell():
                                            with ui.row().classes('gap-2'):
                                                ui.button('View', on_click=lambda a=advert: ui.navigate.to(f"/view_event?title={a.get('title', '')}")).classes('bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm')
                                                ui.button('Edit', on_click=lambda a=advert: ui.navigate.to(f"/edit_event?title={a.get('title', '')}")).classes('bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm')
                                                ui.button('Delete', on_click=lambda a=advert: delete_advert(a.get('title', ''))).classes('bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm')
                        
                        except Exception as e:
                            ui.notify(f"Error loading adverts: {e}", type='negative')
                    
                    ui.timer(0.1, load_adverts, once=True)
                
                async def delete_advert(title: str):
                    try:
                        response = await asyncio.to_thread(requests.delete, f"{base_url}/adverts/{title}")
                        if response.status_code == 200:
                            ui.notify('Advert deleted successfully', type='positive')
                            adverts_table.refresh()
                        else:
                            ui.notify('Failed to delete advert', type='negative')
                    except Exception as e:
                        ui.notify(f"Error deleting advert: {e}", type='negative')
                
                adverts_table()