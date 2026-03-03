# Creative Design Project

A professional E-commerce platform for handmade and machine-made crafts, built with Django.

## 🌟 Features

### 👤 User Features

- **Browse Designs**: Explore a wide range of unique handmade and machine-made designs.
- **Customization**: Request custom text, colors, descriptions, and images for any design.
- **Order Tracking**: Track order status from pending to delivered.
- **Secure Payment**: Integrated payment flow with transaction history.
- **Feedback System**: Rate and review designs and sellers after delivery.
- **Direct Chat**: Communicate directly with sellers about your orders.

### 🏢 Seller Features

- **Design Management**: Add, edit, or delete craft designs with images and descriptions.
- **Order Management**: Process incoming orders, update shipping status, and manage completions.
- **Revenue Dashboard**: Track total earnings and booking statistics.
- **Direct Interaction**: Chat with customers to clarify customization requests.

### 🛡️ Admin Features

- **Seller Verification**: Approve, reject, or block seller registrations.
- **Design Moderation**: Review and approve new designs before they go live.
- **Payment Monitoring**: Oversee all transactions and platform commissions.
- **User Oversight**: View and manage all registered platform users.

## 🛠️ Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Static Assets**: Django Media handles for images and uploads.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Django

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/VishnuSuresh0204/Creative-Design.git
    cd Creative-Design
    ```
2.  **Set up Virtual Environment**:
    ```bash
    python -m venv env
    .\env\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install django pillow
    ```
4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```
5.  **Start Dev Server**:
    ```bash
    python manage.py run_server
    ```

## 📄 License

This project is licensed under the MIT License.
