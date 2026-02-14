"""
EOQ & Inventory Optimization Calculator
Built by Dennis Schmal | Supply Chain Digitalization Manager

Calculate optimal order quantities, safety stock, and reorder points
for better inventory management.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="EOQ Calculator - Dennis Schmal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #0A2540;
    }
    h2 {
        color: #0066FF;
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f0f2f6;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("📦 EOQ & Inventory Optimization Calculator")
st.markdown("""
Calculate Economic Order Quantity (EOQ), Safety Stock, and Reorder Points 
to optimize your inventory management and reduce costs.
""")

# Sidebar inputs
st.sidebar.header("📊 Input Parameters")

st.sidebar.subheader("Demand & Costs")
annual_demand = st.sidebar.number_input(
    "Annual Demand (units/year)",
    min_value=100,
    max_value=10000000,
    value=50000,
    step=1000,
    help="Total units expected to be sold in a year"
)

unit_cost = st.sidebar.number_input(
    "Unit Cost (€)",
    min_value=0.01,
    max_value=100000.0,
    value=50.0,
    step=1.0,
    help="Cost per unit of inventory"
)

order_cost = st.sidebar.number_input(
    "Order Cost (€)",
    min_value=1.0,
    max_value=50000.0,
    value=200.0,
    step=10.0,
    help="Fixed cost per order (admin, shipping, processing)"
)

holding_cost_pct = st.sidebar.slider(
    "Holding Cost (% of unit cost per year)",
    min_value=5,
    max_value=50,
    value=20,
    step=1,
    help="Annual cost to hold one unit in inventory as % of unit cost"
)

st.sidebar.subheader("Lead Time & Service Level")

lead_time_days = st.sidebar.number_input(
    "Lead Time (days)",
    min_value=1,
    max_value=365,
    value=14,
    step=1,
    help="Time between placing order and receiving it"
)

service_level = st.sidebar.slider(
    "Service Level (%)",
    min_value=85,
    max_value=99,
    value=95,
    step=1,
    help="Probability of not running out of stock"
)

demand_variability = st.sidebar.slider(
    "Demand Variability (Coefficient of Variation %)",
    min_value=5,
    max_value=50,
    value=20,
    step=5,
    help="How much demand varies (CV = Std Dev / Mean)"
)

# Calculations
st.header("📈 Results")

# Calculate holding cost per unit
holding_cost_per_unit = unit_cost * (holding_cost_pct / 100)

# Calculate EOQ
eoq = np.sqrt((2 * annual_demand * order_cost) / holding_cost_per_unit)

# Calculate daily demand
daily_demand = annual_demand / 365

# Calculate safety stock
z_scores = {
    85: 1.04, 86: 1.08, 87: 1.13, 88: 1.17, 89: 1.23,
    90: 1.28, 91: 1.34, 92: 1.41, 93: 1.48, 94: 1.55,
    95: 1.65, 96: 1.75, 97: 1.88, 98: 2.05, 99: 2.33
}
z_score = z_scores[service_level]

# Standard deviation of demand during lead time
daily_std_dev = daily_demand * (demand_variability / 100)
lead_time_demand_std = daily_std_dev * np.sqrt(lead_time_days)

safety_stock = z_score * lead_time_demand_std

# Calculate reorder point
average_lead_time_demand = daily_demand * lead_time_days
reorder_point = average_lead_time_demand + safety_stock

# Calculate key metrics
orders_per_year = annual_demand / eoq
days_between_orders = 365 / orders_per_year
total_order_cost_annual = orders_per_year * order_cost
average_inventory = (eoq / 2) + safety_stock
total_holding_cost_annual = average_inventory * holding_cost_per_unit
total_inventory_cost_annual = total_order_cost_annual + total_holding_cost_annual

# Display key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Economic Order Quantity",
        f"{eoq:,.0f} units",
        help="Optimal quantity to order each time"
    )

with col2:
    st.metric(
        "Safety Stock",
        f"{safety_stock:,.0f} units",
        help="Buffer stock to prevent stockouts"
    )

with col3:
    st.metric(
        "Reorder Point",
        f"{reorder_point:,.0f} units",
        help="Inventory level to trigger new order"
    )

with col4:
    st.metric(
        "Orders Per Year",
        f"{orders_per_year:.1f}",
        help="Number of orders needed annually"
    )

# Additional metrics
st.subheader("📊 Detailed Metrics")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Days Between Orders",
        f"{days_between_orders:.1f} days"
    )

with col6:
    st.metric(
        "Average Inventory",
        f"{average_inventory:,.0f} units"
    )

with col7:
    st.metric(
        "Total Annual Cost",
        f"€{total_inventory_cost_annual:,.0f}"
    )

# Cost breakdown
st.subheader("💰 Cost Analysis")

cost_data = pd.DataFrame({
    'Cost Type': ['Ordering Costs', 'Holding Costs'],
    'Annual Cost (€)': [total_order_cost_annual, total_holding_cost_annual]
})

fig_costs = px.bar(
    cost_data,
    x='Cost Type',
    y='Annual Cost (€)',
    title='Annual Inventory Cost Breakdown',
    color='Cost Type',
    color_discrete_map={'Ordering Costs': '#0066FF', 'Holding Costs': '#00B894'}
)
fig_costs.update_layout(showlegend=False, height=400)
st.plotly_chart(fig_costs, use_container_width=True)

col8, col9 = st.columns(2)

with col8:
    st.info(f"""
    **Ordering Costs**: €{total_order_cost_annual:,.0f}/year  
    {orders_per_year:.1f} orders × €{order_cost:.0f} per order
    """)

with col9:
    st.info(f"""
    **Holding Costs**: €{total_holding_cost_annual:,.0f}/year  
    {average_inventory:,.0f} avg units × €{holding_cost_per_unit:.2f} per unit/year
    """)

# Inventory level visualization
st.subheader("📉 Inventory Level Over Time")

# Simulate inventory levels over 2 order cycles
time_points = np.linspace(0, 2 * days_between_orders, 100)
inventory_levels = []

for t in time_points:
    # Sawtooth pattern
    days_in_cycle = t % days_between_orders
    if days_in_cycle < lead_time_days:
        # During lead time, inventory decreasing from previous cycle
        inventory = eoq + safety_stock - (daily_demand * (days_between_orders - lead_time_days + days_in_cycle))
    else:
        # After receiving order
        inventory = eoq + safety_stock - (daily_demand * (days_in_cycle - lead_time_days))
    
    inventory_levels.append(max(safety_stock, inventory))

fig_inventory = go.Figure()

# Inventory level line
fig_inventory.add_trace(go.Scatter(
    x=time_points,
    y=inventory_levels,
    mode='lines',
    name='Inventory Level',
    line=dict(color='#0066FF', width=2)
))

# Reorder point line
fig_inventory.add_hline(
    y=reorder_point,
    line_dash="dash",
    line_color="orange",
    annotation_text=f"Reorder Point ({reorder_point:,.0f} units)",
    annotation_position="right"
)

# Safety stock line
fig_inventory.add_hline(
    y=safety_stock,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Safety Stock ({safety_stock:,.0f} units)",
    annotation_position="right"
)

fig_inventory.update_layout(
    title='Inventory Level Simulation (2 Order Cycles)',
    xaxis_title='Days',
    yaxis_title='Inventory Level (units)',
    height=400,
    hovermode='x unified'
)

st.plotly_chart(fig_inventory, use_container_width=True)

# Summary recommendations
st.subheader("✅ Recommendations")

st.success(f"""
**Optimal Ordering Strategy:**

1. **Order Quantity**: Order {eoq:,.0f} units each time you place an order
2. **Order Frequency**: Place orders approximately every {days_between_orders:.0f} days ({orders_per_year:.1f} times per year)
3. **Reorder Trigger**: When inventory drops to {reorder_point:,.0f} units, place a new order
4. **Safety Buffer**: Maintain {safety_stock:,.0f} units as safety stock to achieve {service_level}% service level
5. **Expected Costs**: Total annual inventory cost of €{total_inventory_cost_annual:,.0f}
   - Ordering: €{total_order_cost_annual:,.0f}
   - Holding: €{total_holding_cost_annual:,.0f}
""")

# Sensitivity analysis
st.subheader("🔍 Sensitivity Analysis")

st.markdown("""
See how changes in key parameters affect your EOQ and total costs:
""")

# EOQ sensitivity to order cost
order_costs_range = np.linspace(order_cost * 0.5, order_cost * 1.5, 20)
eoq_range = np.sqrt((2 * annual_demand * order_costs_range) / holding_cost_per_unit)

fig_sensitivity = go.Figure()

fig_sensitivity.add_trace(go.Scatter(
    x=order_costs_range,
    y=eoq_range,
    mode='lines+markers',
    name='EOQ',
    line=dict(color='#0066FF', width=2)
))

fig_sensitivity.add_vline(
    x=order_cost,
    line_dash="dash",
    line_color="red",
    annotation_text="Current Order Cost"
)

fig_sensitivity.update_layout(
    title='EOQ Sensitivity to Order Cost',
    xaxis_title='Order Cost (€)',
    yaxis_title='Economic Order Quantity (units)',
    height=350
)

st.plotly_chart(fig_sensitivity, use_container_width=True)

# Comparison table
st.subheader("📋 Scenario Comparison")

scenarios = pd.DataFrame({
    'Scenario': [
        'Conservative (Higher Safety Stock)',
        'Current Settings',
        'Aggressive (Lower Safety Stock)'
    ],
    'Service Level': ['99%', f'{service_level}%', '90%'],
    'Safety Stock': [
        f"{z_scores[99] * lead_time_demand_std:,.0f}",
        f"{safety_stock:,.0f}",
        f"{z_scores[90] * lead_time_demand_std:,.0f}"
    ],
    'Reorder Point': [
        f"{average_lead_time_demand + z_scores[99] * lead_time_demand_std:,.0f}",
        f"{reorder_point:,.0f}",
        f"{average_lead_time_demand + z_scores[90] * lead_time_demand_std:,.0f}"
    ],
    'Annual Holding Cost': [
        f"€{((eoq/2) + z_scores[99] * lead_time_demand_std) * holding_cost_per_unit:,.0f}",
        f"€{total_holding_cost_annual:,.0f}",
        f"€{((eoq/2) + z_scores[90] * lead_time_demand_std) * holding_cost_per_unit:,.0f}"
    ]
})

st.dataframe(scenarios, use_container_width=True, hide_index=True)

# Educational content
with st.expander("📚 Learn More: How EOQ Works"):
    st.markdown("""
    ### Economic Order Quantity (EOQ)
    
    EOQ is the optimal order quantity that minimizes the total cost of inventory management.
    
    **Formula:**
    ```
    EOQ = √(2 × Annual Demand × Order Cost / Holding Cost per Unit)
    ```
    
    **Key Concepts:**
    
    - **Ordering Costs**: Fixed costs incurred each time you place an order (admin, shipping, processing)
    - **Holding Costs**: Variable costs of storing inventory (warehousing, insurance, obsolescence, capital)
    - **Trade-off**: Larger orders reduce ordering frequency (lower ordering costs) but increase average inventory (higher holding costs)
    
    ### Safety Stock
    
    Buffer inventory to protect against demand variability and supply uncertainty.
    
    **Formula:**
    ```
    Safety Stock = Z-score × Standard Deviation of Demand during Lead Time
    ```
    
    - Higher service level → Higher Z-score → More safety stock
    - Higher demand variability → More safety stock needed
    - Longer lead time → More safety stock needed
    
    ### Reorder Point
    
    The inventory level at which a new order should be placed.
    
    **Formula:**
    ```
    Reorder Point = (Daily Demand × Lead Time) + Safety Stock
    ```
    
    When inventory drops to this level, trigger a new order to arrive before stockout.
    """)

# Download results
st.subheader("💾 Export Results")

results_df = pd.DataFrame({
    'Metric': [
        'Annual Demand',
        'Unit Cost',
        'Order Cost',
        'Holding Cost %',
        'Lead Time (days)',
        'Service Level',
        'Economic Order Quantity',
        'Safety Stock',
        'Reorder Point',
        'Orders Per Year',
        'Days Between Orders',
        'Average Inventory',
        'Annual Ordering Cost',
        'Annual Holding Cost',
        'Total Annual Cost'
    ],
    'Value': [
        f"{annual_demand:,.0f} units",
        f"€{unit_cost:.2f}",
        f"€{order_cost:.2f}",
        f"{holding_cost_pct}%",
        f"{lead_time_days} days",
        f"{service_level}%",
        f"{eoq:,.0f} units",
        f"{safety_stock:,.0f} units",
        f"{reorder_point:,.0f} units",
        f"{orders_per_year:.1f}",
        f"{days_between_orders:.1f} days",
        f"{average_inventory:,.0f} units",
        f"€{total_order_cost_annual:,.0f}",
        f"€{total_holding_cost_annual:,.0f}",
        f"€{total_inventory_cost_annual:,.0f}"
    ]
})

csv = results_df.to_csv(index=False)
st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name="eoq_calculation_results.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Built by Dennis Schmal</strong> | Supply Chain Digitalization Manager</p>
    <p>
        <a href='https://dennisschmal.de' target='_blank'>Website</a> • 
        <a href='https://www.linkedin.com/in/dennis-schmal/' target='_blank'>LinkedIn</a> • 
        <a href='https://github.com/dschmal' target='_blank'>GitHub</a>
    </p>
    <p style='font-size: 14px; margin-top: 10px;'>
        Want to learn to build tools like this? 
        <a href='https://dennisschmal.de' target='_blank'><strong>Join my weekend cohorts</strong></a>
    </p>
    <p style='font-size: 12px; color: #999; margin-top: 10px;'>
        Free to use • Open source • No signup required
    </p>
</div>
""", unsafe_allow_html=True)
