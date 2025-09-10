# agents/document_generation/db_manager.py
import psycopg2
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class TenderData:
    vendor_id: int
    vendor_name: str
    criteria_responses: Dict[str, Any]
    costs: Dict[str, float]
    scores: Dict[str, float]

class DatabaseManager:
    def __init__(self, config: Dict[str, Any], schema_suffix: str = "_dummydata"):
        self.config = config
        self.connection = None
        
        
        self.cursor = None
        self.schema = f"team5_schema{schema_suffix}"

    def connect(self) -> bool:
        try:
            self.connection = psycopg2.connect(**self.config)
            self.cursor = self.connection.cursor()
            self.cursor.execute(f"SET search_path TO {self.schema};")
            print("Database connection successful.")
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def get_evaluation_data(self) -> List[TenderData]:
        """Fetch all evaluation data from the database"""
        try:
            # Get vendors
            self.cursor.execute("SELECT id, name FROM vendors;")
            vendors = self.cursor.fetchall()

            tender_data = []

            for vendor_id, vendor_name in vendors:
                # Get responses for this vendor
                self.cursor.execute("""
                    SELECT c.name, r.response_text, cat.name as category
                    FROM responses r
                    JOIN criteria c ON r.criteria_id = c.id
                    JOIN criteria_categories cat ON c.criteria_categories_id = cat.id
                    WHERE r.vendors_id = %s;
                """, (vendor_id,))
                responses = self.cursor.fetchall()

                criteria_responses = {}
                for crit_name, resp_text, cat_name in responses:
                    criteria_responses[f"{cat_name}_{crit_name}"] = resp_text

                # Get costs
                self.cursor.execute("""
                    SELECT cat.name, cost.cost
                    FROM costs cost
                    JOIN criteria_categories cat ON cost.criteria_categories_id = cat.id
                    WHERE cost.vendors_id = %s;
                """, (vendor_id,))
                costs = self.cursor.fetchall()
                cost_dict = {cat: cost for cat, cost in costs}

                # Placeholder for scores - in real implementation, calculate based on responses
                scores = {}  # To be calculated

                tender_data.append(TenderData(
                    vendor_id=vendor_id,
                    vendor_name=vendor_name,
                    criteria_responses=criteria_responses,
                    costs=cost_dict,
                    scores=scores
                ))

            return tender_data
        except Exception as e:
            print(f"Error fetching evaluation data: {e}")
            return []

    def get_criteria_weights(self) -> Dict[str, int]:
        """Get criteria weights"""
        try:
            self.cursor.execute("SELECT name, weight FROM criteria;")
            criteria = self.cursor.fetchall()
            return {name: weight for name, weight in criteria}
        except Exception as e:
            print(f"Error fetching criteria weights: {e}")
            return {}
