# AI Usage Log

## Overview
- **AI Tool Used:** Gemini (DeepMind)

## Development Workflow & Prompts

### 1. Project Planning & Division
- **Prompt Given:** "Asked the AI to break the assignment down into 5 sequential sections and execute Section 1 (Project setup and models)."
- **Output Accepted:** The initial Django model architecture (`Product`, `Box`, `Order`, `OrderItem`) using `DecimalField` to prevent floating-point errors.
- **Verification Steps:** Successfully ran `makemigrations` and `migrate`.

### 2. Frontend & Localization (Dollars to Rupees)
- **Prompt Given:** "Connect it with a frontend part where I enter product name and weight with its dimensional and then its calculated price will be shown in the rupees and according to indian market."
- **Output Accepted:** The concept of an interactive frontend UI with dynamic DOM manipulation for adding items, alongside the backend 3D Box Selection Algorithm.
- **Output Rejected/Modified:** The AI initially generated UI code using US Dollars (`$`). I rejected this and forced the AI to correct the currency formatting to strictly use Indian Rupees (`₹`) to match the prompt requirements.

### 3. UI Redesign & Remove Button Integration
- **Prompt Given:** "I want the same UI but in the image I can't remove the item which I add so make a button to which I remove the item."
- **Output Accepted:** The implementation of a dark-mode two-column layout matching a specific visual design. The logic for filtering items out of the Javascript array via a new trash-can button.

### 4. Manual API Calculation Trigger
- **Prompt Given:** "Add 'Find the Box' button and ensure the project is fully functioning in the correct way."
- **Output Accepted:** Transitioned the frontend logic from auto-calculating on every keystroke to utilizing a dedicated 'Find Best Box' submit button, optimizing the amount of REST API calls made to the server.

### 5. Debugging & Mistakes Found
- **Prompt Given:** "Why is it not working? 'No Box Found' error."
- **Mistakes Found:** The AI's initial code successfully created Django test cases with dummy boxes, but it made a mistake by failing to populate the *actual* SQLite development database with any warehouse inventory. When the frontend called the API, it checked an empty database.
- **Verification & Fix:** Debugged the empty database issue and executed a custom Python script (`seed.py`) to inject 5 standard shipping boxes into the local database, which permanently fixed the "No Box Found" error.

## Final Verification
Executed `python manage.py test` to ensure the final implementation flawlessly passes all edge cases (Weight limits, Dimensional 3D checks, and Capacity limits).
