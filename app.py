import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

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
def load_school_types():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM school_types_summary", conn)

@st.cache_data
def load_phase_summary():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM phase_summary", conn)

@st.cache_data
def load_religion_summary():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM religion_summary WHERE ReligiousCharacter != 'Unknown'", conn)

@st.cache_data
def load_gender_summary():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM gender_summary WHERE Gender != 'Unknown'", conn)

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
def search_schools(name="", la="", school_type="", phase="", postcode="", page=1, per_page=20):
    conn = get_connection()
    
    # Build query
    query = 'SELECT * FROM schools WHERE 1=1'
    params = []
    
    if name:
        query += ' AND EstablishmentName LIKE ?'
        params.append(f'%{name}%')
    
    if la:
        query += ' AND "LA (name)" = ?'
        params.append(la)
    
    if school_type:
        query += ' AND "TypeOfEstablishment (name)" = ?'
        params.append(school_type)
    
    if phase:
        query += ' AND "PhaseOfEducation (name)" = ?'
        params.append(phase)
    
    if postcode:
        query += ' AND Postcode LIKE ?'
        params.append(f'{postcode}%')
    
    # Get total count for pagination
    count_query = query.replace('SELECT *', 'SELECT COUNT(*)')
    count_df = pd.read_sql(count_query, conn, params=params)
    total_count = count_df.iloc[0, 0]
    
    # Add pagination
    query += ' ORDER BY EstablishmentName LIMIT ? OFFSET ?'
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

# Load summary statistics
@st.cache_data
def load_summary_stats():
    conn = get_connection()
    total_schools = pd.read_sql("SELECT COUNT(*) as count FROM schools", conn).iloc[0, 0]
    primary_schools = pd.read_sql("SELECT COUNT(*) as count FROM schools WHERE \"PhaseOfEducation (name)\" = 'Primary'", conn).iloc[0, 0]
    secondary_schools = pd.read_sql("SELECT COUNT(*) as count FROM schools WHERE \"PhaseOfEducation (name)\" = 'Secondary'", conn).iloc[0, 0]
    
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
    return fig

# Main app
def main():
    # Load data
    metadata = load_metadata()
    school_types = load_school_types()
    phase_summary = load_phase_summary()
    religion_summary = load_religion_summary()
    gender_summary = load_gender_summary()
    local_authorities = load_local_authorities()
    establishment_types = load_establishment_types()
    phases = load_phases()
    stats = load_summary_stats()
    
    # Sidebar - Filters
    st.sidebar.title("England Schools Dashboard")
    st.sidebar.caption(f"Data from Get Information about Schools service")
    st.sidebar.caption(f"Last updated: {metadata['last_updated']}")
    
    st.sidebar.header("Filters")
    
    name_filter = st.sidebar.text_input("School Name")
    
    la_options = [""] + local_authorities["LA (name)"].tolist()
    la_filter = st.sidebar.selectbox("Local Authority", la_options)
    
    type_options = [""] + establishment_types["TypeOfEstablishment (name)"].tolist()
    type_filter = st.sidebar.selectbox("Establishment Type", type_options)
    
    phase_options = [""] + phases["PhaseOfEducation (name)"].tolist()
    phase_filter = st.sidebar.selectbox("Phase of Education", phase_options)
    
    postcode_filter = st.sidebar.text_input("Postcode")
    
    # Main content
    st.title("England Schools Dashboard")
    
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
        st.plotly_chart(create_school_types_chart(school_types), use_container_width=True)
        st.plotly_chart(create_religion_chart(religion_summary), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_phase_chart(phase_summary), use_container_width=True)
        st.plotly_chart(create_gender_chart(gender_summary), use_container_width=True)
    
    # School list
    st.header("School List")
    
    # Pagination
    page = st.session_state.get("page", 1)
    per_page = 20
    
    # Search schools
    schools, total_count = search_schools(
        name=name_filter,
        la=la_filter,
        school_type=type_filter,
        phase=phase_filter,
        postcode=postcode_filter,
        page=page,
        per_page=per_page
    )
    
    # Pagination controls
    total_pages = (total_count + per_page - 1) // per_page
    
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
    
    # Display schools
    if not schools.empty:
        # Create a DataFrame with only the columns we want to display
        display_df = schools[['URN', 'EstablishmentName', 'LA (name)', 'TypeOfEstablishment (name)', 'PhaseOfEducation (name)', 'Postcode']]
        display_df.columns = ['URN', 'School Name', 'Local Authority', 'Type', 'Phase', 'Postcode']
        
        # Display the table
        st.dataframe(display_df, use_container_width=True)
        
        # School details
        st.header("School Details")
        selected_urn = st.selectbox("Select a school to view details", schools['URN'].tolist(), format_func=lambda x: schools[schools['URN'] == x]['EstablishmentName'].iloc[0])
        
        if selected_urn:
            school_details = get_school_details(selected_urn).iloc[0]
            
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
            
            with col2:
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
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("School Statistics")
                st.write(f"**School Capacity:** {int(school_details['SchoolCapacity'])}")
                st.write(f"**Number of Pupils:** {int(school_details['NumberOfPupils'])}")
                st.write(f"**Percentage FSM:** {school_details['PercentageFSM']}%")
                st.write(f"**Statutory Low Age:** {int(school_details['StatutoryLowAge'])}")
                st.write(f"**Statutory High Age:** {int(school_details['StatutoryHighAge'])}")
                st.write(f"**Nursery Provision:** {school_details['NurseryProvision (name)']}")
                st.write(f"**Official Sixth Form:** {school_details['OfficialSixthForm (name)']}")
            
            with col2:
                st.subheader("Administrative Information")
                st.write(f"**Trust:** {school_details['Trusts (name)']}")
                st.write(f"**Federation:** {school_details['Federations (name)']}")
                st.write(f"**District:** {school_details['DistrictAdministrative (name)']}")
                st.write(f"**Ward:** {school_details['AdministrativeWard (name)']}")
                st.write(f"**Parliamentary Constituency:** {school_details['ParliamentaryConstituency (name)']}")
                st.write(f"**Urban/Rural:** {school_details['UrbanRural (name)']}")
    else:
        st.info("No schools found matching your criteria. Try adjusting your filters.")
    
    # Footer
    st.markdown("---")
    st.caption("Data source: Get Information about Schools service - [https://get-information-schools.service.gov.uk/](https://get-information-schools.service.gov.uk/)")

if __name__ == "__main__":
    main()
