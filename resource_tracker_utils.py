import pandas as pd


def generate_sql_snapshot_insert_values(dfrow):
    """Generates a line of the VALUES part of an INSERT query in the
    Resource Tracker snapshot table, replacing nas for NULLs

    Args:
        dfrow (pandas.Series): dataframe row containing all columns from the resource Tracker
        namely: 'sapid', 'period', 'month', 'employee_name', 'employment_status',
        'employee_group', 'employee_subgroup_code', 'employee_subgroup_text',
        'contract_end', 'service_date', 'company_code', 'company_code_name',
        'cost_center_code', 'cost_center_name', 'cost_center_category',
        'position_id', 'position_name', 'global_role_non_na_cost', 'superior_sapid',
        'superior', 'organization', 'stream', 'function', 'opco', 'reason_for_leaving',
        'business_resource', 'global_resource_work', 'personnel_administrator',
        'location', 'location_description', 'building', 'building_name', 'status',
        'hybrid_scope', 'comment', 'userid', 'email_address',

    Returns:
        str: 1 item of the VALUES part of the INSERT query
    """
    ret = f"({dfrow['sapid']}, '{dfrow['period']}', '{dfrow['month']}', '{dfrow['employee_name']}', '{dfrow['employment_status']}', "
    ret += f"'{dfrow['employee_group']}', '{dfrow['employee_subgroup_code']}', '{dfrow['employee_subgroup_text']}', "
    ret += f"'{dfrow['contract_end']}', '{dfrow['service_date']}', '{dfrow['company_code']}', '{dfrow['company_code_name']}', "
    ret += f"'{dfrow['cost_center_code']}', '{dfrow['cost_center_name']}', '{dfrow['cost_center_category']}', {dfrow['position_id']}, "
    ret += f"'{dfrow['position_name']}', '{dfrow['global_role_non_na_cost']}', {dfrow['superior_sapid']}, '{dfrow['superior']}', "
    ret += f"'{dfrow['organization']}', '{dfrow['stream']}', '{dfrow['function']}', '{dfrow['opco']}', '{dfrow['reason_for_leaving']}', "
    ret += f"'{dfrow['business_resource']}', '{dfrow['global_resource_work']}', '{dfrow['personnel_administrator']}', '{dfrow['location']}', "
    ret += f"'{dfrow['location_description']}', '{dfrow['building']}', '{dfrow['building_name']}', '{dfrow['status']}', "
    ret += f"'{dfrow['hybrid_scope']}','{dfrow['comment']}','{dfrow['userid']}','{dfrow['email_address']}')"

    return ret.replace("'nan'", "NULL")


def generate_sql_insert_snapshot(df):
    """Creates an INSERT query for the resource_tracker_snapshot table
    based on a dataframe with the right columns

    Args:
        df (pandas.DataFrame): df containing the lines to be inserted, with the
        following columns: 'sapid', 'period', 'month', 'employee_name', 'employment_status',
        'employee_group', 'employee_subgroup_code', 'employee_subgroup_text',
        'contract_end', 'service_date', 'company_code', 'company_code_name',
        'cost_center_code', 'cost_center_name', 'cost_center_category',
        'position_id', 'position_name', 'global_role_non_na_cost', 'superior_sapid',
        'superior', 'organization', 'stream', 'function', 'opco', 'reason_for_leaving',
        'business_resource', 'global_resource_work', 'personnel_administrator',
        'location', 'location_description', 'building', 'building_name', 'status',
        'hybrid_scope', 'comment', 'userid', 'email_address',

    Returns: the INSERT statment as a string
    """
    ret = """INSERT INTO [vcort].[resource_tracker_snapshot]
           ([sapid]
           ,[period]
           ,[month]
           ,[employee_name]
           ,[employment_status]
           ,[employee_group]
           ,[employee_subgroup_code]
           ,[employee_subgroup_text]
           ,[contract_end]
           ,[service_date]
           ,[company_code]
           ,[company_code_name]
           ,[cost_center_code]
           ,[cost_center_name]
           ,[cost_center_category]
           ,[position_id]
           ,[position_name]
           ,[global_role_non_na_cost]
           ,[superior_sapid]
           ,[superior]
           ,[organization]
           ,[stream]
           ,[function]
           ,[opco]
           ,[reason_for_leaving]
           ,[business_resource]
           ,[global_resource_work]
           ,[personnel_administrator]
           ,[location]
           ,[location_description]
           ,[building]
           ,[building_name]
           ,[status]
           ,[hybrid_scope]
           ,[comment]
           ,[userid]
           ,[email_address])
     VALUES
"""
    for row in df.to_dict(orient="records"):
        ret += "           " + generate_sql_snapshot_insert_values(row) + ",\n"

    # remove the trailing comma
    ret = ret[:-2]

    return ret
