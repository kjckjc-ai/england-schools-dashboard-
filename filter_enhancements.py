# Establishment Type Group Filter Enhancement

# 1. Load establishment groups
@st.cache_data
def load_establishment_groups():
    conn = get_connection()
    return pd.read_sql("SELECT DISTINCT \"EstablishmentTypeGroup (name)\" FROM schools WHERE \"EstablishmentTypeGroup (name)\" != 'Unknown' ORDER BY \"EstablishmentTypeGroup (name)\"", conn)

# 2. In your sidebar filters section, replace the current establishment type filter with:
establishment_groups = load_establishment_groups()
group_options = establishment_groups["EstablishmentTypeGroup (name)"].tolist()
group_filter = st.sidebar.multiselect("Establishment Type Group", group_options, default=[])

# 3. In your search query building section, replace the current establishment type filter logic with:
if group_filter and len(group_filter) > 0:
    placeholders = ', '.join(['?' for _ in group_filter])
    query += f' AND "EstablishmentTypeGroup (name)" IN ({placeholders})'
    params.extend(group_filter)

# Postcode Prefix Filter Enhancement

# 1. Load postcode prefixes
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

# 2. In your sidebar filters section, replace the current postcode filter with:
postcode_prefixes = load_postcode_prefixes()
postcode_prefix_options = [""] + postcode_prefixes["PostcodePrefix"].tolist()
postcode_prefix_filter = st.sidebar.selectbox(
    "Postcode Prefix", 
    postcode_prefix_options, 
    index=0
)

# 3. Add custom postcode prefix input
custom_postcode = st.sidebar.text_input("Or enter custom postcode prefix:", "")
if custom_postcode:
    postcode_prefix_filter = custom_postcode

# 4. In your search query building section, replace the current postcode filter logic with:
if postcode_prefix_filter:
    query += ' AND Postcode LIKE ?'
    params.append(f'{postcode_prefix_filter}%')
