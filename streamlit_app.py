"""
NutriPlan Pro - Streamlit Web Application
An open-source scientific diet planner for Low-Calorie, High-Protein & High-Fiber nutrition.
Includes extensive pocket-friendly / budget-friendly meal alternatives.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io

from nutrition_engine import (
    convert_weight_to_kg,
    convert_kg_to_lbs,
    calculate_bmi,
    calculate_bmr_tdee,
    calculate_macros,
    generate_weekly_diet_plan,
    build_full_user_profile,
    MEAL_DATABASE,
    DAYS_OF_WEEK,
    filter_meals_by_diet
)

# Page Configuration
st.set_page_config(
    page_title="NutriPlan Pro | Open Source Diet Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #059669, #0d9488);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .badge-protein {
        background-color: #e0e7ff;
        color: #3730a3;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
    }
    .badge-carb {
        background-color: #fef3c7;
        color: #92400e;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
    }
    .badge-fiber {
        background-color: #d1fae5;
        color: #065f46;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
    }
    .badge-fat {
        background-color: #ffe4e6;
        color: #9f1239;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
    }
    .badge-budget {
        background-color: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
        font-weight: 800;
        padding: 2px 7px;
        border-radius: 6px;
        font-size: 0.72rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initializes session state variables."""
    if "plan_generated" not in st.session_state:
        st.session_state.plan_generated = False
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = None
    if "weekly_plan" not in st.session_state:
        st.session_state.weekly_plan = None
    if "grocery_list" not in st.session_state:
        st.session_state.grocery_list = None


init_session_state()

# ----------------- SIDEBAR: INPUT CONTROLS -----------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=300&q=80", use_container_width=True)
    st.markdown("### ⚙️ User Profile & Parameters")
    
    user_name = st.text_input("Full Name", value="Alex Johnson")
    
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        height_cm = st.number_input("Height (cm)", min_value=90.0, max_value=250.0, value=175.0, step=0.5)
    with col_h2:
        total_in = height_cm / 2.54
        ft = int(total_in // 12)
        inch = int(round(total_in % 12))
        st.caption(f"~ {ft}'{inch}\"")

    weight_unit = st.radio("Weight Unit", options=["kg", "lbs"], horizontal=True)
    if weight_unit == "kg":
        weight_val = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=78.0, step=0.5)
    else:
        weight_val = st.number_input("Weight (lbs)", min_value=66.0, max_value=660.0, value=172.0, step=1.0)

    workout_opt = st.selectbox("Do you workout / exercise?", options=["Yes", "No"], index=0)
    
    workout_freq = "sedentary"
    if workout_opt == "Yes":
        workout_freq = st.selectbox(
            "Exercise Frequency / Intensity",
            options=["light", "moderate", "heavy"],
            format_func=lambda x: {
                "light": "Light (1-2 days / week)",
                "moderate": "Moderate (3-5 days / week)",
                "heavy": "Heavy (6-7 days / week)"
            }[x],
            index=1
        )

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        age = st.number_input("Age (years)", min_value=14, max_value=95, value=28, step=1)
    with col_a2:
        gender = st.selectbox("Biological Sex", options=["Male", "Female"], index=0)

    diet_pref = st.selectbox(
        "Dietary Preference",
        options=["any", "vegetarian", "vegan", "pescatarian"],
        format_func=lambda x: {
            "any": "All / Omnivore (Poultry, Meat, Fish, Veg)",
            "vegetarian": "Vegetarian (Dairy, Paneer, Legumes)",
            "vegan": "Vegan (Plant-Based Only)",
            "pescatarian": "Pescatarian (Fish & Plants)"
        }[x]
    )

    budget_pref = st.selectbox(
        "Budget & Cost Focus",
        options=["balanced", "budget_only", "any"],
        format_func=lambda x: {
            "balanced": "Balanced (Mix of Pocket-Friendly & Standard)",
            "budget_only": "Pocket-Friendly Focus ($ Max Savings)",
            "any": "All Available Meals"
        }[x],
        index=0
    )

    generate_btn = st.button("🚀 Generate Diet Plan", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown("🔗 **Open Source Links**")
    st.markdown("[⭐ GitHub Repository](https://github.com/) • [📜 Documentation](https://github.com/)")


# ----------------- PLAN GENERATION TRIGGER -----------------
if generate_btn or (not st.session_state.plan_generated):
    profile = build_full_user_profile(
        name=user_name,
        height_cm=height_cm,
        weight_val=weight_val,
        weight_unit=weight_unit,
        workout=workout_opt.lower(),
        workout_frequency=workout_freq,
        age=age,
        gender=gender.lower(),
        diet_pref=diet_pref,
        budget_pref=budget_pref
    )
    st.session_state.user_profile = profile
    st.session_state.weekly_plan = profile["weekly_plan"]
    st.session_state.grocery_list = profile["grocery_list"]
    st.session_state.plan_generated = True


# ----------------- MAIN CONTENT DISPLAY -----------------
profile = st.session_state.user_profile
weekly_plan = st.session_state.weekly_plan

st.markdown('<div class="main-header">NutriPlan Pro</div>', unsafe_allow_html=True)
st.caption("Evidence-Based Scientific Diet Engineering • High Protein • Low Calorie • Fiber Dense • Pocket Friendly")

# 1. Summary Cards
user = profile["user"]
bmi = profile["bmi"]
energy = profile["energy"]
macros = profile["macros"]

st.markdown("---")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        label="🎯 Target Calories",
        value=f"{energy['target_calories']} kcal",
        delta=f"-{energy['deficit_calories']} kcal ({energy['deficit_percentage']}% Deficit)",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="🥩 High Protein",
        value=f"{macros['protein_g']} g",
        delta=f"{macros['protein_pct']}% of cals"
    )

with col3:
    st.metric(
        label="🌾 Complex Carbs",
        value=f"{macros['carbs_g']} g",
        delta=f"{macros['carbs_pct']}% of cals"
    )

with col4:
    st.metric(
        label="🌱 Fiber Goal",
        value=f"{macros['fiber_g']} g",
        delta="30g+ Daily"
    )

with col5:
    st.metric(
        label="🥑 Healthy Fats",
        value=f"{macros['fat_g']} g",
        delta=f"{macros['fat_pct']}% of cals"
    )

with col6:
    st.metric(
        label="💧 Daily Water",
        value=f"{macros['water_liters']} L",
        delta=f"BMI: {bmi['bmi']} ({bmi['category']})"
    )

# 2. Charts Row
col_c1, col_c2 = st.columns([1, 1])

with col_c1:
    st.markdown("##### 🥧 Macronutrient Energy Ratio")
    macro_df = pd.DataFrame({
        "Nutrient": ["Protein", "Carbohydrates", "Healthy Fats"],
        "Grams": [macros["protein_g"], macros["carbs_g"], macros["fat_g"]],
        "Calories": [macros["protein_g"] * 4, macros["carbs_g"] * 4, macros["fat_g"] * 9]
    })
    fig_donut = px.pie(
        macro_df,
        names="Nutrient",
        values="Calories",
        hole=0.55,
        color="Nutrient",
        color_discrete_map={
            "Protein": "#4f46e5",
            "Carbohydrates": "#f59e0b",
            "Healthy Fats": "#f43f5e"
        }
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=230, showlegend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

with col_c2:
    st.markdown("##### ⚡ Metabolic Energy Breakdown (kcal)")
    fig_bar = go.Figure(data=[
        go.Bar(
            x=["BMR (Resting)", "TDEE (Maintenance)", "Target (Deficit)"],
            y=[energy["bmr"], energy["tdee"], energy["target_calories"]],
            marker_color=["#94a3b8", "#0ea5e9", "#10b981"],
            text=[f"{energy['bmr']} kcal", f"{energy['tdee']} kcal", f"{energy['target_calories']} kcal"],
            textposition='auto',
        )
    ])
    fig_bar.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=230,
        yaxis=dict(title="Calories (kcal)", showgrid=True),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# 3. 7-Day Interactive Weekly Schedule
st.subheader("📅 7-Day High-Protein & Pocket-Friendly Meal Schedule")

tab_mon, tab_tue, tab_wed, tab_thu, tab_fri, tab_sat, tab_sun = st.tabs(DAYS_OF_WEEK)
tabs_dict = {
    "Monday": tab_mon,
    "Tuesday": tab_tue,
    "Wednesday": tab_wed,
    "Thursday": tab_thu,
    "Friday": tab_fri,
    "Saturday": tab_sat,
    "Sunday": tab_sun
}


def apply_chosen_meal(day_name, meal_idx, chosen_meal_obj, target_cals):
    """Applies a specifically selected meal object to session_state."""
    scale = target_cals / chosen_meal_obj["calories"] if chosen_meal_obj["calories"] > 0 else 1.0

    st.session_state.weekly_plan[day_name]["meals"][meal_idx] = {
        "id": chosen_meal_obj["id"],
        "meal_type": chosen_meal_obj.get("meal_type", "Meal"),
        "name": chosen_meal_obj["name"],
        "calories": round(chosen_meal_obj["calories"] * scale),
        "protein": round(chosen_meal_obj["protein"] * scale),
        "carbs": round(chosen_meal_obj["carbs"] * scale),
        "fat": round(chosen_meal_obj["fat"] * scale),
        "fiber": round(chosen_meal_obj["fiber"] * scale),
        "is_budget": chosen_meal_obj.get("is_budget", False),
        "cost_level": chosen_meal_obj.get("cost_level", "$$"),
        "ingredients": chosen_meal_obj["ingredients"],
        "recipe": chosen_meal_obj["recipe"],
        "prep_time": chosen_meal_obj.get("prep_time", "15 mins"),
        "diet_tags": chosen_meal_obj.get("diet", [])
    }
    day_m = st.session_state.weekly_plan[day_name]["meals"]
    st.session_state.weekly_plan[day_name]["totals"] = {
        "calories": sum(m["calories"] for m in day_m),
        "protein": sum(m["protein"] for m in day_m),
        "carbs": sum(m["carbs"] for m in day_m),
        "fat": sum(m["fat"] for m in day_m),
        "fiber": sum(m["fiber"] for m in day_m)
    }


for day_name in DAYS_OF_WEEK:
    with tabs_dict[day_name]:
        day_data = weekly_plan[day_name]
        totals = day_data["totals"]
        
        # Day Totals Banner
        st.info(
            f"**{day_name} Daily Totals:** ⚡ **{totals['calories']} kcal** | "
            f"🥩 **{totals['protein']}g Protein** | "
            f"🌾 **{totals['carbs']}g Carbs** | "
            f"🌱 **{totals['fiber']}g Fiber** | "
            f"🥑 **{totals['fat']}g Fat**"
        )
        
        m_col1, m_col2 = st.columns(2)
        meals = day_data["meals"]

        for idx, meal in enumerate(meals):
            col_target = m_col1 if idx % 2 == 0 else m_col2
            with col_target:
                with st.container(border=True):
                    head_col1, head_col2 = st.columns([3, 1])
                    with head_col1:
                        budget_badge = " 🏷️ *(Pocket-Friendly)*" if meal.get("is_budget") else ""
                        st.markdown(f"**{meal['meal_type'].upper()}: {meal['name']}**{budget_badge}")
                    with head_col2:
                        st.markdown(f"🔥 `{meal['calories']} kcal`")

                    # Badges
                    budget_html = "<span class='badge-budget'>💲 Pocket Friendly ($)</span> " if meal.get("is_budget") else f"<span class='badge-carb'>{meal.get('cost_level', '$$')}</span> "
                    st.markdown(
                        f"{budget_html}"
                        f"<span class='badge-protein'>Protein: {meal['protein']}g</span> "
                        f"<span class='badge-carb'>Carbs: {meal['carbs']}g</span> "
                        f"<span class='badge-fiber'>Fiber: {meal['fiber']}g</span> "
                        f"<span class='badge-fat'>Fat: {meal['fat']}g</span>",
                        unsafe_allow_html=True
                    )
                    
                    with st.expander(f"🛒 Ingredients & Recipe ({meal['prep_time']})"):
                        st.markdown("**Ingredients:**")
                        for ing in meal["ingredients"]:
                            st.markdown(f"- {ing}")
                        st.markdown(f"**Instructions:**\n{meal['recipe']}")

                    # Meal Swap Dropdown Selector (Allows picking ANY meal from full catalog)
                    cat_key = "snack" if "snack" in meal["meal_type"].lower() else meal["meal_type"].lower()
                    all_candidates = filter_meals_by_diet(cat_key, user["diet_pref"].lower(), "any")
                    
                    with st.expander("🔄 Choose / Swap Meal", expanded=False):
                        option_labels = [
                            f"{'(💲 Pocket-Friendly) ' if m.get('is_budget') else ''}{m['name']} (~{m['calories']} kcal, {m['protein']}g P)"
                            for m in all_candidates
                        ]
                        curr_pick_idx = 0
                        for c_i, c_m in enumerate(all_candidates):
                            if c_m["id"] == meal["id"]:
                                curr_pick_idx = c_i
                                break
                        
                        selected_option = st.selectbox(
                            f"Select alternative {meal['meal_type']}:",
                            options=range(len(all_candidates)),
                            format_func=lambda i: option_labels[i],
                            index=curr_pick_idx,
                            key=f"select_{day_name}_{idx}"
                        )
                        
                        if selected_option != curr_pick_idx:
                            picked_meal = all_candidates[selected_option]
                            apply_chosen_meal(day_name, idx, picked_meal, meal["calories"])
                            st.rerun()

st.markdown("---")

# 4. Export & Utility Section
exp_col1, exp_col2 = st.columns(2)

with exp_col1:
    st.subheader("🛒 Weekly Grocery Checklist")
    with st.expander("View Full 7-Day Ingredient Shopping List", expanded=False):
        for item in st.session_state.grocery_list:
            st.checkbox(f"{item['item']} (Used in ~{item['frequency']} meals)", key=f"groc_{item['item']}")

with exp_col2:
    st.subheader("📥 Export & Downloads")
    
    csv_rows = []
    for d in DAYS_OF_WEEK:
        d_data = weekly_plan[d]
        for m in d_data["meals"]:
            csv_rows.append({
                "Day": d,
                "Meal Type": m["meal_type"],
                "Meal Name": m["name"],
                "Pocket Friendly": "Yes ($)" if m.get("is_budget") else "Standard ($$)",
                "Calories": m["calories"],
                "Protein (g)": m["protein"],
                "Carbs (g)": m["carbs"],
                "Fiber (g)": m["fiber"],
                "Fat (g)": m["fat"],
                "Ingredients": "; ".join(m["ingredients"]),
                "Recipe": m["recipe"]
            })
    df_export = pd.DataFrame(csv_rows)
    csv_buffer = df_export.to_csv(index=False)
    
    st.download_button(
        label="📄 Download 7-Day Plan (CSV)",
        data=csv_buffer,
        file_name=f"{user['name'].replace(' ', '_')}_Diet_Plan.csv",
        mime="text/csv",
        use_container_width=True
    )
