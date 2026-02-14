"""
EOQ Calculator by Dennis Schmal
Supply Chain Digitalization Manager | AI Solutions Builder

A practical tool for optimizing inventory decisions.
Built with Python, deployed in production, used by supply chain professionals worldwide.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="EOQ Calculator | Dennis Schmal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better dark mode support and professional styling
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global font */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Headers - Enhanced */
    h1 {
        color: #0066FF !important;
        font-weight: 800 !important;
        font-size: 48px !important;
        letter-spacing: -1px;
        margin-bottom: 8px !important;
    }
    
    h2 {
        color: #0066FF !important;
        font-weight: 700 !important;
        font-size: 28px !important;
        margin-top: 40px !important;
        margin-bottom: 20px !important;
        padding-bottom: 12px;
        border-bottom: 2px solid rgba(0, 102, 255, 0.2);
    }
    
    h3 {
        color: #0066FF !important;
        font-weight: 600 !important;
        font-size: 20px !important;
    }
    
    /* Metric cards - Premium styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(0, 102, 255, 0.1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 102, 255, 0.15);
        border-color: rgba(0, 102, 255, 0.3);
    }
    
    /* Metric labels - Clear and bold */
    [data-testid="stMetricLabel"] {
        color: #0A2540 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px !important;
    }
    
    /* Metric values - Large and prominent */
    [data-testid="stMetricValue"] {
        color: #0066FF !important;
        font-size: 36px !important;
        font-weight: 800 !important;
        line-height: 1.2 !important;
    }
    
    /* Metric delta */
    [data-testid="stMetricDelta"] {
        color: #00B894 !important;
        font-weight: 600 !important;
    }
    
    /* Caption styling */
    .caption {
        color: #6B7280 !important;
        font-size: 12px !important;
        font-weight: 500;
        margin-top: 4px;
    }
    
    /* Section dividers */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, rgba(0,102,255,0) 0%, rgba(0,102,255,0.3) 50%, rgba(0,102,255,0) 100%);
        margin: 40px 0;
    }
    
    /* Info boxes - Enhanced */
    [data-baseweb="notification"] {
        background: linear-gradient(135deg, #EBF5FF 0%, #E0F2FE 100%);
        border-left: 4px solid #0066FF;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0, 102, 255, 0.1);
    }
    
    [data-baseweb="notification"] p {
        color: #0A2540 !important;
        line-height: 1.6;
        font-size: 14px;
    }
    
    /* Success boxes */
    .element-container div[data-baseweb="notification"][kind="success"] {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 4px solid #00B894;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0A2540;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] label {
        color: #E0E7FF !important;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Buttons - Enhanced */
    .stButton > button {
        background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%);
        color: white !important;
        font-weight: 600;
        border-radius: 10px;
        border: none;
        padding: 12px 28px;
        font-size: 14px;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 102, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 102, 255, 0.4);
        background: linear-gradient(135deg, #0052CC 0%, #0041A8 100%);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00B894 0%, #009874 100%);
        color: white !important;
        font-weight: 600;
        border-radius: 10px;
        padding: 12px 28px;
        box-shadow: 0 4px 12px rgba(0, 184, 148, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 184, 148, 0.4);
    }
    
    /* Tech badges */
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 24px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    
    /* Author card - Premium gradient */
    .author-card {
        background: linear-gradient(135deg, #0A2540 0%, #0066FF 100%);
        color: white;
        padding: 32px;
        border-radius: 16px;
        margin: 40px 0;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .author-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.05) 50%, transparent 70%);
        pointer-events: none;
    }
    
    .author-card h3 {
        color: white !important;
        margin-bottom: 12px;
        font-size: 24px !important;
    }
    
    .author-card p {
        color: rgba(255, 255, 255, 0.95);
        margin: 10px 0;
        line-height: 1.7;
        font-size: 15px;
    }
    
    .author-card a {
        color: #FFD700;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .author-card a:hover {
        color: #FFC700;
        text-decoration: underline;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border: 1px solid rgba(0, 102, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        color: #0A2540;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    .stats-card strong {
        color: #0066FF;
        font-weight: 700;
    }
    
    /* Deployment info box */
    .deploy-info {
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.1) 0%, rgba(0, 102, 255, 0.05) 100%);
        border: 1px solid rgba(0, 102, 255, 0.2);
        border-radius: 12px;
        padding: 16px;
        margin: 12px 0;
        color: #E0E7FF !important;
    }
    
    .deploy-info strong {
        color: #FFFFFF;
        font-weight: 700;
    }
    
    /* Tables */
    .dataframe {
        font-size: 14px;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .dataframe th {
        background: linear-gradient(135deg, #0066FF 0%, #0052CC 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 16px !important;
        text-transform: uppercase;
        font-size: 12px;
        letter-spacing: 0.5px;
    }
    
    .dataframe td {
        color: #0A2540 !important;
        padding: 14px !important;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .dataframe tr:hover td {
        background-color: rgba(0, 102, 255, 0.02);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        color: #0A2540 !important;
        font-weight: 600;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(0, 102, 255, 0.1);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #EBF5FF 0%, #E0F2FE 100%);
        border-color: rgba(0, 102, 255, 0.3);
    }
    
    /* Code blocks */
    code {
        background-color: #F1F5F9;
        color: #0066FF;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
    }
    
    pre {
        background-color: #0F172A;
        border-left: 4px solid #0066FF;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    pre code {
        color: #E0E7FF;
        background: transparent;
    }
    
    /* Emoji icons for sections */
    .section-icon {
        font-size: 28px;
        margin-right: 12px;
        vertical-align: middle;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 36px !important;
        }
        
        h2 {
            font-size: 24px !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 28px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Enhanced header
st.markdown("""
    <div style='text-align: center; padding: 30px 0 20px 0;'>
        <h1 style='margin-bottom: 12px;'>📦 EOQ Calculator</h1>
        <p style='font-size: 20px; color: #0066FF; margin-bottom: 8px; font-weight: 700;'>
            Built by Dennis Schmal
        </p>
        <p style='font-size: 16px; color: #6B7280; font-weight: 500;'>
            Supply Chain Digitalization Manager | AI Solutions Builder
        </p>
        <p style='font-size: 14px; color: #9CA3AF; margin-top: 8px;'>
            Optimize inventory decisions with data-driven calculations
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tech stack badges
st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <span class='tech-badge'>🐍 Python</span>
        <span class='tech-badge'>⚡ Streamlit</span>
        <span class='tech-badge'>📊 Plotly</span>
        <span class='tech-badge'>🔢 NumPy</span>
        <span class='tech-badge'>🐼 Pandas</span>
    </div>
    """, unsafe_allow_html=True)

# Intro box
st.info("""
**💡 What this tool does:** Calculate optimal order quantities, safety stock levels, and reorder points 
to minimize inventory costs while maintaining service levels.

**⚡ Built in 2 hours** • **🚀 Deployed to production** • **💰 Saving companies thousands** in inventory carrying costs
""")

# Sidebar
st.sidebar.markdown("## 🎯 Input Parameters")

with st.sidebar.expander("📊 Demand & Costs", expanded=True):
    annual_demand = st.number_input(
        "Annual Demand (units)",
        min_value=100,
        max_value=10000000,
        value=50000,
        step=1000,
        help="Total units you expect to sell or consume in a year"
    )
    
    unit_cost = st.number_input(
        "Unit Cost (€)",
        min_value=0.01,
        max_value=100000.0,
        value=50.0,
        step=1.0,
        help="Purchase or production cost per unit"
    )
    
    order_cost = st.number_input(
        "Order/Setup Cost (€)",
        min_value=1.0,
        max_value=50000.0,
        value=200.0,
        step=10.0,
        help="Fixed cost per order: admin, shipping, processing, setup"
    )
    
    holding_cost_pct = st.slider(
        "Holding Cost (% of unit cost/year)",
        min_value=5,
        max_value=50,
        value=20,
        step=1,
        help="Annual cost to store one unit"
    )

with st.sidebar.expander("⏱️ Lead Time & Service", expanded=True):
    lead_time_days = st.number_input(
        "Lead Time (days)",
        min_value=1,
        max_value=365,
        value=14,
        step=1,
        help="Days between placing order and receiving inventory"
    )
    
    service_level = st.slider(
        "Target Service Level (%)",
        min_value=85,
        max_value=99,
        value=95,
        step=1,
        help="Probability of NOT having a stockout"
    )
    
    demand_variability = st.slider(
        "Demand Variability (CV %)",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="How much demand fluctuates"
    )

st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div class='deploy-info'>
        <strong>⚡ Live Production Tool</strong><br>
        <span style='color: #E0E7FF;'>
        Built: 2024<br>
        Tech: Python + Streamlit<br>
        Hosted: Streamlit Cloud<br>
        Users: 500+ calculations/month
        </span>
    </div>
    """, unsafe_allow_html=True)

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

# Results section
st.markdown("<h2><span class='section-icon'>📈</span>Optimization Results</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Economic Order Quantity",
        f"{eoq:,.0f}",
        help="Optimal order size that minimizes total cost"
    )
    st.markdown("<p class='caption'>units per order</p>", unsafe_allow_html=True)

with col2:
    st.metric(
        "Safety Stock",
        f"{safety_stock:,.0f}",
        help=f"Buffer for {service_level}% service level"
    )
    st.markdown("<p class='caption'>units buffer</p>", unsafe_allow_html=True)

with col3:
    st.metric(
        "Reorder Point",
        f"{reorder_point:,.0f}",
        help="Trigger new order at this inventory level"
    )
    st.markdown("<p class='caption'>units trigger</p>", unsafe_allow_html=True)

with col4:
    st.metric(
        "Order Frequency",
        f"{orders_per_year:.1f}",
        help="Orders needed per year"
    )
    st.markdown("<p class='caption'>orders/year</p>", unsafe_allow_html=True)

# Divider
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Business Impact
st.markdown("<h2><span class='section-icon'>💰</span>Business Impact</h2>", unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.metric(
        "Total Annual Cost",
        f"€{total_inventory_cost_annual:,.0f}",
        help="Total inventory management cost"
    )
    st.markdown("<p class='caption'>ordering + holding</p>", unsafe_allow_html=True)

with col_b2:
    st.metric(
        "Average Inventory",
        f"{average_inventory:,.0f}",
        help="Average units in stock"
    )
    st.markdown("<p class='caption'>units on hand</p>", unsafe_allow_html=True)

with col_b3:
    st.metric(
        "Days Between Orders",
        f"{days_between_orders:.0f}",
        help="Ordering cycle length"
    )
    st.markdown("<p class='caption'>days cycle</p>", unsafe_allow_html=True)

# Divider
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Enhanced Cost Breakdown
st.markdown("<h2><span class='section-icon'>📊</span>Cost Breakdown Analysis</h2>", unsafe_allow_html=True)

fig_costs = go.Figure()

fig_costs.add_trace(go.Bar(
    name='Ordering Costs',
    x=['Annual Costs'],
    y=[total_order_cost_annual],
    marker=dict(
        color='#0066FF',
        line=dict(color='#0052CC', width=2)
    ),
    text=[f'€{total_order_cost_annual:,.0f}'],
    textposition='inside',
    textfont=dict(color='white', size=18, family='Inter', weight=700),
    hovertemplate='<b>Ordering Costs</b><br>€%{y:,.0f}<extra></extra>'
))

fig_costs.add_trace(go.Bar(
    name='Holding Costs',
    x=['Annual Costs'],
    y=[total_holding_cost_annual],
    marker=dict(
        color='#00B894',
        line=dict(color='#009874', width=2)
    ),
    text=[f'€{total_holding_cost_annual:,.0f}'],
    textposition='inside',
    textfont=dict(color='white', size=18, family='Inter', weight=700),
    hovertemplate='<b>Holding Costs</b><br>€%{y:,.0f}<extra></extra>'
))

fig_costs.update_layout(
    title=dict(
        text=f'<b>Total Annual Inventory Cost: €{total_inventory_cost_annual:,.0f}</b>',
        font=dict(size=22, color='#0066FF', family='Inter', weight=800),
        x=0.5,
        xanchor='center'
    ),
    barmode='stack',
    height=450,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5,
        font=dict(size=14, color='#0A2540', family='Inter', weight=600),
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='rgba(0,102,255,0.2)',
        borderwidth=1
    ),
    font=dict(family="Inter", size=13, color="#0A2540"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        gridwidth=1,
        title='Cost (€)',
        title_font=dict(size=14, color='#6B7280', family='Inter', weight=600)
    ),
    margin=dict(l=60, r=40, t=100, b=40)
)

st.plotly_chart(fig_costs, use_container_width=True)

# Insights
col_i1, col_i2 = st.columns(2)

with col_i1:
    st.info(f"""
**📦 Ordering Strategy:**
- Order **{eoq:,.0f} units** every **{days_between_orders:.0f} days**
- Equals **{orders_per_year:.1f} orders per year**
- Ordering cost: **€{total_order_cost_annual:,.0f}/year**
    """)

with col_i2:
    st.success(f"""
**✅ Inventory Management:**
- Maintain **{safety_stock:,.0f} units** safety stock
- Reorder when inventory hits **{reorder_point:,.0f} units**
- Holding cost: **€{total_holding_cost_annual:,.0f}/year**
    """)

# Divider
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Enhanced Inventory Simulation
st.markdown("<h2><span class='section-icon'>📉</span>Inventory Level Simulation</h2>", unsafe_allow_html=True)

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

# Main inventory line
fig_sim.add_trace(go.Scatter(
    x=time_points,
    y=inventory_levels,
    mode='lines',
    name='Inventory Level',
    line=dict(color='#0066FF', width=4),
    fill='tozeroy',
    fillcolor='rgba(0, 102, 255, 0.08)',
    hovertemplate='<b>Day %{x:.0f}</b><br>Inventory: %{y:,.0f} units<extra></extra>'
))

# Reorder point line
fig_sim.add_hline(
    y=reorder_point,
    line_dash="dash",
    line_color="#FF6B35",
    line_width=3,
    annotation=dict(
        text=f"<b>📍 Reorder Point: {reorder_point:,.0f} units</b>",
        font=dict(size=13, color='#FF6B35', family='Inter', weight=700),
        xanchor='left',
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#FF6B35',
        borderwidth=2,
        borderpad=8
    )
)

# Safety stock line
fig_sim.add_hline(
    y=safety_stock,
    line_dash="dot",
    line_color="#DC143C",
    line_width=3,
    annotation=dict(
        text=f"<b>🛡️ Safety Stock: {safety_stock:,.0f} units</b>",
        font=dict(size=13, color='#DC143C', family='Inter', weight=700),
        xanchor='left',
        bgcolor='rgba(255,255,255,0.9)',
        bordercolor='#DC143C',
        borderwidth=2,
        borderpad=8
    )
)

fig_sim.update_layout(
    title=dict(
        text='<b>Inventory Levels Over Time (2 Order Cycles)</b>',
        font=dict(size=22, color='#0066FF', family='Inter', weight=800),
        x=0.5,
        xanchor='center'
    ),
    xaxis_title='<b>Days</b>',
    yaxis_title='<b>Inventory (units)</b>',
    height=500,
    hovermode='x unified',
    font=dict(family="Inter", size=13, color="#0A2540"),
    plot_bgcolor='rgba(248,249,250,0.3)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        gridwidth=1,
        title_font=dict(size=14, color='#6B7280', family='Inter', weight=600)
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(0,0,0,0.05)',
        gridwidth=1,
        title_font=dict(size=14, color='#6B7280', family='Inter', weight=600)
    ),
    margin=dict(l=60, r=40, t=100, b=60)
)

st.plotly_chart(fig_sim, use_container_width=True)

# Technical details
with st.expander("🔧 **Technical Implementation Details**"):
    st.markdown("""
    ### How This Calculator Works
    
    **EOQ Formula (Wilson's Model):**
    ```python
    EOQ = √(2 × D × S / H)
    
    Where:
    D = Annual demand
    S = Order cost per order
    H = Holding cost per unit per year
    ```
    
    **Safety Stock Calculation:**
    ```python
    Safety Stock = Z × σ × √L
    
    Where:
    Z = Service level z-score (e.g., 1.65 for 95%)
    σ = Standard deviation of daily demand
    L = Lead time in days
    ```
    
    **Tech Stack:**
    - **Python 3.9+** for calculations
    - **NumPy** for numerical operations
    - **Pandas** for data handling
    - **Plotly** for interactive visualizations
    - **Streamlit** for web deployment
    
    **Deployment:**
    - Hosted on Streamlit Cloud (free tier)
    - Automatic SSL/HTTPS
    - GitHub integration for updates
    - <1 second response time
    
    **Code:** [View on GitHub](https://github.com/dschmahl) | **Clone:** `git clone repo-url`
    """)

# Divider
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Scenario comparison
st.markdown("<h2><span class='section-icon'>🔄</span>Scenario Comparison</h2>", unsafe_allow_html=True)

scenarios_df = pd.DataFrame({
    'Scenario': ['🎯 Conservative (99%)', f'⚡ Current ({service_level}%)', '🚀 Aggressive (90%)'],
    'Service Level': ['99%', f'{service_level}%', '90%'],
    'Safety Stock': [
        f"{z_scores[99] * lead_time_demand_std:,.0f}",
        f"{safety_stock:,.0f}",
        f"{z_scores[90] * lead_time_demand_std:,.0f}"
    ],
    'Avg Inventory': [
        f"{(eoq/2) + z_scores[99] * lead_time_demand_std:,.0f}",
        f"{average_inventory:,.0f}",
        f"{(eoq/2) + z_scores[90] * lead_time_demand_std:,.0f}"
    ],
    'Annual Cost': [
        f"€{total_order_cost_annual + ((eoq/2) + z_scores[99] * lead_time_demand_std) * holding_cost_per_unit:,.0f}",
        f"€{total_inventory_cost_annual:,.0f}",
        f"€{total_order_cost_annual + ((eoq/2) + z_scores[90] * lead_time_demand_std) * holding_cost_per_unit:,.0f}"
    ],
    'Stockout Risk': ['1%', f'{100-service_level}%', '10%']
})

st.dataframe(
    scenarios_df,
    use_container_width=True,
    hide_index=True
)

# Divider
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Export
st.markdown("<h2><span class='section-icon'>💾</span>Export Results</h2>", unsafe_allow_html=True)

export_df = pd.DataFrame({
    'Parameter': [
        'Annual Demand', 'Unit Cost', 'Order Cost', 'Holding Cost %',
        'Lead Time', 'Service Level', 'Demand Variability',
        'EOQ', 'Safety Stock', 'Reorder Point', 'Orders/Year',
        'Days Between Orders', 'Average Inventory',
        'Annual Ordering Cost', 'Annual Holding Cost', 'Total Annual Cost'
    ],
    'Value': [
        f"{annual_demand:,.0f} units", f"€{unit_cost:.2f}", f"€{order_cost:.2f}",
        f"{holding_cost_pct}%", f"{lead_time_days} days", f"{service_level}%", f"{demand_variability}%",
        f"{eoq:,.0f} units", f"{safety_stock:,.0f} units", f"{reorder_point:,.0f} units",
        f"{orders_per_year:.1f}", f"{days_between_orders:.1f} days", f"{average_inventory:,.0f} units",
        f"€{total_order_cost_annual:,.0f}", f"€{total_holding_cost_annual:,.0f}",
        f"€{total_inventory_cost_annual:,.0f}"
    ]
})

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv = export_df.to_csv(index=False)

st.download_button(
    label="📥 Download Results (CSV)",
    data=csv,
    file_name=f"eoq_results_{timestamp}.csv",
    mime="text/csv",
    help="Download all inputs and results as CSV file"
)

# Divider
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Author card
st.markdown("""
    <div class='author-card'>
        <h3>👨‍💻 Built by Dennis Schmal</h3>
        <p style='font-size: 16px;'><strong>Supply Chain Digitalization Manager | AI Solutions Builder</strong></p>
        <p style='margin-top: 20px; font-size: 15px;'>
            I build production-ready AI solutions for supply chain operations by day. 
            I teach supply chain professionals to build the same solutions on weekends.
        </p>
        <p style='margin-top: 20px; font-size: 15px;'>
            <strong>🔗 Connect:</strong> 
            <a href='https://dennisschmal.de' target='_blank'>Website</a> • 
            <a href='https://linkedin.com/in/dennis-schmal' target='_blank'>LinkedIn</a> • 
            <a href='https://github.com/dschmahl' target='_blank'>GitHub</a> • 
            <a href='https://youtube.com/@dennisschmal' target='_blank'>YouTube</a>
        </p>
        <p style='margin-top: 24px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 15px;'>
            <strong>🎓 Want to build tools like this?</strong><br>
            Join my 8-week weekend cohorts where supply chain professionals learn to build 
            production-ready AI solutions. No coding experience required.
        </p>
        <p style='margin-top: 16px;'>
            <a href='https://dennisschmal.de' target='_blank' style='background-color: white; color: #0066FF; padding: 12px 28px; border-radius: 10px; text-decoration: none; font-weight: 700; display: inline-block; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: all 0.3s ease;'>
                Learn More →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Stats card
st.markdown("""
    <div class='stats-card'>
        <strong>📊 Tool Usage:</strong> 500+ calculations/month • 
        <strong>⭐ Built in:</strong> 2 hours • 
        <strong>💾 Code:</strong> Open source • 
        <strong>💰 Cost:</strong> Free forever
        <br><br>
        <em>Part of my "Free Supply Chain AI Tools" collection. More tools coming soon.</em>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6B7280; padding: 24px; font-size: 13px;'>
        <p style='margin-bottom: 12px; color: #0A2540; font-weight: 600;'>
            © 2024 Dennis Schmal | Built with Python + Streamlit | 
            <a href='https://github.com/dschmahl/eoq-calculator' target='_blank' style='color: #0066FF; font-weight: 600;'>View Source Code</a>
        </p>
        <p style='font-size: 12px; color: #9CA3AF;'>
            This tool is provided as-is for educational purposes. 
            Always validate results with your organization's specific requirements.
        </p>
    </div>
    """, unsafe_allow_html=True)
