from nicegui import ui
from utils.auth import signup, signin, normalize_role
from config import USER_ROLES
from utils.api_client import api_client

def show_login_page(login_user=None, auth_state=None):
    if auth_state and auth_state.is_authenticated:
        next_path = ui.context.client.request.query_params.get('next', '/')
        ui.navigate.to(next_path)
        return

    with ui.element('div').classes('min-h-screen w-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 flex items-center justify-center p-4'):
        with ui.element('div').classes('w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden mx-auto flex items-center justify-center'):
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 min-h-[500px]'):
                # Left Column - Enhanced Branding with Better Visibility
                with ui.element('div').classes('bg-gradient-to-br from-blue-600 via-blue-500 to-blue-700 p-8 flex flex-col justify-center text-white relative overflow-hidden'):
                    # Enhanced decorative elements
                    with ui.element('div').classes('absolute top-4 right-4 w-20 h-20 bg-white/20 rounded-full blur-sm'):
                        pass
                    with ui.element('div').classes('absolute bottom-4 left-4 w-16 h-16 bg-white/20 rounded-full blur-sm'):
                        pass
                    with ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-white/10 rounded-full blur-lg'):
                        pass
                    
                    # Dark overlay for better text contrast
                    with ui.element('div').classes('absolute inset-0 bg-black/20'):
                        pass
                    
                    with ui.element('div').classes('relative z-10 text-center lg:text-left'):
                        with ui.element('div').classes('flex items-center justify-center lg:justify-start gap-2 mb-6'):
                            ui.label('INNO').classes('text-3xl font-bold text-white drop-shadow-lg')
                            ui.icon('star').classes('text-blue-300 text-2xl drop-shadow-lg')
                            ui.label('HUB').classes('text-3xl font-bold text-white drop-shadow-lg')
                        
                        ui.label('Welcome Back!').classes('text-2xl font-bold mb-4 text-white drop-shadow-md')
                        ui.label('Sign in to your account and continue your journey with InnoHub Ghana.').classes('text-white/90 text-base leading-relaxed mb-6 font-medium')
                        ui.label('Buy and Sell with confidence').classes('text-white text-base font-semibold drop-shadow-md')
                
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
                    

                    login_button_ref = {}

                    async def handle_login():
                        email = email_input.value.strip()
                        password = password_input.value

                        if not email or not password:
                            ui.notify("Please enter both email and password", type="negative")
                            return

                        import re
                        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                        if not re.match(email_pattern, email):
                            ui.notify("Please enter a valid email address", type="negative")
                            return

                        if len(password) < 8:
                            ui.notify("Password must be at least 8 characters", type="negative")
                            return

                        btn = login_button_ref.get('button')
                        if btn:
                            btn.disable()
                            btn.props('loading')

                        try:
                            ui.notify("Logging in...", type="info")

                            if not api_client._discovered:
                                await api_client.discover_endpoints()

                            success, response = await api_client.signin(email, password)

                            if success and isinstance(response, dict):
                                token = response.get('access_token') or response.get('token')
                                message = response.get('message', '')

                                if token:
                                    username = 'User'
                                    if 'Welcome back,' in message:
                                        username = message.split('Welcome back, ')[1].split('!')[0] if 'Welcome back,' in message else email.split('@')[0]

                                    raw_role = response.get('role')
                                    role = normalize_role(raw_role)
                                    if not raw_role:
                                        try:
                                            import base64
                                            import json as json_lib
                                            parts = token.split('.')
                                            if len(parts) >= 2:
                                                payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
                                                decoded = base64.b64decode(payload)
                                                token_data = json_lib.loads(decoded)
                                                token_role = token_data.get('role')
                                                if token_role:
                                                    role = normalize_role(token_role)
                                        except Exception as exc:
                                            print(f"Could not decode JWT token: {exc}")
                                            role = normalize_role(USER_ROLES['BUYER'])

                                    user_data = {
                                        'id': response.get('id'),
                                        'name': username,
                                        'email': email,
                                        'role': role,
                                    }

                                    auth_state.set_user(user_data, token)

                                    import json
                                    token_js = json.dumps(token)
                                    user_data_js = json.dumps(user_data)
                                    ui.run_javascript(f'localStorage.setItem("auth_token", {token_js})')
                                    ui.run_javascript(f'localStorage.setItem("user_data", {user_data_js})')
                                    ui.run_javascript('localStorage.setItem("is_authenticated", "true")')

                                    ui.notify("Logged in successfully!", type="positive")

                                    email_input.value = ''
                                    password_input.value = ''

                                    default_path = '/dashboard' if auth_state.is_vendor() else '/'
                                    next_path = ui.context.client.request.query_params.get('next') or default_path
                                    ui.navigate.to(next_path)
                                    return
                                else:
                                    ui.notify("Login failed: No token received", type="negative")
                            else:
                                error_msg = str(response) if response else 'Unknown error'
                                if 'does not exist' in error_msg.lower():
                                    ui.notify("Login failed: User does not exist. Please check your email or create an account.", type="negative")
                                else:
                                    ui.notify(f"Login failed: {error_msg[:100]}", type="negative")
                        except Exception as exc:
                            print(f"Login error: {exc}")
                            ui.notify(f"Login failed: {str(exc)[:100]}", type="negative")
                        finally:
                            if btn:
                                btn.enable()
                                btn.props(remove='loading')

                    login_button_ref['button'] = ui.button('Sign In', on_click=handle_login, icon='login').classes('w-full h-12 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 text-sm sm:text-base')

                    with ui.element('div').classes('text-center mt-4'):
                        ui.label('Don\'t have an account? ').classes('text-gray-600 text-sm')
                        ui.link('Create one here', '/signup').classes('text-blue-600 hover:text-blue-700 font-semibold text-sm no-underline')
                    
                    with ui.element('div').classes('text-center mt-4 text-xs text-gray-500'):
                        ui.label('By continuing you agree to InnoHub\'s ').classes('text-xs text-gray-500')
                        ui.link('Terms and Conditions', '#').classes('text-xs text-blue-600 hover:text-blue-700 no-underline')

def show_signup_page(signup_user=None):
    with ui.element('div').classes('min-h-screen w-screen bg-gradient-to-br from-gray-50 via-white to-gray-50 flex items-center justify-center p-4'):
        with ui.element('div').classes('w-full max-w-4xl bg-white rounded-2xl shadow-2xl overflow-hidden mx-auto'):
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 min-h-[600px]'):
                # Left Column - Enhanced Branding with Better Visibility
                with ui.element('div').classes('bg-gradient-to-br from-blue-600 via-blue-500 to-blue-700 p-8 flex flex-col justify-center text-white relative overflow-hidden'):
                    # Enhanced decorative elements
                    with ui.element('div').classes('absolute top-4 right-4 w-20 h-20 bg-white/20 rounded-full blur-sm'):
                        pass
                    with ui.element('div').classes('absolute bottom-4 left-4 w-16 h-16 bg-white/20 rounded-full blur-sm'):
                        pass
                    with ui.element('div').classes('absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-white/10 rounded-full blur-lg'):
                        pass
                    
                    # Dark overlay for better text contrast
                    with ui.element('div').classes('absolute inset-0 bg-black/20'):
                        pass
                    
                    with ui.element('div').classes('relative z-10 text-center lg:text-left'):
                        with ui.element('div').classes('flex items-center justify-center lg:justify-start gap-2 mb-6'):
                            ui.label('INNO').classes('text-3xl font-bold text-white drop-shadow-lg')
                            ui.icon('star').classes('text-blue-300 text-2xl drop-shadow-lg')
                            ui.label('HUB').classes('text-3xl font-bold text-white drop-shadow-lg')
                        
                        ui.label('Join InnoHub!').classes('text-2xl font-bold mb-4 text-white drop-shadow-md')
                        ui.label('Create your account and start your journey with Ghana\'s premier marketplace. Buy and sell with confidence!').classes('text-white/90 text-base leading-relaxed mb-6 font-medium')
                        ui.label('Join thousands of happy users').classes('text-white text-base font-semibold drop-shadow-md')
                
                # Right Column - Signup Form
                with ui.element('div').classes('p-8 flex flex-col justify-center'):
                    with ui.element('div').classes('text-center mb-6'):
                        ui.label('Create Account').classes('text-2xl font-bold text-gray-800 mb-2')
                        ui.label('Fill in your details to get started').classes('text-gray-600 text-sm')
                    
                    with ui.element('div').classes('space-y-3 mb-6'):
                        with ui.element('div').classes('relative'):
                            ui.icon('person').classes('absolute left-3 top-4 text-gray-400')
                            username_input = ui.input('Username*').classes('w-full h-12 pl-12 pr-4 border border-gray-300 rounded-lg focus:border-primary focus:ring-2 focus:ring-primary/20 bg-gray-50 focus:bg-white transition-all')
                        
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
                            ui.label('Account Type*').classes('text-sm font-medium text-gray-700 mb-2')
                            with ui.element('div').classes('space-y-2'):
                                role_radio_buyer = ui.radio(['Buyer', 'Vendor'], value='Buyer').classes('flex items-center gap-2')
                                ui.label('Buyer - Browse and purchase products').classes('text-xs text-gray-500 ml-6')
                                ui.label('Vendor - Sell products and manage inventory').classes('text-xs text-gray-500 ml-6')
                    
                    async def handle_signup():
                        username = username_input.value.strip()
                        email = email_input.value.strip()
                        password = password_input.value
                        confirm_password = confirm_password_input.value
                        role = normalize_role(role_radio_buyer.value)

                        if not all([username, email, password, confirm_password]):
                            ui.notify('Please fill in all fields', type='negative')
                            return

                        # Email validation
                        import re
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_pattern, email):
                            ui.notify('Please enter a valid email address', type='negative')
                            return

                        # Password validation
                        if len(password) < 8:
                            ui.notify('Password must be at least 8 characters', type='negative')
                            return

                        if password != confirm_password:
                            ui.notify('Passwords do not match', type='negative')
                            return

                        # Username validation
                        if len(username) < 6:
                            ui.notify('Username must be at least 6 characters', type='negative')
                            return

                        ui.notify('Creating your account...', type='info')

                        success, details = await signup(username, email, password, role)
                        details = details or {}
                        if success:
                            auto_login = details.get('auto_login', False)
                            if auto_login:
                                ui.notify('Account created and logged in successfully!', type='positive')
                                next_path = ui.context.client.request.query_params.get('next', '/dashboard')
                            else:
                                ui.notify('Account created successfully! Please sign in.', type='positive')
                                next_path = '/login'
                            ui.navigate.to(next_path)
                        else:
                            error_msg = details.get('error') if isinstance(details, dict) else str(details)
                            if not error_msg:
                                error_msg = 'Email might already exist. Please try again.'
                            ui.notify(f"Signup failed: {error_msg}", type='negative')

                    ui.button('Create Account', on_click=handle_signup, icon='person_add').classes('w-full h-12 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 text-sm sm:text-base')
                    
                    with ui.element('div').classes('text-center mt-4'):
                        ui.label('Already have an account? ').classes('text-gray-600 text-sm')
                        ui.link('Sign in here', '/login').classes('text-blue-600 hover:text-blue-700 font-semibold text-sm no-underline')
                    
                    with ui.element('div').classes('text-center mt-4 text-xs text-gray-500'):
                        ui.label("By creating an account, you agree to InnoHub's ").classes('text-xs text-gray-500')
                        ui.link('Terms and Conditions', '#').classes('text-xs text-blue-600 hover:text-blue-700 no-underline')
                        ui.label(' and ').classes('text-xs text-gray-500')
                        ui.link('Privacy Policy', '#').classes('text-xs text-blue-600 hover:text-blue-700 no-underline')
                        
