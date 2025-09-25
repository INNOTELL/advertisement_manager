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
    
    # Check for existing auth in localStorage first
    try:
        # Check if we have auth data in localStorage
        try:
            token = ui.run_javascript('return localStorage.getItem("auth_token")')
            is_authenticated = ui.run_javascript('return localStorage.getItem("is_authenticated")')
            user_data_str = ui.run_javascript('return localStorage.getItem("user_data")')
        except (RuntimeError, AttributeError):
            print("⚠️ Could not access localStorage - not in UI context")
            token = None
            is_authenticated = None
            user_data_str = None
        
        if token and is_authenticated == "true" and user_data_str:
            import json
            try:
                user_data = json.loads(user_data_str)
                print(f" Found existing auth in localStorage: {token[:20]}...")
                print(f"👤 User data: {user_data}")
                
                # Set the token in API client
                api_client.set_token(token)
                
                # Restore auth state
                auth_state.set_user(user_data, token)
                
                print(f"✅ Auth state restored: {auth_state.is_authenticated}, user: {auth_state.name}")
                return True
            except json.JSONDecodeError:
                print("⚠️ Invalid user data in localStorage")
        else:
            print("ℹ️ No existing auth found in storage")
    except Exception as e:
        print(f"⚠️ Could not check storage: {e}")
    
    # Fallback: Try to restore session from localStorage (legacy)
    try:
        # Check if we're in a UI context
        if hasattr(ui.context, 'client') and ui.context.client:
            try:
                token = ui.run_javascript('return localStorage.getItem("auth_token")')
                if token and token != "null":
                    api_client.set_token(token)
                    success, profile = await api_client.get_profile()
                    if success and profile:
                        auth_state.set_user(profile, token)
                        print(f"✅ Legacy session restored for user: {auth_state.email}")
                        return True
                    else:
                        auth_state.clear()
                        print("❌ Legacy session restoration failed")
            except (RuntimeError, AttributeError):
                print("⚠️ Could not access localStorage - not in UI context")
            else:
                print("ℹ️ No legacy token found")
        else:
            print("ℹ️ Not in UI context, skipping session restoration")
    except Exception as e:
        print(f"❌ Auth initialization error: {e}")
        # Don't clear auth_state here as it might not be initialized yet
    
    return False

async def refresh_auth_state():
    """Force refresh authentication state"""
    try:
        if hasattr(ui.context, 'client') and ui.context.client:
            token = ui.run_javascript('return localStorage.getItem("auth_token")')
            if token and token != "null":
                api_client.set_token(token)
                success, profile = await api_client.get_profile()
                if success and profile:
                    auth_state.set_user(profile, token)
                    print(f"✅ Auth state refreshed for user: {auth_state.email}")
                    return True
                else:
                    auth_state.clear()
                    print("❌ Auth state refresh failed")
                    return False
            else:
                auth_state.clear()
                print("ℹ️ No token found, clearing auth state")
                return False
    except Exception as e:
        print(f"❌ Auth state refresh error: {e}")
        return False

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
                
                # UI notifications handled by signup handlers
                # Redirect to login since signup doesn't return a token
                ui.navigate.to("/login")
                return True
            else:
                # UI notifications handled by signup handlers
                ui.navigate.to("/login")
                return True
        else:
            return False
    except Exception as e:
        # UI notifications handled by signup handlers
        return False

async def signin(email: str, password: str) -> bool:
    """Sign in user"""
    try:
        # Ensure API discovery has run
        if not api_client._discovered:
            print(" API discovery not completed, running now...")
            await api_client.discover_endpoints()
        
        print(f"🔑 Attempting signin for: {email}")
        print(f"📋 Using signin endpoint: {api_client.routes['auth']['signin']}")
        
        success, response = await api_client.signin(email, password)
        print(f"📡 Signin response: success={success}, response={response}")
        
        if success and response:
            if isinstance(response, dict):
                token = response.get("access_token") or response.get("token")
                
                # Extract user info from response
                # The backend response format: {"message": "Welcome back, testuser!", "access_token": "...", "role": "Buyer"}
                message = response.get("message", "")
                username = "User"  # Default
                if "Welcome back," in message:
                    # Extract username from "Welcome back, username!"
                    username = message.split("Welcome back, ")[1].split("!")[0] if "Welcome back," in message else email.split("@")[0]
                
                # Extract role from JWT token if not in response
                role = response.get("role", "buyer")
                if not role or role == "buyer":
                    # Try to decode JWT token to get role
                    try:
                        import base64
                        import json
                        token_parts = token.split('.')
                        if len(token_parts) >= 2:
                            payload = token_parts[1]
                            # Add padding if needed
                            payload += '=' * (4 - len(payload) % 4)
                            decoded = base64.b64decode(payload)
                            token_data = json.loads(decoded)
                            token_role = token_data.get('role', 'User')
                            # Map backend roles to frontend roles
                            if token_role.lower() == 'user':
                                role = 'buyer'
                            elif token_role.lower() == 'vendor':
                                role = 'vendor'
                            else:
                                role = token_role.lower()
                    except Exception as e:
                        print(f"⚠️ Could not decode JWT token: {e}")
                        role = "buyer"  # Default fallback
                
                user_data = {
                    "id": None,  # Backend doesn't return user_id in login response
                    "name": username,
                    "email": email,  # Use the email from login
                    "role": role.lower()
                }
                
                print(f"🎫 Token found: {bool(token)}")
                print(f"👤 User data: {user_data}")
                
                if token:
                    auth_state.set_user(user_data, token)
                    print(f"✅ Auth state set: {auth_state.is_authenticated}, user: {auth_state.name}, email: {auth_state.email}")
                    # UI notifications handled by login handlers
                    print(f"✅ Login successful for: {auth_state.email}")
                    return True
                else:
                    # UI notifications handled by login handlers
                    return False
            else:
                # UI notifications handled by login handlers
                return False
        else:
            # Check if it's a "user not found" error
            error_msg = str(response) if response else "Unknown error"
            print(f"❌ Login failed: {error_msg}")
            
            # UI notifications handled by login handlers
            return False
    except Exception as e:
        print(f"❌ Signin error: {e}")
        # UI notifications handled by login handlers
        return False

def logout():
    """Logout user"""
    # Clear auth state
    auth_state.clear()
    
    # Clear storage
    try:
        # Clear localStorage
        ui.run_javascript('localStorage.removeItem("auth_token")')
        ui.run_javascript('localStorage.removeItem("user_data")')
        ui.run_javascript('localStorage.removeItem("is_authenticated")')
        print("✅ Auth storage cleared")
    except Exception as e:
        print(f"⚠️ Could not clear storage: {e}")
    
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
