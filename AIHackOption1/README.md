# AIHackOption1

## Document Generation Agent Setup and Usage Guide

### Overview

The Document Generation Agent is a specialized AI component designed to automatically create comprehensive tender evaluation reports by integrating with your PostgreSQL database. It generates multiple report types including scoring matrices, source evaluations, cost-risk analyses, and executive dashboards.

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (your existing setup)
- Access to your `team5_schema` database

### Installation Steps

#### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv doc_gen_env
source doc_gen_env/bin/activate  # On Windows: doc_gen_env\Scripts\activate

# Install required packages
pip install -r tender_evaluation_system/requirements.txt
```

#### 2. Directory Structure

The project has the following structure:

```
tender_evaluation_system/
├── agents/
│   ├── document_generation/
│   │   ├── __init__.py
│   │   ├── doc_generation_agent.py
│   │   ├── db_manager.py
│   │   └── mcp_server.py
├── templates/
│   ├── scoring_matrix_template.html
│   ├── source_evaluation_template.html
│   ├── executive_dashboard_template.html
│   └── cost_risk_analysis_template.html
├── outputs/
├── config/
│   └── database_config.py
├── main.py
└── requirements.txt
```

#### 3. Database Configuration

The database configuration is in `config/database_config.py` with your existing credentials.

#### 4. Usage

Run the main script:

```bash
cd tender_evaluation_system
python main.py
```

This will generate all reports and save them to the `outputs/` directory.

### Report Types Generated

- **Scoring Matrix**: Comprehensive vendor scoring across all criteria
- **Source Evaluation Report**: Detailed vendor assessments with recommendations
- **Cost-Risk-Schedule Analysis**: Monte Carlo cost simulations and risk assessments
- **Executive Dashboard**: High-level summary with key metrics

### Integration

The agent can be integrated with your Manager Agent via the MCP server in `agents/document_generation/mcp_server.py`.

### Troubleshooting

- Ensure database connection is working (check `db_connect.py`)
- Verify all dependencies are installed
- Check file permissions for the `outputs/` directory