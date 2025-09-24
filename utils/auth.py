import asyncio
from typing import Optional, Dict, Any
from nicegui import ui
from utils.api_client import api_client
from config import USER_ROLES

class AuthState:
    def __init__(self):
        self.is_authenticated = False
        self.user_id = None
        self.email = None
        self.name = None
        self.role = None
        self.token = None
    
    def set_user(self, user_data: Dict[str, Any], token: str):
        """Set user data from API response"""
        self.is_authenticated = True
        self.user_id = user_data.get("id")
        self.email = user_data.get("email")
        self.name = user_data.get("name") or user_data.get("username")
        self.role = user_data.get("role", "buyer")
        self.token = token
        api_client.set_token(token)
    
    def clear(self):
        """Clear user data"""
        self.is_authenticated = False
        self.user_id = None
        self.email = None
        self.name = None
        self.role = None
        self.token = None
        api_client.clear_token()
    
    def is_vendor(self) -> bool:
        """Check if user is a vendor"""
        return self.role == USER_ROLES["VENDOR"]
    
    def is_buyer(self) -> bool:
        """Check if user is a buyer"""
        return self.role == USER_ROLES["BUYER"]

# Global auth state
auth_state = AuthState()

async def initialize_auth():
    """Initialize authentication on app start"""
    # Discover API endpoints
    await api_client.discover_endpoints()
    
    # Try to restore session from localStorage (only if in UI context)
    try:
        # Check if we're in a UI context
        if hasattr(ui.context, 'client') and ui.context.client:
            token = ui.run_javascript('return localStorage.getItem("auth_token")')
            if token and token != "null":
                api_client.set_token(token)
                success, profile = await api_client.get_profile()
                if success and profile:
                    auth_state.set_user(profile, token)
                    print(f"✅ Session restored for user: {auth_state.email}")
                else:
                    auth_state.clear()
                    print("❌ Session restoration failed")
            else:
                print("ℹ️ No stored token found")
        else:
            print("ℹ️ Not in UI context, skipping session restoration")
    except Exception as e:
        print(f"❌ Auth initialization error: {e}")
        # Don't clear auth_state here as it might not be initialized yet

async def signup(name: str, email: str, password: str, role: str) -> bool:
    """Sign up new user"""
    try:
        success, response = await api_client.signup(name, email, password, role)
        if success:
            # Check if response contains user data
            if isinstance(response, dict):
                # Signup response contains user_id and role, but no token
                user_data = {
                    "id": response.get("user_id"),
                    "name": name,
                    "email": email,
                    "role": response.get("role", role).lower()
                }
                
                ui.notify(f"Account created successfully! Welcome to InnoHub, {name}!", type="positive")
                # Redirect to login since signup doesn't return a token
                ui.navigate.to("/login")
                return True
            else:
                ui.notify("Account created successfully! Please sign in.", type="positive")
                ui.navigate.to("/login")
                return True
        else:
            return False
    except Exception as e:
        ui.notify(f"Signup failed: {str(e)}", type="negative")
        return False

async def signin(email: str, password: str) -> bool:
    """Sign in user"""
    try:
        # Ensure API discovery has run
        if not api_client._discovered:
            print("🔍 API discovery not completed, running now...")
            await api_client.discover_endpoints()
        
        print(f"🔑 Attempting signin for: {email}")
        print(f"📋 Using signin endpoint: {api_client.routes['auth']['signin']}")
        
        success, response = await api_client.signin(email, password)
        print(f"📡 Signin response: success={success}, response={response}")
        
        if success:
            if isinstance(response, dict):
                token = response.get("access_token") or response.get("token")
                
                # Extract user info from response
                # The backend response format: {"message": "Welcome back, testuser!", "access_token": "...", "role": "Buyer"}
                message = response.get("message", "")
                username = "User"  # Default
                if "Welcome back," in message:
                    # Extract username from "Welcome back, username!"
                    username = message.split("Welcome back, ")[1].split("!")[0] if "Welcome back," in message else email.split("@")[0]
                
                user_data = {
                    "id": None,  # Backend doesn't return user_id in login response
                    "name": username,
                    "email": email,  # Use the email from login
                    "role": response.get("role", "buyer").lower()
                }
                
                print(f"🎫 Token found: {bool(token)}")
                print(f"👤 User data: {user_data}")
                
                if token:
                    auth_state.set_user(user_data, token)
                    try:
                        ui.notify(f"Welcome back, {auth_state.name}!", type="positive")
                    except:
                        pass  # Ignore UI context errors
                    print(f"✅ Login successful for: {auth_state.email}")
                    return True
                else:
                    try:
                        ui.notify("Invalid response from server - no token received", type="negative")
                    except:
                        pass
                    return False
            else:
                try:
                    ui.notify("Invalid response format from server", type="negative")
                except:
                    pass
                return False
        else:
            # Check if it's a "user not found" error
            if isinstance(response, str) and any(keyword in response.lower() for keyword in ["not found", "invalid", "incorrect"]):
                try:
                    ui.notify("We can't find your account. Create one?", type="warning")
                except:
                    pass
            else:
                try:
                    ui.notify(f"Login failed: {response}", type="negative")
                except:
                    pass
            return False
    except Exception as e:
        print(f"❌ Signin error: {e}")
        try:
            ui.notify(f"Signin failed: {str(e)}", type="negative")
        except:
            pass
        return False

def logout():
    """Logout user"""
    auth_state.clear()
    ui.notify("You have been signed out", type="info")
    ui.navigate.to("/")

def require_auth(role: Optional[str] = None):
    """Decorator to require authentication for routes"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not auth_state.is_authenticated:
                current_path = ui.context.client.request.path
                ui.navigate.to(f"/login?next={current_path}")
                return
            
            if role and auth_state.role != role:
                ui.notify("Insufficient permissions", type="negative")
                ui.navigate.to("/dashboard")
                return
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_vendor():
    """Require vendor role"""
    return require_auth(USER_ROLES["VENDOR"])

def require_buyer():
    """Require buyer role"""
    return require_auth(USER_ROLES["BUYER"])
