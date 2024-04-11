# CraftConnect

CraftConnect is a platform that connects artisans with customers, providing a marketplace for artisanal goods and services.

## Features

- **Artisan Profiles**: Artisans can create profiles showcasing their skills, portfolio, and contact information.
- **Product Listings**: Artisans can list their products and services for sale, including descriptions, prices, and images.
- **Search and Filters**: Customers can search for artisans and products based on categories, keywords, and location.
- **Messaging System**: Customers can communicate with artisans directly through the platform to discuss orders and specifications.
- **Rating and Reviews**: Customers can leave ratings and reviews for artisans, helping others make informed decisions.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL or SQLite
- **Authentication**: JWT or OAuth
- **Deployment**: AWS, Azure, firebase

## Getting Started

### Prerequisites

- Python and poetry installed for backend development.
- PostgreSQL or SQLite installed and running.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Cozyamy/CraftConnect_Backend.git
cd CraftConnect
```

2. Install backend dependencies:

```bash
poetry shell
poetry install
```

### Running the Application

Start the backend server:

```bash
uvicorn main:app --reload
```

3. Access the application in your browser at `http://localhost:8000`.