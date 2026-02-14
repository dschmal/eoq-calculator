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

# Custom CSS - Dennis Schmal Brand Style
st.markdown("""
    <style>
    /* Main styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styling */
    h1 {
        color: #0A2540;
        font-weight: 700;
        border-bottom: 3px solid #0066FF;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #0066FF;
        font-weight: 600;
        margin-top: 30px;
    }
    
    h3 {
        color: #0A2540;
        font-weight: 500;
    }
    
    /* Metrics styling */
    .stMetric {
        background: linear-gradient(135deg, #f0f2f6 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #0066FF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stMetric label {
        color: #0A2540;
        font-weight: 600;
    }
    
    .stMetric .metric-value {
        color: #0066FF;
        font-size: 28px;
        font-weight: 700;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #0066FF;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: #e8f5e9;
        border-left: 4px solid #00B894;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0066FF;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #0052CC;
        box-shadow: 0 4px 8px rgba(0,102,255,0.3);
    }
    
    /* Tech badge */
    .tech-badge {
        display: inline-block;
        background-color: #0A2540;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    
    /* Author card */
    .author-card {
        background: linear-gradient(135deg, #0A2540 0%, #0066FF 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .author-card h3 {
        color: white;
        margin-bottom: 10px;
    }
    
    .author-card p {
        color: rgba(255,255,255,0.9);
        margin: 5px 0;
    }
    
    .author-card a {
        color: #FFD700;
        text-decoration: none;
        font-weight: 600;
    }
    
    .author-card a:hover {
        text-decoration: underline;
    }
    
    /* Built by badge */
    .built-by {
        background-color: #f0f2f6;
        border-left: 4px solid #0066FF;
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
    }
    
    /* Deployment info */
    .deploy-info {
        background-color: #e3f2fd;
        border: 1px solid #0066FF;
        border-radius: 8px;
        padding: 12px;
        margin: 10px 0;
        font-size: 13px;
        color: #0A2540;
    }
    </style>
    """, unsafe_allow_html=True)

# Header with personal branding
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 42px; margin-bottom: 5px;'>📦 EOQ Calculator</h1>
        <p style='font-size: 18px; color: #666; margin-bottom: 5px;'>
            <strong>Built by Dennis Schmal</strong> | Supply Chain Digitalization Manager
        </p>
        <p style='font-size: 14px; color: #888;'>
            Optimize inventory decisions with data-driven calculations
        </p>
    </div>
    """, unsafe_allow_html=True)

# Tech stack badges
st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <span class='tech-badge'>Python</span>
        <span class='tech-badge'>Streamlit</span>
        <span class='tech-badge'>Plotly</span>
        <span class='tech-badge'>NumPy</span>
        <span class='tech-badge'>Pandas</span>
    </div>
    """, unsafe_allow_html=True)

# Quick intro box
st.info("""
💡 **What this tool does:** Calculate optimal order quantities, safety stock levels, and reorder points 
to minimize inventory costs while maintaining service levels. Built in 2 hours, deployed to production, 
saving companies thousands in inventory carrying costs.
""")

# Sidebar inputs with better organization
st.sidebar.markdown("## 🎯 Input Parameters")

# Collapsible sections in sidebar
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
        help="Annual cost to store one unit (warehousing, insurance, obsolescence, capital cost)"
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
        help="Probability of NOT having a stockout (95% = 1 stockout per 20 cycles)"
    )
    
    demand_variability = st.slider(
        "Demand Variability (CV %)",
        min_value=5,
        max_value=50,
        value=20,
        step=5,
        help="Coefficient of Variation: How much demand fluctuates (StdDev/Mean × 100)"
    )

# Add deployment info in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div class='deploy-info'>
        <strong>⚡ Live Production Tool</strong><br>
        Built: 2024<br>
        Tech: Python + Streamlit<br>
        Hosted: Streamlit Cloud<br>
        Users: 500+ calculations/month
    </div>
    """, unsafe_allow_html=True)

# Core calculations
holding_cost_per_unit = unit_cost * (holding_cost_pct / 100)
eoq = np.sqrt((2 * annual_demand * order_cost) / holding_cost_per_unit)
daily_demand = annual_demand / 365

# Z-scores for service levels
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

# Derived metrics
orders_per_year = annual_demand / eoq
days_between_orders = 365 / orders_per_year
total_order_cost_annual = orders_per_year * order_cost
average_inventory = (eoq / 2) + safety_stock
total_holding_cost_annual = average_inventory * holding_cost_per_unit
total_inventory_cost_annual = total_order_cost_annual + total_holding_cost_annual

# Display results
st.markdown("## 📈 Optimization Results")

# Key metrics in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Economic Order Quantity",
        f"{eoq:,.0f}",
        help="Optimal order size that minimizes total cost"
    )
    st.caption("units per order")

with col2:
    st.metric(
        "Safety Stock",
        f"{safety_stock:,.0f}",
        help=f"Buffer for {service_level}% service level"
    )
    st.caption("units buffer")

with col3:
    st.metric(
        "Reorder Point",
        f"{reorder_point:,.0f}",
        help="Trigger new order at this inventory level"
    )
    st.caption("units trigger")

with col4:
    st.metric(
        "Order Frequency",
        f"{orders_per_year:.1f}",
        help="Orders needed per year"
    )
    st.caption("orders/year")

# Business impact callout
st.markdown("### 💰 Business Impact")

col_impact1, col_impact2, col_impact3 = st.columns(3)

with col_impact1:
    st.metric(
        "Total Annual Cost",
        f"€{total_inventory_cost_annual:,.0f}",
        help="Total inventory management cost"
    )
    st.caption("ordering + holding")

with col_impact2:
    st.metric(
        "Average Inventory",
        f"{average_inventory:,.0f}",
        help="Average units in stock"
    )
    st.caption("units on hand")

with col_impact3:
    st.metric(
        "Days Between Orders",
        f"{days_between_orders:.0f}",
        help="Ordering cycle length"
    )
    st.caption("days cycle")

# Cost breakdown visualization
st.markdown("### 📊 Cost Breakdown Analysis")

fig_costs = go.Figure()

fig_costs.add_trace(go.Bar(
    name='Ordering Costs',
    x=['Annual Costs'],
    y=[total_order_cost_annual],
    marker_color='#0066FF',
    text=[f'€{total_order_cost_annual:,.0f}'],
    textposition='auto',
))

fig_costs.add_trace(go.Bar(
    name='Holding Costs',
    x=['Annual Costs'],
    y=[total_holding_cost_annual],
    marker_color='#00B894',
    text=[f'€{total_holding_cost_annual:,.0f}'],
    textposition='auto',
))

fig_costs.update_layout(
    title=f'Total Annual Inventory Cost: €{total_inventory_cost_annual:,.0f}',
    barmode='stack',
    height=350,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(family="Arial, sans-serif", size=12, color="#0A2540"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig_costs, use_container_width=True)

# Key insights
col_insight1, col_insight2 = st.columns(2)

with col_insight1:
    st.info(f"""
    **Ordering Strategy:**
    - Order **{eoq:,.0f} units** every **{days_between_orders:.0f} days**
    - Equals **{orders_per_year:.1f} orders per year**
    - Ordering cost: **€{total_order_cost_annual:,.0f}/year**
    """)

with col_insight2:
    st.success(f"""
    **Inventory Management:**
    - Maintain **{safety_stock:,.0f} units** safety stock
    - Reorder when inventory hits **{reorder_point:,.0f} units**
    - Holding cost: **€{total_holding_cost_annual:,.0f}/year**
    """)

# Inventory simulation
st.markdown("### 📉 Inventory Level Simulation")

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
    name='Inventory Level',
    line=dict(color='#0066FF', width=3),
    fill='tozeroy',
    fillcolor='rgba(0, 102, 255, 0.1)'
))

fig_sim.add_hline(
    y=reorder_point,
    line_dash="dash",
    line_color="#FF6B35",
    line_width=2,
    annotation_text=f"Reorder Point: {reorder_point:,.0f} units",
    annotation_position="right"
)

fig_sim.add_hline(
    y=safety_stock,
    line_dash="dot",
    line_color="#DC143C",
    line_width=2,
    annotation_text=f"Safety Stock: {safety_stock:,.0f} units",
    annotation_position="right"
)

fig_sim.update_layout(
    title='Inventory Levels Over Time (2 Order Cycles)',
    xaxis_title='Days',
    yaxis_title='Inventory (units)',
    height=400,
    hovermode='x unified',
    font=dict(family="Arial, sans-serif", size=12, color="#0A2540"),
    plot_bgcolor='rgba(248,249,250,0.5)',
    paper_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig_sim, use_container_width=True)

# Technical details (expandable)
with st.expander("🔧 Technical Implementation Details"):
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

# Scenario comparison
st.markdown("### 🔄 Scenario Comparison")

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

st.dataframe(
    scenarios_df,
    use_container_width=True,
    hide_index=True
)

# Export functionality
st.markdown("### 💾 Export Results")

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

# Author card with personal branding
st.markdown("---")
st.markdown("""
    <div class='author-card'>
        <h3>👨‍💻 Built by Dennis Schmal</h3>
        <p><strong>Supply Chain Digitalization Manager | AI Solutions Builder</strong></p>
        <p style='margin-top: 15px;'>
            I build production-ready AI solutions for supply chain operations by day. 
            I teach supply chain professionals to build the same solutions on weekends.
        </p>
        <p style='margin-top: 15px;'>
            <strong>🔗 Connect:</strong> 
            <a href='https://dennisschmal.de' target='_blank'>Website</a> • 
            <a href='https://linkedin.com/in/dennis-schmal' target='_blank'>LinkedIn</a> • 
            <a href='https://github.com/dschmahl' target='_blank'>GitHub</a> • 
            <a href='https://youtube.com/@dennisschmal' target='_blank'>YouTube</a>
        </p>
        <p style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2);'>
            <strong>🎓 Want to build tools like this?</strong><br>
            Join my 8-week weekend cohorts where supply chain professionals learn to build 
            production-ready AI solutions. No coding experience required.
        </p>
        <p style='margin-top: 10px;'>
            <a href='https://dennisschmal.de' target='_blank' style='background-color: white; color: #0066FF; padding: 8px 20px; border-radius: 6px; text-decoration: none; font-weight: 700;'>
                Learn More →
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Usage stats and social proof
st.markdown("""
    <div class='built-by'>
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
    <div style='text-align: center; color: #666; padding: 20px; font-size: 13px;'>
        <p style='margin-bottom: 10px;'>
            © 2024 Dennis Schmal | Built with Python + Streamlit | 
            <a href='https://github.com/dschmahl/eoq-calculator' target='_blank' style='color: #0066FF;'>View Source Code</a>
        </p>
        <p style='font-size: 11px; color: #999;'>
            This tool is provided as-is for educational purposes. 
            Always validate results with your organization's specific requirements.
        </p>
    </div>
    """, unsafe_allow_html=True)
