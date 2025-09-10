from pprint import pprint

from db_access import (
    get_all_vendors,
    get_all_criteria_categories,
    get_all_criteria,
    get_all_responses,
    get_all_costs
)

if __name__ == "__main__":
    print("Vendors:")
    pprint(get_all_vendors())
    print("\nCriteria Categories:")
    pprint(get_all_criteria_categories())
    print("\nCriteria:")
    pprint(get_all_criteria())
    print("\nResponses:")
    pprint(get_all_responses())
    print("\nCosts:")
    pprint(get_all_costs())
