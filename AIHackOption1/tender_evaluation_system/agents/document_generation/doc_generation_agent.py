# agents/document_generation/doc_generation_agent.py
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import jinja2
from .db_manager import TenderData, DatabaseManager

class DocumentGenerationAgent:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.templates_dir = Path(__file__).parent.parent.parent / "templates"
        self.outputs_dir = Path(__file__).parent.parent.parent / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)
        
        # Setup Jinja2 environment
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.templates_dir)),
            autoescape=jinja2.select_autoescape(['html'])
        )

    def generate_all_reports(self, tender_data: List[TenderData]) -> Dict[str, str]:
        """Generate all report types"""
        reports = {}
        
        reports['scoring_matrix'] = self.generate_scoring_matrix(tender_data)
        reports['source_evaluation'] = self.generate_source_evaluation_report(tender_data)
        reports['cost_risk_analysis'] = self.generate_cost_risk_schedule_analysis(tender_data)
        reports['executive_dashboard'] = self.generate_executive_dashboard(tender_data)
        
        return reports

    def generate_scoring_matrix(self, tender_data: List[TenderData]) -> str:
        """Generate scoring matrix report"""
        context = {
            'title': 'Scoring Matrix Report',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'vendors': tender_data,
            'criteria_weights': self.db_manager.get_criteria_weights()
        }
        
        return self._render_template('scoring_matrix_template.html', context, 'scoring_matrix.html')

    def generate_source_evaluation_report(self, tender_data: List[TenderData]) -> str:
        """Generate source evaluation report"""
        context = {
            'title': 'Source Evaluation Report',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'vendors': tender_data
        }
        
        return self._render_template('source_evaluation_template.html', context, 'source_evaluation.html')

    def generate_cost_risk_schedule_analysis(self, tender_data: List[TenderData]) -> str:
        """Generate cost-risk-schedule analysis"""
        context = {
            'title': 'Cost-Risk-Schedule Analysis',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'vendors': tender_data
        }
        
        return self._render_template('cost_risk_analysis_template.html', context, 'cost_risk_analysis.html')

    def generate_executive_dashboard(self, tender_data: List[TenderData]) -> str:
        """Generate executive dashboard"""
        context = {
            'title': 'Executive Dashboard',
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'vendors': tender_data
        }
        
        return self._render_template('executive_dashboard_template.html', context, 'executive_dashboard.html')

    def _render_template(self, template_name: str, context: Dict[str, Any], output_filename: str) -> str:
        """Render a template with context and save to file"""
        try:
            template = self.jinja_env.get_template(template_name)
            output = template.render(**context)
            
            output_path = self.outputs_dir / output_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
            
            return str(output_path)
        except Exception as e:
            print(f"Error rendering template {template_name}: {e}")
            return ""
