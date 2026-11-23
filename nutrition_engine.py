"""
Nutrition & Meal Plan Calculation Engine
Calculates BMR, TDEE, Deficit Calorie Targets, High-Protein / High-Fiber Macro Split,
and generates customizable 7-day meal plans with recipes and grocery lists.
Includes extensive pocket-friendly (budget-friendly) high-protein staples.
"""

from typing import Dict, List, Any, Optional
import math


# Comprehensive High-Protein, Low-Calorie, High-Fiber & Budget-Friendly Meal Database
MEAL_DATABASE = {
    "breakfast": [
        {
            "id": "b1",
            "name": "Spinach & Egg White Scramble with Avocado Whole Wheat Toast",
            "diet": ["non_veg", "any", "pescatarian"],
            "calories": 360,
            "protein": 34,
            "carbs": 26,
            "fat": 12,
            "fiber": 7,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["4 large egg whites + 1 whole egg", "1 cup fresh baby spinach", "1 slice 100% whole grain bread", "1/4 avocado mashed", "Pinch of black pepper & turmeric"],
            "recipe": "Whisk egg whites and whole egg. Sauté spinach in non-stick spray for 1 min, pour in eggs and scramble gently. Toast whole wheat bread and top with mashed avocado.",
            "prep_time": "10 mins"
        },
        {
            "id": "b2",
            "name": "High-Protein Greek Yogurt Berry & Chia Bowl",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 340,
            "protein": 35,
            "carbs": 32,
            "fat": 8,
            "fiber": 9,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["200g 0% fat Greek Yogurt", "1 scoop Whey/Plant Isolate (vanilla)", "1/2 cup blueberries or raspberries", "1 tbsp chia seeds", "10 crushed almonds"],
            "recipe": "Mix Greek yogurt with protein isolate until smooth and creamy. Top with fresh berries, chia seeds, and crushed almonds.",
            "prep_time": "5 mins"
        },
        {
            "id": "b3",
            "name": "Overnight High-Protein High-Fiber Power Oats",
            "diet": ["vegetarian", "vegan", "any", "non_veg", "pescatarian"],
            "calories": 380,
            "protein": 32,
            "carbs": 44,
            "fat": 9,
            "fiber": 11,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["50g rolled oats", "1 scoop plant/whey protein powder", "1 tbsp flaxseed meal", "150ml unsweetened almond milk", "1/2 sliced green apple", "Pinch of cinnamon"],
            "recipe": "Combine oats, protein powder, flaxseed meal, cinnamon, and almond milk in a jar. Refrigerate overnight. Top with sliced apple before serving.",
            "prep_time": "5 mins (make ahead)"
        },
        {
            "id": "b4",
            "name": "Smoked Salmon & Cottage Cheese Sourdough",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 350,
            "protein": 36,
            "carbs": 24,
            "fat": 11,
            "fiber": 5,
            "is_budget": False,
            "cost_level": "$$$",
            "ingredients": ["100g low-fat cottage cheese", "75g wild smoked salmon", "1 slice artisanal sourdough toast", "Capers, cucumber slices, fresh dill"],
            "recipe": "Spread cottage cheese over toasted sourdough. Layer with smoked salmon, cucumber ribbons, capers, and a pinch of fresh dill.",
            "prep_time": "7 mins"
        },
        {
            "id": "b5",
            "name": "Tofu Scramble with Bell Peppers & Black Beans",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 350,
            "protein": 30,
            "carbs": 30,
            "fat": 12,
            "fiber": 10,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["180g firm tofu (crumbled)", "1/3 cup canned black beans (rinsed)", "1/2 diced bell pepper", "1/2 cup kale", "1/2 tsp nutritional yeast, turmeric, garlic powder"],
            "recipe": "Sauté diced peppers in a skillet. Crumble tofu and add spices, black beans, and chopped kale. Cook for 6-8 minutes until golden and fragrant.",
            "prep_time": "12 mins"
        },
        {
            "id": "b6",
            "name": "Protein Banana Oat Pancakes with Sugar-Free Maple Syrup",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 370,
            "protein": 33,
            "carbs": 42,
            "fat": 7,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 medium banana", "40g oat flour", "1 scoop vanilla protein", "2 egg whites (or 50ml almond milk)", "1 tsp baking powder", "1 tbsp sugar-free maple syrup"],
            "recipe": "Blend banana, oat flour, protein powder, egg whites, and baking powder. Cook silver dollar pancakes in a non-stick pan on medium heat for 2 mins each side.",
            "prep_time": "12 mins"
        },
        {
            "id": "b7",
            "name": "Mediterranean Veggie Omelet with Feta & Arugula",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 340,
            "protein": 31,
            "carbs": 14,
            "fat": 18,
            "fiber": 5,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["2 whole eggs + 2 egg whites", "30g light crumbled feta", "1/2 cup cherry tomatoes halved", "1 cup arugula", "1/4 red onion thinly sliced"],
            "recipe": "Whisk eggs. Cook tomatoes and onion in pan, pour eggs and cook until set. Fold with light feta and fresh arugula.",
            "prep_time": "10 mins"
        },
        {
            "id": "b8",
            "name": "Pocket-Friendly Scrambled Eggs with Steamed Peas & Toast",
            "diet": ["non_veg", "vegetarian", "any", "pescatarian"],
            "calories": 350,
            "protein": 32,
            "carbs": 30,
            "fat": 11,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["3 large whole eggs", "1/2 cup frozen green peas (thawed)", "1 slice whole wheat bread", "1/4 tsp black pepper & pinch of chili flakes"],
            "recipe": "Whisk eggs with a splash of water and pepper. Sauté green peas in a pan for 1 min, pour in eggs and scramble gently. Serve alongside toasted whole grain bread.",
            "prep_time": "7 mins"
        },
        {
            "id": "b9",
            "name": "Budget Savory Oatmeal with Boiled Eggs & Spinach",
            "diet": ["non_veg", "vegetarian", "any", "pescatarian"],
            "calories": 360,
            "protein": 30,
            "carbs": 36,
            "fat": 10,
            "fiber": 7,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["45g rolled oats (cooked in water with pinch of salt & turmeric)", "2 hard-boiled eggs (sliced)", "1 cup fresh spinach leaves", "1 tsp soy sauce or hot sauce"],
            "recipe": "Cook oats in simmering salted water for 4 mins. Stir in spinach until wilted. Top with sliced hard-boiled eggs and a dash of hot sauce or black pepper.",
            "prep_time": "8 mins"
        },
        {
            "id": "b10",
            "name": "High-Protein Spiced Moong Dal Cheela (Yellow Lentil Crepes)",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 340,
            "protein": 28,
            "carbs": 44,
            "fat": 6,
            "fiber": 12,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["60g split yellow moong dal (soaked & ground to batter)", "1/2 finely chopped onion", "1 green chili & ginger", "2 tbsp chopped cilantro", "Pinch of cumin & asafoetida"],
            "recipe": "Blend soaked moong dal with ginger and green chili into a smooth pancake batter. Mix in chopped onions and cilantro. Spread onto a hot non-stick pan and cook both sides until crisp.",
            "prep_time": "12 mins"
        },
        {
            "id": "b11",
            "name": "Budget Peanut Butter & Banana Oatmeal Power Bowl",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 380,
            "protein": 24,
            "carbs": 52,
            "fat": 11,
            "fiber": 9,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["55g rolled oats", "1.5 tbsp pure peanut butter", "1 medium banana (sliced)", "1 tbsp roasted flaxseed / sunflower seeds", "Pinch of cinnamon"],
            "recipe": "Cook rolled oats in water or milk. Stir in natural peanut butter while warm until rich and creamy. Top with sliced banana, seeds, and cinnamon.",
            "prep_time": "6 mins"
        },
        {
            "id": "b12",
            "name": "Budget Soya Mince (Granules) Bhurji with Whole Wheat Toast",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 360,
            "protein": 38,
            "carbs": 34,
            "fat": 7,
            "fiber": 11,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["50g soya chunks/granules (boiled & squeezed dry)", "1/2 chopped onion & tomato", "1/2 tsp turmeric, garam masala & cumin", "1 slice whole wheat toast", "1 tsp oil"],
            "recipe": "Sauté onions, tomatoes, and spices in 1 tsp oil. Add minced cooked soya granules and stir fry on medium heat for 6 mins. Serve hot with whole wheat toast.",
            "prep_time": "12 mins"
        },
        {
            "id": "b13",
            "name": "Curd & Sprouted Moong High-Fiber Protein Bowl",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 330,
            "protein": 28,
            "carbs": 38,
            "fat": 6,
            "fiber": 10,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["200g homemade fresh curd / plain yogurt", "3/4 cup boiled sprouted green moong", "1/2 diced cucumber & tomato", "1/2 tsp roasted cumin powder & black salt"],
            "recipe": "Whisk fresh curd in a bowl. Fold in warm boiled sprouted moong, diced cucumbers, tomatoes, roasted cumin powder, and black salt.",
            "prep_time": "5 mins"
        },
        {
            "id": "b14",
            "name": "Budget Canned Tuna & Egg White Breakfast Melt",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 350,
            "protein": 42,
            "carbs": 22,
            "fat": 8,
            "fiber": 5,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1/2 can chunk light tuna in water (drained)", "2 egg whites (scrambled)", "1 slice whole wheat bread", "1 slice light low-fat cheese (or 1 tbsp curd)", "Pinch of black pepper & lemon"],
            "recipe": "Mix drained tuna with scrambled egg whites, lemon juice, and black pepper. Pile onto whole wheat bread, top with light cheese, and toast under a broiler for 3 mins.",
            "prep_time": "8 mins"
        }
    ],
    "lunch": [
        {
            "id": "l1",
            "name": "Grilled Lemon Herb Chicken Breast & Quinoa Buddha Bowl",
            "diet": ["non_veg", "any"],
            "calories": 440,
            "protein": 46,
            "carbs": 38,
            "fat": 10,
            "fiber": 9,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["160g chicken breast", "1/2 cup cooked tri-color quinoa", "1 cup steamed broccoli florets", "1/2 cup roasted zucchini", "1 tbsp lemon-tahini dressing"],
            "recipe": "Season chicken with oregano, garlic, salt and grill for 6-7 mins per side. Assemble bowl with warm quinoa, steamed broccoli, roasted zucchini, and drizzle with lemon tahini.",
            "prep_time": "20 mins"
        },
        {
            "id": "l2",
            "name": "Pan-Seared Salmon Fillet with Asparagus & Sweet Potato Mash",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 460,
            "protein": 42,
            "carbs": 36,
            "fat": 16,
            "fiber": 8,
            "is_budget": False,
            "cost_level": "$$$",
            "ingredients": ["150g Atlantic salmon fillet", "120g sweet potato (boiled & mashed)", "8 spears fresh asparagus", "1 tsp olive oil", "Lemon wedge"],
            "recipe": "Sear salmon skin-side down for 4 mins, flip and cook 3 mins. Steam asparagus and serve alongside mashed sweet potato seasoned with cinnamon and sea salt.",
            "prep_time": "18 mins"
        },
        {
            "id": "l3",
            "name": "Spiced Chickpea & Paneer/Tofu Power Salad",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 420,
            "protein": 34,
            "carbs": 40,
            "fat": 14,
            "fiber": 12,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["120g low-fat paneer or extra-firm tofu", "1/2 cup chickpeas (boiled)", "2 cups mixed greens", "1/2 cucumber diced", "1 tbsp balsamic glaze", "1 tbsp pumpkin seeds"],
            "recipe": "Cube paneer/tofu and pan-sear with cumin, paprika, and chili flakes. Toss with chickpeas, mixed baby greens, cucumbers, and dress with balsamic and pumpkin seeds.",
            "prep_time": "15 mins"
        },
        {
            "id": "l4",
            "name": "Zesty Ground Turkey Burrito Bowl (Brown Rice & Black Beans)",
            "diet": ["non_veg", "any"],
            "calories": 450,
            "protein": 44,
            "carbs": 42,
            "fat": 11,
            "fiber": 10,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["150g extra lean ground turkey (93/7 or 99/1)", "1/3 cup cooked brown rice", "1/3 cup black beans", "1/4 cup salsa fresco", "1/4 avocado diced", "Cilantro & lime"],
            "recipe": "Brown turkey with taco spices (cumin, chili, onion powder). Layer brown rice, rinsed black beans, lean turkey, fresh tomato salsa, diced avocado, and fresh cilantro.",
            "prep_time": "15 mins"
        },
        {
            "id": "l5",
            "name": "Lentil, Edamame & Roasted Vegetable Protein Medley",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 410,
            "protein": 32,
            "carbs": 48,
            "fat": 9,
            "fiber": 14,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1/2 cup cooked brown lentils", "1/2 cup shelled edamame", "1 cup roasted cauliflower & carrots", "1 cup baby spinach", "1 tbsp tahini-lemon dressing"],
            "recipe": "Combine warm cooked brown lentils and steamed edamame with roasted spiced cauliflower and carrots over a bed of raw spinach. Drizzle with lemon tahini.",
            "prep_time": "15 mins"
        },
        {
            "id": "l6",
            "name": "Seared Tuna Steak with Edamame & Sesame Green Beans",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 430,
            "protein": 48,
            "carbs": 24,
            "fat": 14,
            "fiber": 8,
            "is_budget": False,
            "cost_level": "$$$",
            "ingredients": ["160g yellowfin tuna steak", "3/4 cup steamed edamame pods", "1 cup tender green beans", "1 tsp sesame oil", "1 tsp low-sodium soy sauce", "Sesame seeds"],
            "recipe": "Sear tuna steak for 90 seconds on each side in a hot pan. Sauté green beans in sesame oil and low-sodium soy sauce; serve with steamed edamame and sesame seeds.",
            "prep_time": "12 mins"
        },
        {
            "id": "l7",
            "name": "Grilled Lemon-Herb Tofu Steaks with Wild Rice & Asparagus",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 410,
            "protein": 33,
            "carbs": 44,
            "fat": 11,
            "fiber": 9,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["200g firm tofu pressed and sliced", "1/2 cup cooked wild rice", "1 cup roasted asparagus", "1 tbsp lemon-garlic marinade", "1 tbsp nutritional yeast"],
            "recipe": "Marinate tofu in lemon juice, garlic, and herbs. Grill in a grill pan until char marks appear. Serve over cooked wild rice with seasoned roasted asparagus.",
            "prep_time": "18 mins"
        },
        {
            "id": "l8",
            "name": "Budget Canned Tuna & Chickpea Mediterranean Protein Salad",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 410,
            "protein": 45,
            "carbs": 36,
            "fat": 8,
            "fiber": 11,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 can (150g) chunk light tuna in water", "3/4 cup cooked/canned chickpeas (rinsed)", "1 cup chopped cucumbers & tomatoes", "1 tbsp lemon juice & 1 tsp olive oil", "Black pepper & oregano"],
            "recipe": "Drain tuna well. In a large bowl, toss tuna with rinsed chickpeas, crisp cucumber cubes, diced tomatoes, fresh lemon juice, oregano, and olive oil.",
            "prep_time": "8 mins"
        },
        {
            "id": "l9",
            "name": "High-Protein Moong Dal Khichdi with Fresh Curd",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 420,
            "protein": 30,
            "carbs": 58,
            "fat": 6,
            "fiber": 13,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1/2 cup split yellow moong lentils", "1/4 cup brown rice", "1/2 cup frozen mixed peas & carrots", "150g plain low-fat curd / yogurt", "Cumin, ginger, turmeric"],
            "recipe": "Pressure cook or simmer moong dal, brown rice, and vegetables with turmeric, ginger, and salt until soft and creamy. Serve warm accompanied by fresh curd.",
            "prep_time": "20 mins"
        },
        {
            "id": "l10",
            "name": "Budget Soya Chunks & Green Pea Pulao with Spiced Raita",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 430,
            "protein": 42,
            "carbs": 48,
            "fat": 7,
            "fiber": 14,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["55g dry soya chunks (boiled, squeezed & diced)", "1/2 cup cooked brown rice", "1/2 cup green peas", "1/2 sliced onion", "100g curd or cucumber mint relish"],
            "recipe": "Sauté sliced onions, cumin, and spices. Add boiled soya chunks and peas; cook for 4 mins. Fold in warm cooked brown rice. Serve with fresh cucumber raita.",
            "prep_time": "15 mins"
        },
        {
            "id": "l11",
            "name": "Black Bean & Roasted Corn Fiesta Bowl",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 400,
            "protein": 26,
            "carbs": 56,
            "fat": 7,
            "fiber": 16,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 cup canned black beans (rinsed & warmed with cumin)", "1/2 cup sweet corn", "1/3 cup cooked brown rice", "1/4 cup tomato salsa", "Cilantro & squeeze of lime"],
            "recipe": "Heat black beans with ground cumin and garlic powder. Layer warm brown rice, black beans, sweet corn, salsa, and fresh chopped cilantro. Squeeze lime over top.",
            "prep_time": "10 mins"
        },
        {
            "id": "l12",
            "name": "Budget Spiced Egg Bhurji Bowl with Brown Rice & Peas",
            "diet": ["non_veg", "vegetarian", "any", "pescatarian"],
            "calories": 420,
            "protein": 32,
            "carbs": 38,
            "fat": 14,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["3 whole eggs + 1 egg white", "1/2 cup cooked brown rice", "1/2 cup green peas", "1/2 chopped onion & green chili", "Pinch of garam masala & turmeric"],
            "recipe": "Sauté onions, chilies, and peas in a pan. Whisk and pour in eggs with spices, scramble until cooked. Serve over warm steamed brown rice.",
            "prep_time": "12 mins"
        },
        {
            "id": "l13",
            "name": "High-Protein Rajma (Kidney Beans) & Spiced Cauliflower Bowl",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 410,
            "protein": 28,
            "carbs": 56,
            "fat": 6,
            "fiber": 17,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 cup cooked red kidney beans (Rajma)", "1.5 cups grated cauliflower rice (steamed with cumin)", "1/2 cup onion-tomato masala gravy", "Fresh coriander"],
            "recipe": "Simmer cooked kidney beans in seasoned onion-tomato gravy. Sauté cauliflower rice with a pinch of cumin and turmeric for 3 mins. Serve rajma over cauliflower rice.",
            "prep_time": "15 mins"
        },
        {
            "id": "l14",
            "name": "Budget Canned Sardines & White Bean Protein Salad",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 420,
            "protein": 40,
            "carbs": 34,
            "fat": 12,
            "fiber": 10,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 can (120g) sardines in water or light olive oil", "3/4 cup canned cannellini or navy beans (rinsed)", "1 cup chopped spinach or arugula", "1 tbsp lemon juice & cracked black pepper"],
            "recipe": "Gently toss rinsed white beans with leafy greens, lemon juice, and black pepper. Top with flaky drained sardines and fresh parsley.",
            "prep_time": "6 mins"
        }
    ],
    "snack": [
        {
            "id": "s1",
            "name": "Whey / Plant Protein Shake with Ground Flaxseed",
            "diet": ["vegetarian", "vegan", "any", "non_veg", "pescatarian"],
            "calories": 180,
            "protein": 27,
            "carbs": 8,
            "fat": 4,
            "fiber": 4,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["1 scoop Protein Isolate (Chocolate or Vanilla)", "250ml cold water or almond milk", "1 tbsp ground flaxseeds"],
            "recipe": "Shake vigorously in a shaker bottle with ice cubes for 30 seconds until frothy.",
            "prep_time": "2 mins"
        },
        {
            "id": "s2",
            "name": "Low-Fat Cottage Cheese with Cucumber Ribbons & Walnuts",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 190,
            "protein": 22,
            "carbs": 9,
            "fat": 7,
            "fiber": 3,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["150g 1% cottage cheese", "1 mini Persian cucumber sliced", "10g chopped walnuts", "Cracked black pepper"],
            "recipe": "Place cottage cheese in a bowl, arrange cucumber slices, top with chopped walnuts and black pepper.",
            "prep_time": "3 mins"
        },
        {
            "id": "s3",
            "name": "Dry Roasted Spicy Edamame & Apple Slices",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 180,
            "protein": 17,
            "carbs": 21,
            "fat": 4,
            "fiber": 7,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["40g dry roasted edamame", "1 small crisp green apple", "Pinch of cinnamon"],
            "recipe": "Enjoy crunchy dry-roasted edamame alongside crisp apple slices dusted with cinnamon.",
            "prep_time": "2 mins"
        },
        {
            "id": "s4",
            "name": "Hard-Boiled Eggs with Baby Carrots & Hummus",
            "diet": ["non_veg", "vegetarian", "any", "pescatarian"],
            "calories": 200,
            "protein": 16,
            "carbs": 12,
            "fat": 9,
            "fiber": 4,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["2 hard-boiled eggs", "10 baby carrots", "2 tbsp classic hummus", "Everything bagel seasoning"],
            "recipe": "Peel eggs and sprinkle with everything bagel seasoning. Dip carrots in hummus.",
            "prep_time": "3 mins"
        },
        {
            "id": "s5",
            "name": "Greek Yogurt with Chia Seeds & Cinnamon",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 170,
            "protein": 20,
            "carbs": 12,
            "fat": 4,
            "fiber": 5,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["150g non-fat Greek yogurt", "1 tbsp chia seeds", "1 tsp stevia/monkfruit", "1/2 tsp ground cinnamon"],
            "recipe": "Stir chia seeds and sweetener into Greek yogurt. Let sit for 5 minutes to thicken.",
            "prep_time": "5 mins"
        },
        {
            "id": "s6",
            "name": "Roasted Chickpeas Crunch with Celery & Peanut Butter Powder",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 190,
            "protein": 15,
            "carbs": 24,
            "fat": 4,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["45g oven-roasted crunchy chickpeas", "3 celery stalks", "2 tbsp PB2 / defatted peanut powder mixed with water"],
            "recipe": "Spread reconstituted peanut powder onto celery sticks; enjoy alongside crunchy roasted chickpeas.",
            "prep_time": "4 mins"
        },
        {
            "id": "s7",
            "name": "Turkey Breast Roll-Ups with Bell Pepper Strips",
            "diet": ["non_veg", "any"],
            "calories": 160,
            "protein": 24,
            "carbs": 5,
            "fat": 4,
            "fiber": 2,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["100g roasted sliced turkey breast", "1/2 yellow bell pepper sliced into strips", "1 tsp Dijon mustard"],
            "recipe": "Spread a dab of Dijon mustard onto each turkey slice, wrap around pepper sticks and enjoy.",
            "prep_time": "3 mins"
        },
        {
            "id": "s8",
            "name": "Pocket-Friendly Roasted Black Chickpeas (Bhuna Chana)",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 180,
            "protein": 18,
            "carbs": 22,
            "fat": 3,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["50g roasted dry black chickpeas (with husk)", "1/2 tsp chaat masala", "Squeeze of lemon juice"],
            "recipe": "Toss crispy roasted black chickpeas with a pinch of chaat masala and fresh lemon juice for an ultra-cheap, high-protein snack.",
            "prep_time": "1 min"
        },
        {
            "id": "s9",
            "name": "Budget Curd with Roasted Peanuts & Sliced Banana",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 190,
            "protein": 16,
            "carbs": 18,
            "fat": 7,
            "fiber": 4,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["150g homemade plain curd / yogurt", "15g roasted unsalted peanuts", "1/2 sliced ripe banana", "Pinch of cinnamon"],
            "recipe": "Top smooth chilled curd with roasted crunchy peanuts, sliced banana, and cinnamon.",
            "prep_time": "2 mins"
        },
        {
            "id": "s10",
            "name": "Sprouted Moong & Cucumber Protein Chaat",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 170,
            "protein": 16,
            "carbs": 22,
            "fat": 2,
            "fiber": 9,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["3/4 cup steamed sprouted green moong", "1/2 chopped cucumber & tomato", "1 tbsp lemon juice & black pepper", "Fresh cilantro"],
            "recipe": "Mix warm steamed sprouted moong with diced cucumber, tomato, fresh lemon juice, black pepper, and fresh cilantro.",
            "prep_time": "4 mins"
        },
        {
            "id": "s11",
            "name": "Budget 2 Hard-Boiled Eggs with Mustard & Paprika",
            "diet": ["non_veg", "vegetarian", "any", "pescatarian"],
            "calories": 160,
            "protein": 14,
            "carbs": 2,
            "fat": 10,
            "fiber": 1,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["2 whole large eggs", "1 tsp yellow or Dijon mustard", "Smoked paprika & black pepper"],
            "recipe": "Halve hard-boiled eggs, spread a light drop of mustard on each yolk, and dust with smoked paprika.",
            "prep_time": "2 mins"
        },
        {
            "id": "s12",
            "name": "Budget Low-Fat Paneer / Cottage Cheese Cubes with Chaat Masala",
            "diet": ["vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 180,
            "protein": 22,
            "carbs": 6,
            "fat": 7,
            "fiber": 2,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["120g low-fat paneer or firm cottage cheese (cubed)", "1 mini cucumber (sliced)", "Pinch of black salt & chaat masala", "Squeeze of lemon"],
            "recipe": "Toss raw or light-pan-seared paneer cubes with sliced cucumbers, lemon juice, and chaat masala.",
            "prep_time": "3 mins"
        },
        {
            "id": "s13",
            "name": "Crisp Apple Slices with Pure Peanut Butter",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 190,
            "protein": 8,
            "carbs": 24,
            "fat": 9,
            "fiber": 6,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 medium crisp apple (sliced)", "1.5 tbsp 100% natural peanut butter", "Pinch of cinnamon"],
            "recipe": "Slice apple into wedges and dip into creamy natural peanut butter dusted with cinnamon.",
            "prep_time": "2 mins"
        },
        {
            "id": "s14",
            "name": "Budget Dry Roasted Soynuts & Raisin Mix",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 180,
            "protein": 18,
            "carbs": 16,
            "fat": 5,
            "fiber": 7,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["35g dry roasted soybeans (soy nuts)", "10g golden raisins", "Pinch of sea salt"],
            "recipe": "Combine crunchy roasted soybeans with sweet raisins for an inexpensive on-the-go protein boost.",
            "prep_time": "1 min"
        }
    ],
    "dinner": [
        {
            "id": "d1",
            "name": "Herb-Crusted Baked Cod Fillet with Roasted Cauliflower & Green Beans",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 390,
            "protein": 44,
            "carbs": 22,
            "fat": 11,
            "fiber": 9,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["180g Pacific cod fillet", "1.5 cups cauliflower florets", "1 cup fresh green beans", "1 tsp olive oil", "Garlic powder, paprika, fresh parsley, lemon"],
            "recipe": "Toss cauliflower and green beans in olive oil and roast at 200°C (400°F) for 20 mins. Season cod with herbs and bake for 12-14 mins until flaky.",
            "prep_time": "22 mins"
        },
        {
            "id": "d2",
            "name": "Grilled Rosemary Chicken with Steamed Brussels Sprouts & Baked Sweet Potato",
            "diet": ["non_veg", "any"],
            "calories": 420,
            "protein": 45,
            "carbs": 34,
            "fat": 9,
            "fiber": 10,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["160g chicken breast", "100g baked sweet potato", "1 cup halved Brussels sprouts", "1 tsp olive oil", "Fresh rosemary, garlic, sea salt"],
            "recipe": "Marinate chicken in garlic, rosemary and lemon juice. Grill for 6 mins per side. Roast Brussels sprouts in oven with light spray. Serve with warm baked sweet potato.",
            "prep_time": "25 mins"
        },
        {
            "id": "d3",
            "name": "Tofu & Edamame Vegetable Stir-Fry with Miracle Shirataki Noodles",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 360,
            "protein": 34,
            "carbs": 26,
            "fat": 12,
            "fiber": 12,
            "is_budget": False,
            "cost_level": "$$",
            "ingredients": ["180g extra firm tofu cubes", "1/2 cup shelled edamame", "1 pack shirataki or konjac noodles (rinsed)", "1.5 cups stir-fry veg (broccoli, snap peas, peppers)", "1.5 tbsp coconut aminos / low-sodium soy sauce", "Ginger & garlic"],
            "recipe": "Sear tofu until crispy. Add vegetables and stir fry on high heat with ginger and garlic. Add drained noodles and coconut aminos; toss well for 3 mins.",
            "prep_time": "15 mins"
        },
        {
            "id": "d4",
            "name": "Extra Lean Beef Steak (Sirloin) with Asparagus & Garlic Mashed Cauliflower",
            "diet": ["non_veg", "any"],
            "calories": 430,
            "protein": 46,
            "carbs": 18,
            "fat": 18,
            "fiber": 7,
            "is_budget": False,
            "cost_level": "$$$",
            "ingredients": ["150g trimmed lean top sirloin steak", "1.5 cups steamed cauliflower (mashed with 1 tbsp Greek yogurt & garlic)", "10 spears roasted asparagus", "Black pepper & sea salt"],
            "recipe": "Sear sirloin steak in a hot skillet for 3-4 mins per side for medium. Blend steamed cauliflower with Greek yogurt and garlic into creamy mash. Serve with asparagus.",
            "prep_time": "18 mins"
        },
        {
            "id": "d5",
            "name": "High-Protein Lentil & Black Bean Chili with Spinach",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 390,
            "protein": 31,
            "carbs": 52,
            "fat": 6,
            "fiber": 16,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1/2 cup cooked brown lentils", "1/2 cup canned black beans", "1/2 cup crushed canned tomatoes", "1.5 cups fresh baby spinach", "1/2 diced onion & bell pepper", "Chili powder, cumin, smoked paprika"],
            "recipe": "Sauté onion and peppers, add canned tomatoes, lentils, black beans, and chili seasonings. Simmer 12 mins. Stir in spinach at the end until wilted.",
            "prep_time": "20 mins"
        },
        {
            "id": "d6",
            "name": "Grilled Lemon Salmon with Roasted Zucchini Ribbons & Quinoa",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 440,
            "protein": 40,
            "carbs": 32,
            "fat": 15,
            "fiber": 7,
            "is_budget": False,
            "cost_level": "$$$",
            "ingredients": ["140g wild salmon fillet", "1/3 cup cooked quinoa", "1.5 cups sliced zucchini & yellow squash", "1 tsp olive oil", "Garlic herb seasoning"],
            "recipe": "Grill seasoned salmon fillet for 4 mins per side. Sauté zucchini ribbons with garlic and olive oil. Plate with warm quinoa and fresh lemon wedge.",
            "prep_time": "18 mins"
        },
        {
            "id": "d7",
            "name": "Low-Fat Paneer / Tempeh Tikka with Roasted Veggies & Mint Raita",
            "diet": ["vegetarian", "vegan", "any", "non_veg", "pescatarian"],
            "calories": 380,
            "protein": 33,
            "carbs": 28,
            "fat": 13,
            "fiber": 9,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["150g low-fat paneer or tempeh cubes", "1 diced bell pepper & red onion", "2 tbsp non-fat Greek yogurt (or soy yogurt) for marinade", "Tandoori spice blend", "Cucumber mint dip"],
            "recipe": "Marinate paneer/tempeh and vegetable chunks in spiced yogurt. Skewer or spread on a baking sheet and broil at 220°C (425°F) for 12-15 mins until charred.",
            "prep_time": "20 mins"
        },
        {
            "id": "d8",
            "name": "Budget Indian Egg Curry (3 Boiled Eggs) with Brown Rice",
            "diet": ["non_veg", "vegetarian", "any", "pescatarian"],
            "calories": 410,
            "protein": 32,
            "carbs": 36,
            "fat": 14,
            "fiber": 7,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["3 large hard-boiled eggs (peeled & pierced)", "1/2 cup cooked brown rice", "1/2 cup onion-tomato spiced gravy", "1 cup steamed spinach or cabbage", "Cumin, coriander, turmeric"],
            "recipe": "Simmer boiled eggs in a fragrant spiced onion-tomato curry for 6 mins. Serve hot over steamed brown rice with wilted greens.",
            "prep_time": "15 mins"
        },
        {
            "id": "d9",
            "name": "Crispy Budget Soya Chunk & Cabbage Stir-Fry with Garlic Soy",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 370,
            "protein": 44,
            "carbs": 34,
            "fat": 6,
            "fiber": 14,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["60g dehydrated soya chunks (rehydrated & seared)", "2 cups shredded green cabbage & carrots", "1.5 tbsp low-sodium soy sauce", "1 tsp sesame or mustard oil", "Minced garlic & chili flakes"],
            "recipe": "Squeeze rehydrated soya chunks dry and sear in a hot pan until golden brown. Toss in shredded cabbage, garlic, and soy sauce on high heat for 4 minutes.",
            "prep_time": "14 mins"
        },
        {
            "id": "d10",
            "name": "Pan-Seared Budget Tilapia with Frozen Mixed Veggies & Brown Rice",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 390,
            "protein": 42,
            "carbs": 34,
            "fat": 8,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["170g frozen tilapia fillet (thawed)", "1.5 cups steamed frozen mixed veggies (broccoli, peas, carrots)", "1/3 cup cooked brown rice", "1 tsp garlic powder, paprika, lemon juice"],
            "recipe": "Season tilapia fillet with paprika and garlic powder. Pan sear in a non-stick skillet for 3 mins per side. Serve alongside steamed mixed vegetables and warm brown rice.",
            "prep_time": "12 mins"
        },
        {
            "id": "d11",
            "name": "High-Protein Mixed Lentil (Panchmel Dal) Soup with Spinach",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 380,
            "protein": 30,
            "carbs": 54,
            "fat": 5,
            "fiber": 16,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["3/4 cup mixed cooked lentils (Moong, Masoor, Toor, Chana)", "1.5 cups fresh baby spinach", "1/2 cup diced tomatoes", "1 tsp cumin & turmeric tadka", "Lemon wedge"],
            "recipe": "Simmer mixed lentils with tomatoes, turmeric, and water. Stir in fresh spinach until wilted. Top with cumin tadka and a squeeze of fresh lemon juice.",
            "prep_time": "18 mins"
        },
        {
            "id": "d12",
            "name": "Budget Skinless Chicken Thigh Skillet with Green Beans & Sweet Potato",
            "diet": ["non_veg", "any"],
            "calories": 420,
            "protein": 42,
            "carbs": 32,
            "fat": 12,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["160g skinless boneless chicken thighs (diced)", "1 cup frozen/fresh green beans", "100g baked or boiled sweet potato cubes", "Garlic, rosemary, black pepper"],
            "recipe": "Sear chicken thigh pieces in a skillet for 6 mins. Add green beans and sweet potato cubes, seasoning with garlic and rosemary. Cover and cook for 5 mins until tender.",
            "prep_time": "16 mins"
        },
        {
            "id": "d13",
            "name": "Spiced Chickpea (Chole) & Spinach Stew with Brown Rice",
            "diet": ["vegan", "vegetarian", "any", "non_veg", "pescatarian"],
            "calories": 400,
            "protein": 26,
            "carbs": 58,
            "fat": 6,
            "fiber": 16,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 cup cooked chickpeas", "1.5 cups chopped spinach", "1/2 cup tomato-onion curry sauce", "1/3 cup cooked brown rice", "Garam masala & ginger"],
            "recipe": "Simmer chickpeas in spiced curry sauce for 8 mins. Stir in chopped spinach until tender. Plate with warm steamed brown rice.",
            "prep_time": "15 mins"
        },
        {
            "id": "d14",
            "name": "Budget Canned Tuna / Salmon Patties with Steamed Broccoli",
            "diet": ["pescatarian", "non_veg", "any"],
            "calories": 390,
            "protein": 44,
            "carbs": 24,
            "fat": 11,
            "fiber": 8,
            "is_budget": True,
            "cost_level": "$",
            "ingredients": ["1 can (150g) canned salmon or light tuna", "1 whole egg + 2 tbsp oat flour (binder)", "1.5 cups steamed broccoli florets", "1 tsp Dijon mustard, herbs, lemon"],
            "recipe": "Mix drained tuna, egg, oat flour, and mustard into patties. Pan-fry in a non-stick pan for 3 mins each side until golden. Serve with lemon-dressed steamed broccoli.",
            "prep_time": "14 mins"
        }
    ]
}

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def convert_weight_to_kg(val: float, unit: str) -> float:
    """Converts lbs to kg if needed."""
    if unit.lower() in ["lbs", "lb", "pound", "pounds"]:
        return round(val * 0.45359237, 2)
    return round(float(val), 2)


def convert_kg_to_lbs(kg: float) -> float:
    """Converts kg to lbs."""
    return round(kg * 2.20462, 1)


def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
    """Calculates BMI and returns classification and health range."""
    height_m = height_cm / 100.0
    if height_m <= 0 or weight_kg <= 0:
        return {"bmi": 0, "category": "Unknown", "healthy_weight_range_kg": "N/A"}
    
    bmi = round(weight_kg / (height_m ** 2), 1)
    
    if bmi < 18.5:
        category = "Underweight"
        badge_color = "amber"
    elif 18.5 <= bmi < 25.0:
        category = "Normal (Healthy)"
        badge_color = "emerald"
    elif 25.0 <= bmi < 30.0:
        category = "Overweight"
        badge_color = "yellow"
    else:
        category = "Obese"
        badge_color = "red"
        
    min_healthy_kg = round(18.5 * (height_m ** 2), 1)
    max_healthy_kg = round(24.9 * (height_m ** 2), 1)
    
    return {
        "bmi": bmi,
        "category": category,
        "badge_color": badge_color,
        "min_healthy_kg": min_healthy_kg,
        "max_healthy_kg": max_healthy_kg,
        "healthy_weight_range": f"{min_healthy_kg} - {max_healthy_kg} kg"
    }


def calculate_bmr_tdee(
    weight_kg: float,
    height_cm: float,
    age: int = 28,
    gender: str = "male",
    workout: str = "yes",
    workout_frequency: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculates BMR using Mifflin-St Jeor formula and calculates TDEE.
    Mifflin-St Jeor Equation:
      Men: BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) + 5
      Women: BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) - 161
    """
    is_male = gender.lower() in ["male", "m", "man"]
    
    if is_male:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    bmr = round(bmr)

    # Activity multiplier based on workout status / frequency
    is_workout = workout.lower() in ["yes", "true", "1", "y"]
    
    if not is_workout:
        multiplier = 1.2  # Sedentary (little or no exercise)
        activity_label = "Sedentary (No regular workout)"
    else:
        if workout_frequency == "light":
            multiplier = 1.375  # Light exercise 1-3 days/week
            activity_label = "Light Exercise (1-3 days/week)"
        elif workout_frequency == "heavy":
            multiplier = 1.725  # Heavy exercise 6-7 days/week
            activity_label = "Heavy Exercise (6-7 days/week)"
        else:
            multiplier = 1.55   # Moderate exercise 3-5 days/week (default)
            activity_label = "Moderate Workout (3-5 days/week)"
            
    tdee = round(bmr * multiplier)
    
    # Calculate calorie target for Low Calorie diet (High protein fat loss deficit: ~20-25%)
    deficit_pct = 0.22  # 22% calorie deficit
    target_calories = round(tdee * (1 - deficit_pct))
    
    # Safety floor check
    min_floor = 1400 if is_male else 1200
    if target_calories < min_floor:
        target_calories = min_floor
        
    deficit_calories = tdee - target_calories

    return {
        "bmr": bmr,
        "tdee": tdee,
        "multiplier": multiplier,
        "activity_label": activity_label,
        "target_calories": target_calories,
        "deficit_calories": deficit_calories,
        "deficit_percentage": round(deficit_pct * 100)
    }


def calculate_macros(weight_kg: float, target_calories: int) -> Dict[str, Any]:
    """
    Calculates Low Calorie, High Protein, High Fiber macronutrient targets.
    - Protein: 1.8 - 2.2 g per kg of bodyweight (at least ~35% of daily calories)
    - Fiber: 32 - 40 g daily
    - Healthy Fats: 20 - 25% of calories (9 kcal/g)
    - Carbohydrates: Balance of calories (4 kcal/g) focusing on low GI / high fiber carbs
    """
    raw_protein_g = weight_kg * 2.0
    protein_cals = raw_protein_g * 4
    
    min_protein_cals = target_calories * 0.30
    max_protein_cals = target_calories * 0.42
    
    if protein_cals < min_protein_cals:
        protein_cals = min_protein_cals
    elif protein_cals > max_protein_cals:
        protein_cals = max_protein_cals
        
    protein_g = round(protein_cals / 4)
    
    fat_cals = target_calories * 0.22
    fat_g = round(fat_cals / 9)
    
    remaining_cals = target_calories - (protein_g * 4) - (fat_g * 9)
    carb_g = max(round(remaining_cals / 4), 60)
    
    fiber_g = max(round((target_calories / 1000) * 16), 32)
    
    total_macro_cals = (protein_g * 4) + (carb_g * 4) + (fat_g * 9)
    
    protein_pct = round((protein_g * 4 / total_macro_cals) * 100)
    carb_pct = round((carb_g * 4 / total_macro_cals) * 100)
    fat_pct = round((fat_g * 9 / total_macro_cals) * 100)

    water_liters = round((weight_kg * 0.038) + 0.5, 1)

    return {
        "calories": target_calories,
        "protein_g": protein_g,
        "protein_pct": protein_pct,
        "carbs_g": carb_g,
        "carbs_pct": carb_pct,
        "fiber_g": fiber_g,
        "fat_g": fat_g,
        "fat_pct": fat_pct,
        "water_liters": water_liters
    }


def filter_meals_by_diet(category: str, diet_pref: str = "any", budget_pref: str = "any") -> List[Dict[str, Any]]:
    """
    Filters available meals by dietary preference and budget focus.
    """
    all_meals = MEAL_DATABASE.get(category, [])
    
    # 1. Filter by diet type
    if not diet_pref or diet_pref in ["any", "all", "non_veg", "omnivore"]:
        filtered = list(all_meals)
    else:
        filtered = [m for m in all_meals if diet_pref in m.get("diet", [])]
        if not filtered:
            filtered = list(all_meals)
            
    # 2. Sort/Filter based on budget focus
    if budget_pref in ["budget_only", "pocket_friendly", "budget"]:
        budget_subset = [m for m in filtered if m.get("is_budget") is True]
        if budget_subset:
            return budget_subset
    elif budget_pref in ["balanced", "mixed"]:
        # Interleave budget meals so they appear prominently
        budget_items = [m for m in filtered if m.get("is_budget") is True]
        regular_items = [m for m in filtered if not m.get("is_budget")]
        interleaved = []
        max_len = max(len(budget_items), len(regular_items))
        for i in range(max_len):
            if i < len(budget_items):
                interleaved.append(budget_items[i])
            if i < len(regular_items):
                interleaved.append(regular_items[i])
        return interleaved
        
    return filtered


def generate_weekly_diet_plan(
    target_calories: int,
    target_protein: int,
    target_carbs: int,
    target_fiber: int,
    target_fat: int,
    diet_pref: str = "any",
    budget_pref: str = "balanced"
) -> Dict[str, Any]:
    """
    Generates a personalized 7-day meal plan with exact portion scaling,
    ensuring pocket-friendly and varied meals are distributed across all 7 days.
    """
    weekly_plan = {}
    shopping_list: Dict[str, int] = {}
    
    breakfast_options = filter_meals_by_diet("breakfast", diet_pref, budget_pref)
    lunch_options = filter_meals_by_diet("lunch", diet_pref, budget_pref)
    snack_options = filter_meals_by_diet("snack", diet_pref, budget_pref)
    dinner_options = filter_meals_by_diet("dinner", diet_pref, budget_pref)

    for i, day in enumerate(DAYS_OF_WEEK):
        # Pick varied meal rotations (with offset to avoid repetition across categories)
        b_meal = dict(breakfast_options[i % len(breakfast_options)])
        l_meal = dict(lunch_options[(i + 1) % len(lunch_options)])
        s_meal = dict(snack_options[(i + 2) % len(snack_options)])
        d_meal = dict(dinner_options[(i + 3) % len(dinner_options)])
        
        raw_cals = b_meal["calories"] + l_meal["calories"] + s_meal["calories"] + d_meal["calories"]
        scale_factor = target_calories / raw_cals if raw_cals > 0 else 1.0
        
        scaled_meals = []
        for meal_type, meal_item in [
            ("Breakfast", b_meal),
            ("Lunch", l_meal),
            ("Evening Snack", s_meal),
            ("Dinner", d_meal)
        ]:
            scaled_meal = {
                "id": meal_item["id"],
                "meal_type": meal_type,
                "name": meal_item["name"],
                "calories": round(meal_item["calories"] * scale_factor),
                "protein": round(meal_item["protein"] * scale_factor),
                "carbs": round(meal_item["carbs"] * scale_factor),
                "fat": round(meal_item["fat"] * scale_factor),
                "fiber": round(meal_item["fiber"] * scale_factor),
                "is_budget": meal_item.get("is_budget", False),
                "cost_level": meal_item.get("cost_level", "$$"),
                "ingredients": meal_item["ingredients"],
                "recipe": meal_item["recipe"],
                "prep_time": meal_item.get("prep_time", "15 mins"),
                "diet_tags": meal_item.get("diet", [])
            }
            scaled_meals.append(scaled_meal)
            
            for ing in meal_item["ingredients"]:
                shopping_list[ing] = shopping_list.get(ing, 0) + 1

        day_calories = sum(m["calories"] for m in scaled_meals)
        day_protein = sum(m["protein"] for m in scaled_meals)
        day_carbs = sum(m["carbs"] for m in scaled_meals)
        day_fat = sum(m["fat"] for m in scaled_meals)
        day_fiber = sum(m["fiber"] for m in scaled_meals)

        weekly_plan[day] = {
            "day": day,
            "meals": scaled_meals,
            "totals": {
                "calories": day_calories,
                "protein": day_protein,
                "carbs": day_carbs,
                "fat": day_fat,
                "fiber": day_fiber
            }
        }

    grocery_list = [{"item": k, "frequency": v} for k, v in sorted(shopping_list.items(), key=lambda x: x[0])]

    return {
        "weekly_plan": weekly_plan,
        "grocery_list": grocery_list,
        "all_meal_options": {
            "breakfast": filter_meals_by_diet("breakfast", diet_pref, "any"),
            "lunch": filter_meals_by_diet("lunch", diet_pref, "any"),
            "snack": filter_meals_by_diet("snack", diet_pref, "any"),
            "dinner": filter_meals_by_diet("dinner", diet_pref, "any")
        }
    }


def build_full_user_profile(
    name: str,
    height_cm: float,
    weight_val: float,
    weight_unit: str = "kg",
    workout: str = "yes",
    workout_frequency: str = "moderate",
    age: int = 28,
    gender: str = "male",
    diet_pref: str = "any",
    budget_pref: str = "balanced"
) -> Dict[str, Any]:
    """
    Processes all user inputs and creates full personalized nutrition plan & weekly schedule.
    """
    clean_name = name.strip() if name and name.strip() else "Fitness Enthusiast"
    weight_kg = convert_weight_to_kg(weight_val, weight_unit)
    weight_lbs = convert_kg_to_lbs(weight_kg)
    
    bmi_info = calculate_bmi(weight_kg, height_cm)
    energy_info = calculate_bmr_tdee(weight_kg, height_cm, age, gender, workout, workout_frequency)
    macro_info = calculate_macros(weight_kg, energy_info["target_calories"])
    
    plan_info = generate_weekly_diet_plan(
        target_calories=macro_info["calories"],
        target_protein=macro_info["protein_g"],
        target_carbs=macro_info["carbs_g"],
        target_fiber=macro_info["fiber_g"],
        target_fat=macro_info["fat_g"],
        diet_pref=diet_pref,
        budget_pref=budget_pref
    )
    
    return {
        "user": {
            "name": clean_name,
            "height_cm": height_cm,
            "height_ft": f"{int(height_cm // 30.48)}'{int((height_cm % 30.48) / 2.54)}\"",
            "weight_kg": weight_kg,
            "weight_lbs": weight_lbs,
            "weight_display": f"{weight_val} {weight_unit.upper()}",
            "age": age,
            "gender": gender.capitalize(),
            "workout": "Yes" if workout.lower() in ["yes", "true", "1", "y"] else "No",
            "workout_frequency": workout_frequency,
            "diet_pref": diet_pref.capitalize(),
            "budget_pref": budget_pref
        },
        "bmi": bmi_info,
        "energy": energy_info,
        "macros": macro_info,
        "weekly_plan": plan_info["weekly_plan"],
        "grocery_list": plan_info["grocery_list"],
        "all_meal_options": plan_info["all_meal_options"]
    }
