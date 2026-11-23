"""
Generates a professional Word document containing the scientific sources,
clinical formulas, and nutritional methodology of NutriPlan Pro.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def create_scientific_sources_document(filename: str = "NutriPlan_Pro_Scientific_Sources_and_Methodology.docx"):
    doc = docx.Document()

    # 1-inch standard margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Color Palette
    COLOR_PRIMARY = RGBColor(5, 150, 105)     # Emerald Green
    COLOR_DARK = RGBColor(15, 23, 42)          # Slate Dark 900
    COLOR_MUTED = RGBColor(100, 116, 139)      # Slate Muted 500
    COLOR_ACCENT = RGBColor(13, 148, 136)      # Teal Accent

    # Formatting helpers
    def add_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(18)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_MUTED
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLOR_DARK
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        return p

    def add_body(text, bold_prefix=None, bullet=False):
        p = doc.add_paragraph(style='List Bullet' if bullet else 'Normal')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.name = 'Calibri'
            r_bold.font.size = Pt(10.5)
            r_bold.font.bold = True
            r_bold.font.color.rgb = COLOR_DARK
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = COLOR_DARK
        return p

    # Header / Title
    add_title('NutriPlan Pro')
    add_subtitle('Scientific Foundations, Evidence-Based Nutrition Sources & Metabolic Methodology')

    # 1. Executive Summary
    add_h1('1. Executive Overview')
    add_body('NutriPlan Pro is an automated nutrition and dietary formulation system engineered to deliver personalized, low-calorie, high-protein weekly diet plans. Every calculation, macro split, calorie deficit ceiling, and food composition metric within the application is strictly grounded in peer-reviewed clinical nutrition literature, sports medicine consensus, and standardized government nutrient databases.')

    # 2. Metabolic Engine
    add_h1('2. Metabolic Rate & Energy Expenditure Equations')
    add_h2('2.1 Basal Metabolic Rate (BMR): The Mifflin-St Jeor Equation')
    add_body('The application calculates basal energy requirements using the Mifflin-St Jeor Equation (1990), which accounts for body mass, stature, age, and biological sex:')
    add_body('Males: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5', bold_prefix='• ', bullet=False)
    add_body('Females: BMR = (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161', bold_prefix='• ', bullet=False)
    add_body('According to a systematic review published by the Academy of Nutrition and Dietetics (Frankenfield et al., 2005), the Mifflin-St Jeor equation is the most reliable predictive formula for estimating resting metabolic rate in both non-obese and obese individuals within ±10% accuracy.')

    add_h2('2.2 Total Daily Energy Expenditure (TDEE) & Physical Activity Levels')
    add_body('To determine total energy burn, the BMR is scaled by Physical Activity Level (PAL) multipliers established by the World Health Organization (WHO) and the Food and Agriculture Organization (FAO) (WHO Technical Report Series 935):')
    add_body('Sedentary (No regular workout): 1.20 × BMR', bullet=True)
    add_body('Light Activity (1–2 days/week): 1.375 × BMR', bullet=True)
    add_body('Moderate Activity (3–5 days/week): 1.55 × BMR', bullet=True)
    add_body('Heavy / Intense Training (6–7 days/week): 1.725 × BMR', bullet=True)

    # 3. Caloric Deficit
    add_h1('3. Caloric Deficit & Safe Fat-Loss Parameters')
    add_body('The application applies a 20% to 22% caloric deficit from the calculated TDEE. This percentage adheres to guidelines from the American College of Sports Medicine (ACSM) and the National Institutes of Health (NIH):')
    add_body('Deficit Range: A 20–22% deficit promotes a steady rate of fat oxidation (~0.5 to 1.0 kg/week) while preventing excessive metabolic slowing (adaptive thermogenesis).', bullet=True)
    add_body('Safety Floor: To ensure hormonal, thyroid, and micronutrient adequacy, daily calorie targets are bounded by safety minimums (1,200 kcal for females and 1,400–1,500 kcal for males).', bullet=True)

    # 4. Macronutrient Targets
    add_h1('4. Macronutrient Target Formulation')
    add_h2('4.1 High-Protein Strategy (1.8 – 2.2 g per kg Body Mass / ~35% of Total Calories)')
    add_body('Protein intake is elevated based on consensus guidelines from the International Society of Sports Nutrition (ISSN) (Jäger et al., 2017) and Morton et al. (British Journal of Sports Medicine, 2018):')
    add_body('Muscle Protein Synthesis (MPS): Higher protein during an energy deficit preserves lean muscle mass and maintains positive nitrogen balance.', bullet=True)
    add_body('Thermic Effect of Food (TEF): Protein has a TEF of 20–30%, meaning 20–30% of its caloric value is consumed during digestion and processing, boosting daily energy expenditure.', bullet=True)
    add_body('Satiety Signalling: Elevated protein triggers the release of satiety hormones (cholecystokinin, GLP-1, and PYY) while suppressing ghrelin.', bullet=True)

    add_h2('4.2 High Dietary Fiber Target (30 – 38 g/day)')
    add_body('Fiber recommendations follow the USDA Dietary Guidelines for Americans and Institute of Medicine (IOM) Dietary Reference Intakes (DRIs). High fiber slows gastric emptying, flattens post-meal glucose spikes, supports beneficial short-chain fatty acid (SCFA) production in the gut microbiome, and maximizes meal volume per calorie.')

    add_h2('4.3 Complex Carbohydrates & Healthy Essential Fats')
    add_body('Carbohydrates and fats are distributed within the IOM Acceptable Macronutrient Distribution Ranges (AMDR):')
    add_body('Healthy Fats (~20–25% of calories): Focuses on monounsaturated and polyunsaturated fats (olive oil, avocados, nuts, seeds, and wild salmon) for lipid balance and fat-soluble vitamin absorption.', bullet=True)
    add_body('Complex Carbohydrates (~30–35% of calories): Emphasizes complex, low-glycemic sources (oats, quinoa, sweet potatoes, legumes, and cruciferous vegetables) for glycogen replenishment and sustained energy.', bullet=True)

    # 5. Food Database
    add_h1('5. Nutrient Composition & Food Reference Database')
    add_body('All food items, macro breakdowns, and recipe ingredients in NutriPlan Pro are sourced and cross-referenced with the USDA FoodData Central (FDC) Database (U.S. Department of Agriculture, Agricultural Research Service). The catalog incorporates accessible, budget-friendly high-protein staples including whole eggs, yellow and red lentils (dal), chickpeas, black beans, canned tuna, soya chunks (TVP), plain curd, oats, and frozen vegetables to maintain nutritional efficacy without high grocery expenses.')

    # Summary Table
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Nutrient / Calculation'
    hdr_cells[1].text = 'Engine Specification'
    hdr_cells[2].text = 'Primary Authoritative Source'

    for cell in hdr_cells:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="059669"/>')
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.size = Pt(10)

    data_rows = [
        ('Basal Metabolic Rate (BMR)', 'Mifflin-St Jeor Equation', 'American Journal of Clinical Nutrition (1990)'),
        ('Activity Multiplier (TDEE)', '1.20 - 1.725 PAL Multipliers', 'WHO / FAO Technical Report Series 935'),
        ('Caloric Deficit', '20% - 22% deficit with safety floor', 'American College of Sports Medicine (ACSM) / NIH'),
        ('Protein Target', '1.8 - 2.2 g/kg (~35% of calories)', 'International Society of Sports Nutrition (ISSN)'),
        ('Fiber Target', '30 - 38 g daily minimum', 'USDA Dietary Guidelines / Institute of Medicine (IOM)'),
        ('Healthy Fats Target', '20% - 25% of daily calories', 'IOM Acceptable Macronutrient Distribution Ranges'),
        ('Food Profiles & Portions', 'USDA Reference Raw & Cooked Profiles', 'USDA FoodData Central (FDC) Standard Release'),
        ('Hydration Baseline', '35-40 ml/kg body weight + workout offset', 'European Hydration Institute / ACSM Fluid Position')
    ]

    for row_data in data_rows:
        row_cells = table.add_row().cells
        for i, text in enumerate(row_data):
            row_cells[i].text = text
            for p in row_cells[i].paragraphs:
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                for r in p.runs:
                    r.font.size = Pt(9.5)

    # 6. Hydration Guidelines
    add_h1('6. Hydration Guidelines & Fluid Dynamics')
    add_body('The daily water intake calculation is derived from the ACSM Exercise & Fluid Replacement Guidelines and the European Hydration Institute:')
    add_body('Baseline Equation: Daily Water (Liters) = (Weight in kg × 0.038) + 0.50 L workout compensation.', bullet=True)
    add_body('Adequate fluid volume supports cellular osmotic pressure, enhances metabolic toxin clearance during elevated protein intake, and optimizes athletic recovery.', bullet=True)

    # 7. Academic Citations
    add_h1('7. References & Peer-Reviewed Academic Citations')
    citations = [
        'Mifflin, M. D., St Jeor, S. T., Hill, L. A., Scott, B. J., Daugherty, S. A., & Koh, Y. O. (1990). A new predictive equation for resting energy expenditure in healthy individuals. The American Journal of Clinical Nutrition, 51(2), 241-247.',
        'Frankenfield, D., Roth-Yousey, L., & Compher, C. (2005). Comparison of predictive equations for resting metabolic rate in healthy nonobese and obese adults: a systematic review. Journal of the American Dietetic Association, 105(5), 775-789.',
        'Jäger, R., Kerksick, C. M., Campbell, B. I., Cribb, P. J., Wells, S. D., Skwiat, T. M., ... & Antonio, J. (2017). International Society of Sports Nutrition Position Stand: protein and exercise. Journal of the International Society of Sports Nutrition, 14(1), 20.',
        'Morton, R. W., Murphy, K. T., McKellar, S. R., Schoenfeld, B. J., Henselmans, M., Helms, E., ... & Phillips, S. M. (2018). A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training-induced gains in muscle mass and strength in healthy adults. British Journal of Sports Medicine, 52(6), 376-384.',
        'World Health Organization & Food and Agriculture Organization of the United Nations. (2004). Human energy requirements: Report of a Joint FAO/WHO/UNU Expert Consultation (WHO Technical Report Series 935). Rome: FAO.',
        'U.S. Department of Agriculture and U.S. Department of Health and Human Services. (2020). Dietary Guidelines for Americans, 2020-2025 (9th Edition). Washington, D.C.: USDA.',
        'U.S. Department of Agriculture, Agricultural Research Service. (2024). FoodData Central. fdc.nal.usda.gov',
        'Sawka, M. N., Burke, L. M., Eichner, E. R., Maughan, R. J., Montain, S. J., & Stachenfeld, N. S. (2007). American College of Sports Medicine position stand: Exercise and fluid replacement. Medicine & Science in Sports & Exercise, 39(2), 377-390.'
    ]

    for c in citations:
        add_body(c, bullet=True)

    doc.save(filename)
    print(f"Document successfully created: {filename}")


if __name__ == "__main__":
    create_scientific_sources_document()
