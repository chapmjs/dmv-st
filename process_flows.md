# DMV Process Flow Diagrams & Visual Guide

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DMV LICENSE RENEWAL PROCESS                          │
│                  (Multi-Stage, Multi-Product Analysis)                  │
└─────────────────────────────────────────────────────────────────────────┘

                              RESOURCE POOLS
                         ┌────────────────────┐
                         │  Review Clerks (2) │
                         └────────────────────┘
                                  ↓
                         ┌────────────────────┐
                         │  Cashiers (2)      │
                         └────────────────────┘
                                  ↓
                         ┌────────────────────┐
                         │ Vision Agents (2)  │
                         └────────────────────┘
                                  ↓
                         ┌────────────────────┐
                         │ Photo/Printing (4) │
                         └────────────────────┘
```

---

## Product Type Routing

### TYPE 1: Proper Documentation & Pass Eye Exam (76.5% default)

```
                    ┌─────────────────────┐
                    │  ARRIVAL            │
                    │ (100 customers)     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  REVIEW CLERKS (2)  │
                    │  2.5 min/customer   │
                    │  Process: ✓✓✓✓✓     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  CASHIERS (2)       │
                    │  1.0 min/customer   │
                    │  Payment: ✓✓✓✓      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  VISION SCREENING(2)│
                    │  2.0 min/customer   │
                    │  Result: PASS ✓✓✓   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  PHOTO/PRINTING (4) │
                    │  3.0 min/customer   │
                    │  License: ✓✓✓✓✓     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  EXIT (COMPLETE)    │
                    │  76.5 customers     │
                    └─────────────────────┘

Total Time: 2.5 + 1.0 + 2.0 + 3.0 = 8.5 minutes per customer
```

---

### TYPE 2: Proper Documentation & Fail Eye Exam (8.5% default)

```
FIRST VISIT (Same Day):
                    ┌─────────────────────┐
                    │  ARRIVAL (Day 1)    │
                    │  8.5 customers      │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  REVIEW CLERKS (2)  │
                    │  2.5 min/customer   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  CASHIERS (2)       │
                    │  1.0 min/customer   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  VISION SCREENING(2)│
                    │  2.0 min/customer   │
                    │  Result: FAIL ✗✗    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  EXIT (TEMPORARY)   │
                    │  Get eye report     │
                    └──────────┬──────────┘
                               │
                               │
                    ┌──────────▼──────────┐
                    │   [WAIT 3 DAYS]     │
                    │   (Outside process) │
                    └──────────┬──────────┘
                               │
RETURN VISIT (Day 4):
                    ┌──────────▼──────────┐
                    │  ARRIVAL (Day 4)    │
                    │  8.5 customers      │
                    │  (with eye report)  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  VISION SCREENING(2)│
                    │  2.0 min/customer   │
                    │  Result: PASS ✓✓    │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  PHOTO/PRINTING (4) │
                    │  3.0 min/customer   │
                    │  License: ✓✓✓✓✓     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  EXIT (COMPLETE)    │
                    │  8.5 customers      │
                    └─────────────────────┘

First Visit Time: 2.5 + 1.0 + 2.0 = 5.5 minutes
Return Visit Time: 2.0 + 3.0 = 5.0 minutes
Total Time (across 2 visits): 10.5 minutes
Vision Time Contribution: 4.0 minutes (2.0 + 2.0)
```

---

### TYPE 3: Improper Documentation (15% default)

```
                    ┌─────────────────────┐
                    │  ARRIVAL            │
                    │  15 customers       │
                    │  (Missing docs)     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  REVIEW CLERKS (2)  │
                    │  2.5 min/customer   │
                    │  Check: ✗ Incomplete│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  EXIT (REDIRECTED)  │
                    │  Return with proper │
                    │  documentation      │
                    │  15 customers       │
                    └─────────────────────┘

Total Time: 2.5 minutes (then exit)
No further processing until reapplication with proper docs
```

---

## Resource Pool Capacity Analysis

### Visual Representation of Bottleneck

```
RESOURCE CAPACITY COMPARISON (Default Product Mix)

Review Clerks    ▰▰▰▰▰░░░░░░░░░░░░░░░░░░  48/hour (2 units)
Cashiers         ▰▰▰▰▰▰▰▰▰▰▰▰▰▰░░░░░░░░░  141/hour (2 units)
Vision Screening ▰▰▰▰▰▰▰▰▰░░░░░░░░░░░░░░  64/hour (2 units)
Photo/Printing   ▰▰▰▰▰▰▰▰▰▰▰▰▰▰░░░░░░░░░  94/hour (4 units)

                 0     25     50    75   100   125   150
                 └─────┴──────┴─────┴─────┴─────┴──────┘
                       Capacity (customers/hour)

         PROCESS BOTTLENECK
            │
            ▼
         Review Clerks = 48 customers/hour (minimum capacity)
```

---

## Daily Flow in Steady State

```
DAY N (Steady State - Example with 45 arrivals)

NEW ARRIVALS (Day N):
├─ Type 1: 45 × 0.765 = 34.4 customers
├─ Type 2: 45 × 0.085 = 3.8 customers  (first visit only)
└─ Type 3: 45 × 0.150 = 6.8 customers

RETURNING CUSTOMERS (from Day N-3):
└─ Type 2: 45 × 0.085 = 3.8 customers (return visit)

TOTAL CUSTOMERS PROCESSED TODAY:
─────────────────────────────────────

Review Clerks:    45.0 customers (34.4 + 3.8 + 6.8 new arrivals)
                  Total time: 45.0 × 2.5 = 112.5 min
                  Available: 2 × 60 = 120 min
                  Utilization: 93.75% ⚠️ VERY BUSY

Cashiers:         38.2 customers (34.4 + 3.8 type 1 & 2 only)
                  Total time: 38.2 × 1.0 = 38.2 min
                  Available: 2 × 60 = 120 min
                  Utilization: 31.8% 🟢 HEALTHY

Vision Screening: 42.0 customers (34.4 type 1 + 3.8 type 2 first + 3.8 type 2 return)
                  Total time: 42.0 × 2.0 = 84.0 min
                  Available: 2 × 60 = 120 min
                  Utilization: 70.0% 🟡 MODERATE

Photo/Printing:   38.2 customers (34.4 type 1 + 3.8 type 2 return only)
                  Total time: 38.2 × 3.0 = 114.6 min
                  Available: 4 × 60 = 240 min
                  Utilization: 47.8% 🟢 HEALTHY
```

---

## Product Mix Impact on Vision Screening

```
SENSITIVITY ANALYSIS: Effect of Type 2 on Vision Screening

Type 2 %    Vision Time    Vision Capacity    Impact
────────────────────────────────────────────────────
   5%       2.1 min        57/hour          Relaxed ✓
  10%       2.2 min        55/hour
  15%       2.3 min        52/hour          Current benchmark
  20%       2.4 min        50/hour
  25%       2.5 min        48/hour          Tight ⚠️
  30%       2.6 min        46/hour          Critical ✗

Note: Type 2 customers need double vision time (fail + pass visits)
      Each 5% increase in Type 2 adds 0.1 min to aggregate time
```

---

## Understanding the Utilization Heatmap

### Important: Bottleneck ≠ 100% Utilization

**Common Misconception:** "If a resource is the bottleneck, shouldn't it be at 100%?"

**Answer:** No. The bottleneck is at 100% utilization **only when demand equals its capacity**.

#### DMV Example Explained

```
Review Clerks (THE BOTTLENECK):
├─ Maximum Capacity: 48 customers/hour
├─ Current Demand: 45 customers/hour
├─ Utilization: 45 ÷ 48 = 93.75% 
├─ Interpretation: 
│  └─ Can handle 3 more arrivals before hitting 100%
│     (would be 100% at 48 arrivals/hour)
│
└─ Why is it the bottleneck?
   └─ It has the LOWEST capacity (48) compared to others (64, 94, 141)
      So it LIMITS the overall process capacity to 48 max.
```

### When Bottleneck Hits 100%

```
If arrivals increased from 45 to 48:
├─ Review Clerks: 48 ÷ 48 = 100% (FULLY UTILIZED)
├─ Vision: 42 ÷ 64 = 65.6% (still has buffer)
├─ Photo: 48 ÷ 94 = 51% (still has buffer)
└─ Process: At maximum capacity, no buffer for variation

If arrivals increased beyond 48 (e.g., to 50):
├─ Review Clerks: 50 ÷ 48 = 104% (OVERLOADED!)
├─ Status: System cannot handle the demand
└─ Result: Queues form, delays increase
```

```
RESOURCE UTILIZATION MATRIX (Product Mix Changes)

                        Product Type Distribution
         Type1=90%     Type1=80%     Type1=76%     Type1=70%
         Type2=5%      Type2=10%     Type2=9%      Type2=20%
         Type3=5%      Type3=10%     Type3=15%     Type3=10%

Review    🟢 95%        🟢 95%        🟡 94%        🟡 94%
          (2.5 min)     (2.5 min)     (2.5 min)     (2.5 min)

Cashier   🟢 28%        🟢 33%        🟢 32%        🟢 36%
          (0.95 min)    (0.90 min)    (0.85 min)    (0.80 min)

Vision    🟡 74%        🟡 72%        🟡 70%        🟡 65%
          (1.78 min)    (1.82 min)    (1.87 min)    (1.96 min)

Photo     🟢 52%        🟢 50%        🟢 48%        🟢 45%
          (2.7 min)     (2.7 min)     (2.55 min)    (2.4 min)

Legend: 🟢 < 70%  🟡 70-100%  🔴 > 100%
```

---

## Process Improvement Opportunities

```
CURRENT STATE (45 arrivals/hour)
├─ Review Clerks Utilization: 93.75% 🔴 BOTTLENECK
├─ Cashiers: 31.88% 🟢
├─ Vision: 70.13% 🟡
└─ Photo: 47.81% 🟢

IMPROVEMENT OPTIONS:

Option 1: Add 1 More Review Clerk
├─ New Review Capacity: 48 → 72 customers/hour
├─ New Utilization: 93.75% → 62.5% 🟢
├─ Process Capacity: 48 → 64 customers/hour ✓ +33%
└─ Investment: 1 person

Option 2: Reduce Review Time by 10%
├─ New Review Time: 2.5 → 2.25 minutes
├─ New Utilization: 93.75% → 84.4% 🟡
├─ Process Capacity: 48 → 53 customers/hour ✓ +10%
└─ Investment: Process improvement

Option 3: Combine Options 1 & 2
├─ New Review Capacity: 48 → 80 customers/hour
├─ New Utilization: 93.75% → 50.6% 🟢
├─ Process Capacity: 48 → 80 customers/hour ✓ +67%
└─ Investment: 1 person + minor process improvement

RECOMMENDED: Option 1 (Quick win) + Option 2 (Long-term)
```

---

## Demand vs. Capacity Curve

```
CAPACITY PLANNING CHART

Customers
per Hour  120 │
          100 │                          ╱─ Photo/Printing
           80 │            ╱──────────────
           60 │  ╱─────────              
           40 │╱─── Review Clerks (BOTTLENECK)
           20 │
            0 │_____________________________________________________________
              0%    5%     10%    15%    20%    25%    30%
                        Type 2 Percentage (Failure Rate)

Current Point:
├─ Type 2 = 8.5%
├─ Process Capacity = 48/hour
├─ Current Demand = 45/hour
└─ Buffer = 3/hour (6.7%) ⚠️ THIN

Future Scenarios:
├─ If Type 2 increases to 20%: Capacity drops to ~46/hour
├─ If demand increases to 50/hour: Must add resources NOW
└─ If we want 60/hour capacity: Must redesign process
```

---

## Key Metrics Summary Table

```
┌──────────────────────────────────────────────────────────────┐
│              DMV CAPACITY ANALYSIS SUMMARY                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  PROCESS BOTTLENECK:                                         │
│  ├─ Resource: Review Clerks                                  │
│  ├─ Capacity: 48 arrivals/hour                              │
│  ├─ Utilization at 45/hr: 93.75%                            │
│  └─ Status: 🔴 CRITICAL - Little buffer                     │
│                                                               │
│  AGGREGATE PROCESS TIMES (in minutes):                       │
│  ├─ Review Clerks:    2.50  (all products)                  │
│  ├─ Cashiers:         0.85  (Type 1 & 2 only)               │
│  ├─ Vision Screening: 1.87  (includes Type 2 double visit)  │
│  └─ Photo/Printing:   2.55  (Type 1 & 2 only)               │
│                                                               │
│  RESOURCE UTILIZATION (at 45 arrivals/hour):                │
│  ├─ Review Clerks:    93.75% 🔴                             │
│  ├─ Cashiers:         31.88% 🟢                             │
│  ├─ Vision Screening: 70.13% 🟡                             │
│  └─ Photo/Printing:   47.81% 🟢                             │
│                                                               │
│  COMPLETION RATES:                                            │
│  ├─ Type 1 (Complete on Day 1): 76.5%                       │
│  ├─ Type 2 (Complete on Day 4): 8.5%                        │
│  └─ Type 3 (Don't Complete): 15.0%                          │
│                                                               │
│  RISK ASSESSMENT:                                             │
│  ├─ Demand < 45/hr: 🟢 Safe                                 │
│  ├─ 45 ≤ Demand < 48: 🟡 Caution                            │
│  ├─ Demand ≥ 48/hr: 🔴 Overload                             │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Legend & Color Coding

### Status Indicators
```
🟢 GREEN  = Healthy (Utilization < 70%)
           Adequate capacity buffer, good performance

🟡 ORANGE = Caution (Utilization 70-100%)
           Monitor closely, consider expansion plans

🔴 RED    = Critical (Utilization > 100%)
           Overloaded, immediate action required
```

### Time Notation
```
Process Time (T_eff):
└─ Time each customer spends at a resource (minutes)

Aggregate Time (T_eff agg):
└─ Weighted average considering product mix (minutes)

Effective Capacity (C_eff):
└─ Maximum customers resource can serve per hour
```

---

## How to Read the App Visualizations

### Utilization Bar Chart
- **Length of bar** = How busy the resource is
- **Green bar** = Under 70% utilization (good)
- **Orange bar** = 70-100% utilization (be careful)
- **Red bar** = Over 100% utilization (bottleneck)
- **Target line** at 70% = optimal utilization
- **Limit line** at 100% = maximum capacity

### Capacity Comparison Chart
- **Height of bar** = Maximum customers per hour
- **Horizontal line** at 45 = Current demand
- **Gap between bar and line** = Capacity buffer
- **Short gap or bar below line** = Bottleneck resource

---

**These diagrams complement the interactive Streamlit app. Use them alongside the app for complete understanding of the DMV capacity system.**
