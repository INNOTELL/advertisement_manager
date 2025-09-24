import requests
import json
import asyncio
from typing import Dict, Any, Optional, Tuple
from nicegui import ui
from config import BACKEND_BASE_URL, OPENAPI_URL_CANDIDATES, API_ROUTES, SESSION_TTL_MIN

class APIClient:
    def __init__(self):
        self.base_url = BACKEND_BASE_URL
        self.token = None
        self.routes = API_ROUTES.copy()
        self.openapi_spec = None
        self._discovered = False
        # Ensure we always have fallback routes
        self._use_fallback_routes()
    
    async def discover_endpoints(self) -> bool:
        """Discover API endpoints from OpenAPI spec"""
        if self._discovered:
            return True
        
        print(f"🔍 Starting OpenAPI discovery from: {self.base_url}")
        
        for url in OPENAPI_URL_CANDIDATES:
            try:
                print(f"🌐 Trying OpenAPI URL: {url}")
                response = await asyncio.to_thread(requests.get, url, timeout=10)
                print(f"📡 OpenAPI response status: {response.status_code}")
                
                if response.status_code == 200:
                    spec = response.json()
                    if self._validate_openapi_spec(spec):
                        self.openapi_spec = spec
                        self._map_routes(spec)
                        self._discovered = True
                        print(f"✅ OpenAPI discovery successful from: {url}")
                        return True
                    else:
                        print(f"❌ Invalid OpenAPI spec from: {url}")
                else:
                    print(f"❌ HTTP {response.status_code} from: {url}")
            except Exception as e:
                print(f"❌ Failed to fetch OpenAPI from {url}: {e}")
                continue
        
        print("❌ OpenAPI discovery failed, using fallback routes")
        self._use_fallback_routes()
        return False
    
    def _validate_openapi_spec(self, spec: Dict[str, Any]) -> bool:
        """Validate OpenAPI spec structure"""
        required_fields = ["openapi", "info", "paths"]
        return all(field in spec for field in required_fields)
    
    def _map_routes(self, spec: Dict[str, Any]) -> None:
        """Map API routes from OpenAPI spec"""
        paths = spec.get("paths", {})
        
        print(f"🔍 Available paths: {list(paths.keys())}")
        
        # Auth endpoints - be more specific about matching
        for path, operations in paths.items():
            for method, operation in operations.items():
                if isinstance(operation, dict):
                    summary = operation.get("summary", "").lower()
                    operation_id = operation.get("operationId", "").lower()
                    combined = f"{summary} {operation_id} {path}".lower()
                    
                    print(f"🔍 Checking path: {path} {method} - {combined}")
                    
                    # Auth routes - be more specific
                    if method == "post":
                        if any(keyword in combined for keyword in ["login", "signin", "authenticate"]) and not any(bad in combined for bad in ["logout", "signout"]):
                            self.routes["auth"]["signin"] = path
                            print(f"✅ Found signin: {path}")
                        
                        elif any(keyword in combined for keyword in ["signup", "register", "create user"]) and not any(bad in combined for bad in ["login", "signin"]):
                            self.routes["auth"]["signup"] = path
                            print(f"✅ Found signup: {path}")
                    
                    elif method == "get":
                        if any(keyword in combined for keyword in ["me", "profile", "current user"]) and not any(bad in combined for bad in ["recommendations", "ads", "list"]):
                            self.routes["auth"]["me"] = path
                            print(f"✅ Found me: {path}")
                    
                    # Ads routes
                    elif "/ads" in path or "/advertisements" in path or "/adverts" in path:
                        if method == "get" and "{" not in path and "list" in combined:
                            self.routes["ads"]["list"] = path
                            print(f"✅ Found ads list: {path}")
                        elif method == "post" and "create" in combined:
                            self.routes["ads"]["create"] = path
                            print(f"✅ Found ads create: {path}")
                        elif "{" in path:
                            if method == "get" and "detail" in combined:
                                self.routes["ads"]["detail"] = path
                                print(f"✅ Found ads detail: {path}")
                            elif method in ["patch", "put"] and "update" in combined:
                                self.routes["ads"]["update"] = path
                                print(f"✅ Found ads update: {path}")
        
        print(f"🔍 Final discovered routes: {self.routes}")
    
    def _use_fallback_routes(self) -> None:
        """Use fallback routes if discovery fails"""
        self.routes = {
            "auth": {
                "signin": "/auth/login",
                "signup": "/auth/register", 
                "me": "/auth/me"
            },
            "ads": {
                "list": "/adverts",
                "create": "/adverts",
                "detail": "/adverts/{id}",
                "update": "/adverts/{id}"
            }
        }
    
    def set_token(self, token: str) -> None:
        """Set authentication token"""
        self.token = token
        # Store in localStorage for persistence
        try:
            if hasattr(ui.context, 'client') and ui.context.client:
                ui.run_javascript(f'localStorage.setItem("auth_token", "{token}")')
        except:
            pass  # Ignore if not in UI context
    
    def clear_token(self) -> None:
        """Clear authentication token"""
        self.token = None
        try:
            if hasattr(ui.context, 'client') and ui.context.client:
                ui.run_javascript('localStorage.removeItem("auth_token")')
        except:
            pass  # Ignore if not in UI context
    
    def get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    async def request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Tuple[bool, Any]:
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            headers = self.get_headers()
            
            print(f"🌐 HTTP {method} {url}")
            print(f"📋 Headers: {headers}")
            if data:
                print(f"📤 Data: {data}")
            
            response = await asyncio.to_thread(
                requests.request,
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=30
            )
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📥 Response headers: {dict(response.headers)}")
            
            # Handle authentication errors
            if response.status_code in [401, 403]:
                self.clear_token()
                ui.notify("Session expired, please sign in again", type="negative")
                ui.navigate.to(f"/login?next={ui.context.client.request.path}")
                return False, None
            
            # Handle other errors
            if response.status_code >= 400:
                error_msg = "Request failed"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", error_data.get("message", error_msg))
                    print(f"❌ Error response: {error_data}")
                except:
                    error_msg = response.text or error_msg
                    print(f"❌ Error text: {error_msg}")
                
                ui.notify(f"Error: {error_msg}", type="negative")
                return False, error_msg
            
            # Success
            try:
                result = response.json()
                print(f"✅ Success response: {result}")
                return True, result
            except:
                result = response.text
                print(f"✅ Success text: {result}")
                return True, result
                
        except Exception as e:
            print(f"❌ Request exception: {e}")
            ui.notify(f"Network error: {str(e)}", type="negative")
            return False, str(e)
    
    # Auth methods
    async def signup(self, name: str, email: str, password: str, role: str) -> Tuple[bool, Any]:
        """Sign up new user"""
        endpoint = self.routes["auth"]["signup"]
        if not endpoint:
            print("❌ No signup endpoint found!")
            return False, "No signup endpoint configured"
        
        # Backend expects email as query param, username/password as form data
        params = {
            "email": email
        }
        data = {
            "username": name,
            "password": password
        }
        print(f"🌐 Making signup request to: {self.base_url}{endpoint}")
        print(f"📤 Request params: {params}")
        print(f"📤 Request data: {data}")
        
        # Use form data instead of JSON
        try:
            url = f"{self.base_url}{endpoint}"
            response = await asyncio.to_thread(
                requests.post,
                url=url,
                params=params,
                data=data,  # Form data, not JSON
                timeout=30
            )
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📥 Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success response: {result}")
                return True, result
            else:
                error_msg = "Request failed"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", error_data.get("message", error_msg))
                except:
                    error_msg = response.text or error_msg
                
                print(f"❌ Error response: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            print(f"❌ Request exception: {e}")
            return False, str(e)
    
    async def signin(self, email: str, password: str) -> Tuple[bool, Any]:
        """Sign in user"""
        endpoint = self.routes["auth"]["signin"]
        if not endpoint:
            print("❌ No signin endpoint found!")
            return False, "No signin endpoint configured"
        
        # Backend expects credentials as query parameters
        params = {
            "email": email,
            "password": password
        }
        print(f"🌐 Making signin request to: {self.base_url}{endpoint}")
        print(f"📤 Request params: {params}")
        
        try:
            url = f"{self.base_url}{endpoint}"
            response = await asyncio.to_thread(
                requests.post,
                url=url,
                params=params,
                timeout=30
            )
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📥 Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success response: {result}")
                return True, result
            else:
                error_msg = "Request failed"
                try:
                    error_data = response.json()
                    error_msg = error_data.get("detail", error_data.get("message", error_msg))
                except:
                    error_msg = response.text or error_msg
                
                print(f"❌ Error response: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            print(f"❌ Request exception: {e}")
            return False, str(e)
    
    async def get_profile(self) -> Tuple[bool, Any]:
        """Get current user profile"""
        endpoint = self.routes["auth"]["me"]
        return await self.request("GET", endpoint)
    
    # Ads methods
    async def get_ads(self, params: Optional[Dict] = None) -> Tuple[bool, Any]:
        """Get list of ads"""
        endpoint = self.routes["ads"]["list"]
        return await self.request("GET", endpoint, params=params)
    
    async def create_ad(self, ad_data: Dict) -> Tuple[bool, Any]:
        """Create new ad"""
        endpoint = self.routes["ads"]["create"]
        return await self.request("POST", endpoint, ad_data)
    
    async def get_ad(self, ad_id: str) -> Tuple[bool, Any]:
        """Get ad details"""
        endpoint = self.routes["ads"]["detail"].format(id=ad_id)
        return await self.request("GET", endpoint)
    
    async def update_ad(self, ad_id: str, ad_data: Dict) -> Tuple[bool, Any]:
        """Update ad"""
        endpoint = self.routes["ads"]["update"].format(id=ad_id)
        return await self.request("PATCH", endpoint, ad_data)
    
    async def delete_ad(self, ad_id: str) -> Tuple[bool, Any]:
        """Delete ad"""
        endpoint = self.routes["ads"]["detail"].format(id=ad_id)
        return await self.request("DELETE", endpoint)

# Global API client instance
api_client = APIClient()
