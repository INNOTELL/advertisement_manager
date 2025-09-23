from nicegui import ui

def show_footer():
    # Jumia-style footer with newsletter and app download
    with ui.element('div').classes('bg-blue-600 text-white py-6 mt-8'):
        with ui.element('div').classes('container mx-auto px-4'):
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-3 gap-6 items-start'):
                
                # Left Column - Logo
                with ui.element('div').classes('text-center lg:text-left'):
                    with ui.element('div').classes('flex items-center justify-center lg:justify-start gap-2 mb-2'):
                        ui.label('INNO').classes('text-2xl font-bold text-white')
                        ui.icon('star').classes('text-primary text-xl')
                        ui.label('HUB').classes('text-2xl font-bold text-white')
                    ui.label('Ghana').classes('text-xs text-gray-400')
                
                # Middle Column - Newsletter Subscription
                with ui.element('div').classes('text-center lg:text-left'):
                    ui.label('NEW TO INNO HUB?').classes('text-base font-semibold text-white mb-1')
                    ui.label('Subscribe to our newsletter to get updates on our latest offers!').classes('text-gray-300 text-xs mb-3')
                    
                    # Newsletter form
                    with ui.element('div').classes('flex flex-col sm:flex-row gap-2 mb-2'):
                        email_input = ui.input('Enter E-mail Address').classes('flex-1 bg-white text-gray-800 px-3 py-1 rounded border border-gray-300 text-sm').props('outlined')
                        ui.button('Subscribe').classes('bg-gray-600 hover:bg-gray-700 text-white px-4 py-1 rounded font-medium text-sm')
                    
                    # Privacy policy checkbox
                    with ui.element('div').classes('flex items-start gap-2 text-xs text-gray-300'):
                        ui.checkbox().classes('mt-1')
                        ui.label('I agree to InnoHub\'s Privacy and Cookie Policy. You can unsubscribe from newsletters at any time. ').classes('leading-relaxed')
                        ui.link('I accept the Legal Terms', '#').classes('text-primary hover:text-primary-light no-underline')
                
                # Right Column - App Download
                with ui.element('div').classes('text-center lg:text-left'):
                    ui.label('DOWNLOAD INNO HUB FREE APP').classes('text-base font-semibold text-white mb-1')
                    ui.label('Get access to exclusive offers!').classes('text-gray-300 text-xs mb-3')
                    
                    # App icon
                    with ui.element('div').classes('flex items-center justify-center lg:justify-start gap-2 mb-2'):
                        with ui.element('div').classes('w-8 h-8 bg-primary rounded-lg flex items-center justify-center'):
                            ui.icon('star').classes('text-white text-sm')
                        ui.label('InnoHub App').classes('text-white font-medium text-sm')
                    
                    # Download buttons
                    with ui.element('div').classes('space-y-1'):
                        # App Store button
                        with ui.button().classes('w-full sm:w-auto bg-black hover:bg-gray-900 text-white px-3 py-1 rounded flex items-center justify-center gap-1'):
                            ui.icon('phone_iphone').classes('text-white text-sm')
                            ui.label('Download on the App Store').classes('text-xs')
                        
                        # Google Play button
                        with ui.button().classes('w-full sm:w-auto bg-black hover:bg-gray-900 text-white px-3 py-1 rounded flex items-center justify-center gap-1'):
                            ui.icon('android').classes('text-white text-sm')
                            ui.label('GET IT ON Google Play').classes('text-xs')
            
            # Bottom section with links
            with ui.element('div').classes('border-t border-gray-700 mt-4 pt-4'):
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-4 gap-4 mb-4'):
                    # Quick Links
                    with ui.element('div'):
                        ui.label('Quick Links').classes('text-white font-semibold mb-2 text-sm')
                        with ui.element('div').classes('space-y-1 text-xs'):
                            ui.link('Home', '/').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('All Products', '/').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Categories', '/').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Sell Now', '/add_event').classes('block text-gray-300 hover:text-primary-light no-underline')
                    
                    # Customer Service
                    with ui.element('div'):
                        ui.label('Customer Service').classes('text-white font-semibold mb-2 text-sm')
                        with ui.element('div').classes('space-y-1 text-xs'):
                            ui.link('Help Center', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Contact Us', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Shipping Info', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Returns & Refunds', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                    
                    # About
                    with ui.element('div'):
                        ui.label('About').classes('text-white font-semibold mb-2 text-sm')
                        with ui.element('div').classes('space-y-1 text-xs'):
                            ui.link('About Us', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Careers', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Press', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                            ui.link('Blog', '#').classes('block text-gray-300 hover:text-primary-light no-underline')
                    
                    # Connect
                    with ui.element('div'):
                        ui.label('Connect With Us').classes('text-white font-semibold mb-2 text-sm')
                        with ui.row().classes('gap-2 mb-2'):
                            ui.button(icon='facebook').classes('bg-blue-600 hover:bg-blue-700 text-white rounded-full p-1').props('flat round')
                            ui.button(icon='twitter').classes('bg-blue-400 hover:bg-blue-500 text-white rounded-full p-1').props('flat round')
                            ui.button(icon='instagram').classes('bg-pink-600 hover:bg-pink-700 text-white rounded-full p-1').props('flat round')
                            ui.button(icon='linkedin').classes('bg-blue-800 hover:bg-blue-900 text-white rounded-full p-1').props('flat round')
                
                # Copyright
                with ui.element('div').classes('border-t border-gray-700 pt-3 text-center'):
                    ui.label('© 2024 InnoHub. All rights reserved.').classes('text-gray-400 text-xs')
