import psycopg2
from db_connect import cnx

def get_all_vendors():
    """Fetch all vendors from the vendors table."""
    with cnx.cursor() as cursor:
        cursor.execute("SELECT * FROM vendors;")
        return cursor.fetchall()

def get_all_criteria_categories():
    """Fetch all criteria categories from the criteria_categories table."""
    with cnx.cursor() as cursor:
        cursor.execute("SELECT * FROM criteria_categories;")
        return cursor.fetchall()

def get_all_criteria():
    """Fetch all criteria with their category names (join with criteria_categories)."""
    with cnx.cursor() as cursor:
        cursor.execute("""
            SELECT c.id, c.name, c.goal, c.weight, cc.name as category_name
            FROM criteria c
            JOIN criteria_categories cc ON c.criteria_categories_id = cc.id;
        """)
        return cursor.fetchall()

def get_all_responses():
    """Fetch all responses with vendor and criteria info (join with vendors and criteria)."""
    with cnx.cursor() as cursor:
        cursor.execute("""
            SELECT r.id, v.name as vendor_name, c.name as criteria_name, r.response_text
            FROM responses r
            JOIN vendors v ON r.vendors_id = v.id
            JOIN criteria c ON r.criteria_id = c.id;
        """)
        return cursor.fetchall()

def get_all_costs():
    """Fetch all costs with vendor and category info (join with vendors and criteria_categories)."""
    with cnx.cursor() as cursor:
        cursor.execute("""
            SELECT co.id, v.name as vendor_name, cc.name as category_name, co.cost
            FROM costs co
            JOIN vendors v ON co.vendors_id = v.id
            JOIN criteria_categories cc ON co.criteria_categories_id = cc.id;
        """)
        return cursor.fetchall()
