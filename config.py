import os
from typing import Dict, Any

# Backend Configuration
BACKEND_BASE_URL = "https://advertisement-management-api-c2jb.onrender.com"
DOCS_URL = "https://advertisement-management-api-c2jb.onrender.com/docs"
OPENAPI_URL_CANDIDATES = [
    "https://advertisement-management-api-c2jb.onrender.com/openapi.json",
    "https://advertisement-management-api-c2jb.onrender.com/docs/openapi.json"
]

# Session Configuration
SESSION_TTL_MIN = 120

# API Endpoints (matching backend documentation exactly)
API_ROUTES = {
    "auth": {
        "signin": "/Login",
        "signup": "/SignUp", 
        "me": "/advertisers/{id}"  # Backend uses /advertisers/{id} for profile
    },
    "ads": {
        "list": "/adverts",
        "create": "/advert",
        "detail": "/advert_details/{id}",
        "update": "/edit_advert/{id}",
        "delete": "/adverts/{id}",
        "nearby": "/adverts_nearby/{user_location}",
        "search": "/ads/search",
        "recommendations": "/recommendations/"
    },
    "cart": {
        "add": "/cart/add"
    },
    "wishlist": {
        "add": "/wishlist/add"
    },
    "report": {
        "advert": "/adverts/{id}/report"
    }
}

# Backend CategoryEnum (exact match)
CATEGORIES = [
    "Babies & kids",
    "Electronics", 
    "Fashion",
    "Cars",
    "Real Estate",
    "Jobs",
    "Home, Furniture & Appliances",
    "Beauty & Personal Care",
    "Food & Agriculture"
]

# Backend LocationEnum (exact match)
LOCATIONS = [
    "Greater Accra",
    "Central Region",
    "Ashanti Region", 
    "Brong Ahafo Region",
    "Eastern Region",
    "Northern Region",
    "Upper East Region",
    "Upper West Region",
    "Volta Region",
    "Western Region"
]

# User Roles (matching backend RoleEnum)
USER_ROLES = {
    "BUYER": "User",      # Backend uses "User" not "buyer"
    "VENDOR": "Vendor"    # Backend uses "Vendor" not "vendor"
}

# Protected Routes
PROTECTED_ROUTES = [
    "/dashboard",
    "/profile",
    "/orders",
    "/wishlist",
    "/cart",
    "/analytics",
    "/sell",
    "/add_event",
    "/edit_event"
]

# Vendor-only Routes
VENDOR_ROUTES = [
    "/add_event",
    "/edit_event",
    "/analytics",
    "/sell"
]
