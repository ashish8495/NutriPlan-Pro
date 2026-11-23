/**
 * NutriPlan Pro - Interactive Client-Side Application Script
 */

let currentUnit = 'kg';
let currentPlanData = null;
let activeDay = 'Monday';
let macroChartInstance = null;
let energyChartInstance = null;

// Modal tracking state for swapping
let currentSwapContext = null;

const DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

document.addEventListener('DOMContentLoaded', () => {
    updateHeightFtPreview();
    toggleWorkoutFrequency();
});

/**
 * Height preview helper in feet & inches
 */
function updateHeightFtPreview() {
    const heightCm = parseFloat(document.getElementById('height_cm').value);
    const label = document.getElementById('height-ft-label');
    if (!heightCm || isNaN(heightCm)) {
        label.innerText = "~ 5'9\"";
        return;
    }
    const totalInches = heightCm / 2.54;
    const feet = Math.floor(totalInches / 12);
    const inches = Math.round(totalInches % 12);
    label.innerText = `~ ${feet}'${inches}"`;
}

/**
 * Toggle between KG and LBS unit
 */
function setWeightUnit(unit) {
    if (unit === currentUnit) return;
    
    const weightInput = document.getElementById('weight_val');
    const badge = document.getElementById('weight-unit-badge');
    const btnKg = document.getElementById('unit-kg');
    const btnLbs = document.getElementById('unit-lbs');
    
    let currentVal = parseFloat(weightInput.value);

    if (unit === 'lbs') {
        currentUnit = 'lbs';
        btnLbs.className = 'px-2 py-0.5 text-xs font-bold rounded bg-white text-emerald-700 shadow-sm transition';
        btnKg.className = 'px-2 py-0.5 text-xs font-bold rounded text-slate-600 transition';
        badge.innerText = 'LBS';
        if (currentVal && !isNaN(currentVal)) {
            weightInput.value = (currentVal * 2.20462).toFixed(1);
        }
    } else {
        currentUnit = 'kg';
        btnKg.className = 'px-2 py-0.5 text-xs font-bold rounded bg-white text-emerald-700 shadow-sm transition';
        btnLbs.className = 'px-2 py-0.5 text-xs font-bold rounded text-slate-600 transition';
        badge.innerText = 'KG';
        if (currentVal && !isNaN(currentVal)) {
            weightInput.value = (currentVal * 0.453592).toFixed(1);
        }
    }
}

/**
 * Toggle workout frequency container visibility based on workout status
 */
function toggleWorkoutFrequency() {
    const workoutVal = document.getElementById('workout').value;
    const container = document.getElementById('workout-freq-container');
    if (workoutVal === 'no') {
        container.classList.add('opacity-40', 'pointer-events-none');
    } else {
        container.classList.remove('opacity-40', 'pointer-events-none');
    }
}

/**
 * Load sample data for instant demonstration
 */
function loadSampleData() {
    document.getElementById('name').value = 'John Miller';
    document.getElementById('height_cm').value = '178';
    setWeightUnit('kg');
    document.getElementById('weight_val').value = '82';
    document.getElementById('workout').value = 'yes';
    document.getElementById('workout_frequency').value = 'moderate';
    document.getElementById('age').value = '29';
    document.getElementById('gender').value = 'male';
    document.getElementById('diet_pref').value = 'any';
    document.getElementById('budget_pref').value = 'balanced';
    updateHeightFtPreview();
    toggleWorkoutFrequency();

    // Trigger calculation automatically
    document.getElementById('diet-form').dispatchEvent(new Event('submit'));
}

/**
 * Scroll smoothly to input form
 */
function scrollToForm() {
    document.getElementById('input-section').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Handle form submission and API call
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    const name = document.getElementById('name').value.trim() || 'Health Champion';
    const height_cm = parseFloat(document.getElementById('height_cm').value);
    const weight_val = parseFloat(document.getElementById('weight_val').value);
    const workout = document.getElementById('workout').value;
    const workout_frequency = document.getElementById('workout_frequency').value;
    const age = parseInt(document.getElementById('age').value, 10);
    const gender = document.getElementById('gender').value;
    const diet_pref = document.getElementById('diet_pref').value;
    const budget_pref = document.getElementById('budget_pref').value;

    const payload = {
        name,
        height_cm,
        weight_val,
        weight_unit: currentUnit,
        workout,
        workout_frequency,
        age,
        gender,
        diet_pref,
        budget_pref
    };

    // UI Loading state
    document.getElementById('loading-spinner').classList.remove('hidden');
    document.getElementById('results-container').classList.add('hidden');
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Calculating Targets & Meals...';

    try {
        const response = await fetch('/api/generate-plan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            alert('Error generating plan: ' + (result.error || 'Please verify your inputs.'));
            return;
        }

        currentPlanData = result.data;
        renderResults(currentPlanData);

        // Smooth scroll to results
        setTimeout(() => {
            document.getElementById('results-container').scrollIntoView({ behavior: 'smooth' });
        }, 100);

    } catch (err) {
        console.error('Fetch error:', err);
        alert('Network or server error while generating the diet plan. Please check server logs.');
    } finally {
        document.getElementById('loading-spinner').classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fa-solid fa-bolt"></i> Generate Weekly Diet Plan';
    }
}

/**
 * Render all results and dashboard metrics
 */
function renderResults(data) {
    const user = data.user;
    const bmi = data.bmi;
    const energy = data.energy;
    const macros = data.macros;

    const budgetLabel = user.budget_pref === 'budget_only' 
        ? 'Pocket-Friendly Focus ($)' 
        : (user.budget_pref === 'balanced' ? 'Balanced (Pocket-Friendly + Standard)' : 'All Options');

    // Header info
    document.getElementById('res-greeting').innerText = `Personalized Diet Plan for ${user.name}`;
    document.getElementById('res-subtitle').innerText = 
        `Height: ${user.height_cm} cm (${user.height_ft}) | Weight: ${user.weight_display} (${user.weight_kg} kg) | Workout: ${user.workout} (${energy.activity_label}) | Diet: ${user.diet_pref} | Budget: ${budgetLabel}`;

    // Metric Cards
    document.getElementById('res-target-cals').innerText = `${energy.target_calories} kcal`;
    document.getElementById('res-deficit-badge').innerText = `${energy.deficit_percentage}% deficit (-${energy.deficit_calories} kcal)`;
    
    document.getElementById('res-protein-g').innerText = `${macros.protein_g} g`;
    document.getElementById('res-protein-pct').innerText = `${macros.protein_pct}% of total daily calories`;

    document.getElementById('res-carbs-g').innerText = `${macros.carbs_g} g`;
    document.getElementById('res-carbs-pct').innerText = `${macros.carbs_pct}% complex low-GI carbs`;

    document.getElementById('res-fiber-g').innerText = `${macros.fiber_g} g`;
    document.getElementById('res-fat-g').innerText = `${macros.fat_g} g`;
    document.getElementById('res-fat-pct').innerText = `${macros.fat_pct}% healthy fats`;

    document.getElementById('res-water-liters').innerText = `${macros.water_liters} L`;
    document.getElementById('res-bmi-badge').innerText = `BMI: ${bmi.bmi} (${bmi.category})`;

    // Energy stats
    document.getElementById('res-bmr-val').innerText = `${energy.bmr} kcal`;
    document.getElementById('res-tdee-val').innerText = `${energy.tdee} kcal`;
    document.getElementById('res-target-val').innerText = `${energy.target_calories} kcal`;

    // Notes
    document.getElementById('res-bmi-status').innerText = bmi.category;
    document.getElementById('res-ideal-weight').innerText = `Healthy Range: ${bmi.healthy_weight_range}`;

    // Render Charts
    renderMacroChart(macros);
    renderEnergyChart(energy);

    // Render Day Tabs
    renderDayTabs();

    // Render Active Day Meals
    renderActiveDayMeals();

    // Show container
    document.getElementById('results-container').classList.remove('hidden');
}

/**
 * Render Chart.js Macro Doughnut Chart
 */
function renderMacroChart(macros) {
    const ctx = document.getElementById('macroChart').getContext('2d');
    
    document.getElementById('legend-protein').innerText = `${macros.protein_pct}%`;
    document.getElementById('legend-carbs').innerText = `${macros.carbs_pct}%`;
    document.getElementById('legend-fats').innerText = `${macros.fat_pct}%`;

    if (macroChartInstance) {
        macroChartInstance.destroy();
    }

    macroChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Protein', 'Carbohydrates', 'Fats'],
            datasets: [{
                data: [macros.protein_g * 4, macros.carbs_g * 4, macros.fat_g * 9],
                backgroundColor: ['#4f46e5', '#f59e0b', '#f43f5e'],
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const val = context.raw;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = Math.round((val / total) * 100);
                            return ` ${context.label}: ${val} kcal (${pct}%)`;
                        }
                    }
                }
            },
            cutout: '70%'
        }
    });
}

/**
 * Render Chart.js Energy Balance Bar Chart
 */
function renderEnergyChart(energy) {
    const ctx = document.getElementById('energyChart').getContext('2d');

    if (energyChartInstance) {
        energyChartInstance.destroy();
    }

    energyChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['BMR (Basal)', 'TDEE (Burned)', 'Calorie Target'],
            datasets: [{
                label: 'Calories (kcal)',
                data: [energy.bmr, energy.tdee, energy.target_calories],
                backgroundColor: ['#94a3b8', '#0ea5e9', '#10b981'],
                borderRadius: 8,
                barThickness: 32
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => ` ${ctx.raw} kcal/day`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: '#f1f5f9' },
                    ticks: { color: '#64748b', font: { size: 10 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#475569', font: { size: 11, weight: '600' } }
                }
            }
        }
    });
}

/**
 * Render Day Tabs Navigation
 */
function renderDayTabs() {
    const container = document.getElementById('day-tabs-container');
    container.innerHTML = '';

    DAYS.forEach(day => {
        const isActive = day === activeDay;
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = isActive
            ? 'px-4 py-2 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-md shadow-emerald-600/20 transition whitespace-nowrap'
            : 'px-4 py-2 rounded-xl text-xs font-semibold bg-white text-slate-600 border border-slate-200 hover:bg-slate-100 transition whitespace-nowrap';
        btn.innerText = day;
        btn.onclick = () => {
            activeDay = day;
            renderDayTabs();
            renderActiveDayMeals();
        };
        container.appendChild(btn);
    });
}

/**
 * Render Meals for the Currently Selected Day
 */
function renderActiveDayMeals() {
    if (!currentPlanData || !currentPlanData.weekly_plan) return;

    const dayData = currentPlanData.weekly_plan[activeDay];
    if (!dayData) return;

    // Update Daily Totals Summary Bar
    document.getElementById('active-day-title').innerText = activeDay;
    document.getElementById('day-tot-cals').innerText = dayData.totals.calories;
    document.getElementById('day-tot-protein').innerText = `${dayData.totals.protein}g`;
    document.getElementById('day-tot-carbs').innerText = `${dayData.totals.carbs}g`;
    document.getElementById('day-tot-fiber').innerText = `${dayData.totals.fiber}g`;
    document.getElementById('day-tot-fat').innerText = `${dayData.totals.fat}g`;

    const grid = document.getElementById('meals-grid');
    grid.innerHTML = '';

    const mealIcons = {
        'Breakfast': { icon: 'fa-sun', color: 'text-amber-500', bg: 'bg-amber-50', border: 'border-amber-200' },
        'Lunch': { icon: 'fa-utensils', color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200' },
        'Evening Snack': { icon: 'fa-apple-whole', color: 'text-purple-600', bg: 'bg-purple-50', border: 'border-purple-200' },
        'Dinner': { icon: 'fa-moon', color: 'text-indigo-600', bg: 'bg-indigo-50', border: 'border-indigo-200' }
    };

    dayData.meals.forEach((meal, idx) => {
        const theme = mealIcons[meal.meal_type] || { icon: 'fa-bowl-food', color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-200' };

        const card = document.createElement('div');
        card.className = 'bg-white rounded-2xl border border-slate-200/90 shadow-sm p-5 flex flex-col justify-between space-y-4 hover:shadow-md transition duration-200';

        const budgetBadgeHtml = meal.is_budget 
            ? `<span class="inline-flex items-center gap-1 text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 shadow-xs"><i class="fa-solid fa-piggy-bank text-emerald-600"></i> Pocket Friendly ($)</span>`
            : `<span class="inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200">${meal.cost_level || '$$'}</span>`;

        card.innerHTML = `
            <div class="space-y-3">
                <!-- Meal Header -->
                <div class="flex items-start justify-between gap-3">
                    <div class="flex items-center gap-2.5">
                        <div class="w-9 h-9 rounded-xl ${theme.bg} ${theme.color} flex items-center justify-center text-sm font-bold">
                            <i class="fa-solid ${theme.icon}"></i>
                        </div>
                        <div>
                            <div class="flex items-center gap-1.5 flex-wrap">
                                <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400">${meal.meal_type}</span>
                                ${budgetBadgeHtml}
                            </div>
                            <h4 class="text-sm font-bold text-slate-900 leading-snug">${meal.name}</h4>
                        </div>
                    </div>
                    <span class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 font-extrabold text-xs whitespace-nowrap">
                        ${meal.calories} kcal
                    </span>
                </div>

                <!-- Macro Badges -->
                <div class="grid grid-cols-4 gap-2 text-center text-xs">
                    <div class="p-1.5 rounded-lg bg-indigo-50/80 border border-indigo-100">
                        <p class="font-bold text-indigo-700 text-xs">${meal.protein}g</p>
                        <p class="text-[10px] text-slate-400 font-medium">Protein</p>
                    </div>
                    <div class="p-1.5 rounded-lg bg-amber-50/80 border border-amber-100">
                        <p class="font-bold text-amber-700 text-xs">${meal.carbs}g</p>
                        <p class="text-[10px] text-slate-400 font-medium">Carbs</p>
                    </div>
                    <div class="p-1.5 rounded-lg bg-emerald-50/80 border border-emerald-100">
                        <p class="font-bold text-emerald-700 text-xs">${meal.fiber}g</p>
                        <p class="text-[10px] text-slate-400 font-medium">Fiber</p>
                    </div>
                    <div class="p-1.5 rounded-lg bg-rose-50/80 border border-rose-100">
                        <p class="font-bold text-rose-700 text-xs">${meal.fat}g</p>
                        <p class="text-[10px] text-slate-400 font-medium">Fat</p>
                    </div>
                </div>

                <!-- Ingredients -->
                <div class="space-y-1.5 pt-1">
                    <p class="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                        <i class="fa-solid fa-list-check text-emerald-600"></i> Ingredients & Portions:
                    </p>
                    <ul class="text-xs text-slate-600 space-y-1 pl-4 list-disc">
                        ${meal.ingredients.map(ing => `<li>${ing}</li>`).join('')}
                    </ul>
                </div>

                <!-- Prep / Recipe -->
                <div class="p-3 bg-slate-50 rounded-xl text-xs text-slate-600 space-y-1 border border-slate-100">
                    <div class="flex items-center justify-between text-[11px] font-bold text-slate-500">
                        <span><i class="fa-solid fa-kitchen-set text-slate-400"></i> Quick Recipe</span>
                        <span class="text-emerald-700 font-medium"><i class="fa-regular fa-clock"></i> ${meal.prep_time}</span>
                    </div>
                    <p class="leading-relaxed">${meal.recipe}</p>
                </div>
            </div>

            <!-- Footer Action: Swap Meal Modal Trigger & Quick Rotate -->
            <div class="pt-2 border-t border-slate-100 flex items-center justify-between print:hidden">
                <span class="text-[11px] text-slate-400">${meal.is_budget ? 'Budget choice ($)' : 'Standard choice'}</span>
                <div class="flex gap-2">
                    <button type="button" onclick="openSwapModal('${activeDay}', ${idx}, '${meal.meal_type}', '${meal.id}', ${meal.calories})"
                        class="px-3 py-1.5 text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100/90 rounded-lg transition flex items-center gap-1.5 border border-emerald-200">
                        <i class="fa-solid fa-list text-[11px]"></i> Choose / Swap
                    </button>
                    <button type="button" onclick="quickSwapNext('${activeDay}', ${idx}, '${meal.meal_type}', '${meal.id}', ${meal.calories})"
                        title="Quick cycle to next meal"
                        class="px-2.5 py-1.5 text-xs font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
                        <i class="fa-solid fa-arrows-rotate text-[11px]"></i>
                    </button>
                </div>
            </div>
        `;

        grid.appendChild(card);
    });
}

/**
 * Open Swap Modal to show ALL available meals for that category
 */
async function openSwapModal(day, mealIndex, mealType, currentMealId, targetCalories) {
    currentSwapContext = { day, mealIndex, mealType, currentMealId, targetCalories };
    
    document.getElementById('swap-modal-title').innerText = `Select ${mealType} for ${day}`;
    const listContainer = document.getElementById('swap-meal-list');
    listContainer.innerHTML = '<div class="py-8 text-center text-slate-500 text-xs"><i class="fa-solid fa-spinner fa-spin"></i> Loading options...</div>';
    
    document.getElementById('swap-modal').classList.remove('hidden');

    try {
        const diet_pref = (currentPlanData && currentPlanData.user.diet_pref) ? currentPlanData.user.diet_pref.toLowerCase() : 'any';
        const response = await fetch(`/api/category-meals?category=${encodeURIComponent(mealType)}&diet_pref=${encodeURIComponent(diet_pref)}`);
        const result = await response.json();

        if (!result.success || !result.meals || result.meals.length === 0) {
            listContainer.innerHTML = '<p class="text-xs text-slate-500">No alternatives found.</p>';
            return;
        }

        const meals = result.meals;
        document.getElementById('swap-candidate-count').innerText = `${meals.length} meals in catalog (${meals.filter(m => m.is_budget).length} pocket-friendly)`;
        listContainer.innerHTML = '';

        meals.forEach(m => {
            const isCurrent = m.id === currentMealId;
            const itemDiv = document.createElement('div');
            itemDiv.className = `p-3.5 rounded-xl border ${isCurrent ? 'border-emerald-500 bg-emerald-50/50' : 'border-slate-200 hover:border-emerald-300 hover:bg-slate-50'} transition flex flex-col sm:flex-row sm:items-center justify-between gap-3`;

            const budgetPill = m.is_budget 
                ? `<span class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300"><i class="fa-solid fa-piggy-bank"></i> Pocket Friendly ($)</span>`
                : `<span class="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-100 text-slate-600">${m.cost_level || '$$'}</span>`;

            itemDiv.innerHTML = `
                <div class="space-y-1 flex-1">
                    <div class="flex items-center gap-2 flex-wrap">
                        <span class="font-bold text-xs text-slate-900">${m.name}</span>
                        ${budgetPill}
                        ${isCurrent ? '<span class="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-1.5 py-0.5 rounded">Active</span>' : ''}
                    </div>
                    <p class="text-[11px] text-slate-500"><b>Macros:</b> ~${m.calories} kcal | <b>${m.protein}g</b> Protein | <b>${m.fiber}g</b> Fiber | <b>${m.carbs}g</b> Carbs</p>
                    <p class="text-[11px] text-slate-600 italic">Ingredients: ${m.ingredients.slice(0, 3).join(', ')}...</p>
                </div>
                <div>
                    <button type="button" onclick="selectChosenMeal('${m.id}')"
                        class="w-full sm:w-auto px-3.5 py-1.5 text-xs font-bold rounded-lg ${isCurrent ? 'bg-slate-200 text-slate-600 cursor-default' : 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm'} transition">
                        ${isCurrent ? 'Current' : 'Select Meal'}
                    </button>
                </div>
            `;
            listContainer.appendChild(itemDiv);
        });

    } catch (err) {
        console.error(err);
        listContainer.innerHTML = '<p class="text-xs text-rose-500">Error loading meal catalog.</p>';
    }
}

/**
 * Close Swap Modal
 */
function closeSwapModal() {
    document.getElementById('swap-modal').classList.add('hidden');
    currentSwapContext = null;
}

/**
 * Apply the chosen meal from the swap modal
 */
async function selectChosenMeal(chosenMealId) {
    if (!currentSwapContext) return;
    const { day, mealIndex, mealType, currentMealId, targetCalories } = currentSwapContext;

    try {
        const diet_pref = currentPlanData.user.diet_pref.toLowerCase();
        const response = await fetch('/api/swap-meal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                category: mealType.toLowerCase(),
                diet_pref: diet_pref,
                current_meal_id: currentMealId,
                chosen_meal_id: chosenMealId,
                target_calories: targetCalories
            })
        });

        const res = await response.json();
        if (res.success && res.meal) {
            currentPlanData.weekly_plan[day].meals[mealIndex] = res.meal;
            
            const dayMeals = currentPlanData.weekly_plan[day].meals;
            currentPlanData.weekly_plan[day].totals = {
                calories: dayMeals.reduce((acc, m) => acc + m.calories, 0),
                protein: dayMeals.reduce((acc, m) => acc + m.protein, 0),
                carbs: dayMeals.reduce((acc, m) => acc + m.carbs, 0),
                fat: dayMeals.reduce((acc, m) => acc + m.fat, 0),
                fiber: dayMeals.reduce((acc, m) => acc + m.fiber, 0)
            };

            closeSwapModal();
            renderActiveDayMeals();
        }
    } catch (e) {
        console.error('Error applying swap:', e);
    }
}

/**
 * Quick cycle to next meal in candidate list
 */
async function quickSwapNext(day, mealIndex, mealType, currentMealId, targetCalories) {
    try {
        const diet_pref = currentPlanData.user.diet_pref.toLowerCase();
        const response = await fetch('/api/swap-meal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                category: mealType.toLowerCase(),
                diet_pref: diet_pref,
                current_meal_id: currentMealId,
                target_calories: targetCalories
            })
        });

        const res = await response.json();
        if (res.success && res.meal) {
            currentPlanData.weekly_plan[day].meals[mealIndex] = res.meal;
            
            const dayMeals = currentPlanData.weekly_plan[day].meals;
            currentPlanData.weekly_plan[day].totals = {
                calories: dayMeals.reduce((acc, m) => acc + m.calories, 0),
                protein: dayMeals.reduce((acc, m) => acc + m.protein, 0),
                carbs: dayMeals.reduce((acc, m) => acc + m.carbs, 0),
                fat: dayMeals.reduce((acc, m) => acc + m.fat, 0),
                fiber: dayMeals.reduce((acc, m) => acc + m.fiber, 0)
            };

            renderActiveDayMeals();
        }
    } catch (e) {
        console.error('Error quick swapping:', e);
    }
}

/**
 * Open Grocery Shopping List Modal
 */
function openGroceryModal() {
    if (!currentPlanData || !currentPlanData.grocery_list) return;

    const list = currentPlanData.grocery_list;
    const container = document.getElementById('grocery-list-container');
    container.innerHTML = '';

    list.forEach((item, i) => {
        const label = document.createElement('label');
        label.className = 'flex items-center gap-3 p-2.5 rounded-xl hover:bg-slate-50 transition border border-transparent hover:border-slate-200 cursor-pointer';
        label.innerHTML = `
            <input type="checkbox" class="w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500">
            <span class="text-xs text-slate-700 flex-1">${item.item}</span>
            <span class="text-[11px] font-semibold text-slate-400 bg-slate-100 px-2 py-0.5 rounded-md">Used in ~${item.frequency} meals</span>
        `;
        container.appendChild(label);
    });

    document.getElementById('grocery-count').innerText = `${list.length} ingredients total`;
    document.getElementById('grocery-modal').classList.remove('hidden');
}

/**
 * Close Grocery Modal
 */
function closeGroceryModal() {
    document.getElementById('grocery-modal').classList.add('hidden');
}

/**
 * Download Plan as CSV Spreadsheet
 */
async function downloadCSV() {
    if (!currentPlanData) return;

    try {
        const response = await fetch('/api/export/csv', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                weekly_plan: currentPlanData.weekly_plan,
                user_name: currentPlanData.user.name
            })
        });

        if (!response.ok) throw new Error('CSV generation failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${currentPlanData.user.name.replace(/\s+/g, '_')}_Weekly_Diet_Plan.csv`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (e) {
        console.error('Error exporting CSV:', e);
        alert('Failed to export CSV. Please try again.');
    }
}
