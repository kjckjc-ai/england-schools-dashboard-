import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
import base64

# Set page configuration
st.set_page_config(
    page_title="England Schools Dashboard",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
@st.cache_resource
def get_connection():
    return sqlite3.connect("schools.db", check_same_thread=False)

# Load data with caching
@st.cache_data
def load_metadata():
    conn = get_connection()
    metadata = pd.read_sql("SELECT * FROM metadata", conn)
    return metadata.iloc[0]

@st.cache_data
def load_school_types(filters=None):
    conn = get_connection()
    
    query = '''
        SELECT "EstablishmentTypeGroup (name)" as EstablishmentTypeGroup, 
               COUNT(*) as Count
        FROM schools
        WHERE 1=1
    '''
    params = []
    
    if filters:
        if filters.get('name'):
            query += ' AND EstablishmentName LIKE ?'
            params.append(f'%{filters["name"]}%')
            
        if filters.get('trust_name'):
            query += ' AND "Trusts (name)" LIKE ?'
            params.append(f'%{filters["trust_name"]}%')
        
        if filters.get('la'):
            query += ' AND "LA (name)" = ?'
            params.append(filters["la"])
        
        # Updated to use establishment_groups instead of school_types
        if filters.get('establishment_groups') and len(filters["establishment_groups"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["establishment_groups"]])
            query += f' AND "EstablishmentTypeGroup (name)" IN ({placeholders})'
            params.extend(filters["establishment_groups"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        # Updated to use postcode_prefix instead of postcode
        if filters.get('postcode_prefix'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode_prefix"]}%')
            
        if filters.get('gender'):
            query += ' AND "Gender (name)" = ?'
            params.append(filters["gender"])
            
        if filters.get('religion'):
            query += ' AND "ReligiousCharacter (name)" = ?'
            params.append(filters["religion"])
    
    query += ' GROUP BY "EstablishmentTypeGroup (name)" ORDER BY Count DESC'
    
    return pd.read_sql(query, conn, params=params)

@st.cache_data
def load_phase_summary(filters=None):
    conn = get_connection()
    
    query = '''
        SELECT "PhaseOfEducation (name)" as PhaseOfEducation, 
               COUNT(*) as Count
        FROM schools
        WHERE 1=1
    '''
    params = []
    
    if filters:
        if filters.get('name'):
            query += ' AND EstablishmentName LIKE ?'
            params.append(f'%{filters["name"]}%')
            
        if filters.get('trust_name'):
            query += ' AND "Trusts (name)" LIKE ?'
            params.append(f'%{filters["trust_name"]}%')
        
        if filters.get('la'):
            query += ' AND "LA (name)" = ?'
            params.append(filters["la"])
        
        # Updated to use establishment_groups instead of school_types
        if filters.get('establishment_groups') and len(filters["establishment_groups"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["establishment_groups"]])
            query += f' AND "EstablishmentTypeGroup (name)" IN ({placeholders})'
            params.extend(filters["establishment_groups"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        # Updated to use postcode_prefix instead of postcode
        if filters.get('postcode_prefix'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode_prefix"]}%')
            
        if filters.get('gender'):
            query += ' AND "Gender (name)" = ?'
            params.append(filters["gender"])
            
        if filters.get('religion'):
            query += ' AND "ReligiousCharacter (name)" = ?'
            params.append(filters["religion"])
    
    query += ' GROUP BY "PhaseOfEducation (name)" ORDER BY Count DESC'
    
    return pd.read_sql(query, conn, params=params)

@st.cache_data
def load_religion_summary(filters=None):
    conn = get_connection()
    
    query = '''
        SELECT "ReligiousCharacter (name)" as ReligiousCharacter, 
               COUNT(*) as Count
        FROM schools
        WHERE "ReligiousCharacter (name)" != 'Unknown'
    '''
    params = []
    
    if filters:
        if filters.get('name'):
            query += ' AND EstablishmentName LIKE ?'
            params.append(f'%{filters["name"]}%')
            
        if filters.get('trust_name'):
            query += ' AND "Trusts (name)" LIKE ?'
            params.append(f'%{filters["trust_name"]}%')
        
        if filters.get('la'):
            query += ' AND "LA (name)" = ?'
            params.append(filters["la"])
        
        # Updated to use establishment_groups instead of school_types
        if filters.get('establishment_groups') and len(filters["establishment_groups"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["establishment_groups"]])
            query += f' AND "EstablishmentTypeGroup (name)" IN ({placeholders})'
            params.extend(filters["establishment_groups"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        # Updated to use postcode_prefix instead of postcode
        if filters.get('postcode_prefix'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode_prefix"]}%')
            
        if filters.get('gender'):
            query += ' AND "Gender (name)" = ?'
            params.append(filters["gender"])
            
        if filters.get('religion'):
            query += ' AND "ReligiousCharacter (name)" = ?'
            params.append(filters["religion"])
    
    query += ' GROUP BY "ReligiousCharacter (name)" ORDER BY Count DESC'
    
    return pd.read_sql(query, conn, params=params)

@st.cache_data
def load_gender_summary(filters=None):
    conn = get_connection()
    
    query = '''
        SELECT "Gender (name)" as Gender, 
               COUNT(*) as Count
        FROM schools
        WHERE "Gender (name)" != 'Unknown'
    '''
    params = []
    
    if filters:
        if filters.get('name'):
            query += ' AND EstablishmentName LIKE ?'
            params.append(f'%{filters["name"]}%')
            
        if filters.get('trust_name'):
            query += ' AND "Trusts (name)" LIKE ?'
            params.append(f'%{filters["trust_name"]}%')
        
        if filters.get('la'):
            query += ' AND "LA (name)" = ?'
            params.append(filters["la"])
        
        # Updated to use establishment_groups instead of school_types
        if filters.get('establishment_groups') and len(filters["establishment_groups"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["establishment_groups"]])
            query += f' AND "EstablishmentTypeGroup (name)" IN ({placeholders})'
            params.extend(filters["establishment_groups"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        # Updated to use postcode_prefix instead of postcode
        if filters.get('postcode_prefix'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode_prefix"]}%')
            
        if filters.get('gender'):
            query += ' AND "Gender (name)" = ?'
            params.append(filters["gender"])
            
        if filters.get('religion'):
            query += ' AND "ReligiousCharacter (name)" = ?'
            params.append(filters["religion"])
    
    query += ' GROUP BY "Gender (name)" ORDER BY Count DESC'
    
    return pd.read_sql(query, conn, params=params)

@st.cache_data
def load_local_authorities():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"LA (name)\" FROM schools WHERE \"LA (name)\" != 'Unknown' ORDER BY \"LA (name)\"", conn)

@st.cache_data
def load_school_type_options():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"TypeOfEstablishment (name)\" FROM schools ORDER BY \"TypeOfEstablishment (name)\"", conn)

# New function to load establishment type groups
@st.cache_data
def load_establishment_groups():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"EstablishmentTypeGroup (name)\" FROM schools WHERE \"EstablishmentTypeGroup (name)\" != 'Unknown' ORDER BY \"EstablishmentTypeGroup (name)\"", conn)

@st.cache_data
def load_phases():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"PhaseOfEducation (name)\" FROM schools WHERE \"PhaseOfEducation (name)\" != 'Unknown' ORDER BY \"PhaseOfEducation (name)\"", conn)

@st.cache_data
def load_genders():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"Gender (name)\" FROM schools WHERE \"Gender (name)\" != 'Unknown' ORDER BY \"Gender (name)\"", conn)

@st.cache_data
def load_religions():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"ReligiousCharacter (name)\" FROM schools WHERE \"ReligiousCharacter (name)\" != 'Unknown' ORDER BY \"ReligiousCharacter (name)\"", conn)

# New function to load postcode prefixes
@st.cache_data
def load_postcode_prefixes():
    conn = get_connection()
    # Extract the first part of the postcode (before the space)
    query = """
    SELECT DISTINCT SUBSTR(Postcode, 1, INSTR(Postcode, ' ')-1) as PostcodePrefix
    FROM schools
    WHERE Postcode IS NOT NULL AND Postcode != ''
    ORDER BY PostcodePrefix
    """
    return pd.read_sql(query, conn)

def find_similar_schools(name, limit=5):
    conn = get_connection()
    # Simple pattern matching for similar names
    query = "SELECT DISTINCT EstablishmentName FROM schools WHERE EstablishmentName LIKE ? LIMIT ?"
    params = [f'%{name}%', limit]
    return pd.read_sql(query, conn, params=params)["EstablishmentName"].tolist()

def find_similar_trusts(name, limit=5):
    conn = get_connection()
    # Simple pattern matching for similar trust names
    query = "SELECT DISTINCT \"Trusts (name)\" FROM schools WHERE \"Trusts (name)\" LIKE ? AND \"Trusts (name)\" != '' LIMIT ?"
    params = [f'%{name}%', limit]
    return pd.read_sql(query, conn, params=params)["Trusts (name)"].tolist()

@st.cache_data
def search_schools(name="", trust_name="", la="", establishment_groups=None, phase="", postcode_prefix="", gender="", religion="", page=1, per_page=50, show_all=False):
    conn = get_connection()
    
    # Build query
    query = 'SELECT * FROM schools WHERE 1=1'
    params = []
    
    if name:
        # Use LIKE with wildcards for more flexible matching
        query += ' AND EstablishmentName LIKE ?'
        params.append(f'%{name}%')
    
    if trust_name:
        # Use LIKE with wildcards for more flexible matching
        query += ' AND "Trusts (name)" LIKE ?'
        params.append(f'%{trust_name}%')
    
    if la:
        query += ' AND "LA (name)" = ?'
        params.append(la)
    
    # Updated to use establishment_groups instead of school_types
    if establishment_groups and len(establishment_groups) > 0:
        placeholders = ', '.join(['?' for _ in establishment_groups])
        query += f' AND "EstablishmentTypeGroup (name)" IN ({placeholders})'
        params.extend(establishment_groups)
    
    if phase:
        query += ' AND "PhaseOfEducation (name)" = ?'
        params.append(phase)
    
    # Updated to use postcode_prefix instead of postcode
    if postcode_prefix:
        query += ' AND Postcode LIKE ?'
        params.append(f'{postcode_prefix}%')
        
    if gender:
        query += ' AND "Gender (name)" = ?'
        params.append(gender)
        
    if religion:
        query += ' AND "ReligiousCharacter (name)" = ?'
        params.append(religion)
    
    # Get total count for pagination
    count_query = query.replace('SELECT *', 'SELECT COUNT(*)')
    count_df = pd.read_sql(count_query, conn, params=params)
    total_count = count_df.iloc[0, 0]
    
    # Add ordering
    query += ' ORDER BY EstablishmentName'
    
    # Add pagination if not showing all
    if not show_all:
        query += ' LIMIT ? OFFSET ?'
        params.append(per_page)
        params.append((page - 1) * per_page)
    
    # Execute query
    schools = pd.read_sql(query, conn, params=params)
    
    return schools, total_count

@st.cache_data
def get_school_by_urn(urn):
    conn = get_connection()
    query = "SELECT * FROM schools WHERE URN = ?"
    return pd.read_sql(query, conn, params=[urn])

@st.cache_data
def get_trust_schools(trust_name):
    conn = get_connection()
    query = "SELECT * FROM schools WHERE \"Trusts (name)\" = ? ORDER BY EstablishmentName"
    return pd.read_sql(query, conn, params=[trust_name])

def create_infographic_html(school_data):
    # Extract school data
    school_name = school_data['EstablishmentName']
    school_type = school_data['TypeOfEstablishment (name)']
    phase = school_data['PhaseOfEducation (name)']
    address = f"{school_data['Street']}, {school_data['Town']}, {school_data['Postcode']}"
    head_teacher = f"{school_data['HeadFirstName']} {school_data['HeadLastName']}"
    
    # Get numeric data with fallbacks
    try:
        num_pupils = int(school_data['NumberOfPupils']) if not pd.isna(school_data['NumberOfPupils']) else 0
    except:
        num_pupils = 0
        
    try:
        capacity = int(school_data['SchoolCapacity']) if not pd.isna(school_data['SchoolCapacity']) else 0
    except:
        capacity = 0
        
    try:
        fsm_percentage = float(school_data['PercentageFSM']) if not pd.isna(school_data['PercentageFSM']) else 0
    except:
        fsm_percentage = 0
    
    # Calculate utilization
    utilization = (num_pupils / capacity * 100) if capacity > 0 else 0
    
    # Determine FSM color based on percentage
    if fsm_percentage < 10:
        fsm_color = "#4CAF50"  # Green
    elif fsm_percentage < 20:
        fsm_color = "#FFC107"  # Amber
    else:
        fsm_color = "#F44336"  # Red
    
    # Create HTML for the infographic
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>School Infographic</title>
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f7;
            }}
            .infographic {{
                width: 1000px;
                height: 500px;
                background: linear-gradient(to bottom right, #ffffff, #f5f5f7);
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                padding: 30px;
                margin: 20px auto;
                display: flex;
                flex-direction: column;
                position: relative;
                overflow: hidden;
            }}
            .header {{
                width: 100%;
                background-color: #f8f8f8;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }}
            .school-name {{
                font-size: 28px;
                font-weight: 700;
                color: #1d1d1f;
                margin: 0;
            }}
            .school-type {{
                font-size: 16px;
                color: #86868b;
                margin: 5px 0 0 0;
            }}
            .content {{
                display: flex;
                flex: 1;
            }}
            .left-column {{
                flex: 1;
                padding-right: 20px;
            }}
            .right-column {{
                flex: 2;
                display: flex;
                flex-direction: column;
            }}
            .metric-circle {{
                width: 180px;
                height: 180px;
                border-radius: 50%;
                background: white;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                margin: 0 auto 20px auto;
                position: relative;
                border: 10px solid {fsm_color};
            }}
            .metric-value {{
                font-size: 36px;
                font-weight: 700;
                color: #1d1d1f;
            }}
            .metric-label {{
                font-size: 14px;
                color: #86868b;
                text-align: center;
                padding: 0 10px;
            }}
            .metrics-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
            }}
            .metric-box {{
                flex: 1;
                background-color: white;
                border-radius: 15px;
                padding: 15px;
                margin: 0 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                text-align: center;
            }}
            .metric-box:first-child {{
                margin-left: 0;
            }}
            .metric-box:last-child {{
                margin-right: 0;
            }}
            .info-section {{
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            }}
            .info-title {{
                font-size: 18px;
                font-weight: 600;
                color: #1d1d1f;
                margin: 0 0 10px 0;
            }}
            .info-row {{
                display: flex;
                margin-bottom: 10px;
            }}
            .info-label {{
                flex: 1;
                font-size: 14px;
                color: #86868b;
            }}
            .info-value {{
                flex: 2;
                font-size: 14px;
                color: #1d1d1f;
                font-weight: 500;
            }}
            .download-btn {{
                background-color: #0071e3;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.2s;
                margin-top: 10px;
            }}
            .download-btn:hover {{
                background-color: #0077ed;
            }}
            .footer {{
                font-size: 12px;
                color: #86868b;
                text-align: center;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div id="infographic" class="infographic">
            <div class="header">
                <h1 class="school-name">{school_name}</h1>
                <p class="school-type">{school_type} • {phase}</p>
            </div>
            <div class="content">
                <div class="left-column">
                    <div class="metric-circle">
                        <div class="metric-value">{fsm_percentage:.1f}%</div>
                        <div class="metric-label">Free School Meals</div>
                    </div>
                    <div class="metrics-row">
                        <div class="metric-box">
                            <div class="metric-value">{num_pupils}</div>
                            <div class="metric-label">Pupils</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{capacity}</div>
                            <div class="metric-label">Capacity</div>
                        </div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{utilization:.1f}%</div>
                        <div class="metric-label">Utilization</div>
                    </div>
                </div>
                <div class="right-column">
                    <div class="info-section">
                        <h2 class="info-title">School Information</h2>
                        <div class="info-row">
                            <div class="info-label">Address:</div>
                            <div class="info-value">{address}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Head Teacher:</div>
                            <div class="info-value">{head_teacher}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Phone:</div>
                            <div class="info-value">{school_data['TelephoneNum']}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Website:</div>
                            <div class="info-value">{school_data['SchoolWebsite']}</div>
                        </div>
                    </div>
                    <div class="info-section">
                        <h2 class="info-title">Additional Details</h2>
                        <div class="info-row">
                            <div class="info-label">Local Authority:</div>
                            <div class="info-value">{school_data['LA (name)']}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Trust:</div>
                            <div class="info-value">{school_data['Trusts (name)'] if not pd.isna(school_data['Trusts (name)']) else 'N/A'}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Gender:</div>
                            <div class="info-value">{school_data['Gender (name)']}</div>
                        </div>
                        <div class="info-row">
                            <div class="info-label">Religious Character:</div>
                            <div class="info-value">{school_data['ReligiousCharacter (name)']}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div style="text-align: center;">
            <button id="download-btn" class="download-btn">Download Infographic</button>
        </div>
        <script>
            document.getElementById('download-btn').addEventListener('click', function() {{
                html2canvas(document.getElementById('infographic')).then(function(canvas) {{
                    var link = document.createElement('a');
                    link.download = '{school_name.replace(" ", "_")}_infographic.png';
                    link.href = canvas.toDataURL('image/png');
                    link.click();
                }});
            }});
        </script>
    </body>
    </html>
    """
    return html

# Main app
def main():
    # Initialize session state for filters
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'name': '',
            'trust_name': '',
            'la': '',
            'establishment_groups': [],  # Changed from school_types to establishment_groups
            'phase': '',
            'postcode_prefix': '',  # Changed from postcode to postcode_prefix
            'gender': '',
            'religion': '',
            'chart_filters': {
                'school_type': '',
                'phase': '',
                'gender': '',
                'religion': ''
            }
        }
    
    if 'page' not in st.session_state:
        st.session_state.page = 1
        
    if 'show_all' not in st.session_state:
        st.session_state.show_all = False
        
    if 'selected_school' not in st.session_state:
        st.session_state.selected_school = None
        
    if 'viewing_trust' not in st.session_state:
        st.session_state.viewing_trust = None
    
    # Load data
    metadata = load_metadata()
    local_authorities = load_local_authorities()
    establishment_groups = load_establishment_groups()  # New - load establishment groups
    phases = load_phases()
    genders = load_genders()
    religions = load_religions()
    postcode_prefixes = load_postcode_prefixes()  # New - load postcode prefixes
    
    # Sidebar - Filters
    st.sidebar.title("England Schools Dashboard")
    st.sidebar.caption(f"Data from Get Information about Schools service")
    st.sidebar.caption(f"Last updated: {metadata['last_updated']}")
    
    st.sidebar.header("Filters")
    
    # School name
    name_filter = st.sidebar.text_input("School Name", value=st.session_state.filters['name'])
    
    # Show similar school suggestions
    if name_filter and len(name_filter) >= 3:
        similar_schools = find_similar_schools(name_filter)
        if similar_schools:
            st.sidebar.caption("Similar school names:")
            for school in similar_schools:
                if school.lower() != name_filter.lower():
                    st.sidebar.caption(f"• {school}")
    
    # Trust name
    trust_filter = st.sidebar.text_input("Trust Name", value=st.session_state.filters['trust_name'])
    
    # Show similar trust suggestions
    if trust_filter and len(trust_filter) >= 3:
        similar_trusts = find_similar_trusts(trust_filter)
        if similar_trusts:
            st.sidebar.caption("Similar trust names:")
            for trust in similar_trusts:
                if trust.lower() != trust_filter.lower():
                    st.sidebar.caption(f"• {trust}")
    
    # Dropdown filters
    la_options = [""] + local_authorities["LA (name)"].tolist()
    la_filter = st.sidebar.selectbox("Local Authority", la_options, index=la_options.index(st.session_state.filters['la']) if st.session_state.filters['la'] in la_options else 0)
    
    # Changed from school types to establishment groups with multiselect
    group_options = establishment_groups["EstablishmentTypeGroup (name)"].tolist()
    group_filter = st.sidebar.multiselect("Establishment Type Group", group_options, default=st.session_state.filters['establishment_groups'])
    
    phase_options = [""] + phases["PhaseOfEducation (name)"].tolist()
    phase_filter = st.sidebar.selectbox("Phase of Education", phase_options, index=phase_options.index(st.session_state.filters['phase']) if st.session_state.filters['phase'] in phase_options else 0)
    
    # Changed from postcode to postcode prefix with dropdown and custom input
    postcode_prefix_options = [""] + postcode_prefixes["PostcodePrefix"].tolist()
    postcode_prefix_filter = st.sidebar.selectbox(
        "Postcode Prefix", 
        postcode_prefix_options, 
        index=postcode_prefix_options.index(st.session_state.filters['postcode_prefix']) if st.session_state.filters['postcode_prefix'] in postcode_prefix_options else 0
    )
    
    # Custom postcode prefix input
    custom_postcode = st.sidebar.text_input("Or enter custom postcode prefix:", "")
    if custom_postcode:
        postcode_prefix_filter = custom_postcode
    
    gender_options = [""] + genders["Gender (name)"].tolist()
    gender_filter = st.sidebar.selectbox("Gender", gender_options, index=gender_options.index(st.session_state.filters['gender']) if st.session_state.filters['gender'] in gender_options else 0)
    
    religion_options = [""] + religions["ReligiousCharacter (name)"].tolist()
    religion_filter = st.sidebar.selectbox("Religious Character", religion_options, index=religion_options.index(st.session_state.filters['religion']) if st.session_state.filters['religion'] in religion_options else 0)
    
    # Show all results option
    show_all_results = st.sidebar.checkbox("Show all results on one page", value=st.session_state.show_all)
    
    # Apply filters button
    if st.sidebar.button("Apply Filters"):
        st.session_state.filters = {
            'name': name_filter,
            'trust_name': trust_filter,
            'la': la_filter,
            'establishment_groups': group_filter,  # Changed from school_types to establishment_groups
            'phase': phase_filter,
            'postcode_prefix': postcode_prefix_filter,  # Changed from postcode to postcode_prefix
            'gender': gender_filter,
            'religion': religion_filter,
            'chart_filters': st.session_state.filters.get('chart_filters', {
                'school_type': '',
                'phase': '',
                'gender': '',
                'religion': ''
            })
        }
        # Reset pagination when filters change
        st.session_state.page = 1
        st.session_state.show_all = show_all_results
        st.session_state.selected_school = None
        st.session_state.viewing_trust = None
        
    # Reset filters button
    if st.sidebar.button("Reset Filters"):
        st.session_state.filters = {
            'name': '',
            'trust_name': '',
            'la': '',
            'establishment_groups': [],  # Changed from school_types to establishment_groups
            'phase': '',
            'postcode_prefix': '',  # Changed from postcode to postcode_prefix
            'gender': '',
            'religion': '',
            'chart_filters': {
                'school_type': '',
                'phase': '',
                'gender': '',
                'religion': ''
            }
        }
        # Reset pagination when filters change
        st.session_state.page = 1
        st.session_state.show_all = False
        st.session_state.selected_school = None
        st.session_state.viewing_trust = None
        # Rerun to update the UI
        st.rerun()
    
    # Main content
    st.title("England Schools Dashboard")
    
    # Get current filters
    current_filters = st.session_state.filters
    
    # If viewing a specific trust, show that instead of the regular dashboard
    if st.session_state.viewing_trust:
        trust_name = st.session_state.viewing_trust
        trust_schools = get_trust_schools(trust_name)
        
        st.header(f"Schools in {trust_name}")
        st.write(f"Total schools: {len(trust_schools)}")
        
        if st.button("Clear Trust View"):
            st.session_state.viewing_trust = None
            st.rerun()
        
        # Display trust schools
        if not trust_schools.empty:
            # Create a DataFrame with only the columns we want to display
            display_df = trust_schools[['URN', 'EstablishmentName', 'LA (name)', 'EstablishmentTypeGroup (name)', 'PhaseOfEducation (name)', 'Postcode']]
            display_df.columns = ['URN', 'School Name', 'Local Authority', 'Type Group', 'Phase', 'Postcode']
            
            # Add download button
            csv = display_df.to_csv(index=False)
            
            st.download_button(
                label=f"Download {trust_name} Schools as CSV",
                data=csv,
                file_name=f"{trust_name.replace(' ', '_')}_schools.csv",
                mime="text/csv",
                help="Download the trust schools as a CSV file"
            )
            
            # Display the table
            st.dataframe(
                display_df, 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(f"No schools found for trust: {trust_name}")
        
        return
    
    # If a school is selected, show its details
    if st.session_state.selected_school:
        school_urn = st.session_state.selected_school
        school_data = get_school_by_urn(school_urn)
        
        if not school_data.empty:
            school = school_data.iloc[0]
            
            st.header(school['EstablishmentName'])
            st.subheader(f"{school['TypeOfEstablishment (name)']} • {school['PhaseOfEducation (name)']}")
            
            if st.button("Back to School List"):
                st.session_state.selected_school = None
                st.rerun()
            
            # If school has a trust, add button to view all schools in that trust
            if not pd.isna(school['Trusts (name)']) and school['Trusts (name)'] != '':
                if st.button(f"View All Schools in {school['Trusts (name)']}"):
                    st.session_state.viewing_trust = school['Trusts (name)']
                    st.rerun()
            
            # Create tabs for different sections of school information
            tabs = st.tabs(["Basic Info", "Contact Info", "Statistics", "Administrative", "School Infographic"])
            
            with tabs[0]:  # Basic Info
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### School Details")
                    st.write(f"**URN:** {school['URN']}")
                    st.write(f"**Establishment Type:** {school['TypeOfEstablishment (name)']}")
                    st.write(f"**Phase of Education:** {school['PhaseOfEducation (name)']}")
                    st.write(f"**Gender:** {school['Gender (name)']}")
                    st.write(f"**Religious Character:** {school['ReligiousCharacter (name)']}")
                
                with col2:
                    st.markdown("### Location")
                    st.write(f"**Address:** {school['Street']}, {school['Town']}")
                    st.write(f"**Postcode:** {school['Postcode']}")
                    st.write(f"**Local Authority:** {school['LA (name)']}")
                    st.write(f"**Region:** {school['GOR (name)']}")
            
            with tabs[1]:  # Contact Info
                st.markdown("### Contact Information")
                st.write(f"**Phone:** {school['TelephoneNum']}")
                st.write(f"**Website:** {school['SchoolWebsite']}")
                st.write(f"**Email:** {school['Email']}")
                
                st.markdown("### Head Teacher")
                head_name = f"{school['HeadFirstName']} {school['HeadLastName']}"
                st.write(f"**Name:** {head_name}")
                st.write(f"**Title:** {school['HeadPreferredJobTitle']}")
            
            with tabs[2]:  # Statistics
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Pupil Statistics")
                    st.write(f"**Number of Pupils:** {school['NumberOfPupils']}")
                    st.write(f"**School Capacity:** {school['SchoolCapacity']}")
                    
                    # Calculate utilization
                    try:
                        capacity = float(school['SchoolCapacity']) if not pd.isna(school['SchoolCapacity']) else 0
                        pupils = float(school['NumberOfPupils']) if not pd.isna(school['NumberOfPupils']) else 0
                        if capacity > 0:
                            utilization = (pupils / capacity) * 100
                            st.write(f"**Utilization:** {utilization:.1f}%")
                    except:
                        st.write("**Utilization:** N/A")
                    
                    st.write(f"**Free School Meals %:** {school['PercentageFSM']}%")
                
                with col2:
                    st.markdown("### Age Range")
                    st.write(f"**Statutory Low Age:** {school['StatutoryLowAge']}")
                    st.write(f"**Statutory High Age:** {school['StatutoryHighAge']}")
                    
                    st.markdown("### Admissions")
                    st.write(f"**Admissions Policy:** {school['AdmissionsPolicy (name)']}")
            
            with tabs[3]:  # Administrative
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Administrative Details")
                    st.write(f"**Establishment Status:** {school['EstablishmentStatus (name)']}")
                    st.write(f"**Establishment Type Group:** {school['EstablishmentTypeGroup (name)']}")
                    st.write(f"**Establishment Number:** {school['EstablishmentNumber']}")
                    st.write(f"**UKPRN:** {school['UKPRN']}")
                
                with col2:
                    st.markdown("### Trust Information")
                    if not pd.isna(school['Trusts (name)']) and school['Trusts (name)'] != '':
                        st.write(f"**Trust:** {school['Trusts (name)']}")
                        st.write(f"**Trust UID:** {school['Trusts (code)']}")
                    else:
                        st.write("This school is not part of a trust.")
            
            with tabs[4]:  # School Infographic
                # Generate the infographic HTML
                infographic_html = create_infographic_html(school)
                
                # Display the infographic in an iframe
                st.components.v1.html(infographic_html, height=650, scrolling=True)
        else:
            st.error(f"School with URN {school_urn} not found.")
            st.session_state.selected_school = None
        
        return
    
    # Summary statistics
    st.header("Summary Statistics")
    
    # Get total count
    _, total_count = search_schools(
        name=current_filters['name'],
        trust_name=current_filters['trust_name'],
        la=current_filters['la'],
        establishment_groups=current_filters['establishment_groups'],  # Changed from school_types to establishment_groups
        phase=current_filters['phase'],
        postcode_prefix=current_filters['postcode_prefix'],  # Changed from postcode to postcode_prefix
        gender=current_filters['gender'],
        religion=current_filters['religion'],
        page=1,
        per_page=1
    )
    
    st.metric("Total Schools Matching Criteria", f"{total_count:,}")
    
    # Charts
    st.header("School Distribution")
    
    # Load summary data for charts based on current filters
    school_types_data = load_school_types(current_filters)
    phase_data = load_phase_summary(current_filters)
    religion_data = load_religion_summary(current_filters)
    gender_data = load_gender_summary(current_filters)
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        # School Types Chart
        fig_types = px.bar(
            school_types_data, 
            x='EstablishmentTypeGroup', 
            y='Count',
            title='Schools by Establishment Type Group',
            labels={'EstablishmentTypeGroup': 'Establishment Type Group', 'Count': 'Number of Schools'},
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig_types.update_layout(height=400)
        st.plotly_chart(fig_types, use_container_width=True)
        
        # Add filter selector below chart
        selected_type = st.selectbox(
            "Filter by Establishment Type Group",
            [""] + school_types_data['EstablishmentTypeGroup'].tolist(),
            index=0
        )
        
        if selected_type and selected_type != st.session_state.filters['chart_filters']['school_type']:
            st.session_state.filters['chart_filters']['school_type'] = selected_type
            # Update establishment_groups filter with the selected type
            if selected_type:
                st.session_state.filters['establishment_groups'] = [selected_type]
                st.rerun()
        
        # Phase of Education Chart
        fig_phase = px.pie(
            phase_data, 
            values='Count', 
            names='PhaseOfEducation',
            title='Schools by Phase of Education',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_phase.update_layout(height=400)
        st.plotly_chart(fig_phase, use_container_width=True)
        
        # Add filter selector below chart
        selected_phase = st.selectbox(
            "Filter by Phase of Education",
            [""] + phase_data['PhaseOfEducation'].tolist(),
            index=0
        )
        
        if selected_phase and selected_phase != st.session_state.filters['chart_filters']['phase']:
            st.session_state.filters['chart_filters']['phase'] = selected_phase
            # Update phase filter with the selected phase
            if selected_phase:
                st.session_state.filters['phase'] = selected_phase
                st.rerun()
    
    with col2:
        # Religious Character Chart
        fig_religion = px.bar(
            religion_data, 
            x='ReligiousCharacter', 
            y='Count',
            title='Schools by Religious Character',
            labels={'ReligiousCharacter': 'Religious Character', 'Count': 'Number of Schools'},
            color='Count',
            color_continuous_scale='Viridis'
        )
        fig_religion.update_layout(height=400)
        st.plotly_chart(fig_religion, use_container_width=True)
        
        # Add filter selector below chart
        selected_religion = st.selectbox(
            "Filter by Religious Character",
            [""] + religion_data['ReligiousCharacter'].tolist(),
            index=0
        )
        
        if selected_religion and selected_religion != st.session_state.filters['chart_filters']['religion']:
            st.session_state.filters['chart_filters']['religion'] = selected_religion
            # Update religion filter with the selected religion
            if selected_religion:
                st.session_state.filters['religion'] = selected_religion
                st.rerun()
        
        # Gender Chart
        fig_gender = px.pie(
            gender_data, 
            values='Count', 
            names='Gender',
            title='Schools by Gender',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_gender.update_layout(height=400)
        st.plotly_chart(fig_gender, use_container_width=True)
        
        # Add filter selector below chart
        selected_gender = st.selectbox(
            "Filter by Gender",
            [""] + gender_data['Gender'].tolist(),
            index=0
        )
        
        if selected_gender and selected_gender != st.session_state.filters['chart_filters']['gender']:
            st.session_state.filters['chart_filters']['gender'] = selected_gender
            # Update gender filter with the selected gender
            if selected_gender:
                st.session_state.filters['gender'] = selected_gender
                st.rerun()
    
    # School list
    st.header("School List")
    
    # Pagination
    page = st.session_state.page
    per_page = 50
    
    # Search schools with all filters
    schools, total_count = search_schools(
        name=current_filters['name'],
        trust_name=current_filters['trust_name'],
        la=current_filters['la'],
        establishment_groups=current_filters['establishment_groups'],  # Changed from school_types to establishment_groups
        phase=current_filters['phase'],
        postcode_prefix=current_filters['postcode_prefix'],  # Changed from postcode to postcode_prefix
        gender=current_filters['gender'],
        religion=current_filters['religion'],
        page=page,
        per_page=per_page,
        show_all=st.session_state.show_all
    )
    
    # Pagination controls
    total_pages = max(1, (total_count + per_page - 1) // per_page)
    
    if not st.session_state.show_all:
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if st.button("Previous Page", disabled=(page <= 1)):
                st.session_state.page = page - 1
                st.rerun()
        
        with col2:
            st.write(f"Page {page} of {total_pages} (Showing {len(schools)} of {total_count} schools)")
        
        with col3:
            if st.button("Next Page", disabled=(page >= total_pages)):
                st.session_state.page = page + 1
                st.rerun()
    else:
        st.write(f"Showing all {total_count} schools matching your criteria")
    
    # Display schools
    if not schools.empty:
        # Create a DataFrame with only the columns we want to display
        display_df = schools[['URN', 'EstablishmentName', 'LA (name)', 'EstablishmentTypeGroup (name)', 'PhaseOfEducation (name)', 'Gender (name)', 'ReligiousCharacter (name)', 'Trusts (name)', 'Postcode']]
        display_df.columns = ['URN', 'School Name', 'Local Authority', 'Type Group', 'Phase', 'Gender', 'Religious Character', 'Trust', 'Postcode']
        
        # Add download button
        csv = display_df.to_csv(index=False)
        
        # Create a descriptive filename based on filters
        filename_parts = ["schools"]
        if current_filters['name']:
            filename_parts.append(f"name_{current_filters['name'].replace(' ', '_')}")
        if current_filters['trust_name']:
            filename_parts.append(f"trust_{current_filters['trust_name'].replace(' ', '_')}")
        if current_filters['la']:
            filename_parts.append(f"la_{current_filters['la'].replace(' ', '_')}")
        if current_filters['establishment_groups']:  # Changed from school_types to establishment_groups
            filename_parts.append(f"type_{current_filters['establishment_groups'][0].replace(' ', '_')}")
        if current_filters['phase']:
            filename_parts.append(current_filters['phase'].replace(' ', '_'))
        if current_filters['postcode_prefix']:  # Changed from postcode to postcode_prefix
            filename_parts.append(f"postcode_{current_filters['postcode_prefix'].replace(' ', '_')}")
        
        filename = "_".join(filename_parts) + ".csv"
        
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name=filename,
            mime="text/csv",
            help="Download the current search results as a CSV file"
        )
        
        # Display the table
        st.dataframe(
            display_df, 
            use_container_width=True,
            hide_index=True
        )
        
        # Add clickable links to view school details
        st.write("Click on a school's URN to view detailed information:")
        
        # Create columns for the clickable URNs
        cols = st.columns(5)
        for i, (_, row) in enumerate(schools.iterrows()):
            col_idx = i % 5
            if cols[col_idx].button(f"{row['URN']} - {row['EstablishmentName']}", key=f"school_{row['URN']}"):
                st.session_state.selected_school = row['URN']
                st.rerun()
    else:
        st.info("No schools found matching your criteria. Try adjusting your filters.")
    
    # Footer
    st.markdown("---")
    st.caption("Data source: Get Information about Schools service - [https://get-information-schools.service.gov.uk/](https://get-information-schools.service.gov.uk/)")

if __name__ == "__main__":
    main()
