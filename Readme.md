# 🚗 DMV License Renewal Capacity Analysis Tool

A comprehensive Streamlit application for analyzing the capacity of a DMV office using the **Product Aggregation Method** from Operations Engineering and Management.

## 📋 Overview

This tool helps DMV managers and operations analysts understand and optimize their license renewal process by:

- **Calculating system capacity** based on resource availability and processing times
- **Identifying bottleneck resources** that limit throughput
- **Analyzing product mix impact** on system performance
- **Assessing resource utilization** at different demand levels
- **Planning capacity improvements** based on data-driven insights

## ✨ Features

### 1. **Interactive Product Mix Control**
- Adjust the percentage distribution of three applicant types using sliders
- Real-time calculation of system metrics
- Immediate visualization of impact on capacity

### 2. **Comprehensive Capacity Analysis**
- Effective mean process times for each applicant type
- Aggregate process times using product mix
- Capacity calculations for individual resources and resource pools
- Bottleneck identification

### 3. **Multi-Tab Interface**
- **Executive Summary**: Key metrics and resource capacity table
- **Detailed Analysis**: Process times breakdown and individual resource analysis
- **Visualizations**: Capacity charts, product mix pie chart, and utilization analysis
- **Methodology**: Complete explanation of the Product Aggregation Method

### 4. **Utilization Analysis**
- Compare demand to capacity at any applicant arrival rate
- Color-coded utilization charts (green=underutilized, red=overutilized)
- Feasibility assessment for different demand scenarios

## 🏗️ System Architecture

### Process Flow
```
All Applicants (100%)
    ↓
[Review Clerks - 2 resources] 
    ├─→ Type 1 (76.5%) + Type 2 (8.5%) → Continue
    └─→ Type 3 (15%) → Leave
    ↓
[Cashiers - 2 resources] → Type 1 & 2 only
    ↓
[Eye Exam Clerks - 2 resources] → Type 1 & 2 only
    │   ├─→ Type 1 → Pass (proceed)
    │   └─→ Type 2 → Fail (return in 3 days)
    ↓
[Photo/Printing Machines - 4 resources] → Type 1 only (plus Type 2 on return)
    ↓
License Issued
```

### Resource Configuration
| Resource | Quantity | Type 1 (min) | Type 2 (min) | Type 3 (min) |
|----------|----------|--------------|--------------|--------------|
| Review Clerks | 2 | 2.5 | 2.5 | 2.5 |
| Cashiers | 2 | 1.0 | 1.0 | — |
| Eye Exam Clerks | 2 | 2.0 | 4.0* | — |
| Photo/Printing | 4 | 3.0 | 3.0 | — |

*Type 2: 2 min (fail) + 2 min (return to pass) = 4 min total

## 🚀 Installation & Deployment

### Option 1: Local Installation (Recommended for Development)

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Steps
1. **Clone or download the project files**
```bash
# Create a project directory
mkdir dmv-capacity-app
cd dmv-capacity-app
```

2. **Create a virtual environment** (Optional but recommended)
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run dmv_app.py
```

The app will open in your default browser at `http://localhost:8501`

### Option 2: Deploy on Streamlit Cloud (Free & Recommended for Sharing)

This is the easiest way to share your app with others!

#### Prerequisites
- GitHub account
- Streamlit Cloud account (free)

#### Steps

1. **Push code to GitHub**
   - Create a GitHub repository
   - Add your files (`dmv_app.py`, `requirements.txt`, and this README)
   - Push to GitHub

2. **Connect to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Click "Deploy an app"
   - Select your GitHub repository
   - Choose the branch and file (`dmv_app.py`)
   - Click "Deploy!"

Your app will be live at `https://[your-username]-dmv-app.streamlit.app`

### Option 3: Deploy on Heroku

#### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- GitHub repository with code

#### Steps

1. **Create Procfile** (in project root)
```
web: streamlit run --server.port=$PORT --server.address=0.0.0.0 dmv_app.py
```

2. **Create .streamlit/config.toml**
```toml
[server]
port = $PORT
enableXsrfProtection = false

[browser]
gatherUsageStats = false
```

3. **Deploy to Heroku**
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-dmv-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 4: Deploy on Docker

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dmv_app.py .

EXPOSE 8501

CMD ["streamlit", "run", "dmv_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run
```bash
# Build image
docker build -t dmv-capacity-app .

# Run container
docker run -p 8501:8501 dmv-capacity-app
```

### Option 5: Deploy on AWS, Google Cloud, or Azure

Each platform has different deployment options. Common approaches:
- **AWS**: Use EC2 instances, Elastic Beanstalk, or AppRunner
- **Google Cloud**: Use Cloud Run, App Engine, or Compute Engine
- **Azure**: Use App Service or Container Instances

(Contact your cloud provider's documentation for specific instructions)

## 📊 How to Use the App

### 1. **Executive Summary Tab**
- View key metrics: System capacity, bottleneck resource, daily/weekly capacity
- Review capacity summary table for all resources
- Identify which resource is constraining the system

### 2. **Detailed Analysis Tab**
- See process times for each applicant type and resource
- Understand the calculation of aggregate effective time
- Expand individual resources to see detailed calculations
- Check utilization at current demand (45 appl/hr)

### 3. **Visualizations Tab**
- **Capacity Chart**: Visual comparison of resource pool capacities
- **Product Mix Pie**: See distribution of applicant types
- **Utilization Analysis**: 
  - Adjust expected demand (default: 45 applicants/hour)
  - View utilization percentage for each resource
  - See feasibility assessment (Feasible/Infeasible)
  - Review detailed utilization table

### 4. **About Tab**
- Complete methodology explanation
- Problem statement and process flow
- Step-by-step Product Aggregation Method
- Key insights and practical applications
- Example calculations

### 5. **Sidebar Controls**
- Adjust product mix using sliders
- Reset to default values
- Current mix summary

## 📈 Example Scenarios

### Scenario 1: Baseline (Default Product Mix)
- Type 1: 76.5%, Type 2: 8.5%, Type 3: 15%
- System capacity: ~44.2 licenses/hour
- Bottleneck: Eye Exam Clerks
- At 45 appl/hr demand: System is at full capacity

### Scenario 2: Improved Eye Exam Pass Rate
- Reduce Type 2 to 5%, increase Type 1 to 80%
- System capacity: ~45.8 licenses/hour (+1.6 lic/hr)
- Bottleneck: Shifts from Eye Exam to Photo/Printing
- Conclusion: Quality improvement (reducing failures) increases throughput

### Scenario 3: More Type 3 Applicants
- Increase Type 3 to 25%, adjust Type 1 to 68%
- System capacity: ~43.5 licenses/hour (-0.7 lic/hr)
- Bottleneck: Review Clerks
- Conclusion: More incomplete applications slow the system

### Scenario 4: High Demand Planning
- Set demand to 60 applicants/hour
- All resources become overutilized (>100%)
- Feasibility: INFEASIBLE
- Recommendation: Increase Review Clerks or improve process efficiency

## 🔍 Understanding the Mathematics

### Product Aggregation Formula

For a single resource processing K product types:

**Aggregate Effective Time:**
```
T_agg = Σ(p_k × T_k)  where k = 1 to K
```

**Effective Capacity (per hour):**
```
C_eff = 60 minutes/hour ÷ T_agg
```

**Pool Capacity (multiple resources):**
```
C_pool = C_eff × number_of_resources
```

**System Capacity:**
```
C_system = min(C_pool for all resources)  [the bottleneck]
```

**Utilization:**
```
Utilization% = (Demand ÷ Capacity) × 100
```

**Important Clarification: Bottleneck ≠ 100% Utilization**

The **bottleneck** is the resource with the **lowest capacity**, but its utilization depends on actual demand:

```
Example (Default DMV):
├─ Review Clerks Capacity: 48 customers/hour (BOTTLENECK)
├─ Current Demand: 45 customers/hour
├─ Utilization: (45 ÷ 48) × 100% = 93.75% ← This is CORRECT
│
└─ Review Clerks would be at 100% utilization only if:
   ├─ Demand increased to 48/hour (exactly at capacity)
   └─ Any increase beyond 48/hour → System overloaded

Key Point: The bottleneck resource is the constraint preventing higher throughput,
but at the current demand level (45/hr), it's not yet at maximum utilization (93.75%).
```

### Modify Process Times
Edit the `resources_config` dictionary in `dmv_app.py`:

```python
resources_config = {
    "Review Clerks": {
        "Type 1": 2.5,  # Change process time here
        "Type 2": 2.5,
        "Type 3": 2.5,
        "num_resources": 2,  # Change number of resources here
        "description": "Review documents for violations and restrictions"
    },
    # ... other resources
}
```

### Add New Resource Types
1. Add new entry to `resources_config`
2. Define process times for each applicant type
3. Specify number of resources
4. The app will automatically include in calculations

### Change Default Product Mix
Modify the slider default values in the sidebar section:
```python
p1 = st.slider(..., value=76, ...)  # Change default here
```

## 📚 Educational Use

This tool is excellent for teaching:
- Operations Management and capacity planning
- Business process optimization
- Data-driven decision making
- Queuing theory and bottleneck management
- Product mix and product strategy

## ❓ Frequently Asked Questions

**Q: Why does changing product mix affect capacity?**
A: Different applicant types require different amounts of processing time at each resource. A mix with more Type 2 applicants (who fail eye exams) increases load on the Eye Exam resource, potentially changing the bottleneck.

**Q: What does "Aggregate Effective Time" mean?**
A: It's the weighted average processing time across all applicant types, considering the product mix. It represents the average time a "representative applicant" takes at each resource.

**Q: How do I interpret utilization over 100%?**
A: This means the demand exceeds the resource's capacity. The resource cannot keep up, and queues will form. The system is infeasible at that demand level.

**Q: Can I add more resources to increase capacity?**
A: Yes! But only if you increase resources at the bottleneck. Increasing non-bottleneck resources won't help until the bottleneck is relieved.

**Q: What's the ideal utilization percentage?**
A: Generally 70-85% is ideal. It's high enough to be efficient but low enough to absorb variability and avoid excessive queuing.

## 🐛 Troubleshooting

**App won't load:**
- Ensure all requirements are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)
- Try clearing cache: `streamlit cache clear`

**Sliders don't sum to 100%:**
- The app automatically calculates Type 3 percentage
- Ensure Type 1 + Type 2 ≤ 100%

**Charts not displaying:**
- Check internet connection (Plotly needs to load)
- Try refreshing the page
- Clear browser cache

**Deployment issues:**
- Check your requirements.txt has correct package names and versions
- Verify all files are in the correct directory
- Review deployment platform logs for error messages

## 📞 Support & Contributing

For issues, suggestions, or improvements:
1. Document the issue clearly
2. Include steps to reproduce
3. Share relevant product mix settings
4. Provide screenshots if helpful

## 📄 License

This tool is provided for educational and professional use.

## 👨‍💼 Author & Attribution

Built as an educational tool based on:
- **"Operations Engineering and Management: Concepts, Analytics, and Principles for Improvement"**
- **Author:** Seyed M. R. Iravani
- **Publisher:** McGraw-Hill Education
- **ISBN:** 9781260461831

## 🎓 Learning Outcomes

After using this tool, you should be able to:
- ✅ Understand the Product Aggregation Method for capacity analysis
- ✅ Calculate effective process times for multi-product systems
- ✅ Identify bottleneck resources in service processes
- ✅ Assess feasibility of demand scenarios
- ✅ Recommend capacity improvements based on data
- ✅ Explain impact of product mix on system performance
- ✅ Apply operations engineering principles to real systems

## 🚀 Next Steps

1. **Deploy the app** using one of the methods above
2. **Share with stakeholders** for collaborative analysis
3. **Customize for your organization** by modifying process times
4. **Use for planning** to assess capacity expansion needs
5. **Monitor performance** and update assumptions as needed

---

**Happy analyzing! 📊**

For the latest version and updates, check the project repository.
