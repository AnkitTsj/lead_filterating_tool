import gradio as gr
import pandas as pd
import numpy as np
import os

# --- Configuration ---
ODBUS_CSV_PATH = "ODBus_v1.csv"
OUTPUT_CSV_FILE = "filtered_leads.csv"

# --- Mappings for enhanced UX ---
PROVINCE_MAP = {
    "AB": "Alberta",
    "BC": "British Columbia",
    "MB": "Manitoba",
    "NB": "New Brunswick",
    "NL": "Newfoundland and Labrador",
    "NS": "Nova Scotia",
    "NT": "Northwest Territories",
    "NU": "Nunavut",
    "ON": "Ontario",
    "PE": "Prince Edward Island",
    "QC": "Quebec",
    "SK": "Saskatchewan",
    "YT": "Yukon"
}
# Reverse map for filtering
PROVINCE_REV_MAP = {v: k for k, v in PROVINCE_MAP.items()}

# A simplified NAICS description mapping for 2-digit codes.
# In a real scenario, you might load this from a CSV or a small database.
# For the hackathon, hardcoding common ones is acceptable for demo.
NAICS_2_DIGIT_DESCRIPTIONS = {
    "11": "Agriculture, Forestry, Fishing and Hunting",
    "21": "Mining, Quarrying, and Oil and Gas Extraction",
    "22": "Utilities",
    "23": "Construction",
    "31-33": "Manufacturing", # Often grouped
    "41": "Wholesale Trade",
    "44-45": "Retail Trade", # Often grouped
    "48-49": "Transportation and Warehousing", # Often grouped
    "51": "Information and Cultural Industries",
    "52": "Finance and Insurance",
    "53": "Real Estate and Rental and Leasing",
    "54": "Professional, Scientific, and Technical Services",
    "55": "Management of Companies and Enterprises",
    "56": "Administrative and Support, Waste Management and Remediation Services",
    "61": "Educational Services",
    "62": "Health Care and Social Assistance",
    "71": "Arts, Entertainment and Recreation",
    "72": "Accommodation and Food Services",
    "81": "Other Services (except Public Administration)",
    "91": "Public Administration"
}
# Create choices for NAICS dropdown: ["All", "11 - Agriculture...", "21 - Mining...", ...]
NAICS_CHOICES = ["All"] + [f"{code} - {desc}" for code, desc in NAICS_2_DIGIT_DESCRIPTIONS.items()]


# --- Data Handling ---
df_global = None

def load_data(csv_path):
    global df_global
    if df_global is not None:
        return df_global, "Data already loaded."

    try:
        df = pd.read_csv(csv_path, encoding='utf-8', na_values=['..'])
        load_message = f"Loaded {len(df)} records from {csv_path}"

        df['derived_NAICS'] = df['derived_NAICS'].astype(str)
        df['total_no_employees'] = pd.to_numeric(df['total_no_employees'], errors='coerce')

        if 'NAICS_descr' not in df.columns:
            df['NAICS_descr'] = 'N/A'

        df_global = df
        return df, load_message
    except FileNotFoundError:
        error_message = f"Error: Data file not found at {csv_path}. Please check the path."
        return None, error_message
    except Exception as e:
        error_message = f"Error loading data: {e}"
        return None, error_message

def filter_leads(industry_selection, min_employees, province_full_name, city):
    """
    Filters the business leads based on the provided criteria and adds a simulated lead score.
    """
    global df_global
    if df_global is None:
        # Attempt to load data if not already loaded (e.g., if the user refreshes or starts without pre-loading)
        df_global, msg = load_data(ODBUS_CSV_PATH)
        if df_global is None:
            # Return empty DataFrame and error message if load fails
            return pd.DataFrame(), gr.File(visible=False), msg 

    filtered_df = df_global.copy()
    
    # Extract NAICS code from user selection (e.g., "54 - Professional..." -> "54")
    industry_naics = ""
    if industry_selection and industry_selection != "All":
        industry_naics = industry_selection.split(' - ')[0] # Get the 2-digit code

    # Convert full province name to abbreviation for filtering
    province_abbr = ""
    if province_full_name and province_full_name != "All":
        province_abbr = PROVINCE_REV_MAP.get(province_full_name, "")


    if industry_naics:
        if 'derived_NAICS' in filtered_df.columns:
            # Ensure slicing works on string type
            filtered_df = filtered_df[
                filtered_df['derived_NAICS'].astype(str).str.startswith(str(industry_naics), na=False)
            ]

    if min_employees is not None:
        if 'total_no_employees' in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df['total_no_employees'].notna() & (filtered_df['total_no_employees'] >= min_employees)
            ]

    if province_abbr: # Use abbreviation for filtering
        if 'prov_terr' in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df['prov_terr'].astype(str).str.upper() == province_abbr.upper()
            ]

    if city and city != "All":
        if 'city' in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df['city'].astype(str).str.upper() == city.upper()
            ]

    # --- Start of New Lead Scoring Logic ---
    # Assign an initial score of 0
    filtered_df['lead_score'] = 0

    # Rule 1: Employee Count (Example: larger companies score higher)
    # Ensure total_no_employees is numeric and not NaN before comparison
    filtered_df.loc[filtered_df['total_no_employees'].notna() & (filtered_df['total_no_employees'] >= 50), 'lead_score'] += 10
    filtered_df.loc[filtered_df['total_no_employees'].notna() & (filtered_df['total_no_employees'] >= 200), 'lead_score'] += 20 # Cumulative

    # Rule 2: Specific Industries (Example: Tech/Professional services are high value)
    tech_naics_codes = ['51', '54'] # Information; Professional, Scientific, and Technical Services
    filtered_df.loc[filtered_df['derived_NAICS'].astype(str).str[:2].isin(tech_naics_codes), 'lead_score'] += 15

    # Rule 3: Key Provinces/Cities
    high_value_provinces_abbr = ['ON', 'BC'] # Ontario, British Columbia
    filtered_df.loc[filtered_df['prov_terr'].astype(str).str.upper().isin(high_value_provinces_abbr), 'lead_score'] += 5

    high_value_cities = ['TORONTO', 'VANCOUVER', 'MONTREAL']
    filtered_df.loc[filtered_df['city'].astype(str).str.upper().isin(high_value_cities), 'lead_score'] += 5
    # --- End of New Lead Scoring Logic ---

    # Sort by lead score for demonstration of prioritization
    filtered_df = filtered_df.sort_values(by='lead_score', ascending=False)


    if filtered_df.empty:
        return pd.DataFrame(), gr.File(visible=False), "No leads found matching the selected criteria. Try adjusting your filters."
    else:
        # Prepare a subset of columns for display and download, now including lead_score.
        output_df_for_display = filtered_df[[
            'business_name', 'full_address', 'city', 'prov_terr', 'postal_code',
            'derived_NAICS', 'NAICS_descr', 'total_no_employees', 'lead_score' # ADDED: 'lead_score'
        ]].head(1000)

        # For download, include lead_score as well
        csv_output = filtered_df[[
            'business_name', 'full_address', 'city', 'prov_terr', 'postal_code',
            'derived_NAICS', 'NAICS_descr', 'total_no_employees', 'lead_score' # ADDED: 'lead_score'
        ]].to_csv(index=False, encoding='utf-8-sig')

        temp_csv_path = "temp_filtered_leads.csv"
        with open(temp_csv_path, "w", encoding='utf-8-sig') as f:
            f.write(csv_output)

        # Updated output message
        return output_df_for_display, gr.File(value=temp_csv_path, visible=True, label="Download Filtered Leads CSV"), f"Found {len(filtered_df)} leads matching your criteria. Results are sorted by 'Lead Score'."
# --- Gradio Interface ---
# Load data once when the application starts
initial_df, initial_load_message = load_data(ODBUS_CSV_PATH)
if initial_df is None:
    print(initial_load_message)
    # Handle error gracefully: perhaps display a message in the UI or disable controls
else:
    # Use full province names for dropdown
    unique_provinces_full_names = sorted([PROVINCE_MAP.get(abbr, abbr) for abbr in initial_df['prov_terr'].dropna().unique().tolist()])
    unique_provinces_full_names.insert(0, "All")

    unique_cities_all = sorted(initial_df['city'].dropna().unique().tolist())
    unique_cities_all.insert(0, "All")

# Function to update city dropdown based on province selection
def update_cities(selected_province_full_name):
    if selected_province_full_name == "All" or df_global is None:
        return gr.Dropdown(choices=["All"], value="All")
    else:
        # Convert selected full name back to abbreviation for internal filtering
        selected_province_abbr = PROVINCE_REV_MAP.get(selected_province_full_name, "")
        province_df = df_global[df_global['prov_terr'].astype(str).str.upper() == selected_province_abbr.upper()]
        cities_for_province = sorted(province_df['city'].dropna().unique().tolist())
        cities_for_province.insert(0, "All")
        return gr.Dropdown(choices=cities_for_province, value="All")


with gr.Blocks(title="ODBus Intelligent Lead Filtration Tool") as demo:
    gr.Markdown("""
    # 💡 ODBus Intelligent Lead Filtration Tool
    This tool helps sales and marketing teams find targeted business leads
    from Canada's Open Database of Businesses (ODBus). You can filter over **450,000** Canadian companies
    by industry, employee count, province, and city to get highly relevant lead lists.
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Filter Leads")
            
            # Province Dropdown (now with full names)
            province_dropdown = gr.Dropdown(
                choices=unique_provinces_full_names if initial_df is not None else ["All"],
                label="Select Province:",
                value="All"
            )

            # City dropdown
            city_dropdown = gr.Dropdown(
                choices=unique_cities_all if initial_df is not None else ["All"],
                label="Select City:",
                value="All"
            )

            # Link province change to city update
            province_dropdown.change(
                fn=update_cities,
                inputs=province_dropdown,
                outputs=city_dropdown
            )

            # NAICS Dropdown (now with descriptions)
            naics_dropdown = gr.Dropdown(
                choices=NAICS_CHOICES,
                label="Filter by Industry (NAICS Code & Description):",
                value="All"
            )

            min_employees_input = gr.Number(
                label="Minimum Number of Employees:",
                value=10,
                step=10,
                minimum=1
            )

            apply_filters_btn = gr.Button("Apply Filters")

        with gr.Column(scale=3):
            gr.Markdown("## Filtered Leads Results:")
            
            output_dataframe = gr.DataFrame(
                value=pd.DataFrame(),
                headers=["Business Name", "Address", "City", "Province/Territory", "Postal Code", "NAICS Code", "NAICS Description", "Total Employees", "Lead Score"], # ADDED "Lead Score"
                row_count=10,
                col_count=9, # Update column count
                interactive=False
            )
            output_message = gr.Textbox(label="Status", value="Set your filters and click 'Apply Filters'.")
            
            # The download component
            download_file = gr.File(label="Download Filtered Leads CSV", visible=False)


    apply_filters_btn.click(
        fn=filter_leads,
        inputs=[
            naics_dropdown,
            min_employees_input,
            province_dropdown,
            city_dropdown
        ],
        outputs=[output_dataframe, download_file, output_message], # output includes the file component and message
        queue=False
    )


    gr.Markdown("---")
    gr.Markdown("Built with ❤️ using Gradio")

if __name__ == "__main__":
    demo.launch()