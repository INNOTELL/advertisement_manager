from nicegui import ui
import requests
from utils.api import base_url
from datetime import datetime, timedelta

def show_analytics_page(auth_state=None):
    if not auth_state or not auth_state.is_authenticated:
        ui.navigate.to('/login')
        return
    
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-7xl'):
            # Page Header
            with ui.element('div').classes('mb-8'):
                ui.label('Analytics Dashboard').classes('text-3xl font-bold text-gray-800 mb-2')
                ui.label('Track your business performance and insights').classes('text-gray-600')
            
            # Key Metrics
            with ui.element('div').classes('grid grid-cols-1 md:grid-cols-4 gap-6 mb-8'):
                metrics = [
                    {'title': 'Total Revenue', 'value': 'GHS 45,230', 'change': '+12.5%', 'icon': 'attach_money', 'color': 'bg-green-500'},
                    {'title': 'Total Orders', 'value': '1,247', 'change': '+8.2%', 'icon': 'shopping_bag', 'color': 'bg-blue-500'},
                    {'title': 'Active Products', 'value': '89', 'change': '+3.1%', 'icon': 'inventory', 'color': 'bg-purple-500'},
                    {'title': 'Customer Satisfaction', 'value': '4.8/5', 'change': '+0.3', 'icon': 'star', 'color': 'bg-yellow-500'},
                ]
                
                for metric in metrics:
                    with ui.card().classes('p-6 bg-gray-50 shadow-sm hover:shadow-md transition-shadow'):
                        with ui.element('div').classes('flex items-center justify-between mb-4'):
                            ui.icon(metric['icon']).classes(f'text-white text-2xl {metric["color"]} rounded-full p-3')
                            ui.label(metric['change']).classes('text-sm font-medium text-green-600')
                        with ui.element('div'):
                            ui.label(metric['value']).classes('text-2xl font-bold text-gray-800')
                            ui.label(metric['title']).classes('text-sm text-gray-600')
            
            # Charts Section
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'):
                # Sales Chart
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Sales Performance').classes('text-xl font-bold text-gray-800 mb-6')
                    
                    # Simple bar chart representation
                    with ui.element('div').classes('space-y-4'):
                        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
                        sales = [12000, 15000, 18000, 22000, 19000, 25000]
                        
                        for month, amount in zip(months, sales):
                            with ui.element('div').classes('flex items-center justify-between'):
                                ui.label(month).classes('text-sm text-gray-600 w-8')
                                with ui.element('div').classes('flex-1 mx-3'):
                                    ui.element('div').classes('bg-blue-500 rounded-full h-4').style(f'width: {(amount/25000)*100}%')
                                ui.label(f'GHS {amount:,}').classes('text-sm font-medium text-gray-800 w-20 text-right')
                
                # Top Products
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Top Selling Products').classes('text-xl font-bold text-gray-800 mb-6')
                    
                    top_products = [
                        {'name': 'iPhone 14 Pro', 'sales': 45, 'revenue': 'GHS 202,500'},
                        {'name': 'Samsung Galaxy S23', 'sales': 32, 'revenue': 'GHS 121,600'},
                        {'name': 'MacBook Pro M2', 'sales': 18, 'revenue': 'GHS 153,000'},
                        {'name': 'iPad Air', 'sales': 28, 'revenue': 'GHS 84,000'},
                        {'name': 'AirPods Pro', 'sales': 67, 'revenue': 'GHS 80,400'},
                    ]
                    
                    with ui.element('div').classes('space-y-3'):
                        for product in top_products:
                            with ui.element('div').classes('flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200'):
                                with ui.element('div'):
                                    ui.label(product['name']).classes('font-medium text-gray-800')
                                    ui.label(f'{product["sales"]} sales').classes('text-sm text-gray-600')
                                ui.label(product['revenue']).classes('font-semibold text-green-600')
            
            # Recent Activity
            with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                ui.label('Recent Activity').classes('text-xl font-bold text-gray-800 mb-6')
                
                activities = [
                    {'action': 'New Order', 'details': 'iPhone 14 Pro - GHS 4,500', 'time': '2 minutes ago', 'icon': 'shopping_cart', 'color': 'text-green-500'},
                    {'action': 'Product Updated', 'details': 'Samsung Galaxy S23 price changed', 'time': '15 minutes ago', 'icon': 'edit', 'color': 'text-blue-500'},
                    {'action': 'New Review', 'details': '5-star review for MacBook Pro M2', 'time': '1 hour ago', 'icon': 'star', 'color': 'text-yellow-500'},
                    {'action': 'Order Shipped', 'details': 'Order #ORD-001 shipped to customer', 'time': '2 hours ago', 'icon': 'local_shipping', 'color': 'text-purple-500'},
                    {'action': 'New Product', 'details': 'iPad Air added to inventory', 'time': '3 hours ago', 'icon': 'add', 'color': 'text-green-500'},
                ]
                
                with ui.element('div').classes('space-y-3'):
                    for activity in activities:
                        with ui.element('div').classes('flex items-center gap-4 p-3 bg-white rounded-lg border border-gray-200'):
                            ui.icon(activity['icon']).classes(f'{activity["color"]} text-xl')
                            with ui.element('div').classes('flex-1'):
                                ui.label(activity['action']).classes('font-medium text-gray-800')
                                ui.label(activity['details']).classes('text-sm text-gray-600')
                            ui.label(activity['time']).classes('text-xs text-gray-500')
