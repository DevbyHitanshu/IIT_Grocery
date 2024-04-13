# Grocery App Project

This project is a web-based Grocery App designed for users to browse and purchase grocery products. It provides a user-friendly interface for customers and an admin panel for managing categories and products. The application is built using the Flask web framework and SQLite database.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Database Schema](#database-schema)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Features
- User registration and login.
- Secure password hashing for user authentication.
- User roles: Admin and Regular User.
- Personalized welcome messages for users.
- Browsing product sections and items.
- Adding products to the cart.
- Admin panel for managing products and categories.
- Dynamic rendering of content using HTML templates.
- Session management for tracking user activities.

## Technologies Used
- Flask: Lightweight Python web framework.
- SQLite: Self-contained database engine.
- Hashlib: Hashing passwords for security.
- Jinja2: Templating engine for dynamic content.
- Flask-Session: Managing user sessions.
- Flask-url_for: Generating URLs for routes.

## Database Schema
1. Table: users
   - Columns: id, Name, Email, Password (hashed), User_type, active_session

2. Table: sections
   - Columns: id, sec (section name)

3. Table: products
   - Columns: id, name, price, section_id (foreign key)

4. Table: cart
   - Columns: id, product_name, product_price, quantity

## Architecture
The project follows a structured architecture using Flask for web development. Routes handle various functionalities, while Jinja2 templates dynamically render HTML content. User sessions and secure password hashing are implemented. The application supports both user and admin roles, with features tailored to each.

## Usage
1. Run the application: `python app.py`
2. Open your web browser and access the app at: `http://localhost:5000`
3. Register as a user or log in to explore the app and its features.

## Contributors
- Hitanshu Kapoor (Author) - [GitHub](https://github.com/your-username)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
