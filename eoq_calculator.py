"""
EOQ Calculator by Dennis Schmal
Supply Chain Digitalization Manager | AI Solutions Builder

Professional dashboard for inventory optimization.
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

# Professional Dashboard CSS - Clean BI Tool Aesthetic
st.markdown("""
    <style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main container */
    .main {
        background-color: #F5F7FA;
        padding: 1rem;
    }
    
    /* Dashboard card wrapper */
    .dashboard-card {
        background: white;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
        border: 1px solid #E2E8F0;
    }
    
    .dashboard-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
    }
    
    /* Headers */
    h1 {
        color: #1A202C !important;
        font-weight: 700 !important;
        font-size: 32px !important;
        margin-bottom: 8px !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #2D3748 !important;
        font-weight: 600 !important;
        font-size: 20px !important;
        margin-top: 0 !important;
        margin-bottom: 20px !important;
        letter-spacing: -0.3px;
    }
    
    h3 {
        color: #4A5568 !important;
        font-weight: 500 !important;
        font-size: 16px !important;
    }
    
    /* Metric cards - Dashboard style */
    [data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    
    /* Metric labels */
    [data-testid="stMetricLabel"] {
        color: #718096 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Metric values */
    [data-testid="stMetricValue"] {
        color: #2B6CB0 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
    }
    
    /* Caption text */
    .metric-caption {
        color: #A0AEC0;
        font-size: 12px;
        font-weight: 400;
        margin-top: 4px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    
    section[data-testid="stSidebar"] h2 {
        color: #2D3748 !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin-bottom: 16px !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: #4A5568 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    
    /* Info boxes */
    [data-baseweb="notification"] {
        background: #EBF8FF;
        border-left: 4px solid #3182CE;
        border-radius: 6px;
        padding: 16px;
        border-top: 1px solid #BEE3F8;
        border-right: 1px solid #BEE3F8;
        border-bottom: 1px solid #BEE3F8;
    }
    
    [data-baseweb="notification"] p {
        color: #2C5282 !important;
        font-size: 14px;
        line-height: 1.6;
    }
    
    /* Success boxes */
    .element-container div[data-baseweb="notification"][kind="success"] {
        background: #F0FFF4;
        border-left: 4px solid #38A169;
        border-top: 1px solid #C6F6D5;
        border-right: 1px solid #C6F6D5;
        border-bottom: 1px solid #C6F6D5;
    }
    
    .element-container div[data-baseweb="notification"][kind="success"] p {
        color: #22543D !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #3182CE;
        color: white !important;
        font-weight: 500;
        border-radius: 6px;
        border: none;
        padding: 10px 24px;
        font-size: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08);
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #2C5282;
        box-shadow: 0 4px 6px rgba(0,0,0,0.12), 0 2px 4px rgba(0,0,0,0.08);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: #38A169;
        color: white !important;
        font-weight: 500;
        border-radius: 6px;
        padding: 10px 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    
    .stDownloadButton > button:hover {
        background: #2F855A;
    }
    
    /* Tables */
    .dataframe {
        font-size: 13px;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        overflow: hidden;
    }
    
    .dataframe th {
        background: #F7FAFC !important;
        color: #4A5568 !important;
        font-weight: 600 !important;
        padding: 12px !important;
        border-bottom: 2px solid #E2E8F0 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dataframe td {
        color: #2D3748 !important;
        padding: 12px !important;
        border-bottom: 1px solid #F7FAFC !important;
    }
    
    .dataframe tr:hover td {
        background-color: #F7FAFC !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        color: #2D3748 !important;
        font-weight: 500;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 12px 16px;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F7FAFC;
    }
    
    /* Section headers with underline */
    .section-header {
        color: #2D3748;
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 2px solid #E2E8F0;
    }
    
    /* Stats badge */
    .stats-badge {
        display: inline-block;
        background: #EDF2F7;
        color: #4A5568;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
        margin: 4px;
        border: 1px solid #E2E8F0;
    }
    
    /* Author card - Professional */
    .author-card {
        background: linear-gradient(135deg, #2B6CB0 0%, #3182CE 100%);
        color: white;
        padding: 28px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
        margin: 24px 0;
    }
    
    .author-card h3 {
        color: white !important;
        font-size: 22px !important;
        margin-bottom: 12px !important;
    }
    
    .author-card p {
        color: rgba(255,255,255,0.95);
        line-height: 1.6;
        font-size: 14px;
    }
    
    .author-card a {
        color: #FED7D7;
        font-weight: 500;
    }
    
    .author-card a:hover {
        color: white;
        text-decoration: underline;
    }
    
    /* Code blocks */
    code {
        background: #EDF2F7;
        color: #2B6CB0;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 13px;
    }
    
    pre {
        background: #1A202C;
        border: 1px solid #2D3748;
        padding: 16px;
        border-radius: 6px;
    }
    
    pre code {
        color: #E2E8F0;
        background: transparent;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        h1 { font-size: 24px !important; }
        h2 { font-size: 18px !important; }
        [data-testid="stMetricValue"] { font-size: 24px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
    <div style='background: white; padding: 24px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid #E2E8F0;'>
        <h1 style='margin-bottom: 8px;'>📦 EOQ Calculator</h1>
        <p style='color: #718096; font-size: 14px; margin-bottom: 4px;'>
            <strong style='color: #2D3748;'>Dennis Schmal</strong> | Supply Chain Digitalization Manager
        </p>
        <p style='color: #A0AEC0; font-size: 13px; margin: 0;'>
            Professional inventory optimization tool
        </p>
    </div>
    """, unsafe_allow_html=True)

# Quick stats
st.markdown("""
    <div style='background: white; padding: 16px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid #E2E8F0;'>
        <span class='stats-badge'>⚡ Built in 2 hours</span>
        <span class='stats-badge'>🚀 Production-ready</span>
        <span class='stats-badge'>💾 Open source</span>
        <span class='stats-badge'>💰 Free forever</span>
        <span class='stats-badge'>📊 500+ calculations/month</span>
    </div>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## ⚙️ Input Parameters")

with st.sidebar.expander("📊 Demand & Costs", expanded=True):
    annual_demand = st.number_input(
        "Annual Demand (units)",
        min_value=100,
        max_value=10000000,
        value=50000,
        step=1000
    )
    
    unit_cost = st.number_input(
        "Unit Cost (€)",
        min_value=0.01,
        max_value=100000.0,
        value=50.0,
        step=1.0
    )
    
    order_cost = st.number_input(
        "Order/Setup Cost (€)",
        min_value=1.0,
        max_value=50000.0,
        value=200.0,
        step=10.0
    )
    
    holding_cost_pct = st.slider(
        "Holding Cost (%)",
        min_value=5,
        max_value=50,
        value=20,
        step=1
    )

with st.sidebar.expander("⏱️ Lead Time & Service", expanded=True):
    lead_time_days = st.number_input(
        "Lead Time (days)",
        min_value=1,
        max_value=365,
        value=14,
        step=1
    )
    
    service_level = st.slider(
        "Service Level (%)",
        min_value=85,
        max_value=99,
        value=95,
        step=1
    )
    
    demand_variability = st.slider(
        "Demand Variability (%)",
        min_value=5,
        max_value=50,
        value=20,
        step=5
    )

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

# Key Metrics Section
st.markdown("<p class='section-header'>📈 Optimization Results</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Economic Order Quantity",
        f"{eoq:,.0f}"
    )
    st.markdown("<p class='metric-caption'>units per order</p>", unsafe_allow_html=True)

with col2:
    st.metric(
        "Safety Stock",
        f"{safety_stock:,.0f}"
    )
    st.markdown("<p class='metric-caption'>units buffer</p>", unsafe_allow_html=True)

with col3:
    st.metric(
        "Reorder Point",
        f"{reorder_point:,.0f}"
    )
    st.markdown("<p class='metric-caption'>units trigger</p>", unsafe_allow_html=True)

with col4:
    st.metric(
        "Order Frequency",
        f"{orders_per_year:.1f}"
    )
    st.markdown("<p class='metric-caption'>orders/year</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Business Impact
st.markdown("<p class='section-header'>💰 Business Impact</p>", unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    st.metric(
        "Total Annual Cost",
        f"€{total_inventory_cost_annual:,.0f}"
    )
    st.markdown("<p class='metric-caption'>ordering + holding</p>", unsafe_allow_html=True)

with col_b2:
    st.metric(
        "Average Inventory",
        f"{average_inventory:,.0f}"
    )
    st.markdown("<p class='metric-caption'>units on hand</p>", unsafe_allow_html=True)

with col_b3:
    st.metric(
        "Days Between Orders",
        f"{days_between_orders:.0f}"
    )
    st.markdown("<p class='metric-caption'>days cycle</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts Section
st.markdown("<p class='section-header'>📊 Analysis & Insights</p>", unsafe_allow_html=True)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    # Cost Breakdown Chart
    st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid #E2E8F0; margin-bottom: 20px;'>
            <h3 style='color: #2D3748; font-size: 16px; font-weight: 600; margin-bottom: 16px;'>Cost Breakdown</h3>
        </div>
    """, unsafe_allow_html=True)
    
    fig_costs = go.Figure()
    
    fig_costs.add_trace(go.Bar(
        name='Ordering',
        x=['Annual Costs'],
        y=[total_order_cost_annual],
        marker=dict(color='#3182CE'),
        text=[f'€{total_order_cost_annual:,.0f}'],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Roboto'),
        hovertemplate='Ordering: €%{y:,.0f}<extra></extra>'
    ))
    
    fig_costs.add_trace(go.Bar(
        name='Holding',
        x=['Annual Costs'],
        y=[total_holding_cost_annual],
        marker=dict(color='#63B3ED'),
        text=[f'€{total_holding_cost_annual:,.0f}'],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Roboto'),
        hovertemplate='Holding: €%{y:,.0f}<extra></extra>'
    ))
    
    fig_costs.update_layout(
        barmode='stack',
        height=320,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12, color='#4A5568')
        ),
        font=dict(family="Roboto", size=12, color="#4A5568"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F7FAFC',
            title='Cost (€)',
            title_font=dict(size=12, color='#718096')
        ),
        margin=dict(l=50, r=20, t=40, b=20),
        title=dict(
            text=f'Total: €{total_inventory_cost_annual:,.0f}/year',
            font=dict(size=14, color='#2D3748', family='Roboto'),
            x=0.5,
            xanchor='center'
        )
    )
    
    st.plotly_chart(fig_costs, use_container_width=True, config={'displayModeBar': False})

with col_chart2:
    # Inventory Simulation
    st.markdown("""
        <div style='background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); border: 1px solid #E2E8F0; margin-bottom: 20px;'>
            <h3 style='color: #2D3748; font-size: 16px; font-weight: 600; margin-bottom: 16px;'>Inventory Level Simulation</h3>
        </div>
    """, unsafe_allow_html=True)
    
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
        name='Inventory',
        line=dict(color='#3182CE', width=3),
        fill='tozeroy',
        fillcolor='rgba(49,130,206,0.1)',
        hovertemplate='Day %{x:.0f}<br>Inventory: %{y:,.0f}<extra></extra>'
    ))
    
    fig_sim.add_hline(
        y=reorder_point,
        line_dash="dash",
        line_color="#F56565",
        line_width=2,
        annotation=dict(
            text=f"Reorder: {reorder_point:,.0f}",
            font=dict(size=11, color='#F56565'),
            xanchor='left'
        )
    )
    
    fig_sim.add_hline(
        y=safety_stock,
        line_dash="dot",
        line_color="#ED8936",
        line_width=2,
        annotation=dict(
            text=f"Safety: {safety_stock:,.0f}",
            font=dict(size=11, color='#ED8936'),
            xanchor='left'
        )
    )
    
    fig_sim.update_layout(
        height=320,
        hovermode='x unified',
        font=dict(family="Roboto", size=12, color="#4A5568"),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='#F7FAFC',
            title='Days',
            title_font=dict(size=12, color='#718096')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F7FAFC',
            title='Units',
            title_font=dict(size=12, color='#718096')
        ),
        margin=dict(l=50, r=20, t=20, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig_sim, use_container_width=True, config={'displayModeBar': False})

# Insights
col_i1, col_i2 = st.columns(2)

with col_i1:
    st.info(f"""
**📦 Ordering Strategy**

• Order **{eoq:,.0f} units** every **{days_between_orders:.0f} days**  
• Equals **{orders_per_year:.1f} orders per year**  
• Annual ordering cost: **€{total_order_cost_annual:,.0f}**
    """)

with col_i2:
    st.success(f"""
**✅ Inventory Management**

• Maintain **{safety_stock:,.0f} units** safety stock  
• Reorder when inventory hits **{reorder_point:,.0f} units**  
• Annual holding cost: **€{total_holding_cost_annual:,.0f}**
    """)

st.markdown("<br>", unsafe_allow_html=True)

# Scenario Comparison
st.markdown("<p class='section-header'>🔄 Scenario Comparison</p>", unsafe_allow_html=True)

scenarios_df = pd.DataFrame({
    'Scenario': ['Conservative (99%)', f'Current ({service_level}%)', 'Aggressive (90%)'],
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

st.dataframe(scenarios_df, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# Technical Details
with st.expander("🔧 Technical Implementation"):
    st.markdown("""
    ### Formulas
    
    **EOQ:** `√(2 × D × S / H)` where D=demand, S=order cost, H=holding cost
    
    **Safety Stock:** `Z × σ × √L` where Z=service level, σ=demand std dev, L=lead time
    
    **Tech Stack:** Python • NumPy • Pandas • Plotly • Streamlit
    
    **Code:** [GitHub](https://github.com/dschmahl) | Built in 2 hours | Open source
    """)

# Export
st.markdown("<p class='section-header'>💾 Export Results</p>", unsafe_allow_html=True)

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
    mime="text/csv"
)

st.markdown("<br>", unsafe_allow_html=True)

# Author Section
st.markdown("""
    <div class='author-card'>
        <h3>Built by Dennis Schmal</h3>
        <p style='font-size: 15px; margin-bottom: 16px;'>
            <strong>Supply Chain Digitalization Manager | AI Solutions Builder</strong>
        </p>
        <p>
            I build production-ready AI solutions for supply chain operations by day. 
            I teach supply chain professionals to build the same solutions on weekends.
        </p>
        <p style='margin-top: 16px;'>
            <strong>Connect:</strong> 
            <a href='https://dennisschmal.de'>Website</a> • 
            <a href='https://linkedin.com/in/dennis-schmal'>LinkedIn</a> • 
            <a href='https://github.com/dschmahl'>GitHub</a> • 
            <a href='https://youtube.com/@dennisschmal'>YouTube</a>
        </p>
        <p style='margin-top: 16px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.3);'>
            <strong>🎓 Want to build tools like this?</strong> Join my 8-week weekend cohorts.
            No coding experience required.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #A0AEC0; padding: 16px; font-size: 12px;'>
        <p style='color: #4A5568; font-weight: 500; margin-bottom: 8px;'>
            © 2024 Dennis Schmal | Built with Python + Streamlit | 
            <a href='https://github.com/dschmahl/eoq-calculator' style='color: #3182CE;'>Source Code</a>
        </p>
        <p style='color: #CBD5E0;'>
            This tool is provided as-is for educational purposes.
        </p>
    </div>
    """, unsafe_allow_html=True)
