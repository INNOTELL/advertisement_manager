# InnoHub - Advertisement Management Platform

A comprehensive e-commerce marketplace platform inspired by Jumia, built with NiceGUI and FastAPI. This platform allows vendors to list products and users to browse and purchase items in a modern, responsive interface.

## 🚀 Features

### Frontend Features
- **Modern Jumia-inspired UI** with orange theme and responsive design
- **Authentication System** with signup/login for vendors and users
- **Vendor Dashboard** with product management and analytics
- **Product Listing** with grid/list view and advanced filtering
- **Product Detail Pages** with image galleries and related products
- **Search & Filter** functionality by category, price, and keywords
- **Mobile-responsive** design for all screen sizes

### Backend Integration
- **RESTful API** integration with external backend
- **CRUD Operations** for product management
- **User Authentication** with role-based access control
- **File Upload** support for product images
- **Real-time Updates** with optimistic UI updates

### AI-Powered Features
- **AI Description Generation** - Automatically generate product descriptions
- **Price Suggestion** - AI-powered price recommendations
- **Smart Recommendations** - Related products suggestions

## 🛠️ Technology Stack

- **Frontend**: NiceGUI (Python web framework)
- **Styling**: Tailwind CSS
- **Backend**: FastAPI
- **Authentication**: Custom JWT-based system
- **Database**: External API integration
- **Icons**: Material Design Icons

## 📋 Requirements

- Python 3.8+
- pip package manager

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd advertisement_manager
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

4. **Access the platform**
   - Open your browser and navigate to `http://localhost:8080`
   - The application will automatically reload on code changes

## 🎯 User Roles

### Vendors
- Create and manage product listings
- Access vendor dashboard with analytics
- Edit and delete their own products
- Use AI features for product optimization

### Users
- Browse and search products
- View product details
- Add products to wishlist
- Contact vendors

## 📱 Pages & Features

### Home Page (`/`)
- Hero banner with call-to-action
- Featured categories with icons
- Product grid with search and filtering
- Responsive design for all devices

### Authentication (`/login`, `/signup`)
- Clean, modern login/signup forms
- Role selection (Vendor/User)
- Form validation and error handling

### Vendor Dashboard (`/dashboard`)
- Product management table
- Analytics cards (total products, views, etc.)
- Quick actions for product management
- Search and filter own products

### Product Management
- **Add Product** (`/add_event`): Form with AI features
- **Edit Product** (`/edit_event`): Update existing listings
- **View Product** (`/view_event`): Detailed product page

## 🔧 API Integration

The platform integrates with the following backend endpoints:

- `POST /Sign up` - User registration
- `POST /Login` - User authentication
- `POST /advert` - Create new product
- `GET /adverts` - Get all products
- `GET /advert_details/{id}` - Get product details
- `PUT /edit_advert/{title}` - Update product
- `DELETE /adverts/{title}` - Delete product

## 🎨 Design System

### Color Palette
- **Primary Orange**: #FF6B35 (Jumia-inspired)
- **Background**: Light gray (#F8F9FA)
- **Text**: Dark gray (#1F2937)
- **Success**: Green (#10B981)
- **Error**: Red (#EF4444)

### Typography
- **Font**: Inter (Google Fonts)
- **Headings**: Bold, various sizes
- **Body**: Regular weight, readable sizes

## 📁 Project Structure

```
advertisement_manager/
├── components/
│   ├── header.py          # Navigation and search
│   └── footer.py          # Footer with links
├── pages/
│   ├── auth.py            # Login/signup pages
│   ├── dashboard.py       # Vendor dashboard
│   ├── home.py            # Homepage with product grid
│   ├── add_event.py       # Add product form
│   ├── edit_event.py      # Edit product form
│   └── view_event.py      # Product detail page
├── utils/
│   └── api.py             # API configuration
├── main.py                # Application entry point
├── theme.py               # Styling and theme
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🔐 Authentication Flow

1. **Signup**: Users create accounts with email, username, and password
2. **Login**: Authentication with backend API
3. **Role Assignment**: Automatic vendor/user role detection
4. **Protected Routes**: Role-based access to vendor features
5. **Session Management**: Persistent authentication state

## 🎯 AI Features Implementation

### Description Generation
- Analyzes product title and category
- Generates compelling product descriptions
- Improves listing quality and conversion

### Price Suggestion
- Category-based pricing recommendations
- Market analysis for competitive pricing
- Helps vendors set optimal prices

## 📱 Responsive Design

- **Mobile-first** approach
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px)
- **Grid System**: Responsive product grids
- **Navigation**: Collapsible mobile menu
- **Touch-friendly** buttons and interactions

## 🚀 Deployment

The application can be deployed to any Python hosting platform:

1. **Heroku**: Add Procfile and requirements.txt
2. **Railway**: Direct deployment from GitHub
3. **Vercel**: Python runtime support
4. **Docker**: Containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Built with ❤️ using NiceGUI and FastAPI**