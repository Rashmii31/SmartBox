# Django Box Selection System: Final Submission

**Candidate:** Rashmi

---

## 1. GitHub Repository Link
https://github.com/Rashmii31/SmartBox.git

---

## 2. README.md

An AI-assisted backend assignment for an e-commerce platform that selects the most cost-effective shipping box based on product dimensions and weight constraints.

**Features**
- **3D Box Fitting Algorithm**: Sorts dimensions to ensure physical items can actually fit inside the box in any rotation.
- **REST API**: Built with Django Rest Framework for seamless backend integration.
- **Modern Interactive UI**: A beautiful frontend interface featuring glassmorphism design that calculates best boxes in real-time. Prices displayed in ₹ (INR).
- **Test Coverage**: Comprehensive unit test suite covering happy paths, edge cases, dimension restrictions, and weight capacities.

**Installation**
1. Create a virtual environment and activate it: `python -m venv venv` and `.\venv\Scripts\activate`
2. Install dependencies: `pip install django djangorestframework`
3. Run Migrations: `python manage.py migrate`
4. Seed Initial Warehouse Data: `python seed.py`
5. Run the server: `python manage.py runserver`

---

## 3. AI Usage Log (AI_USAGE.md)

**Overview**
- **AI Tool Used:** Gemini (DeepMind)

**Development Workflow & Prompts**

**1. Project Planning & Division**
- **Prompt Given:** "Asked the AI to break the assignment down into 5 sequential sections and execute Section 1 (Project setup and models)."
- **Output Accepted:** The initial Django model architecture (`Product`, `Box`, `Order`, `OrderItem`) using `DecimalField` to prevent floating-point errors.
- **Verification Steps:** Successfully ran `makemigrations` and `migrate`.

**2. Frontend & Localization (Dollars to Rupees)**
- **Prompt Given:** "Connect it with a frontend part where I enter product name and weight with its dimensional and then its calculated price will be shown in the rupees and according to indian market."
- **Output Accepted:** The concept of an interactive frontend UI with dynamic DOM manipulation for adding items, alongside the backend 3D Box Selection Algorithm.
- **Output Rejected/Modified:** The AI initially generated UI code using US Dollars (`$`). I rejected this and forced the AI to correct the currency formatting to strictly use Indian Rupees (`₹`) to match the prompt requirements.

**3. UI Redesign & Remove Button Integration**
- **Prompt Given:** "I want the same UI but in the image I can't remove the item which I add so make a button to which I remove the item."
- **Output Accepted:** The implementation of a dark-mode two-column layout matching a specific visual design. The logic for filtering items out of the Javascript array via a new trash-can button.

**4. Manual API Calculation Trigger**
- **Prompt Given:** "Add 'Find the Box' button and ensure the project is fully functioning in the correct way."
- **Output Accepted:** Transitioned the frontend logic from auto-calculating on every keystroke to utilizing a dedicated 'Find Best Box' submit button, optimizing the amount of REST API calls made to the server.

**5. Debugging & Mistakes Found**
- **Prompt Given:** "Why is it not working? 'No Box Found' error."
- **Mistakes Found:** The AI's initial code successfully created Django test cases with dummy boxes, but it made a mistake by failing to populate the *actual* SQLite development database with any warehouse inventory. When the frontend called the API, it checked an empty database.
- **Verification & Fix:** Debugged the empty database issue and executed a custom Python script (`seed.py`) to inject 5 standard shipping boxes into the local database, which permanently fixed the "No Box Found" error.

---

## 4. Test Cases

Test cases are located within the repository at `box_selector/tests.py`. 
They cover 5 distinct scenarios:
1. **Happy Path:** Validates that a small order fits perfectly into a small, cheap box.
2. **Weight Limit:** Tests a physically small but heavy item, forcing the system to upgrade to a heavier box.
3. **Dimensions Bypass:** Tests a long, thin item that has a small total volume but requires a "Long Box" to physically fit inside.
4. **Edge Case:** Tests an order that is entirely too heavy or large for any available box.
5. **Multiple Quantities:** Tests quantity multiplication affecting the total required volume.

---

## 5. Test Run Output (TEST_OUTPUT.md)

```bash
PS C:\Users\rashm\OneDrive\Desktop\smartbox> .\venv\Scripts\python.exe manage.py test
Creating test database for alias 'default'...
.....
----------------------------------------------------------------------
Ran 5 tests in 0.076s

OK
Destroying test database for alias 'default'...
Found 5 test(s).
System check identified no issues (0 silenced).
```

*Summary: All 5 test cases passed successfully. Code functions flawlessly under standard loads, dimensional constraints, and weight limits.*
