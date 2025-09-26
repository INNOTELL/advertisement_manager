import requests
import json
import asyncio
from typing import Dict, Any, Optional, Tuple
from nicegui import ui
from config import BACKEND_BASE_URL, OPENAPI_URL_CANDIDATES, API_ROUTES, SESSION_TTL_MIN
from utils.api import ai_api_key

class APIClient:
    def __init__(self):
        self.base_url = BACKEND_BASE_URL
        self.token = None
        self.routes = API_ROUTES.copy()
        self.openapi_spec = None
        self._discovered = False
        # Ensure we always have fallback routes
        self._use_fallback_routes()
        print(f"🔧 API Client initialized with fallback routes: {self.routes}")
    
    async def discover_endpoints(self) -> bool:
        """Discover API endpoints from OpenAPI spec"""
        if self._discovered:
            return True
        
        print(f"🔍 Starting OpenAPI discovery from: {self.base_url}")
        
        for url in OPENAPI_URL_CANDIDATES:
            try:
                print(f"🌐 Trying OpenAPI URL: {url}")
                response = await asyncio.to_thread(requests.get, url, timeout=30)
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
        self._discovered = True  # Mark as discovered even with fallback
        return True  # Return True since we have fallback routes
    
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
                            elif method == "delete":
                                self.routes["ads"]["delete"] = path
                                print(f"✅ Found ads delete: {path}")
        
        print(f"🔍 Final discovered routes: {self.routes}")
    
    def _use_fallback_routes(self) -> None:
        """Use fallback routes if discovery fails"""
        self.routes = {
            "auth": {
                "signin": "/Login",  # POST /Login with email/password as query params
                "signup": "/SignUp",  # POST /SignUp with email/role as query params, username/password in body
                "me": "/me"  # This might not exist, we'll handle it
            },
            "ads": {
                "list": "/adverts",  # GET /adverts
                "create": "/advert",  # POST /advert
                "detail": "/advert_details/{id}",  # GET /advert_details/{id}
                "update": "/edit_advert/{id}",  # PUT /edit_advert/{id}
                "delete": "/adverts/{id}"  # DELETE /adverts/{id}
            },
            "ai": {
                "generate_image": "/ai/generate-image",  # POST /ai/generate-image
                "text_generation": "/ai/generate-text"  # POST /ai/generate-text
            }
        }
    
    def set_token(self, token: str) -> None:
        """Set authentication token"""
        self.token = token
        # Store in localStorage for persistence - only in UI context
        try:
            # Check if we're in a proper UI context
            if (hasattr(ui.context, 'client') and 
                ui.context.client and 
                hasattr(ui.context.client, 'request')):
                ui.run_javascript(f'localStorage.setItem("auth_token", "{token}")')
        except Exception as e:
            print(f"⚠️ Could not access localStorage - not in UI context: {e}")
            pass  # Ignore if not in UI context
    
    def clear_token(self) -> None:
        """Clear authentication token"""
        self.token = None
        try:
            # Check if we're in a proper UI context
            if (hasattr(ui.context, 'client') and 
                ui.context.client and 
                hasattr(ui.context.client, 'request')):
                ui.run_javascript('localStorage.removeItem("auth_token")')
        except Exception as e:
            print(f"⚠️ Could not access localStorage - not in UI context: {e}")
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
                # Only show UI notifications if we're in a UI context
                try:
                    if response.status_code == 401:
                        ui.notify("Session expired, please sign in again", type="negative")
                    else:
                        ui.notify("Access denied. Please check your permissions.", type="negative")
                    ui.navigate.to(f"/login?next={ui.context.client.request.path}")
                except (RuntimeError, AttributeError):
                    # We're in a background task, just log the error
                    print("⚠️ Authentication error - not in UI context")
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
            # Only show UI notifications if we're in a UI context
            try:
                ui.notify(f"Network error: {str(e)}", type="negative")
            except (RuntimeError, AttributeError):
                # We're in a background task, just log the error
                print(f"⚠️ Network error - not in UI context: {e}")
            return False, str(e)
    
    # Auth methods
    async def signup(self, name: str, email: str, password: str, role: str) -> Tuple[bool, Any]:
        """Sign up new user"""
        endpoint = self.routes["auth"]["signup"]
        if not endpoint:
            print("❌ No signup endpoint found!")
            return False, "No signup endpoint configured"
        
        # According to backend API spec: email and role as query params, username/password as form data
        params = {
            "email": email,
            "role": role  # Backend expects "User" or "Vendor"
        }
        data = {
            "username": name,  # 6-20 characters
            "password": password  # minimum 8 characters
        }
        print(f"🌐 Making signup request to: {self.base_url}{endpoint}")
        print(f"📤 Request params: {params}")
        print(f"📤 Request data: {data}")
        
        # Use form data with query params (not JSON)
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
                
                # Extract and set token
                token = result.get('access_token') or result.get('token')
                if token:
                    self.set_token(token)
                    print(f"✅ Token set successfully")
                else:
                    print(f"⚠️ No token found in response")
                
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
        
        # Backend expects category and location as query params (from CategoryEnum and LocationEnum)
        params = {
            "category": ad_data.get("category"),  # Must be from CategoryEnum
            "location": ad_data.get("location")   # Must be from LocationEnum
        }
        
        # Backend expects multipart/form-data, not JSON
        try:
            url = f"{self.base_url}{endpoint}"
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}" if self.token else ""
            }
            
            print(f"🌐 HTTP POST {url}")
            print(f"📋 Headers: {headers}")
            print(f"📤 Params: {params}")
            
            # Prepare form data (matching backend Body_new_advert_advert_post schema)
            form_data = {
                "title": ad_data.get("title"),        # Required string
                "description": ad_data.get("description"),  # Required string
                "price": str(ad_data.get("price", 0))  # Required number
            }
            
            # Add optional fields
            if "contact_name" in ad_data:
                form_data["contact_name"] = ad_data["contact_name"]
            if "contact_phone" in ad_data:
                form_data["contact_phone"] = ad_data["contact_phone"]
            
            print(f"📤 Form data: {form_data}")
            
            # Handle image if provided
            files = None
            if "image" in ad_data and ad_data["image"]:
                # If image is base64, we need to convert it to a file-like object
                import base64
                import io
                
                image_data = ad_data["image"]
                if isinstance(image_data, str) and image_data.startswith('data:image'):
                    # Extract base64 data from data URL
                    header, encoded = image_data.split(',', 1)
                    image_bytes = base64.b64decode(encoded)
                elif isinstance(image_data, str):
                    # Assume it's base64 string
                    image_bytes = base64.b64decode(image_data)
                else:
                    # Assume it's already bytes
                    image_bytes = image_data
                
                # Create file-like object
                image_file = io.BytesIO(image_bytes)
                files = {"image": ("image.jpg", image_file, "image/jpeg")}
                print(f"📤 Image file prepared: {len(image_bytes)} bytes")
            
            response = await asyncio.to_thread(
                requests.post,
                url=url,
                data=form_data,
                files=files,
                params=params,
                headers=headers,
                timeout=30
            )
            
            print(f"📡 Response status: {response.status_code}")
            print(f"📥 Response headers: {dict(response.headers)}")
            
            # Handle authentication errors
            if response.status_code in [401, 403]:
                self.clear_token()
                try:
                    ui.notify("Session expired, please sign in again", type="negative")
                    ui.navigate.to(f"/login?next={ui.context.client.request.path}")
                except (RuntimeError, AttributeError):
                    print("⚠️ Authentication error - not in UI context")
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
                
                try:
                    ui.notify(f"Error: {error_msg}", type="negative")
                except (RuntimeError, AttributeError):
                    print(f"⚠️ Error notification - not in UI context")
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
            try:
                ui.notify(f"Network error: {str(e)}", type="negative")
            except (RuntimeError, AttributeError):
                print(f"⚠️ Network error - not in UI context: {e}")
            return False, str(e)
    
    async def get_ad(self, ad_id: str) -> Tuple[bool, Any]:
        """Get ad details"""
        endpoint = self.routes["ads"]["detail"].format(id=ad_id)
        return await self.request("GET", endpoint)
    
    async def update_ad(self, ad_id: str, ad_data: Dict) -> Tuple[bool, Any]:
        """Update ad"""
        endpoint = self.routes["ads"]["update"].format(id=ad_id)
        return await self.request("PUT", endpoint, ad_data)
    
    async def update_ad_with_location(self, ad_id: str, ad_data: Dict, location: str) -> Tuple[bool, Any]:
        """Update ad with location as query parameter"""
        endpoint = self.routes["ads"]["update"].format(id=ad_id)
        params = {"location": location}
        return await self.request("PUT", endpoint, ad_data, params)
    
    async def delete_ad(self, ad_id: str) -> Tuple[bool, Any]:
        """Delete ad"""
        endpoint = self.routes["ads"]["delete"].format(id=ad_id)
        return await self.request("DELETE", endpoint)
    
    async def generate_ai_image(self, prompt_data: Dict) -> Tuple[bool, Any]:
        """Generate AI image using backend API"""
        endpoint = self.routes.get("ai", {}).get("generate_image", "/ai/generate-image")
        return await self.request("POST", endpoint, prompt_data)
    
    async def generate_ai_text(self, text_data: Dict) -> Tuple[bool, Any]:
        """Generate AI text using backend API"""
        endpoint = self.routes.get("ai", {}).get("text_generation", "/ai/generate-text")
        return await self.request("POST", endpoint, text_data)
    
    # Cart Management
    async def add_to_cart(self, advert_id: str, quantity: int = 1) -> Tuple[bool, Any]:
        """Add item to cart"""
        endpoint = self.routes["cart"]["add"]
        params = {
            "advert_id": advert_id,
            "quantity": quantity
        }
        return await self.request("POST", endpoint, params=params)
    
    # Wishlist Management  
    async def add_to_wishlist(self, advert_id: str) -> Tuple[bool, Any]:
        """Add item to wishlist"""
        endpoint = self.routes["wishlist"]["add"]
        params = {
            "advert_id": advert_id
        }
        return await self.request("POST", endpoint, params=params)
    
    # Search and Filter
    async def search_ads(self, keyword: str, category: str = None, location: str = None, 
                        min_price: float = None, max_price: float = None) -> Tuple[bool, Any]:
        """Search adverts with filters"""
        endpoint = self.routes["ads"]["search"]
        params = {
            "keyword": keyword
        }
        if category:
            params["category"] = category
        if location:
            params["location"] = location
        if min_price is not None:
            params["min_price"] = min_price
        if max_price is not None:
            params["max_price"] = max_price
        return await self.request("GET", endpoint, params=params)
    
    # Get nearby adverts
    async def get_nearby_ads(self, user_location: str) -> Tuple[bool, Any]:
        """Get adverts near a specific location"""
        endpoint = self.routes["ads"]["nearby"].format(user_location=user_location)
        return await self.request("GET", endpoint)
    
    # Get recommendations
    async def get_recommendations(self, category: str) -> Tuple[bool, Any]:
        """Get advert recommendations by category"""
        endpoint = self.routes["ads"]["recommendations"]
        params = {
            "category": category
        }
        return await self.request("GET", endpoint, params=params)
    
    # Report advert
    async def report_advert(self, advert_id: str, reason: str) -> Tuple[bool, Any]:
        """Report an inappropriate advert"""
        endpoint = self.routes["report"]["advert"].format(id=advert_id)
        data = {
            "reason": reason
        }
        return await self.request("POST", endpoint, data)
    
    def check_ai_readiness(self) -> str:
        """Check AI API readiness and return status string"""
        if not ai_api_key or ai_api_key == "your_ai_api_key_here":
            return "AI API key not configured. Please set AI_API_KEY in your .env file."
        
        if not self._discovered:
            return "API endpoints not discovered yet. Please wait for initialization."
        
        ai_endpoints = self.routes.get("ai", {})
        if not ai_endpoints:
            return "AI endpoints not available in API specification."
        
        return "AI integration ready. API key configured and endpoints available."

# Global API client instance
api_client = APIClient()
