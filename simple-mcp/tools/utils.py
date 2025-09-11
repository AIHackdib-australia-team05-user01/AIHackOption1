from typing import List, Tuple
import psycopg2.extras as extras

def exec_values_upsert(cur, sql_prefix: str, rows: List[Tuple], template: str, suffix: str = ""):
    if not rows:
        return 0
    sql = sql_prefix + " VALUES %s " + suffix
    extras.execute_values(cur, sql, rows, template=template)
    return len(rows)
