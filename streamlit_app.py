import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

# Set page config
st.set_page_config(page_title="Chipotle Bowl Tracker", page_icon="🌯", layout="wide")

# Initialize session state for data storage
if 'mb_data' not in st.session_state:
    st.session_state.mb_data = [
        ("2024-08-02", 922),
        ("2024-08-15", 694),
        ("2024-08-22", 835),
        ("2024-09-06", 838),
        ("2024-09-13", 611),
        ("2024-09-25", 710),
        ("2024-11-01", 689),
        ("2024-11-22", 731),
        ("2024-12-12", 734),
        ("2024-12-22", 718),
        ("2025-01-03", 685),
        ("2025-01-24", 860),
        ("2025-02-06", 753),
        ("2025-05-01", 789),
        ("2025-05-08", 706),
        ("2025-03-30", 604),
        ("2025-07-05", 748),
        ("2025-07-26", 830)
    ]

if 'mc_data' not in st.session_state:
    st.session_state.mc_data = [
        ("2024-08-22", 892),
        ("2024-09-06", 759),
        ("2024-09-13", 708),
        ("2024-09-25", 705),
        ("2024-11-01", 678),
        ("2024-11-22", 726),
        ("2024-12-12", 748),
        ("2024-12-22", 713),
        ("2025-01-03", 750),
        ("2025-01-24", 827),
        ("2025-02-06", 772),
        ("2025-05-01", 914),
        ("2025-05-08", 734),
        ("2025-05-30", 623),
        ("2025-07-26", 887)
    ]

# Title and description
st.title("🌯 Chipotle Bowl Weight Tracker")
st.markdown("*Tracking our Chipotle portions*")

# Add new data entry section
with st.expander("➕ Add New Bowl Weight", expanded=False):
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        customer = st.selectbox("Customer", ["Customer 1 (MB)", "Customer 2 (MC)"])
    
    with col2:
        entry_date = st.date_input("Date", value=date.today(), max_value=date.today())
    
    with col3:
        weight = st.number_input("Weight (grams)", min_value=300, max_value=1500, value=750, step=1)
    
    with col4:
        st.write("")  # Spacer
        st.write("")  # Spacer
        if st.button("Add Entry", type="primary"):
            date_str = entry_date.strftime("%Y-%m-%d")
            
            if customer == "Customer 1 (MB)":
                # Check if date already exists
                existing_dates = [d[0] for d in st.session_state.mb_data]
                if date_str in existing_dates:
                    st.error("Entry for this date already exists for MB!")
                else:
                    st.session_state.mb_data.append((date_str, weight))
                    st.success(f"Added {weight}g for MB on {date_str}")
                    st.rerun()
            else:
                # Check if date already exists
                existing_dates = [d[0] for d in st.session_state.mc_data]
                if date_str in existing_dates:
                    st.error("Entry for this date already exists for MC!")
                else:
                    st.session_state.mc_data.append((date_str, weight))
                    st.success(f"Added {weight}g for MC on {date_str}")
                    st.rerun()

# Data management section
with st.expander("🗑️ Manage Data", expanded=False):
    st.markdown("### Delete Entries")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Customer 1 (MB)**")
        # Create DataFrame for display
        df_mb_temp = pd.DataFrame(st.session_state.mb_data, columns=["Date", "Weight (g)"])
        df_mb_temp = df_mb_temp.sort_values("Date", ascending=False)
        
        if len(df_mb_temp) > 0:
            # Create selection list
            mb_entries = [f"{row['Date']}: {row['Weight (g)']}g" for _, row in df_mb_temp.iterrows()]
            mb_to_delete = st.selectbox("Select MB entry to delete", ["None"] + mb_entries, key="mb_delete")
            
            if mb_to_delete != "None" and st.button("Delete MB Entry", key="del_mb"):
                date_to_delete = mb_to_delete.split(":")[0]
                st.session_state.mb_data = [(d, w) for d, w in st.session_state.mb_data if d != date_to_delete]
                st.success(f"Deleted MB entry for {date_to_delete}")
                st.rerun()
    
    with col2:
        st.markdown("**Customer 2 (MC)**")
        # Create DataFrame for display
        df_mc_temp = pd.DataFrame(st.session_state.mc_data, columns=["Date", "Weight (g)"])
        df_mc_temp = df_mc_temp.sort_values("Date", ascending=False)
        
        if len(df_mc_temp) > 0:
            # Create selection list
            mc_entries = [f"{row['Date']}: {row['Weight (g)']}g" for _, row in df_mc_temp.iterrows()]
            mc_to_delete = st.selectbox("Select MC entry to delete", ["None"] + mc_entries, key="mc_delete")
            
            if mc_to_delete != "None" and st.button("Delete MC Entry", key="del_mc"):
                date_to_delete = mc_to_delete.split(":")[0]
                st.session_state.mc_data = [(d, w) for d, w in st.session_state.mc_data if d != date_to_delete]
                st.success(f"Deleted MC entry for {date_to_delete}")
                st.rerun()

# Export/Import data section
with st.expander("💾 Export/Import Data", expanded=False):
    st.markdown("### Export Current Data")
    st.markdown("Copy this code to save your current data:")
    
    export_code = f"""# MB Data
mb_data = {st.session_state.mb_data}

# MC Data  
mc_data = {st.session_state.mc_data}"""
    
    st.code(export_code, language="python")
    
    st.markdown("### Import Data")
    st.warning("⚠️ This will replace all current data!")
    
    import_text = st.text_area("Paste your data here (Python format)", height=150)
    
    if st.button("Import Data"):
        try:
            # Create a safe namespace for exec
            namespace = {}
            exec(import_text, namespace)
            
            if 'mb_data' in namespace:
                st.session_state.mb_data = namespace['mb_data']
            if 'mc_data' in namespace:
                st.session_state.mc_data = namespace['mc_data']
            
            st.success("Data imported successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error importing data: {e}")

# Create DataFrames from session state
df_mb = pd.DataFrame(st.session_state.mb_data, columns=["Date", "Weight (g)"])
df_mb["Date"] = pd.to_datetime(df_mb["Date"])
df_mb["Customer"] = "Customer 1 (MB)"

df_mc = pd.DataFrame(st.session_state.mc_data, columns=["Date", "Weight (g)"])
df_mc["Date"] = pd.to_datetime(df_mc["Date"])
df_mc["Customer"] = "Customer 2 (MC)"

# Sort by date
df_mb = df_mb.sort_values("Date")
df_mc = df_mc.sort_values("Date")

# Create the main plot
fig = go.Figure()

# Add MB's data
fig.add_trace(go.Scatter(
    x=df_mb["Date"],
    y=df_mb["Weight (g)"],
    mode='lines+markers',
    name='Customer 1 (MB)',
    connectgaps=False, 
    line=dict(color='#FF6B35', width=2),
    marker=dict(size=8),
    hovertemplate='<b>MB</b><br>Date: %{x|%b %d, %Y}<br>Weight: %{y}g<extra></extra>'
))

# Add MC's data
fig.add_trace(go.Scatter(
    x=df_mc["Date"],
    y=df_mc["Weight (g)"],
    mode='lines+markers',
    name='Customer 2 (MC)',
    connectgaps=False, 
    line=dict(color='#004E89', width=2),
    marker=dict(size=8),
    hovertemplate='<b>MC</b><br>Date: %{x|%b %d, %Y}<br>Weight: %{y}g<extra></extra>'
))

# Add average lines
mb_avg = df_mb["Weight (g)"].mean() if len(df_mb) > 0 else 0
mc_avg = df_mc["Weight (g)"].mean() if len(df_mc) > 0 else 0

if mb_avg > 0:
    fig.add_hline(y=mb_avg, line_dash="dash", line_color="#FF6B35", opacity=0.5,
                  annotation_text=f"MB Avg: {mb_avg:.0f}g", annotation_position="right")
if mc_avg > 0:
    fig.add_hline(y=mc_avg, line_dash="dash", line_color="#004E89", opacity=0.5,
                  annotation_text=f"MC Avg: {mc_avg:.0f}g", annotation_position="right")

# Update layout
fig.update_layout(
    title="Bowl Weight Over Time",
    xaxis_title="Date",
    yaxis_title="Weight (grams)",
    yaxis_range=[0, 1000],  
    height=500,
    hovermode='x unified',
    showlegend=True,
    template="plotly_white"
)

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Statistics section
st.markdown("---")
st.subheader("📊 Statistics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Customer 1 (MB)")
    if len(df_mb) > 0:
        max_idx = df_mb['Weight (g)'].idxmax()
        min_idx = df_mb['Weight (g)'].idxmin()
        max_date = df_mb.loc[max_idx, 'Date'].strftime('%b %d, %Y')
        min_date = df_mb.loc[min_idx, 'Date'].strftime('%b %d, %Y')
        
        mb_stats = {
            "🏆 Personal Best": f"{df_mb['Weight (g)'].max()}g ({max_date})",
            "😢 Personal Worst": f"{df_mb['Weight (g)'].min()}g ({min_date})",
            "📊 Average": f"{mb_avg:.0f}g",
            "📈 Std Dev": f"{df_mb['Weight (g)'].std():.0f}g",
            "🌯 Total Bowls": len(df_mb),
            "📉 Range": f"{df_mb['Weight (g)'].max() - df_mb['Weight (g)'].min()}g"
        }
        for stat, value in mb_stats.items():
            st.metric(stat, value)
    else:
        st.info("No data available for MB")

with col2:
    st.markdown("### Customer 2 (MC)")
    if len(df_mc) > 0:
        max_idx = df_mc['Weight (g)'].idxmax()
        min_idx = df_mc['Weight (g)'].idxmin()
        max_date = df_mc.loc[max_idx, 'Date'].strftime('%b %d, %Y')
        min_date = df_mc.loc[min_idx, 'Date'].strftime('%b %d, %Y')
        
        mc_stats = {
            "🏆 Personal Best": f"{df_mc['Weight (g)'].max()}g ({max_date})",
            "😢 Personal Worst": f"{df_mc['Weight (g)'].min()}g ({min_date})",
            "📊 Average": f"{mc_avg:.0f}g",
            "📈 Std Dev": f"{df_mc['Weight (g)'].std():.0f}g",
            "🌯 Total Bowls": len(df_mc),
            "📉 Range": f"{df_mc['Weight (g)'].max() - df_mc['Weight (g)'].min()}g"
        }
        for stat, value in mc_stats.items():
            st.metric(stat, value)
    else:
        st.info("No data available for MC")

# Fun facts section
st.markdown("---")
st.subheader("🎯 Fun Facts")

# Calculate who got more on same days
if len(df_mb) > 0 and len(df_mc) > 0:
    same_dates = set(df_mb["Date"]).intersection(set(df_mc["Date"]))
    mb_wins = 0
    mc_wins = 0

    for date in same_dates:
        mb_weight = df_mb[df_mb["Date"] == date]["Weight (g)"].values[0]
        mc_weight = df_mc[df_mc["Date"] == date]["Weight (g)"].values[0]
        if mb_weight > mc_weight:
            mb_wins += 1
        else:
            mc_wins += 1

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"📅 **Same-day orders:** {len(same_dates)} times")

    with col2:
        st.success(f"🏆 **MB got more:** {mb_wins}/{len(same_dates)} times")

    with col3:
        st.warning(f"🥈 **MC got more:** {mc_wins}/{len(same_dates)} times")

    # Consistency score (lower std dev = more consistent)
    if df_mb['Weight (g)'].std() < df_mc['Weight (g)'].std():
        consistency_winner = "MB"
        consistency_diff = df_mc['Weight (g)'].std() - df_mb['Weight (g)'].std()
    else:
        consistency_winner = "MC"
        consistency_diff = df_mb['Weight (g)'].std() - df_mc['Weight (g)'].std()

    st.info(f"🎯 **Most consistent portions:** {consistency_winner} (by {consistency_diff:.1f}g std dev)")
else:
    st.info("Add more data to see fun facts!")

# Recent entries section
st.markdown("---")
st.subheader("📝 Recent Entries")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Customer 1 (MB) - Last 5 entries**")
    if len(df_mb) > 0:
        recent_mb = df_mb.nlargest(5, 'Date')[['Date', 'Weight (g)']].sort_values('Date', ascending=False)
        recent_mb['Date'] = recent_mb['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(recent_mb, hide_index=True, use_container_width=True)
    else:
        st.info("No entries yet")

with col2:
    st.markdown("**Customer 2 (MC) - Last 5 entries**")
    if len(df_mc) > 0:
        recent_mc = df_mc.nlargest(5, 'Date')[['Date', 'Weight (g)']].sort_values('Date', ascending=False)
        recent_mc['Date'] = recent_mc['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(recent_mc, hide_index=True, use_container_width=True)
    else:
        st.info("No entries yet")

# Footer
st.markdown(
    """<h1 style="text-align: center;"> *🌯 The weight of happiness cannot be measured in grams alone! 🌯*</h1>""",
    unsafe_allow_html=True)
