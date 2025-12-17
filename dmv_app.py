import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="DMV License Renewal Capacity", layout="wide", initial_sidebar_state="expanded")

st.title("🚗 DMV License Renewal - Capacity Analysis Tool")

st.markdown("""
This tool analyzes the capacity of the **Willowglen County DMV** office for renewing driving licenses
using the **Product Aggregation Method** from Operations Engineering.

**Three types of applicants arrive at the DMV:**
- **Type 1**: Proper documentation + Pass eye exam (default 76.5%)
- **Type 2**: Proper documentation + Fail eye exam, must return (default 8.5%)  
- **Type 3**: No proper documentation (default 15%)
""")

# ============================================================================
# SIDEBAR - PRODUCT MIX ADJUSTMENT
# ============================================================================
with st.sidebar:
    st.subheader("📊 Product Mix Control Panel")
    st.write("Adjust the percentage of each applicant type")
    
    p1 = st.slider(
        "Type 1: Proper docs + Pass exam (%)", 
        min_value=0, max_value=100, value=76,
        help="Applicants with proper documentation who pass the eye exam on first attempt"
    )
    p2 = st.slider(
        "Type 2: Fail exam (%)", 
        min_value=0, max_value=100, value=9,
        help="Applicants who fail the eye exam and must return with eye report"
    )
    p3 = 100 - p1 - p2
    
    if p3 < 0:
        st.error("❌ Sum exceeds 100%. Please adjust sliders.")
        st.stop()
    
    st.write(f"**Type 3: No proper docs:** {p3}%")
    
    # Convert to decimals
    p1_dec = p1 / 100
    p2_dec = p2 / 100
    p3_dec = p3 / 100
    
    st.divider()
    st.info(f"""
    **Current Product Mix:**
    - Type 1: {p1_dec:.1%}
    - Type 2: {p2_dec:.1%}
    - Type 3: {p3_dec:.1%}
    """)
    
    # Reset button
    if st.button("🔄 Reset to Default"):
        st.session_state.clear()
        st.rerun()

# ============================================================================
# RESOURCE CONFIGURATION
# ============================================================================
resources_config = {
    "Review Clerks": {
        "Type 1": 2.5,
        "Type 2": 2.5,
        "Type 3": 2.5,  # All applicants need document review
        "num_resources": 2,
        "description": "Review documents for violations and restrictions"
    },
    "Cashiers": {
        "Type 1": 1.0,
        "Type 2": 1.0,
        "Type 3": 0.0,  # Type 3 leaves at review stage
        "num_resources": 2,
        "description": "Process license renewal payment"
    },
    "Eye Exam Clerks": {
        "Type 1": 2.0,
        "Type 2": 4.0,  # Fails once (2 min), returns to pass (2 min) = 4 min total
        "Type 3": 0.0,  # Type 3 leaves at review stage
        "num_resources": 2,
        "description": "Conduct vision screening test"
    },
    "Photo/Printing Machines": {
        "Type 1": 3.0,
        "Type 2": 3.0,
        "Type 3": 0.0,  # Type 3 leaves at review stage
        "num_resources": 4,
        "description": "Take photo and print license"
    },
}

# ============================================================================
# CAPACITY CALCULATION FUNCTION
# ============================================================================
def calculate_capacity(p1, p2, p3, resources_config):
    """Calculate capacity metrics for each resource using product aggregation method"""
    results = {}
    
    for resource_name, resource_info in resources_config.items():
        t1 = resource_info["Type 1"]
        t2 = resource_info["Type 2"]
        t3 = resource_info["Type 3"]
        num_resources = resource_info["num_resources"]
        
        # Aggregate effective mean process time (in minutes)
        # T_agg = p1*T1 + p2*T2 + p3*T3
        t_agg = p1 * t1 + p2 * t2 + p3 * t3
        
        # Effective capacity per hour per resource
        # C_eff = 60 minutes/hour / T_agg
        if t_agg > 0:
            capacity_per_hour = 60 / t_agg
            pool_capacity = capacity_per_hour * num_resources
        else:
            capacity_per_hour = float('inf')
            pool_capacity = float('inf')
        
        results[resource_name] = {
            "t1": t1,
            "t2": t2,
            "t3": t3,
            "t_agg": t_agg,
            "capacity_per_hour": capacity_per_hour,
            "num_resources": num_resources,
            "pool_capacity": pool_capacity,
            "description": resource_info["description"]
        }
    
    return results

results = calculate_capacity(p1_dec, p2_dec, p3_dec, resources_config)

# Find bottleneck
bottleneck_resource = min(
    results.items(), 
    key=lambda x: x[1]['pool_capacity'] if x[1]['pool_capacity'] != float('inf') else float('inf')
)
system_capacity = bottleneck_resource[1]['pool_capacity']

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["📋 Executive Summary", "📊 Detailed Analysis", "📈 Visualizations", "❓ About"])

# ============================================================================
# TAB 1: EXECUTIVE SUMMARY
# ============================================================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "System Capacity",
            f"{system_capacity:.2f}",
            "licenses/hr",
            help="Maximum number of licenses the DMV can renew per hour"
        )
    
    with col2:
        st.metric(
            "Bottleneck Resource",
            bottleneck_resource[0].replace(" Clerks", "").replace(" Machines", ""),
            help="The resource limiting the system's capacity"
        )
    
    with col3:
        daily_capacity = system_capacity * 8
        st.metric(
            "8-Hour Capacity",
            f"{daily_capacity:.0f}",
            "licenses/day",
            help="Maximum number of licenses in an 8-hour operating day"
        )
    
    with col4:
        weekly_capacity = system_capacity * 8 * 5
        st.metric(
            "Weekly Capacity",
            f"{weekly_capacity:.0f}",
            "licenses/week",
            help="Maximum number of licenses in a 40-hour week"
        )
    
    st.divider()
    
    # Summary table
    st.subheader("📋 Resource Capacity Summary Table")
    
    summary_data = []
    for resource_name, data in results.items():
        bottleneck_indicator = "🔴" if resource_name == bottleneck_resource[0] else ""
        summary_data.append({
            "🎯": bottleneck_indicator,
            "Resource": resource_name,
            "# Units": data['num_resources'],
            "Agg. Time (min)": f"{data['t_agg']:.3f}",
            "Capacity/Unit/hr": f"{data['capacity_per_hour']:.2f}" if data['capacity_per_hour'] != float('inf') else "∞",
            "Pool Capacity/hr": f"{data['pool_capacity']:.2f}" if data['pool_capacity'] != float('inf') else "∞",
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    st.caption("🔴 = Bottleneck resource (limits system capacity)")

# ============================================================================
# TAB 2: DETAILED ANALYSIS
# ============================================================================
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Process Times by Applicant Type (minutes)")
        
        process_times = []
        for resource_name, data in results.items():
            process_times.append({
                "Resource": resource_name,
                "Type 1": f"{data['t1']:.1f}",
                "Type 2": f"{data['t2']:.1f}",
                "Type 3": f"{data['t3']:.1f}",
                "Aggregate": f"{data['t_agg']:.3f}"
            })
        
        process_df = pd.DataFrame(process_times)
        st.dataframe(process_df, use_container_width=True, hide_index=True)
        
        st.caption("Aggregate = Weighted average using product mix")
    
    with col2:
        st.subheader("Capacity per Hour (licenses/hr)")
        
        capacity_data = []
        for resource_name, data in results.items():
            capacity_data.append({
                "Resource": resource_name,
                "Per Unit": f"{data['capacity_per_hour']:.2f}" if data['capacity_per_hour'] != float('inf') else "∞",
                "Pool Total": f"{data['pool_capacity']:.2f}" if data['pool_capacity'] != float('inf') else "∞"
            })
        
        capacity_df = pd.DataFrame(capacity_data)
        st.dataframe(capacity_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Detailed resource breakdowns
    st.subheader("🔍 Detailed Resource Analysis")
    
    for i, (resource_name, data) in enumerate(results.items()):
        with st.expander(f"📌 {resource_name} - {data['description']}", expanded=i==0):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write("**Process Times by Type:**")
                st.code(f"""
Type 1: {data['t1']:.1f} min
Type 2: {data['t2']:.1f} min
Type 3: {data['t3']:.1f} min
                """, language="text")
            
            with col2:
                st.write("**Aggregate Calculation:**")
                calc_text = f"T_agg = {p1:.1%}×{data['t1']} + {p2:.1%}×{data['t2']} + {p3:.1%}×{data['t3']}"
                st.code(f"""{calc_text}
       = {data['t_agg']:.3f} min
                """, language="text")
            
            with col3:
                st.write("**Effective Capacity:**")
                if data['capacity_per_hour'] != float('inf'):
                    st.code(f"""
Per unit: {data['capacity_per_hour']:.2f} lic/hr
Pool ({data['num_resources']} units):
  {data['pool_capacity']:.2f} lic/hr
                    """, language="text")
                else:
                    st.code(f"Infinite (no processing)", language="text")
            
            # Utilization at 45 applicants/hour
            st.divider()
            st.write("**Utilization at 45 applicants/hour:**")
            if data['pool_capacity'] != float('inf') and data['pool_capacity'] > 0:
                util = (45 / data['pool_capacity']) * 100
                if util <= 100:
                    st.success(f"{util:.1f}% utilized")
                else:
                    st.error(f"{util:.1f}% utilized (OVERLOADED)")
            else:
                st.info("Not involved in processing")

# ============================================================================
# TAB 3: VISUALIZATIONS
# ============================================================================
with tab3:
    col1, col2 = st.columns(2)
    
    # --------- CAPACITY CHART ---------
    with col1:
        capacity_list = [results[r]['pool_capacity'] for r in results.keys() 
                        if results[r]['pool_capacity'] != float('inf')]
        resource_names = [r for r in results.keys() 
                         if results[r]['pool_capacity'] != float('inf')]
        
        # Color code: green for non-bottleneck, red for bottleneck
        colors = ['#e74c3c' if r == bottleneck_resource[0] else '#2ecc71' 
                 for r in resource_names]
        
        fig_capacity = go.Figure(data=[
            go.Bar(
                x=resource_names,
                y=capacity_list,
                marker=dict(
                    color=colors,
                    line=dict(color='black', width=2)
                ),
                text=[f"{c:.1f}" for c in capacity_list],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Capacity: %{y:.2f} licenses/hr<extra></extra>'
            )
        ])
        
        system_cap = min(capacity_list)
        fig_capacity.add_hline(
            y=system_cap,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text=f"System Capacity: {system_cap:.2f}/hr",
            annotation_position="right",
            annotation_font_size=12
        )
        
        fig_capacity.update_layout(
            title="Resource Pool Capacity (licenses/hour)",
            xaxis_title="Resource",
            yaxis_title="Capacity (licenses/hour)",
            height=500,
            hovermode='x',
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig_capacity, use_container_width=True)
    
    # --------- PRODUCT MIX PIE CHART ---------
    with col2:
        fig_mix = go.Figure(data=[go.Pie(
            labels=['Type 1<br>(Proper docs, pass exam)',
                    'Type 2<br>(Fail exam)',
                    'Type 3<br>(No proper docs)'],
            values=[p1, p2, p3],
            marker=dict(colors=['#2ecc71', '#f39c12', '#e74c3c']),
            textinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>%{percent}<br>(%{value}%)<extra></extra>'
        )])
        
        fig_mix.update_layout(
            title="Product Mix Distribution",
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_mix, use_container_width=True)
    
    st.divider()
    
    # --------- UTILIZATION ANALYSIS ---------
    st.subheader("⏱️ Utilization Analysis")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        demand = st.number_input(
            "Applicants per hour",
            value=45,
            min_value=0,
            max_value=200,
            step=5,
            help="Expected arrival rate of applicants at the DMV"
        )
    
    if demand > 0 and system_capacity > 0:
        utilization_data = []
        for resource_name, data in results.items():
            if data['pool_capacity'] != float('inf') and data['pool_capacity'] > 0:
                util = (demand / data['pool_capacity']) * 100
                utilization_data.append({
                    "Resource": resource_name,
                    "Pool Capacity": data['pool_capacity'],
                    "Demand": demand,
                    "Utilization %": util
                })
        
        util_df = pd.DataFrame(utilization_data)
        
        with col2:
            fig_util = go.Figure(data=[
                go.Bar(
                    x=util_df["Resource"],
                    y=util_df["Utilization %"],
                    marker=dict(
                        color=util_df["Utilization %"],
                        colorscale=['#2ecc71', '#f39c12', '#e74c3c'],
                        cmin=0,
                        cmax=150,
                        showscale=True,
                        colorbar=dict(title="Utilization %"),
                        line=dict(color='black', width=1.5)
                    ),
                    text=[f"{u:.1f}%" for u in util_df["Utilization %"]],
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Utilization: %{y:.1f}%<extra></extra>'
                )
            ])
            
            fig_util.add_hline(
                y=100,
                line_dash="dash",
                line_color="red",
                line_width=2,
                annotation_text="Full Capacity (100%)",
                annotation_position="right"
            )
            
            fig_util.update_layout(
                title=f"Resource Utilization at {demand} applicants/hour",
                xaxis_title="Resource",
                yaxis_title="Utilization (%)",
                height=500,
                hovermode='x',
                template='plotly_white'
            )
            
            st.plotly_chart(fig_util, use_container_width=True)
        
        # Feasibility check
        st.subheader("✅ Feasibility Assessment")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("System Capacity", f"{system_capacity:.2f} appl/hr")
        
        with col2:
            st.metric("Demand", f"{demand} appl/hr")
        
        with col3:
            if demand <= system_capacity:
                spare_capacity = system_capacity - demand
                spare_percent = (spare_capacity / system_capacity) * 100
                st.success(
                    f"✅ **Feasible**\n\n"
                    f"Spare: {spare_capacity:.2f} appl/hr\n"
                    f"({spare_percent:.1f}% buffer)"
                )
            else:
                shortage = demand - system_capacity
                shortage_percent = (shortage / demand) * 100
                st.error(
                    f"❌ **Infeasible**\n\n"
                    f"Shortage: {shortage:.2f} appl/hr\n"
                    f"({shortage_percent:.1f}% over capacity)"
                )
        
        st.divider()
        
        # Detailed utilization table
        st.dataframe(
            util_df.style.format({
                'Pool Capacity': '{:.2f}',
                'Demand': '{:.0f}',
                'Utilization %': '{:.1f}'
            }),
            use_container_width=True,
            hide_index=True
        )

# ============================================================================
# TAB 4: ABOUT & METHODOLOGY
# ============================================================================
with tab4:
    st.markdown("""
    ## 📚 About This Tool
    
    This tool implements the **Product Aggregation Method** for capacity analysis based on:
    - *Operations Engineering and Management: Concepts, Analytics, and Principles for Improvement*
    - Authors: Seyed M. R. Iravani
    
    ### 🎯 Problem Statement
    
    The Willowglen County DMV office renews driving licenses with the following process:
    
    1. **Review Clerks (2)** - Review documents, check violations (2.5 min per applicant)
    2. **Cashiers (2)** - Process payment (1 min per applicant with proper docs)
    3. **Eye Exam Clerks (2)** - Vision screening test (2 min per applicant)
    4. **Photo/Printing Machines (4)** - Take photo and print license (3 min per applicant)
    
    **Applicant Types:**
    - **Type 1 (76.5%)**: Proper documentation + Pass eye exam
    - **Type 2 (8.5%)**: Proper documentation + Fail eye exam (must return after getting eye report)
    - **Type 3 (15%)**: No proper documentation (leave at review stage)
    
    ### 📐 Methodology: Product Aggregation Method
    
    **Step 1: Calculate Aggregate Effective Time**
    
    For each resource, calculate the weighted average process time across all product types:
    
    $$T_{eff}^{agg} = \\sum_{k=1}^{K} p_k \\times T_k$$
    
    Where:
    - $p_k$ = proportion of type k applicants in the product mix
    - $T_k$ = process time for type k at this resource
    - $K$ = number of product types
    
    **Step 2: Calculate Capacity per Resource**
    
    $$C_{eff} = \\frac{60 \\text{ min/hour}}{T_{eff}^{agg}}$$
    
    **Step 3: Calculate Pool Capacity**
    
    For resource pools with multiple units:
    
    $$C_{pool} = C_{eff} \\times \\text{(number of units)}$$
    
    **Step 4: Identify Bottleneck**
    
    The bottleneck is the resource with the lowest pool capacity.
    
    **Step 5: System Capacity**
    
    $$C_{system} = \\min(C_{pool}) = C_{bottleneck}$$
    
    ### 💡 Key Insights
    
    1. **Product Mix Impact**: The aggregate process time is sensitive to the product mix
       - More Type 1 applicants → Lower aggregate times → Higher capacity
       - More Type 2 applicants → Higher aggregate times → Lower capacity
       - More Type 3 applicants → Lower aggregate times → Higher capacity (fewer resources needed)
    
    2. **Type 2 Effect**: Type 2 applicants require the eye exam resource twice
       - On first visit: 2 minutes (fails)
       - On return visit: 2 minutes (passes) + 3 minutes (photo/printing)
       - Total contribution to eye exam: 4 minutes per Type 2 applicant
    
    3. **Bottleneck Identification**: Focus improvement efforts on the bottleneck resource
       - In the default scenario, the Eye Exam Clerks or Photo/Printing Machines may be the bottleneck
       - Increasing capacity of non-bottleneck resources won't improve system performance
    
    4. **Utilization Analysis**: Compare demand to capacity
       - Utilization = (Demand / Capacity) × 100%
       - Ideally, utilization should be 70-85% to allow for variability
       - Over 100% means the system is overloaded
    
    ### 🔧 Practical Applications
    
    **Scenario 1: Current Demand is 45 applicants/hour**
    - Check utilization of each resource
    - Identify bottleneck resource
    - Plan capacity improvements
    
    **Scenario 2: Demand Forecasted to Increase**
    - Adjust demand slider
    - Identify when system will become infeasible
    - Decide whether to add resources or change product mix assumptions
    
    **Scenario 3: Change Product Mix**
    - Adjust sliders for different applicant type distributions
    - See how system capacity changes
    - Understand impact of service quality improvements
    
    ### 📊 Example Calculations
    
    **For Eye Exam Clerks with default mix (76.5%, 8.5%, 15%):**
    
    - Type 1 process time: 2.0 minutes
    - Type 2 process time: 4.0 minutes (fails once, returns)
    - Type 3 process time: 0.0 minutes (not applicable)
    - Aggregate: (0.765 × 2.0) + (0.085 × 4.0) + (0.15 × 0.0) = **1.87 minutes**
    - Capacity per clerk: 60 / 1.87 = **32.1 licenses/hour**
    - Pool capacity (2 clerks): 32.1 × 2 = **64.2 licenses/hour**
    
    ### 📝 References
    
    - Iravani, S.M.R. (2024). Operations Engineering and Management. McGraw-Hill.
    - Chapter 4: Process Capacity Analysis
    - Product Aggregation Method for Multi-Product Systems
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 0.9em;'>
    <p>DMV License Renewal Capacity Analysis Tool | Based on Operations Engineering & Management (Iravani)</p>
    <p>Built with Streamlit 📊 and Plotly 📈</p>
</div>
""", unsafe_allow_html=True)
