"""
Comprehensive Unit Tests for Diet Planner & Nutrition Engine.
"""

import unittest
import json
from nutrition_engine import (
    convert_weight_to_kg,
    convert_kg_to_lbs,
    calculate_bmi,
    calculate_bmr_tdee,
    calculate_macros,
    generate_weekly_diet_plan,
    build_full_user_profile,
    DAYS_OF_WEEK,
    MEAL_DATABASE
)
from app import app


class TestNutritionEngine(unittest.TestCase):

    def test_weight_conversions(self):
        # 100 lbs to kg
        kg = convert_weight_to_kg(100, "lbs")
        self.assertAlmostEqual(kg, 45.36, delta=0.1)

        # 75 kg should stay 75
        kg_same = convert_weight_to_kg(75, "kg")
        self.assertEqual(kg_same, 75.0)

        # 75 kg to lbs
        lbs = convert_kg_to_lbs(75)
        self.assertAlmostEqual(lbs, 165.3, delta=0.2)

    def test_bmi_calculation(self):
        # Height 175cm, Weight 70kg -> BMI ~ 22.86 (Normal)
        bmi_res = calculate_bmi(70, 175)
        self.assertEqual(bmi_res["bmi"], 22.9)
        self.assertEqual(bmi_res["category"], "Normal (Healthy)")

        # Overweight case: Height 170cm, Weight 85kg -> BMI ~ 29.4
        bmi_overweight = calculate_bmi(85, 170)
        self.assertEqual(bmi_overweight["category"], "Overweight")

    def test_bmr_and_tdee(self):
        # Male, 80kg, 180cm, age 30, workout Yes (moderate)
        res_male = calculate_bmr_tdee(80, 180, 30, "male", "yes", "moderate")
        # BMR = 10*80 + 6.25*180 - 5*30 + 5 = 800 + 1125 - 150 + 5 = 1780
        self.assertEqual(res_male["bmr"], 1780)
        # TDEE = 1780 * 1.55 = 2759
        self.assertEqual(res_male["tdee"], 2759)
        # Low Calorie Target with 22% deficit = 2759 * 0.78 = ~2152
        self.assertGreater(res_male["tdee"], res_male["target_calories"])
        self.assertGreater(res_male["target_calories"], 1400)

        # Sedentary case (workout = no)
        res_sedentary = calculate_bmr_tdee(80, 180, 30, "male", "no")
        self.assertEqual(res_sedentary["multiplier"], 1.2)
        self.assertLess(res_sedentary["tdee"], res_male["tdee"])

    def test_macros_high_protein_and_fiber(self):
        # Target 2000 calories for 80kg individual
        macros = calculate_macros(80, 2000)
        # Protein ~ 160g (2.0g per kg)
        self.assertGreaterEqual(macros["protein_g"], 150)
        # Fiber >= 30g
        self.assertGreaterEqual(macros["fiber_g"], 30)
        # Carbs present
        self.assertGreater(macros["carbs_g"], 50)
        # Water intake present
        self.assertGreater(macros["water_liters"], 2.0)

    def test_weekly_meal_plan_generation(self):
        plan = generate_weekly_diet_plan(1800, 160, 150, 32, 45, "any")
        weekly = plan["weekly_plan"]
        
        # Check all 7 days present
        self.assertEqual(len(weekly), 7)
        for day in DAYS_OF_WEEK:
            self.assertIn(day, weekly)
            day_data = weekly[day]
            # 4 meals per day
            self.assertEqual(len(day_data["meals"]), 4)
            # Daily total calories reasonably close to target
            self.assertGreater(day_data["totals"]["calories"], 1400)
            self.assertGreater(day_data["totals"]["protein"], 100)
            self.assertGreater(day_data["totals"]["fiber"], 20)

        # Check grocery list
        self.assertGreater(len(plan["grocery_list"]), 5)

    def test_vegetarian_and_vegan_plans(self):
        veg_plan = generate_weekly_diet_plan(1800, 150, 160, 35, 45, "vegetarian")
        self.assertEqual(len(veg_plan["weekly_plan"]), 7)

        vegan_plan = generate_weekly_diet_plan(1800, 140, 170, 38, 45, "vegan")
        self.assertEqual(len(vegan_plan["weekly_plan"]), 7)

    def test_budget_friendly_meals_present(self):
        for category, meals in MEAL_DATABASE.items():
            budget_meals = [m for m in meals if m.get("is_budget") is True]
            self.assertGreaterEqual(len(budget_meals), 3, f"Category {category} should have budget options")


class TestFlaskEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"NutriPlan Pro", response.data)

    def test_generate_plan_api(self):
        payload = {
            "name": "Sarah Connor",
            "height_cm": 168,
            "weight_val": 140,
            "weight_unit": "lbs",
            "workout": "yes",
            "workout_frequency": "heavy",
            "age": 32,
            "gender": "female",
            "diet_pref": "any"
        }
        response = self.client.post("/api/generate-plan",
                                    data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["user"]["name"], "Sarah Connor")
        self.assertIn("weekly_plan", data["data"])
        self.assertIn("macros", data["data"])
        self.assertIn("energy", data["data"])

    def test_generate_plan_validation(self):
        # Invalid height
        bad_payload = {"height_cm": 10, "weight_val": 70}
        response = self.client.post("/api/generate-plan",
                                    data=json.dumps(bad_payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_swap_meal_api(self):
        payload = {
            "category": "breakfast",
            "diet_pref": "any",
            "current_meal_id": "b1",
            "target_calories": 360
        }
        response = self.client.post("/api/swap-meal",
                                    data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("name", data["meal"])
        self.assertIn("protein", data["meal"])

    def test_export_csv_api(self):
        profile = build_full_user_profile("Test User", 175, 75)
        payload = {
            "weekly_plan": profile["weekly_plan"],
            "user_name": "Test User"
        }
        response = self.client.post("/api/export/csv",
                                    data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/csv")
        self.assertIn(b"Monday", response.data)
        self.assertIn(b"Calories", response.data)


if __name__ == "__main__":
    unittest.main()
