from nicegui import ui
from utils.auth import signup

def show_vendor_signup():
    ui.add_head_html('''
    <style>
        body {
            background-color: #f0f2f5;
        }
    </style>
''')
    ui.query(".nicegui-content").classes("m-0 p-0")
    
    with ui.element('div').classes('min-h-screen flex items-center justify-center p-4'):
        with ui.card().classes('w-full max-w-md bg-white shadow-xl rounded-2xl p-8'):
            ui.label('Vendor Sign Up').classes('text-3xl font-bold text-orange-900 text-center mb-6')
            
            # Form fields
            username_input = ui.input(placeholder='Username').props('outlined rounded-md dense').classes('w-full mb-4')
            email_input = ui.input(placeholder='Email').props('type=email outlined rounded-md dense').classes('w-full mb-4')
            password_input = ui.input(placeholder='Password', password=True, password_toggle_button=True).props('outlined rounded-md dense').classes('w-full mb-4')
            confirm_password_input = ui.input(placeholder='Confirm Password', password=True, password_toggle_button=True).props('outlined rounded-md dense').classes('w-full mb-4')
            
            # Terms checkbox
            terms_checkbox = ui.checkbox(text="I agree to the terms and conditions").classes('mb-6')
            
            # Signup button
            async def handle_vendor_signup():
                username = username_input.value.strip()
                email = email_input.value.strip()
                password = password_input.value
                confirm_password = confirm_password_input.value
                
                # Validation
                if not all([username, email, password, confirm_password]):
                    ui.notify('Please fill in all fields', type='negative')
                    return
                
                if not terms_checkbox.value:
                    ui.notify('Please accept the terms and conditions', type='negative')
                    return
                
                if password != confirm_password:
                    ui.notify('Passwords do not match', type='negative')
                    return
                
                if len(password) < 8:
                    ui.notify('Password must be at least 8 characters', type='negative')
                    return
                
                # Signup as vendor
                ui.notify('Creating your vendor account...', type='info')

                success, details = await signup(username, email, password, 'Vendor')
                details = details or {}
                if success:
                    auto_login = details.get('auto_login', False)
                    if auto_login:
                        ui.notify('Vendor account created and logged in successfully!', type='positive')
                        ui.navigate.to('/vendor/dashboard')
                    else:
                        ui.notify('Vendor account created successfully! Please sign in.', type='positive')
                        ui.navigate.to('/vendor/signin')
                else:
                    error_msg = details.get('error') if isinstance(details, dict) else str(details)
                    if not error_msg:
                        error_msg = 'Email might already exist. Please try again.'
                    ui.notify(f"Signup failed: {error_msg}", type='negative')
            
            ui.button('Sign Up as Vendor', on_click=handle_vendor_signup).classes('w-full bg-orange-500 hover:bg-orange-600 text-white py-3 px-6 rounded-lg font-semibold mb-4')
            
            # Links
            with ui.element('div').classes('text-center space-y-2'):
                ui.link('Already have an account? Sign In', '/vendor/signin').classes('text-orange-600 hover:text-orange-800')
                ui.link('Back to Home', '/').classes('text-gray-600 hover:text-gray-800')


