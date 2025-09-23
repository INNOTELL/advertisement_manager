from nicegui import ui

def show_sell_page(auth_state=None):
    with ui.element('div').classes('min-h-screen bg-white py-8'):
        with ui.element('div').classes('container mx-auto px-4 max-w-6xl'):
            # Page Header
            with ui.element('div').classes('mb-8 text-center'):
                with ui.element('div').classes('flex items-center justify-center gap-3 mb-4'):
                    ui.icon('store').classes('text-orange-500 text-4xl')
                    ui.label('SELL ON INNO HUB').classes('text-3xl font-bold text-gray-800')
                ui.label('Make more money by selling on Ghana\'s premier marketplace').classes('text-gray-600 text-lg')
                ui.label('💰 Start selling today and grow your business').classes('text-orange-500 font-medium mt-2')

            # Main Content
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8'):
                # Left Column - Benefits
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Why Sell on InnoHub?').classes('text-xl font-bold text-gray-800 mb-4')
                    
                    benefits = [
                        {'icon': 'trending_up', 'title': 'Reach More Customers', 'desc': 'Access thousands of buyers across Ghana'},
                        {'icon': 'payment', 'title': 'Secure Payments', 'desc': 'Get paid safely and on time'},
                        {'icon': 'support_agent', 'title': 'Seller Support', 'desc': 'Dedicated support team to help you succeed'},
                        {'icon': 'analytics', 'title': 'Sales Analytics', 'desc': 'Track your performance with detailed insights'},
                        {'icon': 'inventory', 'title': 'Easy Inventory', 'desc': 'Manage your products with our simple tools'},
                        {'icon': 'local_shipping', 'title': 'Delivery Support', 'desc': 'Use our delivery network for shipping'}
                    ]
                    
                    for benefit in benefits:
                        with ui.element('div').classes('flex items-start gap-3 mb-4'):
                            ui.icon(benefit['icon']).classes('text-orange-500 text-xl mt-1')
                            with ui.element('div'):
                                ui.label(benefit['title']).classes('font-semibold text-gray-800')
                                ui.label(benefit['desc']).classes('text-sm text-gray-600')

                # Right Column - Success Stories
                with ui.card().classes('p-6 bg-gray-50 shadow-sm'):
                    ui.label('Success Stories').classes('text-xl font-bold text-gray-800 mb-4')
                    
                    stories = [
                        {'name': 'Sarah Mensah', 'business': 'Fashion Store', 'revenue': 'GHS 15,000/month', 'icon': 'person'},
                        {'name': 'Kwame Asante', 'business': 'Electronics Shop', 'revenue': 'GHS 25,000/month', 'icon': 'person'},
                        {'name': 'Ama Osei', 'business': 'Home Decor', 'revenue': 'GHS 8,500/month', 'icon': 'person'}
                    ]
                    
                    for story in stories:
                        with ui.card().classes('p-4 mb-3 border border-gray-200 hover:border-orange-500 transition-colors'):
                            with ui.element('div').classes('flex items-center gap-3'):
                                ui.icon(story['icon']).classes('text-orange-500 text-lg')
                                with ui.element('div').classes('flex-1'):
                                    ui.label(story['name']).classes('font-semibold text-gray-800')
                                    ui.label(story['business']).classes('text-sm text-gray-600')
                                ui.label(story['revenue']).classes('text-sm font-bold text-green-600')

            # Seller Plans Section
            with ui.card().classes('p-6 bg-white shadow-sm mb-8'):
                ui.label('Choose Your Seller Plan').classes('text-2xl font-bold text-gray-800 mb-6 text-center')
                
                plans = [
                    {
                        'name': 'Starter',
                        'price': 'Free',
                        'features': ['Up to 10 products', 'Basic analytics', 'Email support', 'Standard listing'],
                        'icon': 'star',
                        'color': 'bg-gray-500'
                    },
                    {
                        'name': 'Professional',
                        'price': 'GHS 50/month',
                        'features': ['Up to 100 products', 'Advanced analytics', 'Priority support', 'Featured listings'],
                        'icon': 'business',
                        'color': 'bg-orange-500'
                    },
                    {
                        'name': 'Enterprise',
                        'price': 'GHS 150/month',
                        'features': ['Unlimited products', 'Full analytics', 'Dedicated support', 'Premium placement'],
                        'icon': 'diamond',
                        'color': 'bg-purple-500'
                    }
                ]
                
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-3 gap-6'):
                    for plan in plans:
                        with ui.card().classes(f'p-6 border-2 {"border-orange-500" if plan["name"] == "Professional" else "border-gray-200"} hover:border-orange-500 transition-colors cursor-pointer'):
                            with ui.element('div').classes('text-center mb-4'):
                                ui.icon(plan['icon']).classes(f'text-white text-2xl {plan["color"]} rounded-full p-3 mx-auto mb-3')
                                ui.label(plan['name']).classes('text-xl font-bold text-gray-800')
                                ui.label(plan['price']).classes('text-2xl font-bold text-orange-500')
                            
                            with ui.element('div').classes('space-y-2'):
                                for feature in plan['features']:
                                    with ui.element('div').classes('flex items-center gap-2'):
                                        ui.icon('check').classes('text-green-500 text-sm')
                                        ui.label(feature).classes('text-sm text-gray-600')
                            
                            if plan['name'] == 'Professional':
                                ui.button('Most Popular', icon='star').classes('w-full mt-4 bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg font-semibold')
                            else:
                                ui.button('Choose Plan', icon='arrow_forward').classes('w-full mt-4 bg-gray-500 hover:bg-gray-600 text-white py-2 rounded-lg font-semibold')

            # How to Start Section
            with ui.card().classes('p-6 bg-white shadow-sm mb-8'):
                ui.label('How to Start Selling').classes('text-2xl font-bold text-gray-800 mb-6 text-center')
                
                steps = [
                    {'step': '1', 'title': 'Create Account', 'desc': 'Sign up as a seller', 'icon': 'person_add'},
                    {'step': '2', 'title': 'Add Products', 'desc': 'Upload your product listings', 'icon': 'add_box'},
                    {'step': '3', 'title': 'Set Prices', 'desc': 'Price your products competitively', 'icon': 'attach_money'},
                    {'step': '4', 'title': 'Start Selling', 'desc': 'Begin receiving orders', 'icon': 'shopping_cart'}
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
                ui.label('Ready to Start Selling?').classes('text-2xl font-bold mb-4')
                ui.label('Join thousands of successful sellers on InnoHub').classes('text-orange-100 mb-6')
                
                with ui.element('div').classes('flex flex-col sm:flex-row gap-4 justify-center'):
                    ui.button('Start Selling Now', icon='store', on_click=lambda: ui.navigate.to('/add_event')).classes('bg-white text-orange-500 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold')
                    ui.button('Learn More', icon='info').classes('bg-orange-600 hover:bg-orange-700 text-white px-8 py-3 rounded-lg font-semibold border border-white')

            # Contact Info
            with ui.element('div').classes('mt-8 text-center text-gray-600'):
                ui.label('Need Help Getting Started?').classes('text-lg font-semibold mb-2')
                ui.label('📞 +233 123 456 789 | 📧 sellers@innohub.com').classes('text-sm')
