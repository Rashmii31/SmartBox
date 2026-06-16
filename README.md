# Django Box Selection System

An AI-assisted backend assignment for an e-commerce platform that selects the most cost-effective shipping box based on product dimensions and weight constraints.

## Features
- **3D Box Fitting Algorithm**: Sorts dimensions to ensure physical items can actually fit inside the box in any rotation.
- **REST API**: Built with Django Rest Framework for seamless backend integration.
- **Modern Interactive UI**: A beautiful frontend interface featuring glassmorphism design that calculates best boxes in real-time. Prices displayed in ₹ (INR).
- **Test Coverage**: Comprehensive unit test suite covering happy paths, edge cases, dimension restrictions, and weight capacities.

## Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install django djangorestframework
   ```

3. Run Migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```
   Visit `http://localhost:8000/` to interact with the UI.

## Testing
Run the automated test suite with:
```bash
python manage.py test
```

See `TEST_OUTPUT.md` for test run logs and `AI_USAGE.md` for the AI workflow documentation.
