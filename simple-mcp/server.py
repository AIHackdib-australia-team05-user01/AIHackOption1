# server.py
from fastmcp import FastMCP
import json
from typing import Any, Dict, List, Tuple
from db_connect import DBConnect
import psycopg2
import psycopg2.extras as extras
from tools.text_to_string import read_file_to_text

mcp = FastMCP("rfp-mcp")

@mcp.tool
def get_all_documents() -> str:
    """Gets all the rfp and executive summary documents from storage"""
    print("Getting documents")
    vendor1_exec_summary = read_file_to_text("tender_docs/Vendor 1 Executive Summary.docx")
    vendor1_rfp = read_file_to_text("tender_docs/Vendor 1 RFP.xlsx")
    vendor2_exec_summary = read_file_to_text("tender_docs/Vendor 2 Executive Summary.docx")
    vendor2_rfp = read_file_to_text("tender_docs/Vendor 2 RFP.xlsx")
    vendor3_exec_summary = read_file_to_text("tender_docs/Vendor 3 Executive Summary.docx")
    vendor3_rfp = read_file_to_text("tender_docs/Vendor 3 RFP.xlsx")
    
    return f"""The executive summary for vendor 1 is: {vendor1_exec_summary}
    The RFP for vendor 1 is: {vendor1_rfp}
    The executive summary for vendor 2 is: {vendor2_exec_summary}
    The RFP for vendor 2 is: {vendor2_rfp}
    The executive summary for vendor 3 is: {vendor3_exec_summary}
    The RFP for vendor 3 is: {vendor3_rfp}
    """

@mcp.tool
def get_schema() -> str:
    print("Getting schema")
    """Gets the json schema that reflects what the database schema is"""
    with open("database.schema.json", "r", encoding="utf-8") as f:
        return f.read()


def _exec_values_upsert(cur, sql_prefix: str, rows: List[Tuple], template: str, suffix: str = ""):
    if not rows:
        return 0
    sql = sql_prefix + " VALUES %s " + suffix
    extras.execute_values(cur, sql, rows, template=template)
    return len(rows)


@mcp.tool
def load_rfp_json(data: Any) -> Dict[str, int]:
    """
    Store RFP extraction dict (or JSON string) into team5 Postgres database.

    Args:
      data: Python dict OR JSON string with keys:
            vendors, criteriaCategories, criteria, responses, costs.

    Returns:
      Counts per table inserted/updated (rows attempted).
    """
    print("Storing RFP data")
    if isinstance(data, str):
        data = json.loads(data)
        print("loaded data")
    if not isinstance(data, dict):
        print("data is wrong")
        raise ValueError("`data` must be a dict or JSON string.")

    # Basic shape checks
    vendors = data.get("vendors", [])
    cats = data.get("criteriaCategories", [])
    crit = data.get("criteria", [])
    resp = data.get("responses", [])
    costs = data.get("costs", [])
    print("Checking data shape")

    print("Connecting to Db . . .")
    db = DBConnect(dummy=False)
    print("Connected to the Db")
    cnx = db.cnx
    cur = db.cursor

    # Wrap in a transaction
    try:
        # 1) vendors(id, name)
        print("Creating vendors transaction")
        v_rows = [(int(x["id"]), str(x["name"])) for x in vendors]
        v_sql = "INSERT INTO vendors (id, name)"
        v_tpl = "(%s, %s)"
        v_suf = "ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name"
        c_v = _exec_values_upsert(cur, v_sql, v_rows, v_tpl, v_suf)
        print("Vendors transaction created")

        # 2) criteria_categories(id, name)
        print("Creating criteria categories transaction")
        ccat_rows = [(int(x["id"]), str(x["name"])) for x in cats]
        ccat_sql = "INSERT INTO criteria_categories (id, name)"
        ccat_tpl = "(%s, %s)"
        ccat_suf = "ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name"
        c_ccat = _exec_values_upsert(
            cur, ccat_sql, ccat_rows, ccat_tpl, ccat_suf)
        print("Criteria Categories transaction created")

        # 3) criteria(id, criteria_categories_id, name, goal, weight)
        # input uses `category_id` -> FK column is criteria_categories_id
        print("Creating criteria transaction")
        crit_rows = [
            (
                int(x["id"]),
                int(x["category_id"]),
                str(x["name"]),
                str(x["goal"]),
                float(x.get("weight", 1.0)),
            )
            for x in crit
        ]
        crit_sql = "INSERT INTO criteria (id, criteria_categories_id, name, goal, weight)"
        crit_tpl = "(%s, %s, %s, %s, %s)"
        crit_suf = """ON CONFLICT (id) DO UPDATE SET
                        criteria_categories_id=EXCLUDED.criteria_categories_id,
                        name=EXCLUDED.name,
                        goal=EXCLUDED.goal,
                        weight=EXCLUDED.weight"""
        c_crit = _exec_values_upsert(
            cur, crit_sql, crit_rows, crit_tpl, crit_suf)
        print("Criteria transaction created")

        # 4) responses(id, criteria_id, vendors_id, response_text)
        print("Creating responses transaction")
        resp_rows = [
            (
                int(x["id"]),
                int(x["criteria_id"]),
                int(x["vendor_id"]),
                str(x["response_text"]),
            )
            for x in resp
        ]
        resp_sql = "INSERT INTO responses (id, criteria_id, vendors_id, response_text)"
        resp_tpl = "(%s, %s, %s, %s)"
        resp_suf = """ON CONFLICT (id) DO UPDATE SET
                        criteria_id=EXCLUDED.criteria_id,
                        vendors_id=EXCLUDED.vendors_id,
                        response_text=EXCLUDED.response_text"""
        c_resp = _exec_values_upsert(
            cur, resp_sql, resp_rows, resp_tpl, resp_suf)
        print("Responses transaction created")

        # 5) costs(id, criteria_categories_id, vendors_id, cost)
        # input uses `criteria_category_id` -> FK column is criteria_categories_id
        print("Creating costs transaction")
        cost_rows = [
            (
                int(x["id"]),
                int(x["criteria_category_id"]),
                int(x["vendor_id"]),
                float(x["cost"]),
            )
            for x in costs
        ]
        cost_sql = "INSERT INTO costs (id, criteria_categories_id, vendors_id, cost)"
        cost_tpl = "(%s, %s, %s, %s)"
        cost_suf = """ON CONFLICT (id) DO UPDATE SET
                        criteria_categories_id=EXCLUDED.criteria_categories_id,
                        vendors_id=EXCLUDED.vendors_id,
                        cost=EXCLUDED.cost"""
        c_cost = _exec_values_upsert(
            cur, cost_sql, cost_rows, cost_tpl, cost_suf)
        print("Costs transaction created")

        cnx.commit()
        print("Transactions committed")
        return {
            "vendors": c_v,
            "criteria_categories": c_ccat,
            "criteria": c_crit,
            "responses": c_resp,
            "costs": c_cost,
        }

    except psycopg2.Error as e:
        cnx.rollback()
        # Bubble up a concise DB error; FastMCP will show this as the tool error
        raise RuntimeError(f"DB error: {e.pgerror or e}") from e
    except Exception:
        cnx.rollback()
        raise
