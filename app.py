"""
Flask Web Application for High-Protein, Low-Calorie Diet Planner.
"""

from flask import Flask, render_template, request, jsonify, Response
import json
import csv
import io
from nutrition_engine import (
    build_full_user_profile,
    MEAL_DATABASE,
    DAYS_OF_WEEK,
    filter_meals_by_diet
)

app = Flask(__name__)


@app.route("/")
def index():
    """Renders the main diet planner web page."""
    return render_template("index.html")


@app.route("/api/generate-plan", methods=["POST"])
def generate_plan():
    """API endpoint to calculate macros and generate 7-day personalized meal plan."""
    try:
        data = request.get_json() or {}
        name = data.get("name", "Health Champion")
        height_cm = float(data.get("height_cm", 175))
        weight_val = float(data.get("weight_val", 75))
        weight_unit = data.get("weight_unit", "kg").lower()
        workout = data.get("workout", "yes")
        workout_frequency = data.get("workout_frequency", "moderate")
        age = int(data.get("age", 28))
        gender = data.get("gender", "male")
        diet_pref = data.get("diet_pref", "any")
        budget_pref = data.get("budget_pref", "balanced")

        # Validation checks
        if height_cm <= 50 or height_cm > 260:
            return jsonify({"success": False, "error": "Please enter a valid height between 50 cm and 260 cm."}), 400
        if weight_val <= 20 or weight_val > 400:
            return jsonify({"success": False, "error": "Please enter a valid weight."}), 400

        profile = build_full_user_profile(
            name=name,
            height_cm=height_cm,
            weight_val=weight_val,
            weight_unit=weight_unit,
            workout=workout,
            workout_frequency=workout_frequency,
            age=age,
            gender=gender,
            diet_pref=diet_pref,
            budget_pref=budget_pref
        )

        return jsonify({
            "success": True,
            "data": profile
        })
    except ValueError as ve:
        return jsonify({"success": False, "error": f"Invalid numerical input: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Server error: {str(e)}"}), 500


@app.route("/api/category-meals", methods=["GET"])
def get_category_meals():
    """Returns all available meals for a category and diet preference."""
    category = request.args.get("category", "breakfast").lower()
    diet_pref = request.args.get("diet_pref", "any").lower()
    
    if "snack" in category:
        category_key = "snack"
    elif "lunch" in category:
        category_key = "lunch"
    elif "dinner" in category:
        category_key = "dinner"
    else:
        category_key = "breakfast"
        
    meals = filter_meals_by_diet(category_key, diet_pref, "any")
    return jsonify({
        "success": True,
        "category": category_key,
        "meals": meals
    })


@app.route("/api/swap-meal", methods=["POST"])
def swap_meal():
    """Swap a meal in the current plan with a specific or next alternative."""
    try:
        data = request.get_json() or {}
        meal_category = data.get("category", "breakfast").lower()
        diet_pref = data.get("diet_pref", "any")
        current_meal_id = data.get("current_meal_id")
        chosen_meal_id = data.get("chosen_meal_id")
        target_calories = float(data.get("target_calories", 400))

        if "snack" in meal_category:
            category_key = "snack"
        elif "lunch" in meal_category:
            category_key = "lunch"
        elif "dinner" in meal_category:
            category_key = "dinner"
        else:
            category_key = "breakfast"

        available_meals = filter_meals_by_diet(category_key, diet_pref, "any")
        if not available_meals:
            available_meals = MEAL_DATABASE.get(category_key, [])

        if chosen_meal_id:
            picked = [m for m in available_meals if m["id"] == chosen_meal_id]
            new_raw_meal = picked[0] if picked else available_meals[0]
        else:
            # Rotate to next item in candidates
            curr_indices = [i for i, m in enumerate(available_meals) if m["id"] == current_meal_id]
            curr_idx = curr_indices[0] if curr_indices else -1
            next_idx = (curr_idx + 1) % len(available_meals)
            new_raw_meal = available_meals[next_idx]

        scale = target_calories / new_raw_meal["calories"] if new_raw_meal["calories"] > 0 else 1.0

        swapped_meal = {
            "id": new_raw_meal["id"],
            "meal_type": meal_category.capitalize(),
            "name": new_raw_meal["name"],
            "calories": round(new_raw_meal["calories"] * scale),
            "protein": round(new_raw_meal["protein"] * scale),
            "carbs": round(new_raw_meal["carbs"] * scale),
            "fat": round(new_raw_meal["fat"] * scale),
            "fiber": round(new_raw_meal["fiber"] * scale),
            "is_budget": new_raw_meal.get("is_budget", False),
            "cost_level": new_raw_meal.get("cost_level", "$$"),
            "ingredients": new_raw_meal["ingredients"],
            "recipe": new_raw_meal["recipe"],
            "prep_time": new_raw_meal.get("prep_time", "15 mins"),
            "diet_tags": new_raw_meal.get("diet", [])
        }

        return jsonify({
            "success": True,
            "meal": swapped_meal
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/export/csv", methods=["POST"])
def export_csv():
    """Generates and downloads a CSV export of the weekly diet plan."""
    try:
        data = request.get_json() or {}
        weekly_plan = data.get("weekly_plan", {})
        user_name = data.get("user_name", "My_Diet_Plan")

        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Day", "Meal Type", "Meal Name", "Calories (kcal)", "Protein (g)", "Carbs (g)", "Fiber (g)", "Fat (g)", "Ingredients", "Instructions"])

        for day in DAYS_OF_WEEK:
            day_data = weekly_plan.get(day, {})
            meals = day_data.get("meals", [])
            for m in meals:
                writer.writerow([
                    day,
                    m.get("meal_type", ""),
                    m.get("name", ""),
                    m.get("calories", 0),
                    m.get("protein", 0),
                    m.get("carbs", 0),
                    m.get("fiber", 0),
                    m.get("fat", 0),
                    "; ".join(m.get("ingredients", [])),
                    m.get("recipe", "")
                ])
            # Day total row
            totals = day_data.get("totals", {})
            writer.writerow([
                day,
                "TOTAL FOR DAY",
                "---",
                totals.get("calories", 0),
                totals.get("protein", 0),
                totals.get("carbs", 0),
                totals.get("fiber", 0),
                totals.get("fat", 0),
                "",
                ""
            ])
            writer.writerow([])  # blank row

        output.seek(0)
        filename = f"{user_name.replace(' ', '_')}_Diet_Plan.csv"
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
