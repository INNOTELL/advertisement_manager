from nicegui import ui

def show_login_page(login_user=None, auth_state=None):
    with ui.element('div').classes('min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 flex items-center justify-center p-4'):
        with ui.element('div').classes('w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden mx-auto flex items-center justify-center'):
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 min-h-[500px]'):
                # Left Column - Branding
                with ui.element('div').classes('bg-gradient-to-br from-primary to-primary-dark p-8 flex flex-col justify-center text-white relative'):
                    with ui.element('div').classes('absolute top-4 right-4 w-20 h-20 bg-white/10 rounded-full'):
                        pass
                    with ui.element('div').classes('absolute bottom-4 left-4 w-16 h-16 bg-white/10 rounded-full'):
                        pass
                    
                    with ui.element('div').classes('relative z-10 text-center lg:text-left'):
                        with ui.element('div').classes('flex items-center justify-center lg:justify-start gap-2 mb-4'):
                            ui.label('INNO').classes('text-2xl font-bold text-white')
                            ui.icon('star').classes('text-yellow-300 text-xl')
                            ui.label('HUB').classes('text-2xl font-bold text-white')
                        ui.label('Welcome Back!').classes('text-xl font-bold mb-3')
                        ui.label('Sign in to your account and continue your journey with InnoHub Ghana.').classes('text-white/80 text-sm leading-relaxed mb-4')
                        ui.label('🛒 Buy and Sell with confidence').classes('text-yellow-200 text-sm font-medium')
                
                # Right Column - Login Form
                with ui.element('div').classes('p-8 flex flex-col justify-center'):
                    with ui.element('div').classes('text-center mb-6'):
                        ui.label('Sign In').classes('text-2xl font-bold text-gray-800 mb-2')
                        ui.label('Enter your credentials to access your account').classes('text-gray-600 text-sm')
                    
                    with ui.element('div').classes('space-y-4 mb-6'):
                        with ui.element('div').classes('relative'):
                            ui.icon('email').classes('absolute left-3 top-4 text-gray-400')
                            email_input = ui.input('Email or Mobile Number*').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all')
                        
                        with ui.element('div').classes('relative'):
                            ui.icon('lock').classes('absolute left-3 top-4 text-gray-400')
                            password_input = ui.input('Password*').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all').props('type=password')
                    
                    def handle_login():
                        email = email_input.value.strip()
                        password = password_input.value
                        
                        if not email or not password:
                            ui.notify('Please enter both email and password', type='negative')
                            return
                        
                        # Accept any email or phone format for testing
                        import re
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        phone_pattern = r'^(\+233|0)[0-9]{9}$'
                        simple_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$'
                        simple_phone = r'^[0-9]{10,15}$'
                        
                        # Accept any reasonable email or phone format
                        if not (re.match(email_pattern, email) or re.match(phone_pattern, email) or 
                               re.match(simple_email, email) or re.match(simple_phone, email) or
                               len(email) >= 3):  # Accept any input with at least 3 characters
                            ui.notify('Please enter a valid email or phone number', type='negative')
                            return
                        
                        # Accept any password with at least 3 characters
                        if len(password) < 3:
                            ui.notify('Password must be at least 3 characters', type='negative')
                            return
                        
                        if login_user:
                            ui.notify('Logging in...', type='info')
                            # Use asyncio.create_task for proper async handling
                            try:
                                import asyncio
                                
                                async def handle_login_async():
                                    success = await login_user(email, password)
                                    if success:
                                        ui.notify('Login successful! Welcome back!', type='positive')
                                        # Small delay to ensure state is set
                                        import time
                                        time.sleep(0.1)
                                        ui.navigate.to('/dashboard')
                                    else:
                                        ui.notify('Login failed. Please check your credentials.', type='negative')
                                
                                # Create task instead of using run_until_complete
                                asyncio.create_task(handle_login_async())
                                
                            except Exception as e:
                                ui.notify(f'Login error: {str(e)}', type='negative')
                        else:
                            ui.notify('Login function not available', type='negative')
                    
                    ui.button('Sign In', on_click=handle_login, icon='login').classes('w-full h-12 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 text-sm sm:text-base')
                    
                    with ui.element('div').classes('text-center mt-4'):
                        ui.label('Don\'t have an account? ').classes('text-gray-600 text-sm')
                        ui.link('Create one here', '/signup').classes('text-primary hover:text-primary-dark font-semibold text-sm no-underline')
                    
                    with ui.element('div').classes('space-y-3 mt-4'):
                        ui.button('Facebook', icon='facebook').classes('w-full h-12 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg flex items-center justify-center gap-2 text-sm sm:text-base')
                        ui.button('Google', icon='google').classes('w-full h-12 bg-white hover:bg-gray-50 text-gray-700 font-medium rounded-lg border border-gray-300 flex items-center justify-center gap-2 text-sm sm:text-base')
                    
                    with ui.element('div').classes('text-center mt-4 text-xs text-gray-500'):
                        ui.label('By continuing you agree to InnoHub\'s ').classes('text-xs text-gray-500')
                        ui.link('Terms and Conditions', '#').classes('text-xs text-primary hover:text-primary-dark no-underline')

def show_signup_page(signup_user=None):
    with ui.element('div').classes('min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 flex items-center justify-center p-4'):
        with ui.element('div').classes('w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden mx-auto'):
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 min-h-[600px]'):
                # Left Column - Branding
                with ui.element('div').classes('bg-gradient-to-br from-primary to-primary-dark p-8 flex flex-col justify-center text-white relative'):
                    with ui.element('div').classes('absolute top-4 right-4 w-20 h-20 bg-white/10 rounded-full'):
                        pass
                    with ui.element('div').classes('absolute bottom-4 left-4 w-16 h-16 bg-white/10 rounded-full'):
                        pass
                    
                    with ui.element('div').classes('relative z-10 text-center lg:text-left'):
                        with ui.element('div').classes('flex items-center justify-center lg:justify-start gap-2 mb-4'):
                            ui.label('INNO').classes('text-2xl font-bold text-white')
                            ui.icon('star').classes('text-yellow-300 text-xl')
                            ui.label('HUB').classes('text-2xl font-bold text-white')
                        ui.label('Join InnoHub!').classes('text-xl font-bold mb-3')
                        ui.label('Create your account and start your journey with Ghana\'s premier marketplace. Buy and sell with confidence!').classes('text-white/80 text-sm leading-relaxed mb-4')
                        ui.label('🌟 Join thousands of happy users').classes('text-yellow-200 text-sm font-medium')
                
                # Right Column - Signup Form
                with ui.element('div').classes('p-8 flex flex-col justify-center'):
                    with ui.element('div').classes('text-center mb-6'):
                        ui.label('Create Account').classes('text-2xl font-bold text-gray-800 mb-2')
                        ui.label('Fill in your details to get started').classes('text-gray-600 text-sm')
                    
                    with ui.element('div').classes('space-y-3 mb-6'):
                        with ui.element('div').classes('relative'):
                            ui.icon('person').classes('absolute left-3 top-4 text-gray-400')
                            username_input = ui.input('Full Name*').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all')
                        
                        with ui.element('div').classes('relative'):
                            ui.icon('email').classes('absolute left-3 top-4 text-gray-400')
                            email_input = ui.input('Email Address*').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all')
                        
                        with ui.element('div').classes('relative'):
                            ui.icon('lock').classes('absolute left-3 top-4 text-gray-400')
                            password_input = ui.input('Password*').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all').props('type=password')
                        
                        with ui.element('div').classes('relative'):
                            ui.icon('lock').classes('absolute left-3 top-4 text-gray-400')
                            confirm_password_input = ui.input('Confirm Password*').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all').props('type=password')
                        
                        with ui.element('div').classes('relative'):
                            ui.icon('work').classes('absolute left-3 top-4 text-gray-400')
                            user_type_select = ui.select(['Buyer', 'Seller'], value='Buyer', label='Account Type').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all').props('outlined')
                    
                    def handle_signup():
                        username = username_input.value.strip()
                        email = email_input.value.strip()
                        password = password_input.value
                        confirm_password = confirm_password_input.value
                        
                        if not all([username, email, password, confirm_password]):
                            ui.notify('Please fill in all fields', type='negative')
                            return
                        
                        # Accept any reasonable email format for testing
                        import re
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        simple_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$'
                        
                        # Accept any email format or even simple text with @
                        if not (re.match(email_pattern, email) or re.match(simple_email, email) or 
                               '@' in email or len(email) >= 3):
                            ui.notify('Please enter a valid email address', type='negative')
                            return
                        
                        # Accept any password with at least 3 characters
                        if len(password) < 3:
                            ui.notify('Password must be at least 3 characters', type='negative')
                            return
                        
                        if password != confirm_password:
                            ui.notify('Passwords do not match', type='negative')
                            return
                        
                        # Accept any username with at least 2 characters
                        if len(username) < 2:
                            ui.notify('Username must be at least 2 characters', type='negative')
                            return
                        
                        if signup_user:
                            ui.notify('Creating your account...', type='info')
                            # Use asyncio.create_task for proper async handling
                            try:
                                import asyncio
                                
                                async def handle_signup_async():
                                    success = await signup_user(email, username, password)
                                    if success:
                                        ui.notify('Account created successfully! Welcome to InnoHub!', type='positive')
                                        ui.navigate.to('/login')
                                    else:
                                        ui.notify('Signup failed. Email might already exist. Please try again.', type='negative')
                                
                                # Create task instead of using run_until_complete
                                asyncio.create_task(handle_signup_async())
                                
                            except Exception as e:
                                ui.notify(f'Signup error: {str(e)}', type='negative')
                        else:
                            ui.notify('Signup function not available', type='negative')
                    
                    ui.button('Create Account', on_click=handle_signup, icon='person_add').classes('w-full h-12 bg-orange-500 hover:bg-orange-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 text-sm sm:text-base')
                    
                    with ui.element('div').classes('text-center mt-4'):
                        ui.label('Already have an account? ').classes('text-gray-600 text-sm')
                        ui.link('Sign in here', '/login').classes('text-primary hover:text-primary-dark font-semibold text-sm no-underline')
                    
                    with ui.element('div').classes('space-y-3 mt-4'):
                        ui.button('Facebook', icon='facebook').classes('w-full h-12 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg flex items-center justify-center gap-2 text-sm sm:text-base')
                        ui.button('Google', icon='google').classes('w-full h-12 bg-white hover:bg-gray-50 text-gray-700 font-medium rounded-lg border border-gray-300 flex items-center justify-center gap-2 text-sm sm:text-base')
                    
                    with ui.element('div').classes('text-center mt-4 text-xs text-gray-500'):
                        ui.label('By creating an account, you agree to InnoHub\'s ').classes('text-xs text-gray-500')
                        ui.link('Terms and Conditions', '#').classes('text-xs text-primary hover:text-primary-dark no-underline')
                        ui.label(' and ').classes('text-xs text-gray-500')
                        ui.link('Privacy Policy', '#').classes('text-xs text-primary hover:text-primary-dark no-underline')