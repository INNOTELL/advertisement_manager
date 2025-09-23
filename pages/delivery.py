from nicegui import ui

def show_delivery_page(auth_state=None):
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8 text-center'):
                with ui.element('div').classes('flex items-center justify-center gap-3 mb-4'):
                    ui.icon('local_shipping').classes('text-orange-500 text-4xl')
                    ui.label('INNO HUB DELIVERY').classes('text-3xl font-bold text-gray-800')
                ui.label('Send parcels easily across Ghana').classes('text-gray-600 text-lg')
                ui.label('🚚 Fast, reliable, and affordable delivery service').classes('text-orange-500 font-medium mt-2')

            # Main Content
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'):
                # Left Column - Features
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Why Choose InnoHub Delivery?').classes('text-xl font-bold text-gray-800 mb-4')
                    
                    features = [
                        {'icon': 'speed', 'title': 'Fast Delivery', 'desc': 'Same-day and next-day delivery options'},
                        {'icon': 'security', 'title': 'Secure Handling', 'desc': 'Your packages are safe with us'},
                        {'icon': 'tracking', 'title': 'Real-time Tracking', 'desc': 'Track your package every step of the way'},
                        {'icon': 'support', 'title': '24/7 Support', 'desc': 'Round-the-clock customer service'}
                    ]
                    
                    for feature in features:
                        with ui.element('div').classes('flex items-start gap-3 mb-4'):
                            ui.icon(feature['icon']).classes('text-orange-500 text-xl mt-1')
                            with ui.element('div'):
                                ui.label(feature['title']).classes('font-semibold text-gray-800')
                                ui.label(feature['desc']).classes('text-sm text-gray-600')

                # Right Column - Delivery Options
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Delivery Options').classes('text-xl font-bold text-gray-800 mb-4')
                    
                    options = [
                        {'type': 'Same Day', 'price': 'GHS 25', 'time': 'Within 4 hours', 'icon': 'flash_on'},
                        {'type': 'Next Day', 'price': 'GHS 15', 'time': 'Next business day', 'icon': 'schedule'},
                        {'type': 'Standard', 'price': 'GHS 10', 'time': '2-3 business days', 'icon': 'local_shipping'},
                        {'type': 'Economy', 'price': 'GHS 8', 'time': '3-5 business days', 'icon': 'savings'}
                    ]
                    
                    for option in options:
                        with ui.card().classes('p-4 mb-3 border border-gray-200 hover:border-orange-500 transition-colors cursor-pointer'):
                            with ui.element('div').classes('flex items-center justify-between'):
                                with ui.element('div').classes('flex items-center gap-3'):
                                    ui.icon(option['icon']).classes('text-orange-500 text-lg')
                                    with ui.element('div'):
                                        ui.label(option['type']).classes('font-semibold text-gray-800')
                                        ui.label(option['time']).classes('text-sm text-gray-600')
                                ui.label(option['price']).classes('text-lg font-bold text-orange-500')

            # How It Works Section
            with ui.card().classes('p-6 bg-white shadow-sm mb-8'):
                ui.label('How It Works').classes('text-2xl font-bold text-gray-800 mb-6 text-center')
                
                steps = [
                    {'step': '1', 'title': 'Book Your Delivery', 'desc': 'Schedule pickup online or call us', 'icon': 'book_online'},
                    {'step': '2', 'title': 'Package Collection', 'desc': 'We collect your package safely', 'icon': 'inventory'},
                    {'step': '3', 'title': 'Track & Monitor', 'desc': 'Follow your package in real-time', 'icon': 'gps_fixed'},
                    {'step': '4', 'title': 'Safe Delivery', 'desc': 'Package delivered to destination', 'icon': 'home'}
                ]
                
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6'):
                    for step in steps:
                        with ui.element('div').classes('text-center'):
                            with ui.element('div').classes('w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center mx-auto mb-3'):
                                ui.label(step['step']).classes('text-white text-xl font-bold')
                            ui.icon(step['icon']).classes('text-orange-500 text-2xl mb-2')
                            ui.label(step['title']).classes('font-semibold text-gray-800 mb-1')
                            ui.label(step['desc']).classes('text-sm text-gray-600')

            # CTA Section
            with ui.element('div').classes('text-center bg-gradient-to-r from-orange-500 to-orange-600 text-white p-8 rounded-lg'):
                ui.label('Ready to Send Your Package?').classes('text-2xl font-bold mb-4')
                ui.label('Join thousands of satisfied customers who trust InnoHub Delivery').classes('text-orange-100 mb-6')
                
                with ui.element('div').classes('flex flex-col sm:flex-row gap-4 justify-center'):
                    ui.button('Book Delivery Now', icon='local_shipping').classes('bg-white text-orange-500 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold')
                    ui.button('Track Package', icon='track_changes').classes('bg-orange-600 hover:bg-orange-700 text-white px-8 py-3 rounded-lg font-semibold border border-white')

            # Contact Info
            with ui.element('div').classes('mt-8 text-center text-gray-600'):
                ui.label('Need Help? Contact Us').classes('text-lg font-semibold mb-2')
                ui.label('📞 +233 123 456 789 | 📧 delivery@innohub.com').classes('text-sm')
