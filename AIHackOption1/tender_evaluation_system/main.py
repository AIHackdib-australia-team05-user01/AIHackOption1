# main.py
from agents.document_generation.db_manager import DatabaseManager
from agents.document_generation.doc_generation_agent import DocumentGenerationAgent
from config.database_config import DATABASE_CONFIG, SCHEMA_SUFFIX

def main():
    # Initialize database manager
    db_manager = DatabaseManager(DATABASE_CONFIG, SCHEMA_SUFFIX)
    
    if db_manager.connect():
        # Initialize document generation agent
        doc_agent = DocumentGenerationAgent(db_manager)
        
        # Get evaluation data
        tender_data = db_manager.get_evaluation_data()
        
        if tender_data:
            # Generate all reports
            reports = doc_agent.generate_all_reports(tender_data)
            
            print("Generated Reports:")
            for report_type, file_path in reports.items():
                print(f"- {report_type}: {file_path}")
        else:
            print("No tender data found in database")
        
        db_manager.close()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    main()
