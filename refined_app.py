import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
from fuzzywuzzy import process, fuzz

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
        
        if filters.get('school_types') and len(filters["school_types"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["school_types"]])
            query += f' AND "TypeOfEstablishment (name)" IN ({placeholders})'
            params.extend(filters["school_types"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        if filters.get('postcode'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode"]}%')
            
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
        
        if filters.get('school_types') and len(filters["school_types"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["school_types"]])
            query += f' AND "TypeOfEstablishment (name)" IN ({placeholders})'
            params.extend(filters["school_types"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        if filters.get('postcode'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode"]}%')
            
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
        
        if filters.get('school_types') and len(filters["school_types"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["school_types"]])
            query += f' AND "TypeOfEstablishment (name)" IN ({placeholders})'
            params.extend(filters["school_types"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        if filters.get('postcode'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode"]}%')
            
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
        
        if filters.get('school_types') and len(filters["school_types"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["school_types"]])
            query += f' AND "TypeOfEstablishment (name)" IN ({placeholders})'
            params.extend(filters["school_types"])
        
        if filters.get('phase'):
            query += ' AND "PhaseOfEducation (name)" = ?'
            params.append(filters["phase"])
        
        if filters.get('postcode'):
            query += ' AND Postcode LIKE ?'
            params.append(f'{filters["postcode"]}%')
            
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
def load_establishment_types():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"TypeOfEstablishment (name)\" FROM schools WHERE \"TypeOfEstablishment (name)\" != 'Unknown' ORDER BY \"TypeOfEstablishment (name)\"", conn)

@st.cache_data
def load_phases():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"PhaseOfEducation (name)\" FROM schools WHERE \"PhaseOfEducation (name)\" != 'Unknown' ORDER BY \"PhaseOfEducation (name)\"", conn)

@st.cache_data
def load_trusts():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"Trusts (name)\" FROM schools WHERE \"Trusts (name)\" != 'Unknown' ORDER BY \"Trusts (name)\"", conn)

@st.cache_data
def load_genders():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"Gender (name)\" FROM schools WHERE \"Gender (name)\" != 'Unknown' ORDER BY \"Gender (name)\"", conn)

@st.cache_data
def load_religions():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"ReligiousCharacter (name)\" FROM schools WHERE \"ReligiousCharacter (name)\" != 'Unknown' ORDER BY \"ReligiousCharacter (name)\"", conn)

@st.cache_data
def load_all_school_names():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT EstablishmentName FROM schools ORDER BY EstablishmentName", conn)

@st.cache_data
def load_all_trust_names():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"Trusts (name)\" FROM schools WHERE \"Trusts (name)\" != 'Unknown' ORDER BY \"Trusts (name)\"", conn)

def fuzzy_search_schools(search_term, all_schools, limit=10, threshold=70):
    """Perform fuzzy search on school names"""
    if not search_term:
        return []
    
    # Get all school names as a list
    school_names = all_schools['EstablishmentName'].tolist()
    
    # Use process.extract to find the best matches
    matches = process.extract(search_term, school_names, 
                             scorer=fuzz.token_sort_ratio, 
                             limit=limit)
    
    # Filter matches by threshold
    filtered_matches = [match[0] for match in matches if match[1] >= threshold]
    
    return filtered_matches

def fuzzy_search_trusts(search_term, all_trusts, limit=10, threshold=70):
    """Perform fuzzy search on trust names"""
    if not search_term:
        return []
    
    # Get all trust names as a list
    trust_names = all_trusts['Trusts (name)'].tolist()
    
    # Use process.extract to find the best matches
    matches = process.extract(search_term, trust_names, 
                             scorer=fuzz.token_sort_ratio, 
                             limit=limit)
    
    # Filter matches by threshold
    filtered_matches = [match[0] for match in matches if match[1] >= threshold]
    
    return filtered_matches

@st.cache_data
def search_schools(name="", trust_name="", la="", school_types=None, phase="", postcode="", gender="", religion="", show_all=False, page=1, per_page=20):
    conn = get_connection()
    
    # Build query
    query = 'SELECT * FROM schools WHERE 1=1'
    params = []
    
    if name:
        # For fuzzy search, we'll get the results from Python after querying
        # But still add a basic filter to reduce initial result set
        query += ' AND EstablishmentName LIKE ?'
        params.append(f'%{name}%')
    
    if trust_name:
        # For fuzzy search, we'll get the results from Python after querying
        # But still add a basic filter to reduce initial result set
        query += ' AND "Trusts (name)" LIKE ?'
        params.append(f'%{trust_name}%')
    
    if la:
        query += ' AND "LA (name)" = ?'
        params.append(la)
    
    if school_types and len(school_types) > 0:
        placeholders = ', '.join(['?' for _ in school_types])
        query += f' AND "TypeOfEstablishment (name)" IN ({placeholders})'
        params.extend(school_types)
    
    if phase:
        query += ' AND "PhaseOfEducation (name)" = ?'
        params.append(phase)
    
    if postcode:
        query += ' AND Postcode LIKE ?'
        params.append(f'{postcode}%')
        
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
    
    # Add pagination if not showing all results
    if not show_all:
        query += ' LIMIT ? OFFSET ?'
        params.append(per_page)
        params.append((page - 1) * per_page)
    
    # Execute query
    schools = pd.read_sql(query, conn, params=params)
    
    # Apply fuzzy search filtering if needed
    if name and len(schools) > 0:
        # Get fuzzy matches
        all_schools = pd.DataFrame({'EstablishmentName': schools['EstablishmentName'].unique()})
        fuzzy_matches = fuzzy_search_schools(name, all_schools, limit=100, threshold=60)
        
        # Filter the results to only include fuzzy matches
        if fuzzy_matches:
            schools = schools[schools['EstablishmentName'].isin(fuzzy_matches)]
    
    if trust_name and len(schools) > 0:
        # Get fuzzy matches
        all_trusts = pd.DataFrame({'Trusts (name)': schools['Trusts (name)'].unique()})
        fuzzy_matches = fuzzy_search_trusts(trust_name, all_trusts, limit=100, threshold=60)
        
        # Filter the results to only include fuzzy matches
        if fuzzy_matches:
            schools = schools[schools['Trusts (name)'].isin(fuzzy_matches)]
    
    return schools, total_count

@st.cache_data
def get_school_details(urn):
    conn = get_connection()
    query = "SELECT * FROM schools WHERE URN = ?"
    return pd.read_sql(query, conn, params=[urn])

@st.cache_data
def get_trust_schools(trust_name):
    conn = get_connection()
    query = "SELECT * FROM schools WHERE \"Trusts (name)\" = ?"
    return pd.read_sql(query, conn, params=[trust_name])

# Load summary statistics
@st.cache_data
def load_summary_stats(filters=None):
    conn = get_connection()
    
    # Base queries
    total_query = "SELECT COUNT(*) as count FROM schools WHERE 1=1"
    primary_query = "SELECT COUNT(*) as count FROM schools WHERE \"PhaseOfEducation (name)\" = 'Primary'"
    secondary_query = "SELECT COUNT(*) as count FROM schools WHERE \"PhaseOfEducation (name)\" = 'Secondary'"
    
    params_total = []
    params_primary = []
    params_secondary = []
    
    # Add filters if provided
    if filters:
        if filters.get('name'):
            filter_clause = ' AND EstablishmentName LIKE ?'
            total_query += filter_clause
            primary_query += filter_clause
            secondary_query += filter_clause
            params_total.append(f'%{filters["name"]}%')
            params_primary.append(f'%{filters["name"]}%')
            params_secondary.append(f'%{filters["name"]}%')
            
        if filters.get('trust_name'):
            filter_clause = ' AND "Trusts (name)" LIKE ?'
            total_query += filter_clause
            primary_query += filter_clause
            secondary_query += filter_clause
            params_total.append(f'%{filters["trust_name"]}%')
            params_primary.append(f'%{filters["trust_name"]}%')
            params_secondary.append(f'%{filters["trust_name"]}%')
        
        if filters.get('la'):
            filter_clause = ' AND "LA (name)" = ?'
            total_query += filter_clause
            primary_query += filter_clause
            secondary_query += filter_clause
            params_total.append(filters["la"])
            params_primary.append(filters["la"])
            params_secondary.append(filters["la"])
        
        if filters.get('school_types') and len(filters["school_types"]) > 0:
            placeholders = ', '.join(['?' for _ in filters["school_types"]])
            filter_clause = f' AND "TypeOfEstablishment (name)" IN ({placeholders})'
            total_query += filter_clause
            primary_query += filter_clause
            secondary_query += filter_clause
            params_total.extend(filters["school_types"])
            params_primary.extend(filters["school_types"])
            params_secondary.extend(filters["school_types"])
        
        if filters.get('phase'):
            filter_clause = ' AND "PhaseOfEducation (name)" = ?'
            total_query += filter_clause
            # Don't add to primary/secondary as they already have phase filters
            params_total.append(filters["phase"])
        
        if filters.get('postcode'):
            filter_clause = ' AND Postcode LIKE ?'
            total_query += filter_clause
            primary_query += filter_clause
            secondary_query += filter_clause
            params_total.append(f'{filters["postcode"]}%')
            params_primary.append(f'{filters["postcode"]}%')
            params_secondary.append(f'{filters["postcode"]}%')
            
        if filters.get('gender'):
            filter_clause = ' AND "Gender (name)" = ?'
            total_query += filter_clause
            primary_query += filter_clause
            secondary_query += filter_clause
            params_total.append(filters["gender"])
            params_primary.append(filters["gender"])
            params_secondary.append(filters["gender"])
            
        if filters.get('religion'):
            filter_clause = ' AND "ReligiousCharacter (name)" = ?'
            total_query += filter_clause
            primary_query += filter_clause
            secondary_query += filter_clause
            params_total.append(filters["religion"])
            params_primary.append(filters["religion"])
            params_secondary.append(filters["religion"])
    
    # Execute queries
    total_schools = pd.read_sql(total_query, conn, params=params_total).iloc[0, 0]
    primary_schools = pd.read_sql(primary_query, conn, params=params_primary).iloc[0, 0]
    secondary_schools = pd.read_sql(secondary_query, conn, params=params_secondary).iloc[0, 0]
    
    return {
        "total": total_schools,
        "primary": primary_schools,
        "secondary": secondary_schools
    }

# Create charts
def create_school_types_chart(data):
    fig = px.pie(
        data, 
        values='Count', 
        names='EstablishmentTypeGroup',
        title='School Types Distribution',
        hole=0.4,
    )
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
    fig.update_traces(
        hoverinfo='label+percent+value',
        textinfo='label+value',
        textfont_size=12,
    )
    return fig

def create_phase_chart(data):
    fig = px.bar(
        data, 
        x='PhaseOfEducation', 
        y='Count',
        title='Phase of Education',
        color='PhaseOfEducation',
        labels={'PhaseOfEducation': 'Phase', 'Count': 'Number of Schools'}
    )
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0), xaxis_tickangle=-45)
    return fig

def create_religion_chart(data):
    fig = px.pie(
        data, 
        values='Count', 
        names='ReligiousCharacter',
        title='Religious Character',
        hole=0.4,
    )
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
    fig.update_traces(
        hoverinfo='label+percent+value',
        textinfo='label+value',
        textfont_size=12,
    )
    return fig

def create_gender_chart(data):
    fig = px.pie(
        data, 
        values='Count', 
        names='Gender',
        title='Gender Distribution',
        hole=0.4,
    )
    fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
    fig.update_traces(
        hoverinfo='label+percent+value',
        textinfo='label+value',
        textfont_size=12,
    )
    return fig

# Main app
def main():
    # Initialize session state for filters
    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'name': '',
            'trust_name': '',
            'la': '',
            'school_types': [],
            'phase': '',
            'postcode': '',
            'gender': '',
            'religion': '',
            'show_all': False
        }
    
    # Load data
    metadata = load_metadata()
    local_authorities = load_local_authorities()
    establishment_types = load_establishment_types()
    phases = load_phases()
    trusts = load_trusts()
    genders = load_genders()
    religions = load_religions()
    all_school_names = load_all_school_names()
    all_trust_names = load_all_trust_names()
    
    # Sidebar - Filters
    st.sidebar.title("England Schools Dashboard")
    st.sidebar.caption(f"Data from Get Information about Schools service")
    st.sidebar.caption(f"Last updated: {metadata['last_updated']}")
    
    st.sidebar.header("Filters")
    
    # School name with fuzzy search suggestions
    name_filter = st.sidebar.text_input("School Name", value=st.session_state.filters['name'])
    if name_filter:
        # Show suggestions based on fuzzy search
        suggestions = fuzzy_search_schools(name_filter, all_school_names, limit=5, threshold=60)
        if suggestions:
            selected_suggestion = st.sidebar.selectbox(
                "Did you mean:", 
                [""] + suggestions,
                index=0
            )
            if selected_suggestion:
                name_filter = selected_suggestion
    
    # Trust name with fuzzy search suggestions
    trust_filter = st.sidebar.text_input("Trust Name", value=st.session_state.filters['trust_name'])
    if trust_filter:
        # Show suggestions based on fuzzy search
        suggestions = fuzzy_search_trusts(trust_filter, all_trust_names, limit=5, threshold=60)
        if suggestions:
            selected_suggestion = st.sidebar.selectbox(
                "Did you mean:", 
                [""] + suggestions,
                index=0
            )
            if selected_suggestion:
                trust_filter = selected_suggestion
    
    # Dropdown filters
    la_options = [""] + local_authorities["LA (name)"].tolist()
    la_filter = st.sidebar.selectbox("Local Authority", la_options, index=la_options.index(st.session_state.filters['la']) if st.session_state.filters['la'] in la_options else 0)
    
    # Multiple establishment type selection
    type_options = establishment_types["TypeOfEstablishment (name)"].tolist()
    type_filter = st.sidebar.multiselect("Establishment Type(s)", type_options, default=st.session_state.filters['school_types'])
    
    phase_options = [""] + phases["PhaseOfEducation (name)"].tolist()
    phase_filter = st.sidebar.selectbox("Phase of Education", phase_options, index=phase_options.index(st.session_state.filters['phase']) if st.session_state.filters['phase'] in phase_options else 0)
    
    # Gender filter
    gender_options = [""] + genders["Gender (name)"].tolist()
    gender_filter = st.sidebar.selectbox("Gender", gender_options, index=gender_options.index(st.session_state.filters['gender']) if st.session_state.filters['gender'] in gender_options else 0)
    
    # Religious character filter
    religion_options = [""] + religions["ReligiousCharacter (name)"].tolist()
    religion_filter = st.sidebar.selectbox("Religious Character", religion_options, index=religion_options.index(st.session_state.filters['religion']) if st.session_state.filters['religion'] in religion_options else 0)
    
    postcode_filter = st.sidebar.text_input("Postcode", value=st.session_state.filters['postcode'])
    
    # Show all results option
    show_all_results = st.sidebar.checkbox("Show all results on one page", value=st.session_state.filters['show_all'])
    
    # Apply filters button
    if st.sidebar.button("Apply Filters"):
        st.session_state.filters = {
            'name': name_filter,
            'trust_name': trust_filter,
            'la': la_filter,
            'school_types': type_filter,
            'phase': phase_filter,
            'postcode': postcode_filter,
            'gender': gender_filter,
            'religion': religion_filter,
            'show_all': show_all_results
        }
        # Reset pagination when filters change
        st.session_state.page = 1
        
    # Reset filters button
    if st.sidebar.button("Reset Filters"):
        st.session_state.filters = {
            'name': '',
            'trust_name': '',
            'la': '',
            'school_types': [],
            'phase': '',
            'postcode': '',
            'gender': '',
            'religion': '',
            'show_all': False
        }
        # Reset pagination when filters change
        st.session_state.page = 1
        # Rerun to update the UI
        st.rerun()
    
    # Main content
    st.title("England Schools Dashboard")
    
    # Get current filters
    current_filters = st.session_state.filters
    
    # Load data with current filters
    school_types = load_school_types(current_filters)
    phase_summary = load_phase_summary(current_filters)
    religion_summary = load_religion_summary(current_filters)
    gender_summary = load_gender_summary(current_filters)
    stats = load_summary_stats(current_filters)
    
    # Summary statistics
    st.header("Summary Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Schools", f"{stats['total']:,}")
    
    with col2:
        st.metric("Primary Schools", f"{stats['primary']:,}")
    
    with col3:
        st.metric("Secondary Schools", f"{stats['secondary']:,}")
    
    # Charts
    st.header("School Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # School Types Chart
        school_types_chart = create_school_types_chart(school_types)
        st.plotly_chart(school_types_chart, use_container_width=True)
        
        # Add click functionality for school types
        st.caption("Click on a school type in the chart to filter results")
        selected_type = st.selectbox(
            "Filter by School Type",
            [""] + school_types['EstablishmentTypeGroup'].tolist(),
            index=0
        )
        if selected_type:
            # Find the establishment types that belong to this group
            conn = get_connection()
            matching_types = pd.read_sql(
                'SELECT DISTINCT "TypeOfEstablishment (name)" FROM schools WHERE "EstablishmentTypeGroup (name)" = ?',
                conn,
                params=[selected_type]
            )
            # Update the filters
            if matching_types.shape[0] > 0:
                st.session_state.filters['school_types'] = matching_types["TypeOfEstablishment (name)"].tolist()
                st.rerun()
        
        # Religious Character Chart
        religion_chart = create_religion_chart(religion_summary)
        st.plotly_chart(religion_chart, use_container_width=True)
        
        # Add click functionality for religious character
        st.caption("Click on a religious character in the chart to filter results")
        selected_religion = st.selectbox(
            "Filter by Religious Character",
            [""] + religion_summary['ReligiousCharacter'].tolist(),
            index=0
        )
        if selected_religion:
            # Update the filters
            st.session_state.filters['religion'] = selected_religion
            st.rerun()
    
    with col2:
        # Phase of Education Chart
        phase_chart = create_phase_chart(phase_summary)
        st.plotly_chart(phase_chart, use_container_width=True)
        
        # Add click functionality for phase
        st.caption("Click on a phase in the chart to filter results")
        selected_phase = st.selectbox(
            "Filter by Phase of Education",
            [""] + phase_summary['PhaseOfEducation'].tolist(),
            index=0
        )
        if selected_phase:
            # Update the filters
            st.session_state.filters['phase'] = selected_phase
            st.rerun()
        
        # Gender Chart
        gender_chart = create_gender_chart(gender_summary)
        st.plotly_chart(gender_chart, use_container_width=True)
        
        # Add click functionality for gender
        st.caption("Click on a gender in the chart to filter results")
        selected_gender = st.selectbox(
            "Filter by Gender",
            [""] + gender_summary['Gender'].tolist(),
            index=0
        )
        if selected_gender:
            # Update the filters
            st.session_state.filters['gender'] = selected_gender
            st.rerun()
    
    # School list
    st.header("School List")
    
    # Pagination
    page = st.session_state.get("page", 1)
    per_page = 50  # Increased from 20 to 50
    
    # Search schools with all filters
    schools, total_count = search_schools(
        name=current_filters['name'],
        trust_name=current_filters['trust_name'],
        la=current_filters['la'],
        school_types=current_filters['school_types'],
        phase=current_filters['phase'],
        postcode=current_filters['postcode'],
        gender=current_filters['gender'],
        religion=current_filters['religion'],
        show_all=current_filters['show_all'],
        page=page,
        per_page=per_page
    )
    
    # Pagination controls (only show if not showing all results)
    if not current_filters['show_all']:
        total_pages = max(1, (total_count + per_page - 1) // per_page)
        
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
        st.write(f"Showing all {len(schools)} schools matching your criteria")
    
    # Display schools
    if not schools.empty:
        # Create a DataFrame with only the columns we want to display
        display_df = schools[['URN', 'EstablishmentName', 'LA (name)', 'TypeOfEstablishment (name)', 'PhaseOfEducation (name)', 'Trusts (name)', 'Gender (name)', 'ReligiousCharacter (name)', 'Postcode']]
        display_df.columns = ['URN', 'School Name', 'Local Authority', 'Type', 'Phase', 'Trust', 'Gender', 'Religious Character', 'Postcode']
        
        # Add download button with proper naming
        csv = display_df.to_csv(index=False)
        
        # Create a descriptive filename based on filters
        filename_parts = ["schools"]
        if current_filters['name']:
            filename_parts.append(f"name_{current_filters['name'].replace(' ', '_')}")
        if current_filters['trust_name']:
            filename_parts.append(f"trust_{current_filters['trust_name'].replace(' ', '_')}")
        if current_filters['la']:
            filename_parts.append(f"la_{current_filters['la'].replace(' ', '_')}")
        if current_filters['phase']:
            filename_parts.append(current_filters['phase'].replace(' ', '_'))
        
        filename = "_".join(filename_parts) + ".csv"
        
        col1, col2 = st.columns([3, 1])
        with col2:
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name=filename,
                mime="text/csv",
                help="Download the current search results as a CSV file"
            )
        
        # Display the table with improved formatting
        st.dataframe(
            display_df, 
            use_container_width=True,
            column_config={
                "URN": st.column_config.NumberColumn(format="%d"),
                "School Name": st.column_config.TextColumn(width="large"),
                "Trust": st.column_config.TextColumn(width="large"),
            },
            hide_index=True
        )
        
        # School details
        st.header("School Details")
        selected_urn = st.selectbox("Select a school to view details", schools['URN'].tolist(), format_func=lambda x: schools[schools['URN'] == x]['EstablishmentName'].iloc[0])
        
        if selected_urn:
            school_details = get_school_details(selected_urn).iloc[0]
            
            # Create tabs for different categories of information
            tabs = st.tabs(["Basic Info", "Contact Info", "Statistics", "Administrative"])
            
            with tabs[0]:  # Basic Info tab
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Basic Information")
                    st.write(f"**URN:** {school_details['URN']}")
                    st.write(f"**Name:** {school_details['EstablishmentName']}")
                    st.write(f"**Type:** {school_details['TypeOfEstablishment (name)']}")
                    st.write(f"**Phase:** {school_details['PhaseOfEducation (name)']}")
                    st.write(f"**Local Authority:** {school_details['LA (name)']}")
                    st.write(f"**Establishment Group:** {school_details['EstablishmentTypeGroup (name)']}")
                    st.write(f"**Gender:** {school_details['Gender (name)']}")
                    st.write(f"**Religious Character:** {school_details['ReligiousCharacter (name)']}")
            
            with tabs[1]:  # Contact Info tab
                st.subheader("Contact Information")
                st.write(f"**Address:** {school_details['FullAddress']}")
                st.write(f"**Postcode:** {school_details['Postcode']}")
                st.write(f"**Telephone:** {school_details['TelephoneNum']}")
                
                website = school_details['SchoolWebsite']
                if website and website != 'Not provided':
                    st.write(f"**Website:** [{website}]({website})")
                else:
                    st.write("**Website:** Not provided")
                
                st.write(f"**Head Teacher:** {school_details['HeadTeacherFullName']}")
                st.write(f"**Head Title:** {school_details['HeadPreferredJobTitle']}")
            
            with tabs[2]:  # Statistics tab
                st.subheader("School Statistics")
                st.write(f"**School Capacity:** {int(school_details['SchoolCapacity'])}")
                st.write(f"**Number of Pupils:** {int(school_details['NumberOfPupils'])}")
                st.write(f"**Percentage FSM:** {school_details['PercentageFSM']}%")
                st.write(f"**Statutory Low Age:** {int(school_details['StatutoryLowAge'])}")
                st.write(f"**Statutory High Age:** {int(school_details['StatutoryHighAge'])}")
                st.write(f"**Nursery Provision:** {school_details['NurseryProvision (name)']}")
                st.write(f"**Official Sixth Form:** {school_details['OfficialSixthForm (name)']}")
            
            with tabs[3]:  # Administrative tab
                st.subheader("Administrative Information")
                trust_name = school_details['Trusts (name)']
                st.write(f"**Trust:** {trust_name}")
                
                # Add button to view all schools in this trust
                if trust_name != 'Unknown':
                    if st.button(f"View All Schools in {trust_name}"):
                        st.session_state.view_trust = trust_name
                        st.rerun()
                
                st.write(f"**Federation:** {school_details['Federations (name)']}")
                st.write(f"**District:** {school_details['DistrictAdministrative (name)']}")
                st.write(f"**Ward:** {school_details['AdministrativeWard (name)']}")
                st.write(f"**Parliamentary Constituency:** {school_details['ParliamentaryConstituency (name)']}")
                st.write(f"**Urban/Rural:** {school_details['UrbanRural (name)']}")
    else:
        st.info("No schools found matching your criteria. Try adjusting your filters.")
    
    # View all schools in a trust if requested
    if hasattr(st.session_state, 'view_trust'):
        trust_name = st.session_state.view_trust
        st.header(f"All Schools in {trust_name}")
        
        # Get all schools in this trust
        trust_schools = get_trust_schools(trust_name)
        
        if not trust_schools.empty:
            # Create a DataFrame with only the columns we want to display
            trust_display_df = trust_schools[['URN', 'EstablishmentName', 'LA (name)', 'TypeOfEstablishment (name)', 'PhaseOfEducation (name)', 'Gender (name)', 'ReligiousCharacter (name)', 'Postcode']]
            trust_display_df.columns = ['URN', 'School Name', 'Local Authority', 'Type', 'Phase', 'Gender', 'Religious Character', 'Postcode']
            
            # Add download button for trust schools
            csv = trust_display_df.to_csv(index=False)
            filename = f"schools_in_{trust_name.replace(' ', '_')}.csv"
            
            col1, col2 = st.columns([3, 1])
            with col2:
                st.download_button(
                    label="Download Trust Schools as CSV",
                    data=csv,
                    file_name=filename,
                    mime="text/csv",
                    help="Download all schools in this trust as a CSV file"
                )
            
            # Display the table
            st.dataframe(
                trust_display_df, 
                use_container_width=True,
                column_config={
                    "URN": st.column_config.NumberColumn(format="%d"),
                    "School Name": st.column_config.TextColumn(width="large"),
                },
                hide_index=True
            )
            
            # Add button to clear trust view
            if st.button("Clear Trust View"):
                del st.session_state.view_trust
                st.rerun()
        else:
            st.info(f"No schools found for trust: {trust_name}")
    
    # Footer
    st.markdown("---")
    st.caption("Data source: Get Information about Schools service - [https://get-information-schools.service.gov.uk/](https://get-information-schools.service.gov.uk/)")

if __name__ == "__main__":
    main()
