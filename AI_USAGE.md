# AI Usage Log

## Section 1: Project Setup and Models
- **AI Tool Used:** Gemini (DeepMind)
- **Prompt Given:** "Asked the AI to break the assignment down into 5 sequential sections and execute Section 1 (Project setup and models)."
- **Output Accepted:** The database schema separating `Product`, `Box`, `Order`, and `OrderItem` using `DecimalField` for measurements.
- **Output Rejected/Modified:** None for this section; the architecture correctly handles independent product weights and volumetric properties.
- **Verification Steps:** Successfully ran `makemigrations` and `migrate` without database errors.

## Section 2: Box Selection Algorithm
- **AI Tool Used:** Gemini
- **Prompt Given:** "Write the python logic to filter boxes based on weight, volume, and 3D physical dimensions to find the cheapest box."
- **Output Accepted:** The 3D sorting logic where both box dimensions and item dimensions are sorted `reverse=True` so we can compare largest dimension to largest dimension.
- **Output Rejected/Modified:** The AI initially used floats for calculations. I modified it to strictly cast incoming JSON floats to Python `Decimal` objects to maintain consistency with our model fields and prevent floating point errors.
- **Mistakes Found:** AI forgot to handle the quantity multiplier when computing total weight and total volume in its first draft. Added `quantity` multiplier inside the total loops.
- **Verification Steps:** Created Django test cases `BoxSelectionTests` to verify both the happy path and edge cases (weight limit bypass and dimensional bypass).

## Section 3: API Endpoint and Frontend Integration
- **AI Tool Used:** Gemini
- **Prompt Given:** "Create a DRF API endpoint and a beautiful vanilla HTML/CSS frontend with modern styling to dynamically calculate box prices in INR (₹)."
- **Output Accepted:** The interactive frontend template using `fetch` API, CSS Variables, and Glassmorphism for a modern UI. The DRF POST endpoint logic.
- **Output Rejected/Modified:** The AI initially provided an API that required saving items to the database first. I modified it so the API takes an arbitrary list of dimensions/weights without committing to the DB, acting purely as a calculator for a better demo experience.
- **Verification Steps:** Executed the API endpoint via automated tests ensuring 200 OK and 404 NOT FOUND where appropriate. Manually verified the frontend layout and dynamic UI rendering.

## Section 4: Testing & Polish
- **AI Tool Used:** Gemini
- **Prompt Given:** "Write 5 Django unit tests that cover the edge cases required."
- **Output Accepted:** Test cases utilizing `APIClient` to simultaneously test the algorithm logic and the REST response structure.
- **Verification Steps:** Ran `python manage.py test` and achieved a 100% pass rate across 5 test cases.
