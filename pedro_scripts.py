# Pedro's useful scripts


def listPedroScripts():
    """
    Signature: listScripts()

    Prints the objects and functions in this file that do not start with _
    """
    print("Available Scripts:")
    for i in _dirResults:
        if str(i)[0] != "_":
            print("    " + i)


def sharepoint_list_filter_value_string(items_to_list):
    """Signature: sharepoint_list_filter_value_string(items_to_list)

    returns a string that can be pasted in the values field of a filter of
    a sharepoint list

    Args:
        items_to_list (str | iterable of strs): string separated by \n or
        iterable containing strings that will be concatenated to a filter
        string
    """
    from collections.abc import Iterable

    try:
        list_items = items_to_list.split("\n")
    except AttributeError:
        list_items = items_to_list

    return "%3B%23".join(list_items)


def calcdeltas(last, curr, ret=None):
    """
    Signature: calcdeltas(last,curr,ret=None)

    returns a list of deltas (as float) between last and current
    the function will zip the two arguments, matching 1st item of
    last to 1st item

    last: iterable with starting points
    curr: iterable with ending points
    ret :  optional string that determines the type of return
        None or float: returns the proportion (current - last)/last
        difference: current - last
        percent: the signed percentage change (eg -35%)
        full: dictionary with the difference, float, and percent
    """
    ret_difference = [(c - l) for l, c in zip(last, curr)]
    ret_float = [dif / l for dif, l in zip(ret_difference, last)]
    ret_percent = [f"{f:+.0%}" for f in ret_float]
    if ret is None or ret == "float":
        return ret_float
    elif ret == "difference":
        return ret_difference
    elif ret == "percent":
        return ret_percent
    elif ret == "full":
        print(
            "returning a dictionary with the following keys{'difference': ... , 'float': ..., 'percent': ...}"
        )
        return {
            "difference": ret_difference,
            "float": ret_float,
            "percent": ret_percent,
        }
    else:
        print("wrong type ret provided, returning the default list with floats")
        return ret_float


def clean_emails_outlook(email_string, print_line=None, sep="; "):
    """
    Signature: clean_emails_outlook(email_string, print_line = None, sep="; ")

    Given a email string coming from outlook, finds actual email addresses and
    returns them as a list of strings

    email_string:   string with an email coming from a copy/past from outlook,
                    with the actual email address between < and >
    print_line:     If None, will only return the list (default behavior)
                    if equals to "one_line", will print all found emails in one line
                    separated by separator sep.
                    if "multiple", will print all found emails, each in one line, with
                    separator sep
    sep:            separator for the print statement (if print_line is not None)

    """
    import re

    pat = re.compile(r"(?<=\<)(.*?@.*?)(?=\>)")
    r = pat.findall(email_string)
    if print_line == "one_line":
        for i in r:
            print(i, end=sep)
    elif print_line == "multiple":
        for i in r:
            print(i + sep)
    else:
        for i in r:
            print(i)
    return r


def pbi_teams_url(url="", print_or_return="print", copy_to_clipboard=True):
    """
    Signature: pbi_teams_url(url="", print_or_return="print")

    Parses the new URLs coming from the 'Chat in Teams' feature in PowerBI
    and shortens them so they can be used in Office files and SharepPoint Lists

    url:            the url in question if None or empty string, will use what's in the clipboard
    print_or_return:if "print", will only print the resuting
    """
    import urllib.parse as up
    import json
    import pyperclip

    valid_starting_str = "https://teams.microsoft.com/l/entity/"

    if not url:
        url = pyperclip.paste()
        print("Copied from clipboard!")
        if not url.startswith(valid_starting_str):
            print(
                f"URL doesn't look like a bookmark sharing (starts with {url[0:len(valid_starting_str)]}"
            )

    # extract the parameter 'context' from the url and url-decode it
    parsed = up.urlparse(url)
    j = up.parse_qs(parsed.query)["context"][0]
    # the parameter is a json string. Bring it to a dictionary in Python and
    # extract the real url
    d = json.loads(j)
    real_url = d["subEntityId"]

    # build the url
    new_url = up.unquote(d["subEntityId"])

    if copy_to_clipboard:
        pyperclip.copy(new_url)
        print("Simplified URL copied to clipboard!")

    if print_or_return == "print":
        print(new_url)
    else:
        return new_url


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


def make_json(csvFilePath, jsonFilePath, key_column):
    """
    Signature: make_json(csvFilePath, jsonFilePath)

    Function to convert a CSV to JSON
    Takes the file paths as arguments

    """
    import csv
    import json

    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:

            # Assuming a column named 'No' to
            # be the primary key
            key = rows[key_column]
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))


def flatten(list_of_lists):
    """Flattens a list of lists (2 levels)

    Args:
        list_of_lists (list): list of lists (ie: [ [a,b], [c], []])

    Returns:
        list: a single list with all the items of the list_of_lists
    """
    return [item for sublist in list_of_lists for item in sublist]


##################################################################################################
# module load code
_dirResults = dir()
_dirResults.sort()
if __name__ == "__main__":
    pass
else:
    print("Helper Scripts loaded!")
    listPedroScripts()
