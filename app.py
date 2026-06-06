import streamlit as st
import uuid
import importlib
import languages
importlib.reload(languages)
from languages import LANGUAGES
from predictor import UnifiedDiseasePredictor

# Set page config
st.set_page_config(
    page_title="Global Multi-Disease Diagnostic System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Clinical Aesthetics (Dark Slate / Teal Theme, No Emojis)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container background */
    .stApp {
        background-color: #0e1117;
        color: #e2e8f0;
    }
    
    /* Custom Card Design */
    .medical-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .card-header {
        font-size: 20px;
        font-weight: 600;
        color: #38bdf8;
        border-bottom: 2px solid rgba(56, 189, 248, 0.2);
        padding-bottom: 8px;
        margin-bottom: 15px;
    }
    
    /* Results Styling */
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
    }
    
    .status-healthy {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid #10b981;
    }
    
    .status-mild {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid #f59e0b;
    }
    
    .status-high {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    
    .status-critical {
        background-color: rgba(220, 38, 38, 0.25);
        color: #f87171;
        border: 2px solid #ef4444;
        font-size: 16px;
    }
    
    /* Hero Banner for Home Page */
    .hero-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid rgba(56, 189, 248, 0.1);
        border-radius: 16px;
        padding: 45px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .hero-title {
        font-size: 40px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 15px;
    }
    
    .hero-subtitle {
        font-size: 18px;
        color: #94a3b8;
        margin-bottom: 30px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# Output translations for disease stages across languages
obesity_stages_map = {
    "English": {
        "Insufficient Weight": "Insufficient Weight",
        "Normal Weight": "Normal Weight",
        "Overweight Level I": "Overweight Level I",
        "Overweight Level II": "Overweight Level II",
        "Obesity Type I": "Obesity Type I",
        "Obesity Type II": "Obesity Type II",
        "Obesity Type III": "Obesity Type III"
    },
    "Español": {
        "Insufficient Weight": "Peso Insuficiente",
        "Normal Weight": "Peso Normal",
        "Overweight Level I": "Sobrepeso Nivel I",
        "Overweight Level II": "Sobrepeso Nivel II",
        "Obesity Type I": "Obesidad Tipo I",
        "Obesity Type II": "Obesidad Tipo II",
        "Obesity Type III": "Obesidad Tipo III"
    },
    "Français": {
        "Insufficient Weight": "Poids Insuffisant",
        "Normal Weight": "Poids Normal",
        "Overweight Level I": "Surpoids Niveau I",
        "Overweight Level II": "Surpoids Niveau II",
        "Obesity Type I": "Obesite de Type I",
        "Obesity Type II": "Obesite de Type II",
        "Obesity Type III": "Obesite de Type III"
    },
    "Chinese": {
        "Insufficient Weight": "体重过轻",
        "Normal Weight": "正常体重",
        "Overweight Level I": "超重一级",
        "Overweight Level II": "超重二级",
        "Obesity Type I": "肥胖一级",
        "Obesity Type II": "肥胖二级",
        "Obesity Type III": "肥胖三级"
    },
    "Arabic": {
        "Insufficient Weight": "وزن غير كافٍ",
        "Normal Weight": "وزن طبيعي",
        "Overweight Level I": "زيادة وزن من المستوى الأول",
        "Overweight Level II": "زيادة وزن من المستوى الثاني",
        "Obesity Type I": "سمنة من النوع الأول",
        "Obesity Type II": "سمنة من النوع الثاني",
        "Obesity Type III": "سمنة من النوع الثالث"
    },
    "Hindi": {
        "Insufficient Weight": "कम वजन",
        "Normal Weight": "सामान्य वजन",
        "Overweight Level I": "अधिक वजन स्तर I",
        "Overweight Level II": "अधिक वजन स्तर II",
        "Obesity Type I": "मोटापा प्रकार I",
        "Obesity Type II": "मोटापा प्रकार II",
        "Obesity Type III": "मोटापा प्रकार III"
    },
    "Urdu": {
        "Insufficient Weight": "کم وزن",
        "Normal Weight": "نارمل وزن",
        "Overweight Level I": "زیادہ وزن لیول I",
        "Overweight Level II": "زیادہ وزن لیول II",
        "Obesity Type I": "موٹاپا ٹائپ I",
        "Obesity Type II": "موٹاپا ٹائپ II",
        "Obesity Type III": "موٹاپا ٹائپ III"
    }
}

diab_stages_map = {
    "English": {"Non-Diabetic": "Non-Diabetic", "Prediabetic": "Prediabetic", "Diabetic": "Diabetic"},
    "Español": {"Non-Diabetic": "No Diabetico", "Prediabetic": "Prediabetico", "Diabetic": "Diabetico"},
    "Français": {"Non-Diabetic": "Non diabetique", "Prediabetic": "Prediabetique", "Diabetic": "Diabetique"},
    "Chinese": {"Non-Diabetic": "非糖尿病", "Prediabetic": "糖尿病前期", "Diabetic": "糖尿病"},
    "Arabic": {"Non-Diabetic": "غير مصاب بالسكري", "Prediabetic": "في مرحلة ما قبل السكري", "Diabetic": "مصاب بالسكري"},
    "Hindi": {"Non-Diabetic": "गैर-मधुमेही", "Prediabetic": "प्री-डायबिटिक", "Diabetic": "मधुमेही"},
    "Urdu": {"Non-Diabetic": "غیر ذیابیطس", "Prediabetic": "ذیابیطس سے پہلے کا مرحلہ", "Diabetic": "ذیابیطس کا مریض"}
}

heart_stages_map = {
    "English": {"Low Risk": "Low Risk", "High Risk": "High Risk"},
    "Español": {"Low Risk": "Riesgo Bajo", "High Risk": "Riesgo Alto"},
    "Français": {"Low Risk": "Risque Faible", "High Risk": "Risque Eleve"},
    "Chinese": {"Low Risk": "低风险", "High Risk": "高风险"},
    "Arabic": {"Low Risk": "خطر منخفض", "High Risk": "خطر مرتفع"},
    "Hindi": {"Low Risk": "कम जोखिम", "High Risk": "उच्च जोखिम"},
    "Urdu": {"Low Risk": "کم خطرہ", "High Risk": "زیادہ خطرہ"}
}

health_status_map = {
    "English": {"Healthy": "Healthy", "Mild Risk": "Mild Risk", "High Risk": "High Risk", "Critical": "Critical"},
    "Español": {"Healthy": "Saludable", "Mild Risk": "Riesgo Leve", "High Risk": "Riesgo Alto", "Critical": "Critico"},
    "Français": {"Healthy": "Sain", "Mild Risk": "Risque Modere", "High Risk": "Risque Eleve", "Critical": "Critique"},
    "Chinese": {"Healthy": "健康", "Mild Risk": "轻度风险", "High Risk": "高风险", "Critical": "危急"},
    "Arabic": {"Healthy": "سليم صحيا", "Mild Risk": "خطر طفيف", "High Risk": "خطر مرتفع", "Critical": "حرج"},
    "Hindi": {"Healthy": "स्वस्थ", "Mild Risk": "हल्का जोखिम", "High Risk": "उच्च जोखिम", "Critical": "गंभीर"},
    "Urdu": {"Healthy": "صحت مند", "Mild Risk": "معمولی خطرہ", "High Risk": "زیادہ خطرہ", "Critical": "انتہائی تشویشناک"}
}


# Initialize Session States
if "page" not in st.session_state:
    st.session_state.page = "home"

if "patient_id" not in st.session_state:
    st.session_state.patient_id = f"PAT-{uuid.uuid4().hex[:6].upper()}"

if "results" not in st.session_state:
    st.session_state.results = None

# Load ML Predictor
@st.cache_resource
def get_predictor():
    return UnifiedDiseasePredictor(model_dir="saved_models")

predictor = get_predictor()


# ----------------- PAGE 1: HOME PAGE -----------------
if st.session_state.page == "home":
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-title'>Global Multimodal Disease Diagnostic System</div>
        <div class='hero-subtitle'>An advanced predictive research system for Obesity classification, Diabetes staging, and Cardiovascular risk mapping. Utilizing global machine learning pipelines and clinical guidelines to evaluate patient profiles.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature description blocks
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='medical-card'>
            <div class='card-header'>Obesity Classification</div>
            Analyze anthropometric and diet features to classify patient weight into 7 discrete clinical categories, ranging from Insufficient Weight to Severe Class III Obesity.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='medical-card'>
            <div class='card-header'>Diabetes Staging</div>
            Evaluate metabolic risk levels to stage patients as Non-Diabetic, Prediabetic, or Diabetic, enabling early dietary and clinical interventions.
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='medical-card'>
            <div class='card-header'>Cardiovascular Risk</div>
            Assess cardiovascular markers (lipid levels, blood pressure, family history, and stress) to evaluate overall risk for heart disease.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='text-align: center; margin-top: 40px;'>", unsafe_allow_html=True)
    if st.button("Get Started", use_container_width=True, type="primary"):
        st.session_state.page = "diagnostics"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ----------------- PAGE 2: DIAGNOSTICS & PREDICTION -----------------
elif st.session_state.page == "diagnostics":
    
    # --- SIDEBAR CONTROLS ---
    st.sidebar.markdown(f"### Configuration")
    
    # Language Selection dropdown
    selected_lang = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
    txt = LANGUAGES[selected_lang]
    
    # Go back button
    if st.sidebar.button(txt["return_home"], use_container_width=True):
        st.session_state.page = "home"
        st.session_state.results = None
        st.rerun()
        
    st.sidebar.markdown("---")
    
    # Patient Info Container
    st.sidebar.markdown(f"### {txt['patient_info']}")
    
    # Unique patient ID generator (automatically set, user can refresh)
    st.sidebar.text_input(txt["patient_id"], value=st.session_state.patient_id, disabled=True)
    if st.sidebar.button("Generate New ID"):
        st.session_state.patient_id = f"PAT-{uuid.uuid4().hex[:6].upper()}"
        st.rerun()
        
    patient_name = st.sidebar.text_input(txt["patient_name"], placeholder="John Doe")
    
    st.sidebar.markdown("---")
    
    # Preset Demo Patient Profiles to make testing easy
    st.sidebar.markdown("### Demo Patient Presets")
    demo_profile = st.sidebar.selectbox(
        "Load Test Profile",
        ["None", "Healthy Young Adult", "Prediabetic & Overweight", "High-Risk Cardiovascular Patient"]
    )
    
    # Set default values based on selected profile
    presets = {
        "None": {},
        "Healthy Young Adult": {
            "Age": 24, "Gender": txt["female"], "Height": 1.70, "Weight": 60, "BP": 115, "Chol": 170,
            "Smoking": txt["no_val"], "Exercise": txt["high"], "Alcohol": txt["none"], "Stress": txt["low"],
            "Sleep": 8.0, "Water": 2.5, "Screen": 2.0, "GenHealth": 2, "FamilyHeart": txt["no_val"], "FamilyWeight": txt["no_val"],
            "Veg": 3, "Meals": 3, "Snacks": txt["sometimes"], "HighCal": txt["no_val"], "CalMon": txt["yes"]
        },
        "Prediabetic & Overweight": {
            "Age": 42, "Gender": txt["male"], "Height": 1.75, "Weight": 92, "BP": 135, "Chol": 210,
            "Smoking": txt["no_val"], "Exercise": txt["low"], "Alcohol": txt["sometimes"], "Stress": txt["medium"],
            "Sleep": 6.5, "Water": 1.5, "Screen": 4.5, "GenHealth": 3, "FamilyHeart": txt["no_val"], "FamilyWeight": txt["yes"],
            "Veg": 2, "Meals": 3, "Snacks": txt["frequently"], "HighCal": txt["yes"], "CalMon": txt["no_val"]
        },
        "High-Risk Cardiovascular Patient": {
            "Age": 59, "Gender": txt["male"], "Height": 1.68, "Weight": 98, "BP": 158, "Chol": 255,
            "Smoking": txt["yes"], "Exercise": txt["low"], "Alcohol": txt["high"], "Stress": txt["high"],
            "Sleep": 5.0, "Water": 1.0, "Screen": 5.5, "GenHealth": 5, "FamilyHeart": txt["yes"], "FamilyWeight": txt["yes"],
            "Veg": 1, "Meals": 4, "Snacks": txt["always"], "HighCal": txt["yes"], "CalMon": txt["no_val"]
        }
    }
    
    active_preset = presets.get(demo_profile, {})

    # --- MAIN DIAGNOSTIC FORM ---
    st.title(txt["home_title"])
    st.write(txt["home_subtitle"])
    
    # Form layout with tabs
    tab_list = [txt["demographics_vitals"], txt["lifestyle_habits"], txt["diet_history"]]
    if "active_tab_key" not in st.session_state:
        st.session_state["active_tab_key"] = tab_list[0]
        
    tab1, tab2, tab3 = st.tabs(tab_list, key="active_tab_key")
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider(
                txt["age"], 18, 100, 
                value=int(active_preset.get("Age", 35))
            )
            gender = st.radio(
                txt["gender"], [txt["male"], txt["female"]], 
                index=0 if active_preset.get("Gender", txt["male"]) == txt["male"] else 1
            )
            height = st.number_input(
                txt["height"], 1.0, 2.5, 
                value=float(active_preset.get("Height", 1.70)), step=0.01
            )
            weight = st.number_input(
                txt["weight"], 30, 200, 
                value=int(active_preset.get("Weight", 70))
            )
        with col2:
            blood_pressure = st.slider(
                txt["blood_pressure"], 80, 200, 
                value=int(active_preset.get("BP", 120))
            )
            cholesterol = st.slider(
                txt["cholesterol"], 100, 400, 
                value=int(active_preset.get("Chol", 190))
            )
        
        # Next button for demographics
        st.write("")
        if st.button(txt["next_btn"], key="btn_next_1", use_container_width=True, type="primary"):
            st.session_state["active_tab_key"] = tab_list[1]
            st.rerun()
            
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            smoking = st.radio(
                txt["smoking"], [txt["yes"], txt["no_val"]], 
                index=0 if active_preset.get("Smoking", txt["no_val"]) == txt["yes"] else 1
            )
            exercise = st.selectbox(
                txt["exercise"], [txt["low"], txt["medium"], txt["high"]], 
                index=[txt["low"], txt["medium"], txt["high"]].index(active_preset.get("Exercise", txt["medium"]))
            )
            alcohol = st.selectbox(
                txt["alcohol"], [txt["none"], txt["sometimes"], txt["frequently"], txt["high"]], 
                index=[txt["none"], txt["sometimes"], txt["frequently"], txt["high"]].index(active_preset.get("Alcohol", txt["none"]))
            )
        with col2:
            stress = st.selectbox(
                txt["stress"], [txt["low"], txt["medium"], txt["high"]], 
                index=[txt["low"], txt["medium"], txt["high"]].index(active_preset.get("Stress", txt["medium"]))
            )
            sleep_hours = st.slider(
                txt["sleep"], 3.0, 12.0, 
                value=float(active_preset.get("Sleep", 7.0)), step=0.5
            )
            water_liters = st.slider(
                txt["water"], 0.5, 5.0, 
                value=float(active_preset.get("Water", 2.0)), step=0.5
            )
            screen_time = st.slider(
                txt["screentime"], 0.0, 16.0, 
                value=float(active_preset.get("Screen", 2.0)), step=0.5
            )
            
        # Next button for daily habits
        st.write("")
        if st.button(txt["next_btn"], key="btn_next_2", use_container_width=True, type="primary"):
            st.session_state["active_tab_key"] = tab_list[2]
            st.rerun()
            
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            family_heart = st.radio(
                txt["family_heart"], [txt["yes"], txt["no_val"]], 
                index=0 if active_preset.get("FamilyHeart", txt["no_val"]) == txt["yes"] else 1
            )
            family_weight = st.radio(
                txt["family_weight"], [txt["yes"], txt["no_val"]], 
                index=0 if active_preset.get("FamilyWeight", txt["no_val"]) == txt["yes"] else 1
            )
            gen_health = st.selectbox(
                txt["gen_health"], 
                [1, 2, 3, 4, 5], 
                format_func=lambda x: {1: txt["exc"], 2: txt["vgood"], 3: txt["good"], 4: txt["fair"], 5: txt["poor"]}[x],
                index=active_preset.get("GenHealth", 3) - 1
            )
        with col2:
            veg_freq = st.slider(
                txt["veg_freq"], 1.0, 3.0, 
                value=float(active_preset.get("Veg", 2.0)), step=0.5
            )
            meals_count = st.slider(
                txt["meals_count"], 1.0, 4.0, 
                value=float(active_preset.get("Meals", 3.0)), step=1.0
            )
            snack_freq = st.selectbox(
                txt["snack_freq"], [txt["none"], txt["sometimes"], txt["frequently"], txt["always"]], 
                index=[txt["none"], txt["sometimes"], txt["frequently"], txt["always"]].index(active_preset.get("Snacks", txt["sometimes"]))
            )
            high_cal = st.radio(
                "Eat high-caloric food frequently?", [txt["yes"], txt["no_val"]], 
                index=0 if active_preset.get("HighCal", txt["no_val"]) == txt["yes"] else 1
            )
            cal_mon = st.radio(
                "Monitor daily calories consumption?", [txt["yes"], txt["no_val"]], 
                index=0 if active_preset.get("CalMon", txt["no_val"]) == txt["yes"] else 1
            )
            
        # Submit prediction
        st.write("")
        if st.button(txt["generate_report"], use_container_width=True, type="primary"):
            if not patient_name.strip():
                st.error(txt["error_name"])
            else:
                with st.spinner(txt["generating"]):
                    # Map inputs to model format dictionary
                    # Enforce English mappings for the prediction backend
                    gender_en = "Male" if gender == txt["male"] else "Female"
                    smoking_en = "Yes" if smoking == txt["yes"] else "No"
                    exercise_en = "High" if exercise == txt["high"] else ("Medium" if exercise == txt["medium"] else "Low")
                    alcohol_en = "High" if alcohol == txt["high"] else ("Frequently" if alcohol == txt["frequently"] else ("Sometimes" if alcohol == txt["sometimes"] else "None"))
                    stress_en = "High" if stress == txt["high"] else ("Medium" if stress == txt["medium"] else "Low")
                    family_heart_en = "Yes" if family_heart == txt["yes"] else "No"
                    family_weight_en = "Yes" if family_weight == txt["yes"] else "No"
                    snack_freq_en = "Always" if snack_freq == txt["always"] else ("Frequently" if snack_freq == txt["frequently"] else ("Sometimes" if snack_freq == txt["sometimes"] else "no"))
                    high_cal_en = "Yes" if high_cal == txt["yes"] else "No"
                    cal_mon_en = "Yes" if cal_mon == txt["yes"] else "No"
                    
                    patient_data = {
                        'Age': age,
                        'Gender': gender_en,
                        'Height': height,
                        'Weight': weight,
                        'Smoking': smoking_en,
                        'Alcohol': alcohol_en,
                        'Exercise': exercise_en,
                        'HighBP': "Yes" if blood_pressure >= 140 else "No",
                        'BloodPressure': blood_pressure,
                        'HighChol': "Yes" if cholesterol >= 240 else "No",
                        'CholesterolLevel': cholesterol,
                        'FamilyHeartDisease': family_heart_en,
                        'FamilyOverweight': family_weight_en,
                        'StressLevel': stress_en,
                        'SleepHours': sleep_hours,
                        'HighCaloricFood': high_cal_en,
                        'VegetablesFreq': veg_freq,
                        'MealsCount': meals_count,
                        'SnackBetweenMeals': snack_freq_en,
                        'WaterLiters': water_liters,
                        'CaloriesMonitoring': cal_mon_en,
                        'ScreenTimeHours': screen_time,
                        'GeneralHealthScore': gen_health,
                        'LowHDL': "Yes" if cholesterol > 240 and blood_pressure > 140 else "No", # heuristic placeholder
                        'HighLDL': "Yes" if cholesterol > 200 else "No",
                        'TriglycerideLevel': 150.0,
                        'FastingSugar': 95.0,
                        'CRPLevel': 1.5,
                        'HomocysteineLevel': 10.0
                    }
                    
                    # Execute prediction
                    results = predictor.predict(patient_data)
                    
                    # Store in session state
                    st.session_state.results = results
                
    # --- RENDER RESULTS ---
    if st.session_state.results:
        res = st.session_state.results
        
        st.markdown("---")
        st.markdown(f"## {txt['results_header']}")
        
        # Display Patient Name and Unique ID
        col_name, col_id = st.columns(2)
        with col_name:
            st.markdown(f"**{txt['patient_name']}:** {patient_name}")
        with col_id:
            st.markdown(f"**{txt['patient_id']}:** {st.session_state.patient_id}")
            
        # 1. Overall Health Severity Status Card
        h_status = res["HealthStatus"]
        translated_health_status = health_status_map[selected_lang].get(h_status, h_status)
        
        badge_class = "status-healthy"
        if h_status == "Mild Risk": badge_class = "status-mild"
        elif h_status == "High Risk": badge_class = "status-high"
        elif h_status == "Critical": badge_class = "status-critical"
        
        st.markdown(f"""
        <div class='medical-card'>
            <div class='card-header'>{txt['health_status']}</div>
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <span style='font-size: 18px;'>Calculated Patient Health Classification:</span>
                <span class='status-badge {badge_class}'>{translated_health_status.upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Individual Disease Cards
        col_ob, col_diab, col_heart = st.columns(3)
        
        # Translate outcomes
        translated_ob_status = obesity_stages_map[selected_lang].get(res["ObesityStatus"], res["ObesityStatus"])
        translated_diab_status = diab_stages_map[selected_lang].get(res["DiabetesStatus"], res["DiabetesStatus"])
        translated_heart_status = heart_stages_map[selected_lang].get(res["HeartDiseaseStatus"], res["HeartDiseaseStatus"])
        
        with col_ob:
            st.markdown(f"""
            <div class='medical-card' style='height: 100%;'>
                <div class='card-header'>{txt['obesity_status']}</div>
                <strong>Classification:</strong> {translated_ob_status}<br>
                <strong>Calculated BMI:</strong> {res['BMI']}<br>
            </div>
            """, unsafe_allow_html=True)
            
        with col_diab:
            st.markdown(f"""
            <div class='medical-card' style='height: 100%;'>
                <div class='card-header'>{txt['diab_status']}</div>
                <strong>Classification:</strong> {translated_diab_status}<br>
                <strong>Diabetes Risk:</strong> {res['DiabetesProbability']}%<br>
                <strong>Prediabetes Risk:</strong> {res['PrediabetesProbability']}%<br>
            </div>
            """, unsafe_allow_html=True)
            
        with col_heart:
            st.markdown(f"""
            <div class='medical-card' style='height: 100%;'>
                <div class='card-header'>{txt['heart_status']}</div>
                <strong>Classification:</strong> {translated_heart_status}<br>
                <strong>Cardiovascular Risk:</strong> {res['HeartDiseaseProbability']}%<br>
            </div>
            """, unsafe_allow_html=True)
            
        # 3. Probabilities Breakdown Panel
        st.markdown(f"""
        <div class='medical-card'>
            <div class='card-header'>{txt['probabilities']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.metric(txt["prediab_prob"], f"{res['PrediabetesProbability']}%")
        with col_p2:
            st.metric(txt["diab_prob"], f"{res['DiabetesProbability']}%")
        with col_p3:
            st.metric(txt["heart_prob"], f"{res['HeartDiseaseProbability']}%")
            
        # 4. Precautionary Measures Checklist
        st.markdown(f"""
        <div class='medical-card'>
            <div class='card-header'>{txt['precautions']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display precautions in localized context or standard list
        for item in res["PrecautionaryMeasures"]:
            st.markdown(f"* {item}")
            
        # 5. Reset button
        st.write("")
        if st.button(txt["reset"], use_container_width=True):
            st.session_state.results = None
            st.session_state.patient_id = f"PAT-{uuid.uuid4().hex[:6].upper()}"
            st.rerun()
