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

# API Endpoints (will be discovered dynamically)
API_ROUTES = {
    "auth": {
        "signin": "",
        "signup": "",
        "me": ""
    },
    "ads": {
        "list": "",
        "create": "",
        "detail": "",
        "update": ""
    }
}

# User Roles
USER_ROLES = {
    "BUYER": "buyer",
    "VENDOR": "vendor"
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
