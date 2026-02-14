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

# Dark theme CSS - matching stock peer analysis style
st.markdown("""
    <style>
    /* Dark theme - matching reference */
    .main {
        background-color: #0E1117;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Headers - white text */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    h1 {
        font-size: 28px !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 18px !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Subtitle text */
    .subtitle {
        color: #A0AEC0;
        font-size: 14px;
        margin-bottom: 2rem;
    }
    
    /* Metric cards - dark theme */
    [data-testid="stMetric"] {
        background-color: #1A202C;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #2D3748;
    }
    
    [data-testid="stMetricLabel"] {
        color: ##FFFFFF !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase;
    }
    
    [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    /* Captions */
    .stCaptionContainer p, [data-testid="stCaptionContainer"] p {
        color: #718096 !important;
        font-size: 12px !important;
    }
    
    /* Sidebar - dark */
    section[data-testid="stSidebar"] {
        background-color: #1A202C;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #1A202C;
    }
    
    /* Sidebar text - white/light gray */
    section[data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
        font-size: 16px !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid #2D3748 !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #E2E8F0 !important;
        font-size: 14px !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }
    
    section[data-testid="stSidebar"] input {
        background-color: #2D3748 !important;
        color: #FFFFFF !important;
        border: 1px solid #4A5568 !important;
    }
    
    section[data-testid="stSidebar"] [data-baseweb="slider"] {
        margin-top: 0.5rem !important;
    }
    
    /* Pills/badges - like stock tickers */
    .metric-pill {
        display: inline-block;
        background-color: #2B6CB0;
        color: white;
        padding: 0.4rem 0.9rem;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .info-pill {
        display: inline-block;
        background-color: #2D3748;
        color: #A0AEC0;
        padding: 0.4rem 0.8rem;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    /* Info/Success boxes - dark theme */
    .stAlert {
        background-color: #1A365D !important;
        border-left: 4px solid #3182CE !important;
        border-radius: 6px !important;
    }
    
    [data-baseweb="notification"] p {
        color: #90CDF4 !important;
    }
    
    .element-container div[kind="success"] {
        background-color: #1C4532 !important;
        border-left: 4px solid #38A169 !important;
    }
    
    .element-container div[kind="success"] p {
        color: #9AE6B4 !important;
    }
    
    /* Tables - dark theme */
    .dataframe {
        background-color: #1A202C !important;
        color: #E2E8F0 !important;
    }
    
    .dataframe th {
        background-color: #2D3748 !important;
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    
    .dataframe td {
        background-color: #1A202C !important;
        color: #E2E8F0 !important;
        border-bottom: 1px solid #2D3748 !important;
    }
    
    .dataframe tr:hover td {
        background-color: #2D3748 !important;
    }
    
    /* Buttons - dark theme */
    .stButton > button {
        background-color: #3182CE !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
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
        font-weight: 600 !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #2F855A !important;
    }
    
    /* Expander - dark theme */
    .streamlit-expanderHeader {
        background-color: #1A202C !important;
        color: #E2E8F0 !important;
        border: 1px solid #2D3748 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #2D3748 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("# 📦 EOQ Calculator")
st.markdown("<p class='subtitle'>Optimize inventory decisions with data-driven calculations</p>", unsafe_allow_html=True)

# Pills showing key info
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <span class='metric-pill'>EOQ Model</span>
    <span class='metric-pill'>Safety Stock</span>
    <span class='metric-pill'>Reorder Point</span>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## ⚙️ Input Parameters")

st.sidebar.markdown("### 📊 Demand & Costs")
annual_demand = st.sidebar.number_input(
    "Annual Demand (units)",
    min_value=100,
    max_value=10000000,
    value=50000,
    step=1000
)

unit_cost = st.sidebar.number_input(
    "Unit Cost (€)",
    min_value=0.01,
    max_value=100000.0,
    value=50.0,
    step=1.0
)

order_cost = st.sidebar.number_input(
    "Order Cost (€)",
    min_value=1.0,
    max_value=50000.0,
    value=200.0,
    step=10.0
)

holding_cost_pct = st.sidebar.slider(
    "Holding Cost (%)",
    min_value=5,
    max_value=50,
    value=20,
    step=1
)

st.sidebar.markdown("### ⏱️ Lead Time & Service")

lead_time_days = st.sidebar.number_input(
    "Lead Time (days)",
    min_value=1,
    max_value=365,
    value=14,
    step=1
)

service_level = st.sidebar.slider(
    "Service Level (%)",
    min_value=85,
    max_value=99,
    value=95,
    step=1
)

demand_variability = st.sidebar.slider(
    "Demand Variability (%)",
    min_value=5,
    max_value=50,
    value=20,
    step=5
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='color: #A0AEC0; font-size: 12px; padding: 1rem 0;'>
    <strong style='color: #E2E8F0;'>Built by Dennis Schmal</strong><br>
    Supply Chain Digitalization Manager<br><br>
    <a href='https://dennisschmal.de' style='color: #3182CE;'>Website</a> • 
    <a href='https://github.com/dschmal' style='color: #3182CE;'>GitHub</a>
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

# Key metrics
st.markdown("## 📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("EOQ", f"{eoq:,.0f}")
    st.caption("units per order")

with col2:
    st.metric("Safety Stock", f"{safety_stock:,.0f}")
    st.caption("units buffer")

with col3:
    st.metric("Reorder Point", f"{reorder_point:,.0f}")
    st.caption("units trigger")

with col4:
    st.metric("Order Frequency", f"{orders_per_year:.1f}")
    st.caption("orders/year")

st.markdown("")

# Business impact
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

# Main chart - Inventory simulation with multiple scenarios
st.markdown("## 📊 Inventory Level Analysis")

time_points = np.linspace(0, 3 * days_between_orders, 200)

# Create data for current scenario and alternatives
scenarios = {
    'Current': {'safety': safety_stock, 'color': '#3B82F6'},  # Blue
    'Conservative': {'safety': z_scores[99] * lead_time_demand_std, 'color': '#10B981'},  # Green
    'Aggressive': {'safety': z_scores[90] * lead_time_demand_std, 'color': '#F59E0B'},  # Yellow
}

fig_main = go.Figure()

for scenario_name, scenario_data in scenarios.items():
    inventory_levels = []
    scenario_safety = scenario_data['safety']
    scenario_reorder = average_lead_time_demand + scenario_safety
    
    for t in time_points:
        days_in_cycle = t % days_between_orders
        if days_in_cycle < lead_time_days:
            inventory = eoq + scenario_safety - (daily_demand * (days_between_orders - lead_time_days + days_in_cycle))
        else:
            inventory = eoq + scenario_safety - (daily_demand * (days_in_cycle - lead_time_days))
        inventory_levels.append(max(scenario_safety, inventory))
    
    fig_main.add_trace(go.Scatter(
        x=time_points,
        y=inventory_levels,
        mode='lines',
        name=scenario_name,
        line=dict(color=scenario_data['color'], width=2),
        hovertemplate='%{y:,.0f} units<extra></extra>'
    ))

# Add reorder point line
fig_main.add_hline(
    y=reorder_point,
    line_dash="dash",
    line_color="#EF4444",
    line_width=1.5,
    annotation_text="Reorder Point",
    annotation_position="right",
    annotation=dict(font=dict(size=11, color='#EF4444'))
)

fig_main.update_layout(
    height=400,
    plot_bgcolor='#0E1117',
    paper_bgcolor='#0E1117',
    font=dict(size=12, color='#E2E8F0'),
    xaxis=dict(
        showgrid=True,
        gridcolor='#2D3748',
        gridwidth=0.5,
        title='Days',
        title_font=dict(color='#A0AEC0')
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#2D3748',
        gridwidth=0.5,
        title='Inventory (units)',
        title_font=dict(color='#A0AEC0')
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color='#E2E8F0')
    ),
    margin=dict(l=60, r=40, t=60, b=60),
    hovermode='x unified'
)

st.plotly_chart(fig_main, use_container_width=True, config={'displayModeBar': False})

st.markdown("")

# Grid of smaller charts - 2x2 layout
st.markdown("## 📊 Detailed Analysis")

col_c1, col_c2 = st.columns(2)

with col_c1:
    st.markdown("**Cost Breakdown**")
    
    fig_costs = go.Figure()
    
    categories = ['Ordering', 'Holding']
    values = [total_order_cost_annual, total_holding_cost_annual]
    colors = ['#3B82F6', '#10B981']
    
    fig_costs.add_trace(go.Bar(
        x=categories,
        y=values,
        marker=dict(color=colors),
        text=[f'€{v:,.0f}' for v in values],
        textposition='inside',
        textfont=dict(color='white', size=14),
        hovertemplate='%{x}: €%{y:,.0f}<extra></extra>'
    ))
    
    fig_costs.update_layout(
        height=300,
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font=dict(size=12, color='#E2E8F0'),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2D3748',
            gridwidth=0.5,
            title='Cost (€)',
            title_font=dict(color='#A0AEC0')
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig_costs, use_container_width=True, config={'displayModeBar': False})

with col_c2:
    st.markdown("**Cost Impact by Service Level**")
    
    service_levels = [85, 90, 95, 99]
    costs = []
    
    for sl in service_levels:
        z = z_scores[sl]
        ss = z * lead_time_demand_std
        avg_inv = (eoq / 2) + ss
        total_cost = total_order_cost_annual + (avg_inv * holding_cost_per_unit)
        costs.append(total_cost)
    
    fig_service = go.Figure()
    
    fig_service.add_trace(go.Scatter(
        x=service_levels,
        y=costs,
        mode='lines+markers',
        line=dict(color='#F59E0B', width=3),
        marker=dict(size=8, color='#F59E0B'),
        hovertemplate='%{x}%: €%{y:,.0f}<extra></extra>'
    ))
    
    fig_service.update_layout(
        height=300,
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font=dict(size=12, color='#E2E8F0'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#2D3748',
            gridwidth=0.5,
            title='Service Level (%)',
            title_font=dict(color='#A0AEC0')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2D3748',
            gridwidth=0.5,
            title='Total Cost (€)',
            title_font=dict(color='#A0AEC0')
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig_service, use_container_width=True, config={'displayModeBar': False})

st.markdown("")

col_c3, col_c4 = st.columns(2)

with col_c3:
    st.markdown("**Order Quantity Impact**")
    
    # Show different order quantities
    order_qtys = np.linspace(eoq * 0.5, eoq * 1.5, 50)
    total_costs = []
    
    for qty in order_qtys:
        orders = annual_demand / qty
        order_cost_total = orders * order_cost
        avg_inv = (qty / 2) + safety_stock
        holding_cost_total = avg_inv * holding_cost_per_unit
        total_costs.append(order_cost_total + holding_cost_total)
    
    fig_qty = go.Figure()
    
    # Total cost curve
    fig_qty.add_trace(go.Scatter(
        x=order_qtys,
        y=total_costs,
        mode='lines',
        name='Total Cost',
        line=dict(color='#8B5CF6', width=3),
        fill='tozeroy',
        fillcolor='rgba(139, 92, 246, 0.1)',
        hovertemplate='Qty: %{x:,.0f}<br>Cost: €%{y:,.0f}<extra></extra>'
    ))
    
    # Optimal point
    fig_qty.add_vline(
        x=eoq,
        line_dash="dash",
        line_color='#3B82F6',
        line_width=2,
        annotation_text=f"EOQ: {eoq:,.0f}",
        annotation_position="top",
        annotation=dict(font=dict(size=11, color='#3B82F6'))
    )
    
    fig_qty.update_layout(
        height=300,
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font=dict(size=12, color='#E2E8F0'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#2D3748',
            gridwidth=0.5,
            title='Order Quantity',
            title_font=dict(color='#A0AEC0')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2D3748',
            gridwidth=0.5,
            title='Total Cost (€)',
            title_font=dict(color='#A0AEC0')
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig_qty, use_container_width=True, config={'displayModeBar': False})

with col_c4:
    st.markdown("**Monthly Demand Pattern**")
    
    # Simulate monthly demand with variability
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_avg = annual_demand / 12
    np.random.seed(42)
    monthly_demand = monthly_avg + np.random.normal(0, monthly_avg * (demand_variability/100), 12)
    monthly_demand = np.maximum(monthly_demand, 0)
    
    fig_monthly = go.Figure()
    
    fig_monthly.add_trace(go.Bar(
        x=months,
        y=monthly_demand,
        marker=dict(
            color=monthly_demand,
            colorscale='Viridis',
            showscale=False
        ),
        hovertemplate='%{x}: %{y:,.0f} units<extra></extra>'
    ))
    
    # Average line
    fig_monthly.add_hline(
        y=monthly_avg,
        line_dash="dash",
        line_color='#EF4444',
        line_width=1.5,
        annotation_text=f"Avg: {monthly_avg:,.0f}",
        annotation_position="right",
        annotation=dict(font=dict(size=10, color='#EF4444'))
    )
    
    fig_monthly.update_layout(
        height=300,
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font=dict(size=12, color='#E2E8F0'),
        xaxis=dict(
            showgrid=False,
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#2D3748',
            gridwidth=0.5,
            title='Demand (units)',
            title_font=dict(color='#A0AEC0')
        ),
        margin=dict(l=60, r=20, t=20, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})

st.markdown("")

# Insights
col_i1, col_i2 = st.columns(2)

with col_i1:
    st.info(f"""
**📦 Ordering Strategy**

• Order **{eoq:,.0f} units** every **{days_between_orders:.0f} days**  
• Frequency: **{orders_per_year:.1f} orders/year**  
• Ordering cost: **€{total_order_cost_annual:,.0f}/year**
    """)

with col_i2:
    st.success(f"""
**✅ Inventory Management**

• Safety stock: **{safety_stock:,.0f} units**  
• Reorder at: **{reorder_point:,.0f} units**  
• Holding cost: **€{total_holding_cost_annual:,.0f}/year**
    """)

st.markdown("")

# Scenario table
st.markdown("## 🔄 Scenario Comparison")

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
    ]
})

st.dataframe(scenarios_df, use_container_width=True, hide_index=True)

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

# Technical details
with st.expander("🔧 Technical Details"):
    st.markdown("""
    **Formulas:**
    - EOQ = √(2 × D × S / H)
    - Safety Stock = Z × σ × √L  
    - Reorder Point = (Daily Demand × Lead Time) + Safety Stock
    
    **Tech Stack:** Python • NumPy • Pandas • Plotly • Streamlit
    
    **Built by Dennis Schmal** | [GitHub](https://github.com/dschmahl) • [Website](https://dennisschmal.de)
    """)
