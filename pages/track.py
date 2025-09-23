from nicegui import ui

def show_track_page(auth_state=None):
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8 text-center'):
                with ui.element('div').classes('flex items-center justify-center gap-3 mb-4'):
                    ui.icon('track_changes').classes('text-orange-500 text-4xl')
                    ui.label('TRACK YOUR ORDER').classes('text-3xl font-bold text-gray-800')
                ui.label('Stay up to date with your package delivery').classes('text-gray-600 text-lg')
                ui.label('📍 Real-time tracking for all your orders').classes('text-orange-500 font-medium mt-2')

            # Tracking Input Section
            with ui.card().classes('p-6 bg-gray-50 shadow-sm mb-8'):
                ui.label('Track Your Package').classes('text-xl font-bold text-gray-800 mb-4 text-center')
                
                with ui.element('div').classes('max-w-md mx-auto'):
                    with ui.row().classes('gap-3'):
                        tracking_input = ui.input('Enter tracking number').classes('flex-1').props('outlined')
                        ui.button('Track', icon='search').classes('bg-orange-500 hover:bg-orange-600 text-white px-6 py-2 rounded-lg')
                    
                    ui.label('Example: INH123456789').classes('text-sm text-gray-500 mt-2 text-center')

            # Main Content
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'):
                # Left Column - Tracking Features
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Tracking Features').classes('text-xl font-bold text-gray-800 mb-4')
                    
                    features = [
                        {'icon': 'gps_fixed', 'title': 'Real-time Location', 'desc': 'See exactly where your package is'},
                        {'icon': 'schedule', 'title': 'Delivery Timeline', 'desc': 'Get estimated delivery times'},
                        {'icon': 'notifications', 'title': 'SMS & Email Updates', 'desc': 'Receive notifications at every step'},
                        {'icon': 'history', 'title': 'Delivery History', 'desc': 'View complete delivery timeline'},
                        {'icon': 'support', 'title': '24/7 Support', 'desc': 'Get help whenever you need it'},
                        {'icon': 'security', 'title': 'Secure Tracking', 'desc': 'Your tracking info is protected'}
                    ]
                    
                    for feature in features:
                        with ui.element('div').classes('flex items-start gap-3 mb-4'):
                            ui.icon(feature['icon']).classes('text-orange-500 text-xl mt-1')
                            with ui.element('div'):
                                ui.label(feature['title']).classes('font-semibold text-gray-800')
                                ui.label(feature['desc']).classes('text-sm text-gray-600')

                # Right Column - Sample Tracking Status
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Sample Tracking Status').classes('text-xl font-bold text-gray-800 mb-4')
                    
                    # Sample tracking timeline
                    tracking_steps = [
                        {'status': 'Delivered', 'time': 'Today, 2:30 PM', 'location': 'Accra, Ghana', 'icon': 'check_circle', 'color': 'text-green-500'},
                        {'status': 'Out for Delivery', 'time': 'Today, 8:00 AM', 'location': 'Accra Distribution Center', 'icon': 'local_shipping', 'color': 'text-blue-500'},
                        {'status': 'In Transit', 'time': 'Yesterday, 6:45 PM', 'location': 'Kumasi Hub', 'icon': 'flight', 'color': 'text-orange-500'},
                        {'status': 'Package Received', 'time': 'Yesterday, 10:30 AM', 'location': 'Kumasi Sorting Facility', 'icon': 'inventory', 'color': 'text-gray-500'}
                    ]
                    
                    for i, step in enumerate(tracking_steps):
                        with ui.element('div').classes('flex items-start gap-3 mb-4'):
                            ui.icon(step['icon']).classes(f'{step["color"]} text-lg mt-1')
                            with ui.element('div').classes('flex-1'):
                                ui.label(step['status']).classes('font-semibold text-gray-800')
                                ui.label(step['time']).classes('text-sm text-gray-600')
                                ui.label(step['location']).classes('text-xs text-gray-500')
                            if i == 0:
                                ui.label('✓').classes('text-green-500 text-lg font-bold')

            # Delivery Status Cards
            with ui.card().classes('p-6 bg-white shadow-sm mb-8'):
                ui.label('Common Delivery Statuses').classes('text-2xl font-bold text-gray-800 mb-6 text-center')
                
                statuses = [
                    {'status': 'Order Confirmed', 'desc': 'Your order has been received and confirmed', 'icon': 'receipt', 'color': 'bg-blue-500'},
                    {'status': 'Processing', 'desc': 'Your package is being prepared for shipment', 'icon': 'build', 'color': 'bg-yellow-500'},
                    {'status': 'Shipped', 'desc': 'Your package is on its way to you', 'icon': 'local_shipping', 'color': 'bg-orange-500'},
                    {'status': 'In Transit', 'desc': 'Package is moving through our network', 'icon': 'flight', 'color': 'bg-purple-500'},
                    {'status': 'Out for Delivery', 'desc': 'Package is out for final delivery', 'icon': 'delivery_dining', 'color': 'bg-indigo-500'},
                    {'status': 'Delivered', 'desc': 'Package has been successfully delivered', 'icon': 'check_circle', 'color': 'bg-green-500'}
                ]
                
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'):
                    for status in statuses:
                        with ui.card().classes('p-4 border border-gray-200 hover:border-orange-500 transition-colors'):
                            with ui.element('div').classes('flex items-center gap-3 mb-2'):
                                ui.icon(status['icon']).classes(f'text-white text-lg {status["color"]} rounded-full p-2')
                                ui.label(status['status']).classes('font-semibold text-gray-800')
                            ui.label(status['desc']).classes('text-sm text-gray-600')

            # How to Track Section
            with ui.card().classes('p-6 bg-white shadow-sm mb-8'):
                ui.label('How to Track Your Package').classes('text-2xl font-bold text-gray-800 mb-6 text-center')
                
                steps = [
                    {'step': '1', 'title': 'Get Tracking Number', 'desc': 'Receive tracking number via SMS/email', 'icon': 'sms'},
                    {'step': '2', 'title': 'Enter Tracking ID', 'desc': 'Input your tracking number above', 'icon': 'keyboard'},
                    {'step': '3', 'title': 'View Status', 'desc': 'See real-time delivery status', 'icon': 'visibility'},
                    {'step': '4', 'title': 'Get Updates', 'desc': 'Receive notifications automatically', 'icon': 'notifications'}
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
                ui.label('Need Help with Tracking?').classes('text-2xl font-bold mb-4')
                ui.label('Our customer service team is here to help you track your packages').classes('text-orange-100 mb-6')
                
                with ui.element('div').classes('flex flex-col sm:flex-row gap-4 justify-center'):
                    ui.button('Contact Support', icon='support_agent').classes('bg-white text-orange-500 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold')
                    ui.button('Track Another Package', icon='search').classes('bg-orange-600 hover:bg-orange-700 text-white px-8 py-3 rounded-lg font-semibold border border-white')

            # Contact Info
            with ui.element('div').classes('mt-8 text-center text-gray-600'):
                ui.label('Tracking Support').classes('text-lg font-semibold mb-2')
                ui.label('📞 +233 123 456 789 | 📧 tracking@innohub.com').classes('text-sm')
