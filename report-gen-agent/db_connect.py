import psycopg2

class DBConnect:
    def __init__(self, dummy = False):
        try:
            self.cnx = psycopg2.connect(
                user="team5hack",
                password="IneedApa$$word",
                host="team5-postgres-db.postgres.database.azure.com",
                port=5432,
                database="postgres"
            )
            print("Connection successful.")
        except Exception as e:
            print(f"Connection failed: {e}")
            exit(1)

        self.cursor = self.cnx.cursor()
        if dummy:
            dummydata = '_dummydata'
        else:
            dummydata = ''
        self.cursor.execute(f"SET search_path TO team5_schema{dummydata};")

    def get_all_vendors(self):
        """Fetch all vendors from the vendors table."""
        self.cursor.execute("SELECT * FROM vendors;")
        return self.cursor.fetchall()

    def get_all_criteria_categories(self):
        """Fetch all criteria categories from the criteria_categories table."""
        self.cursor.execute("SELECT * FROM criteria_categories;")
        return self.cursor.fetchall()

    def get_all_criteria(self):
        """Fetch all criteria with their category names (join with criteria_categories)."""
        self.cursor.execute("""
            SELECT c.id, c.name, c.goal, c.weight, cc.name as category_name
            FROM criteria c
            JOIN criteria_categories cc ON c.criteria_categories_id = cc.id;
        """)
        return self.cursor.fetchall()

    def get_all_responses(self):
        """Fetch all responses with vendor and criteria info (join with vendors and criteria)."""
        self.cursor.execute("""
            SELECT r.id, v.name as vendor_name, c.name as criteria_name, r.response_text
            FROM responses r
            JOIN vendors v ON r.vendors_id = v.id
            JOIN criteria c ON r.criteria_id = c.id;
        """)
        return self.cursor.fetchall()

    def get_all_costs(self):
        """Fetch all costs with vendor and category info (join with vendors and criteria_categories)."""
        self.cursor.execute("""
            SELECT co.id, v.name as vendor_name, cc.name as category_name, co.cost
            FROM costs co
            JOIN vendors v ON co.vendors_id = v.id
            JOIN criteria_categories cc ON co.criteria_categories_id = cc.id;
        """)
        return self.cursor.fetchall()



if __name__ == "__main__":
    db = DBConnect(True)

    vendors = db.get_all_vendors()
    for vendor in vendors:
        print(vendor)

    criteria_categories = db.get_all_criteria_categories()
    for criteria_category in criteria_categories:
            print(criteria_category)

    criterias = db.get_all_criteria()
    for criteria in criterias:
        print(criteria)

    responses = db.get_all_responses()
    for response in responses:
        print(response)

    costs = db.get_all_costs()
    for cost in costs:
        print(cost)


