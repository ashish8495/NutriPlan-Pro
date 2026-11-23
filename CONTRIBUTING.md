# Contributing to NutriPlan Pro

Thank you for your interest in contributing to **NutriPlan Pro**! As an open-source project, we welcome contributions from developers, nutrition scientists, fitness enthusiasts, and dietitians.

---

## 🛠️ How You Can Contribute

1. **Add New Recipes & Meals**:
   - Expand the meal catalog in `nutrition_engine.py` (e.g., regional cuisines, vegan recipes, keto dishes).
   - Ensure all macros (calories, protein, carbs, fiber, fat) are validated against **USDA FoodData Central**.

2. **Enhance Nutritional Algorithms**:
   - Add body fat percentage input (Katch-McArdle formula for BMR).
   - Add micronutrient tracking (Iron, Calcium, Vitamin D, Potassium).
   - Add custom carb cycling or refeed day schedules.

3. **Improve UI & UX**:
   - Add new interactive charts and visual filters.
   - Improve mobile responsiveness and print stylesheets.

4. **Fix Bugs & Improve Test Coverage**:
   - Add new unit tests in `tests/test_nutrition.py`.

---

## 🚀 Development Setup

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/NutriPlan-Pro.git
   cd NutriPlan-Pro
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**:
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Run the Test Suite**:
   ```bash
   python -m unittest discover -s tests -v
   ```

---

## 📋 Pull Request Guidelines

1. Create a descriptive branch: `git checkout -b feature/my-new-feature`
2. Follow PEP 8 guidelines for Python code style.
3. Ensure all tests pass before submitting your PR.
4. Provide a clear PR description explaining the changes and any nutritional references used.

---

## 📄 License
By contributing to NutriPlan Pro, you agree that your contributions will be licensed under the project's **MIT License**.
