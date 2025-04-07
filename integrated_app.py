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

def find_similar_schools(search_term, all_schools, limit=5):
    """Find similar school names using simple string matching"""
    if not search_term:
        return []
    
    search_term = search_term.lower()
    
    # Get all school names as a list
    school_names = all_schools['EstablishmentName'].tolist()
    
    # Find schools that contain the search term
    matches = [name for name in school_names if search_term in name.lower()]
    
    # If we don't have enough matches, try more flexible matching
    if len(matches) < limit:
        # Split search term into words
        search_words = search_term.split()
        
        # Find schools that contain any of the search words
        for word in search_words:
            if len(word) > 2:  # Only use words with more than 2 characters
                word_matches = [name for name in school_names if word in name.lower()]
                for match in word_matches:
                    if match not in matches:
                        matches.append(match)
                        if len(matches) >= limit:
                            break
                if len(matches) >= limit:
                    break
    
    return matches[:limit]

def find_similar_trusts(search_term, all_trusts, limit=5):
    """Find similar trust names using simple string matching"""
    if not search_term:
        return []
    
    search_term = search_term.lower()
    
    # Get all trust names as a list
    trust_names = all_trusts['Trusts (name)'].tolist()
    
    # Find trusts that contain the search term
    matches = [name for name in trust_names if search_term in name.lower()]
    
    # If we don't have enough matches, try more flexible matching
    if len(matches) < limit:
        # Split search term into words
        search_words = search_term.split()
        
        # Find trusts that contain any of the search words
        for word in search_words:
            if len(word) > 2:  # Only use words with more than 2 characters
                word_matches = [name for name in trust_names if word in name.lower()]
                for match in word_matches:
                    if match not in matches:
                        matches.append(match)
                        if len(matches) >= limit:
                            break
                if len(matches) >= limit:
                    break
    
    return matches[:limit]

@st.cache_data
def search_schools(name="", trust_name="", la="", school_types=None, phase="", postcode="", gender="", religion="", show_all=False, page=1, per_page=20):
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

# Infographic Generator HTML
def get_infographic_html():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>School Infographic Generator</title>
        <style>
            /* Apple-inspired styling */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            }
            
            body {
                background-color: #f5f5f7;
                color: #1d1d1f;
                line-height: 1.5;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .infographic {
                background-color: white;
                border-radius: 20px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
                padding: 40px;
                margin-bottom: 30px;
                overflow: hidden;
            }
            
            .infographic-header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .school-name {
                font-size: 32px;
                font-weight: 600;
                margin-bottom: 10px;
                color: #1d1d1f;
            }
            
            .school-details {
                font-size: 16px;
                color: #86868b;
                margin-bottom: 5px;
            }
            
            .rating-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 30px 0;
            }
            
            .rating-circle {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: white;
                font-weight: 600;
                background: linear-gradient(135deg, #42a1ec, #0070c9);
                box-shadow: 0 4px 15px rgba(0, 112, 201, 0.2);
            }
            
            .rating-label {
                font-size: 14px;
                margin-bottom: 5px;
            }
            
            .rating-value {
                font-size: 28px;
            }
            
            .metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            
            .metric-card {
                background-color: #f5f5f7;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            }
            
            .metric-title {
                font-size: 14px;
                color: #86868b;
                margin-bottom: 10px;
            }
            
            .metric-value {
                font-size: 24px;
                font-weight: 600;
                color: #1d1d1f;
            }
            
            .section-title {
                font-size: 20px;
                font-weight: 600;
                margin: 30px 0 15px;
                color: #1d1d1f;
            }
            
            .highlights-container {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            
            .highlight-card {
                background-color: #f5f5f7;
                border-radius: 12px;
                padding: 20px;
            }
            
            .highlight-title {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 10px;
                color: #1d1d1f;
            }
            
            .highlight-list {
                list-style-type: none;
            }
            
            .highlight-item {
                margin-bottom: 10px;
                font-size: 14px;
                color: #515154;
                position: relative;
                padding-left: 20px;
            }
            
            .highlight-item:before {
                content: "•";
                color: #0070c9;
                font-size: 18px;
                position: absolute;
                left: 0;
                top: -2px;
            }
            
            .footer {
                text-align: center;
                margin-top: 30px;
                font-size: 12px;
                color: #86868b;
            }
            
            .download-btn {
                display: inline-block;
                background: linear-gradient(135deg, #42a1ec, #0070c9);
                color: white;
                font-weight: 600;
                padding: 12px 24px;
                border-radius: 30px;
                text-decoration: none;
                margin-top: 20px;
                box-shadow: 0 4px 10px rgba(0, 112, 201, 0.2);
                transition: all 0.3s ease;
            }
            
            .download-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(0, 112, 201, 0.3);
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .infographic {
                    padding: 20px;
                }
                
                .metrics-grid,
                .highlights-container {
                    grid-template-columns: 1fr;
                }
                
                .school-name {
                    font-size: 24px;
                }
                
                .rating-circle {
                    width: 120px;
                    height: 120px;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div id="infographic" class="infographic">
                <!-- Infographic content will be generated here -->
            </div>
            
            <div style="text-align: center;">
                <button id="downloadBtn" class="download-btn">Download Infographic</button>
            </div>
        </div>

        <!-- Include html2canvas for image generation -->
        <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
        
        <script>
            // Function to generate the infographic based on school data
            function generateInfographic(schoolData) {
                const infographicEl = document.getElementById('infographic');
                
                // Format capacity utilization
                const capacityUtilization = schoolData.numberOfPupils && schoolData.schoolCapacity 
                    ? Math.round((parseInt(schoolData.numberOfPupils) / parseInt(schoolData.schoolCapacity)) * 100) 
                    : 0;
                
                // Determine rating color based on FSM percentage
                let ratingColor = 'linear-gradient(135deg, #42a1ec, #0070c9)'; // Default blue
                let ratingText = 'Average';
                
                const fsmPercentage = parseFloat(schoolData.fsmPercentage) || 0;
                
                if (fsmPercentage > 30) {
                    ratingColor = 'linear-gradient(135deg, #ff5e3a, #ff2d55)'; // Red
                    ratingText = 'High FSM';
                } else if (fsmPercentage > 20) {
                    ratingColor = 'linear-gradient(135deg, #ffcc00, #ff9500)'; // Orange
                    ratingText = 'Medium FSM';
                } else if (fsmPercentage < 10) {
                    ratingColor = 'linear-gradient(135deg, #34c759, #30b94d)'; // Green
                    ratingText = 'Low FSM';
                }
                
                // Build the HTML for the infographic
                const html = `
                    <div class="infographic-header">
                        <h1 class="school-name">${schoolData.name}</h1>
                        <p class="school-details">${schoolData.category || 'School'}</p>
                        <p class="school-details">${schoolData.address || ''}</p>
                        <p class="school-details">URN: ${schoolData.urn || 'N/A'}</p>
                    </div>
                    
                    <div class="rating-container">
                        <div class="rating-circle" style="background: ${ratingColor}">
                            <span class="rating-label">FSM Percentage</span>
                            <span class="rating-value">${fsmPercentage}%</span>
                            <span class="rating-label">${ratingText}</span>
                        </div>
                    </div>
                    
                    <h2 class="section-title">Key Metrics</h2>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <p class="metric-title">School Capacity</p>
                            <p class="metric-value">${schoolData.schoolCapacity || 'N/A'}</p>
                        </div>
                        <div class="metric-card">
                            <p class="metric-title">Number of Pupils</p>
                            <p class="metric-value">${schoolData.numberOfPupils || 'N/A'}</p>
                        </div>
                        <div class="metric-card">
                            <p class="metric-title">Capacity Utilization</p>
                            <p class="metric-value">${capacityUtilization}%</p>
                        </div>
                        <div class="metric-card">
                            <p class="metric-title">FSM Percentage</p>
                            <p class="metric-value">${fsmPercentage}%</p>
                        </div>
                    </div>
                    
                    <div class="highlights-container">
                        <div class="highlight-card">
                            <h3 class="highlight-title">School Information</h3>
                            <ul class="highlight-list">
                                <li class="highlight-item">School Type: ${schoolData.schoolType || 'N/A'}</li>
                                <li class="highlight-item">Phase of Education: ${schoolData.phaseOfEducation || 'N/A'}</li>
                                <li class="highlight-item">Local Authority: ${schoolData.laName || 'N/A'}</li>
                                <li class="highlight-item">Head Teacher: ${schoolData.headTeacher || 'N/A'}</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>Data from Get Information about Schools service</p>
                        <p>Generated on ${new Date().toLocaleDateString()}</p>
                    </div>
                `;
                
                // Set the HTML content
                infographicEl.innerHTML = html;
                
                // Set up download button
                document.getElementById('downloadBtn').addEventListener('click', function() {
                    html2canvas(document.getElementById('infographic')).then(canvas => {
                        const link = document.createElement('a');
                        link.download = `${schoolData.name.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_infographic.png`;
                        link.href = canvas.toDataURL('image/png');
                        link.click();
                    });
                });
            }
            
            // Function to create infographic from external data
            window.createInfographic = function(schoolData) {
                generateInfographic(schoolData);
            };
            
            // Initialize with empty data if none provided
            document.addEventListener('DOMContentLoaded', function() {
                // Check if we're in an iframe
                if (window.location !== window.parent.location) {
                    // We're in an iframe, wait for data from parent
                    console.log('Waiting for data from parent...');
                } else {
                    // We're not in an iframe, show demo data
                    generateInfographic({
                        name: "Example School",
                        urn: "123456",
                        category: "Primary School",
                        address: "123 School Street, City, Postcode",
                        schoolCapacity: "500",
                        numberOfPupils: "450",
                        fsmPercentage: "15.2",
                        schoolType: "Academy",
                        phaseOfEducation: "Primary",
                        headTeacher: "Mrs. Jane Smith",
                        laName: "Local Authority"
                    });
                }
            });
        </script>
    </body>
    </html>
    """

# Function to create an iframe with the infographic generator
def create_infographic_iframe(school_data):
    # Get the HTML content
    html_content = get_infographic_html()
    
    # Create a unique HTML file for this school
    html_file = f"school_infographic_{school_data['urn']}.html"
    
    # Write the HTML content to a file
    with open(html_file, "w") as f:
        f.write(html_content)
    
    # Create JavaScript to send data to the iframe
    js_code = f"""
    <script>
        // Wait for iframe to load
        document.getElementById('infographicFrame').onload = function() {{
            // Send school data to iframe
            const schoolData = {school_data};
            document.getElementById('infographicFrame').contentWindow.createInfographic(schoolData);
        }};
    </script>
    """
    
    # Create iframe HTML
    iframe_html = f"""
    <iframe id="infographicFrame" src="{html_file}" width="100%" height="800px" frameborder="0"></iframe>
    {js_code}
    """
    
    return iframe_html

# Function to create a standalone infographic component
def create_infographic_component(school_details):
    # Convert school details to the format expected by the infographic generator
    school_data = {
        "name": school_details['EstablishmentName'],
        "urn": str(school_details['URN']),
        "category": school_details['TypeOfEstablishment (name)'],
        "address": school_details['FullAddress'],
        "schoolCapacity": str(int(school_details['SchoolCapacity'])),
        "numberOfPupils": str(int(school_details['NumberOfPupils'])),
        "fsmPercentage": str(school_details['PercentageFSM']),
        "schoolType": school_details['EstablishmentTypeGroup (name)'],
        "phaseOfEducation": school_details['PhaseOfEducation (name)'],
        "headTeacher": school_details['HeadTeacherFullName'],
        "laName": school_details['LA (name)']
    }
    
    # Convert the school data to a JSON string for JavaScript
    school_data_json = str(school_data).replace("'", '"')
    
    # Get the HTML content
    html_content = get_infographic_html()
    
    # Create a unique filename for this school
    html_filename = f"/tmp/school_infographic_{school_data['urn']}.html"
    
    # Write the HTML content to a file
    with open(html_filename, "w") as f:
        f.write(html_content)
    
    # Create JavaScript to initialize the infographic with school data
    js_code = f"""
    <script>
        // Wait for iframe to load
        document.getElementById('infographicFrame').onload = function() {{
            // Send school data to iframe
            const schoolData = {school_data_json};
            document.getElementById('infographicFrame').contentWindow.createInfographic(schoolData);
        }};
    </script>
    """
    
    # Create iframe HTML
    iframe_html = f"""
    <div style="width:100%; height:800px; overflow:hidden; border:none;">
        <iframe id="infographicFrame" src="data:text/html;base64,{base64.b64encode(html_content.encode()).decode()}" 
                width="100%" height="800px" frameborder="0"></iframe>
    </div>
    {js_code}
    """
    
    return iframe_html

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
    
    # School name with similar search suggestions
    name_filter = st.sidebar.text_input("School Name", value=st.session_state.filters['name'])
    if name_filter:
        # Show suggestions based on similar search
        suggestions = find_similar_schools(name_filter, all_school_names, limit=5)
        if suggestions:
            selected_suggestion = st.sidebar.selectbox(
                "Did you mean:", 
                [""] + suggestions,
                index=0
            )
            if selected_suggestion:
                name_filter = selected_suggestion
    
    # Trust name with similar search suggestions
    trust_filter = st.sidebar.text_input("Trust Name", value=st.session_state.filters['trust_name'])
    if trust_filter:
        # Show suggestions based on similar search
        suggestions = find_similar_trusts(trust_filter, all_trust_names, limit=5)
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
            tabs = st.tabs(["Basic Info", "Contact Info", "Statistics", "Administrative", "Infographic"])
            
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
                
            with tabs[4]:  # Infographic tab
                st.subheader("School Infographic")
                st.write("Below is an Apple-inspired infographic for this school. You can download it as an image using the button at the bottom.")
                
                # Display the infographic
                infographic_html = create_infographic_component(school_details)
                st.components.v1.html(infographic_html, height=850)
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
