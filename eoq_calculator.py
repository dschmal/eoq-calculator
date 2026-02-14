"""
EOQ Calculator by Dennis Schmal
Supply Chain Digitalization Manager | AI Solutions Builder
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Page config
st.set_page_config(
    page_title="EOQ Calculator | Dennis Schmal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optimized CSS for Streamlit rendering
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #F8F9FA;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Headers - Clean and simple */
    h1, h2, h3 {
        color: #1A202C !important;
        font-weight: 600 !important;
    }
    
    h1 {
        font-size: 28px !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 18px !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    [data-testid="stMetricLabel"] {
        color: #718096 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        color: #2C5282 !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar - FIXED for readability */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        padding: 2rem 1rem !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #FFFFFF !important;
    }
    
    /* Sidebar text - HIGH CONTRAST */
    section[data-testid="stSidebar"] label {
        color: #2D3748 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        margin-bottom: 0.5rem !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #2D3748 !important;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: #1A202C !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #E2E8F0 !important;
    }
    
    /* Number inputs in sidebar */
    section[data-testid="stSidebar"] input {
        color: #1A202C !important;
        font-weight: 600 !important;
    }
    
    /* Slider in sidebar */
    section[data-testid="stSidebar"] [data-baseweb="slider"] {
        margin-top: 1rem !important;
    }
    
    /* Expander in sidebar */
    section[data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #F7FAFC !important;
        color: #2D3748 !important;
        font-weight: 600 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }
    
    section[data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background-color: #EDF2F7 !important;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #EBF8FF !important;
        border-left: 4px solid #3182CE !important;
        border-radius: 6px !important;
        padding: 1rem !important;
    }
    
    [data-baseweb="notification"] p {
        color: #2C5282 !important;
        font-size: 14px !important;
    }
    
    /* Success boxes */
    .element-container div[kind="success"] {
        background-color: #F0FFF4 !important;
        border-left: 4px solid #38A169 !important;
    }
    
    .element-container div[kind="success"] p {
        color: #22543D !important;
    }
    
    /* Tables */
    .dataframe {
        font-size: 13px !important;
    }
    
    .dataframe th {
        background-color: #F7FAFC !important;
        color: #4A5568 !important;
        font-weight: 600 !important;
        text-align: left !important;
    }
    
    .dataframe td {
        color: #2D3748 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #3182CE !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        background-color: #2C5282 !important;
    }
    
    .stDownloadButton > button {
        background-color: #38A169 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #2F855A !important;
    }
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Custom cards */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    .stat-badge {
        display: inline-block;
        background: #EDF2F7;
        color: #4A5568;
        padding: 0.4rem 0.8rem;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
        margin: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("# 📦 EOQ Calculator")
st.markdown("**Dennis Schmal** · Supply Chain Digitalization Manager")
st.markdown("")

# Quick info badges
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <span class='stat-badge'>⚡ 2-hour build</span>
    <span class='stat-badge'>🚀 Production tool</span>
    <span class='stat-badge'>💾 Open source</span>
    <span class='stat-badge'>📊 500+ users/month</span>
</div>
""", unsafe_allow_html=True)

# Sidebar - OPTIMIZED
st.sidebar.markdown("## ⚙️ Configuration")

st.sidebar.markdown("### 📊 Demand & Costs")
annual_demand = st.sidebar.number_input(
    "Annual Demand (units)",
    min_value=100,
    max_value=10000000,
    value=50000,
    step=1000,
    help="Total units expected per year"
)

unit_cost = st.sidebar.number_input(
    "Unit Cost (€)",
    min_value=0.01,
    max_value=100000.0,
    value=50.0,
    step=1.0,
    help="Cost per unit"
)

order_cost = st.sidebar.number_input(
    "Order Cost (€)",
    min_value=1.0,
    max_value=50000.0,
    value=200.0,
    step=10.0,
    help="Fixed cost per order"
)

holding_cost_pct = st.sidebar.slider(
    "Holding Cost (%)",
    min_value=5,
    max_value=50,
    value=20,
    step=1,
    help="Annual holding cost as % of unit cost"
)

st.sidebar.markdown("### ⏱️ Lead Time & Service")

lead_time_days = st.sidebar.number_input(
    "Lead Time (days)",
    min_value=1,
    max_value=365,
    value=14,
    step=1,
    help="Days from order to delivery"
)

service_level = st.sidebar.slider(
    "Service Level (%)",
    min_value=85,
    max_value=99,
    value=95,
    step=1,
    help="Probability of not stocking out"
)

demand_variability = st.sidebar.slider(
    "Demand Variability (%)",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
    help="Demand fluctuation (CV%)"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**💡 Tool Info**")
st.sidebar.markdown("Built: 2024 · Tech: Python + Streamlit")
st.sidebar.markdown("[GitHub](https://github.com/dschmahl) · [Website](https://dennisschmal.de)")

# Calculations
holding_cost_per_unit = unit_cost * (holding_cost_pct / 100)
eoq = np.sqrt((2 * annual_demand * order_cost) / holding_cost_per_unit)
daily_demand = annual_demand / 365

z_scores = {
    85: 1.04, 86: 1.08, 87: 1.13, 88: 1.17, 89: 1.23,
    90: 1.28, 91: 1.34, 92: 1.41, 93: 1.48, 94: 1.55,
    95: 1.65, 96: 1.75, 97: 1.88, 98: 2.05, 99: 2.33
}
z_score = z_scores[service_level]

daily_std_dev = daily_demand * (demand_variability / 100)
lead_time_demand_std = daily_std_dev * np.sqrt(lead_time_days)
safety_stock = z_score * lead_time_demand_std
average_lead_time_demand = daily_demand * lead_time_days
reorder_point = average_lead_time_demand + safety_stock

orders_per_year = annual_demand / eoq
days_between_orders = 365 / orders_per_year
total_order_cost_annual = orders_per_year * order_cost
average_inventory = (eoq / 2) + safety_stock
total_holding_cost_annual = average_inventory * holding_cost_per_unit
total_inventory_cost_annual = total_order_cost_annual + total_holding_cost_annual

# Results
st.markdown("## 📈 Optimization Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("EOQ", f"{eoq:,.0f}", help="Economic Order Quantity")
    st.caption("units per order")

with col2:
    st.metric("Safety Stock", f"{safety_stock:,.0f}", help=f"{service_level}% service level")
    st.caption("units buffer")

with col3:
    st.metric("Reorder Point", f"{reorder_point:,.0f}", help="When to order")
    st.caption("units trigger")

with col4:
    st.metric("Orders/Year", f"{orders_per_year:.1f}", help="Order frequency")
    st.caption("orders annually")

st.markdown("")

# Business Impact
st.markdown("## 💰 Business Impact")

col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.metric("Total Annual Cost", f"€{total_inventory_cost_annual:,.0f}")
    st.caption("ordering + holding")

with col_b2:
    st.metric("Avg Inventory", f"{average_inventory:,.0f}")
    st.caption("units on hand")

with col_b3:
    st.metric("Order Cycle", f"{days_between_orders:.0f}")
    st.caption("days between orders")

st.markdown("")

# Charts
st.markdown("## 📊 Visual Analysis")

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown("**Cost Breakdown**")
    
    fig_costs = go.Figure()
    
    fig_costs.add_trace(go.Bar(
        x=['Ordering', 'Holding'],
        y=[total_order_cost_annual, total_holding_cost_annual],
        marker=dict(
            color=['#3182CE', '#63B3ED'],
            line=dict(color='white', width=2)
        ),
        text=[f'€{total_order_cost_annual:,.0f}', f'€{total_holding_cost_annual:,.0f}'],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial'),
        hovertemplate='%{x}: €%{y:,.0f}<extra></extra>'
    ))
    
    fig_costs.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, color='#4A5568'),
        xaxis=dict(
            showgrid=False,
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title='Cost (€)'
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig_costs, use_container_width=True, config={'displayModeBar': False})
    
    st.caption(f"Total: €{total_inventory_cost_annual:,.0f}/year")

with col_c2:
    st.markdown("**Inventory Levels Over Time**")
    
    time_points = np.linspace(0, 2 * days_between_orders, 100)
    inventory_levels = []
    
    for t in time_points:
        days_in_cycle = t % days_between_orders
        if days_in_cycle < lead_time_days:
            inventory = eoq + safety_stock - (daily_demand * (days_between_orders - lead_time_days + days_in_cycle))
        else:
            inventory = eoq + safety_stock - (daily_demand * (days_in_cycle - lead_time_days))
        inventory_levels.append(max(safety_stock, inventory))
    
    fig_sim = go.Figure()
    
    fig_sim.add_trace(go.Scatter(
        x=time_points,
        y=inventory_levels,
        mode='lines',
        line=dict(color='#3182CE', width=3),
        fill='tozeroy',
        fillcolor='rgba(49,130,206,0.1)',
        hovertemplate='Day %{x:.0f}<br>Inventory: %{y:,.0f}<extra></extra>',
        showlegend=False
    ))
    
    fig_sim.add_hline(
        y=reorder_point,
        line_dash="dash",
        line_color="#E53E3E",
        line_width=2,
        annotation_text=f"Reorder: {reorder_point:,.0f}",
        annotation_position="right",
        annotation=dict(font=dict(size=10, color='#E53E3E'))
    )
    
    fig_sim.add_hline(
        y=safety_stock,
        line_dash="dot",
        line_color="#DD6B20",
        line_width=2,
        annotation_text=f"Safety: {safety_stock:,.0f}",
        annotation_position="right",
        annotation=dict(font=dict(size=10, color='#DD6B20'))
    )
    
    fig_sim.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12, color='#4A5568'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title='Days'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title='Units'
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_sim, use_container_width=True, config={'displayModeBar': False})
    
    st.caption("2 order cycles shown")

st.markdown("")

# Insights
col_i1, col_i2 = st.columns(2)

with col_i1:
    st.info(f"""
**📦 Ordering Strategy**

• Order **{eoq:,.0f} units** every **{days_between_orders:.0f} days**  
• Equals **{orders_per_year:.1f} orders per year**  
• Ordering cost: **€{total_order_cost_annual:,.0f}/year**
    """)

with col_i2:
    st.success(f"""
**✅ Inventory Management**

• Keep **{safety_stock:,.0f} units** as safety stock  
• Reorder at **{reorder_point:,.0f} units**  
• Holding cost: **€{total_holding_cost_annual:,.0f}/year**
    """)

st.markdown("")

# Scenario Comparison
st.markdown("## 🔄 Scenario Comparison")

scenarios = pd.DataFrame({
    'Scenario': ['Conservative (99%)', f'Current ({service_level}%)', 'Aggressive (90%)'],
    'Service Level': ['99%', f'{service_level}%', '90%'],
    'Safety Stock': [
        f"{z_scores[99] * lead_time_demand_std:,.0f}",
        f"{safety_stock:,.0f}",
        f"{z_scores[90] * lead_time_demand_std:,.0f}"
    ],
    'Average Inventory': [
        f"{(eoq/2) + z_scores[99] * lead_time_demand_std:,.0f}",
        f"{average_inventory:,.0f}",
        f"{(eoq/2) + z_scores[90] * lead_time_demand_std:,.0f}"
    ],
    'Annual Cost': [
        f"€{total_order_cost_annual + ((eoq/2) + z_scores[99] * lead_time_demand_std) * holding_cost_per_unit:,.0f}",
        f"€{total_inventory_cost_annual:,.0f}",
        f"€{total_order_cost_annual + ((eoq/2) + z_scores[90] * lead_time_demand_std) * holding_cost_per_unit:,.0f}"
    ]
})

st.dataframe(scenarios, use_container_width=True, hide_index=True)

st.markdown("")

# Export
st.markdown("## 💾 Export Results")

export_data = pd.DataFrame({
    'Parameter': [
        'Annual Demand', 'Unit Cost', 'Order Cost', 'Holding Cost %',
        'Lead Time', 'Service Level', 'Demand Variability',
        'EOQ', 'Safety Stock', 'Reorder Point', 'Orders/Year',
        'Days Between Orders', 'Average Inventory',
        'Annual Ordering Cost', 'Annual Holding Cost', 'Total Annual Cost'
    ],
    'Value': [
        f"{annual_demand:,.0f} units", f"€{unit_cost:.2f}", f"€{order_cost:.2f}",
        f"{holding_cost_pct}%", f"{lead_time_days} days", f"{service_level}%", 
        f"{demand_variability}%", f"{eoq:,.0f} units", f"{safety_stock:,.0f} units",
        f"{reorder_point:,.0f} units", f"{orders_per_year:.1f}",
        f"{days_between_orders:.1f} days", f"{average_inventory:,.0f} units",
        f"€{total_order_cost_annual:,.0f}", f"€{total_holding_cost_annual:,.0f}",
        f"€{total_inventory_cost_annual:,.0f}"
    ]
})

csv = export_data.to_csv(index=False)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

st.download_button(
    "📥 Download CSV",
    data=csv,
    file_name=f"eoq_results_{timestamp}.csv",
    mime="text/csv"
)

st.markdown("")
st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 13px; padding: 2rem 0 1rem 0;'>
    <p style='margin-bottom: 0.5rem;'><strong style='color: #2D3748;'>Built by Dennis Schmal</strong></p>
    <p style='margin-bottom: 0.5rem;'>Supply Chain Digitalization Manager | AI Solutions Builder</p>
    <p style='margin-bottom: 1rem;'>
        <a href='https://dennisschmal.de' style='color: #3182CE; text-decoration: none;'>Website</a> • 
        <a href='https://linkedin.com/in/dennis-schmal' style='color: #3182CE; text-decoration: none;'>LinkedIn</a> • 
        <a href='https://github.com/dschmahl' style='color: #3182CE; text-decoration: none;'>GitHub</a>
    </p>
    <p style='font-size: 12px; color: #A0AEC0;'>
        🎓 Learn to build tools like this in 8-week weekend cohorts • No coding experience required
    </p>
</div>
""", unsafe_allow_html=True)

# Technical note
with st.expander("🔧 Technical Details"):
    st.markdown("""
    **Formulas Used:**
    - EOQ = √(2 × Annual Demand × Order Cost / Holding Cost)
    - Safety Stock = Z-score × σ × √Lead Time
    - Reorder Point = (Daily Demand × Lead Time) + Safety Stock
    
    **Tech Stack:** Python • NumPy • Pandas • Plotly • Streamlit
    
    **Open Source:** [View on GitHub](https://github.com/dschmahl)
    """)
