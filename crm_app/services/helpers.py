import json

def build_where_query(filter, table = None):
    filter = json.loads(filter)
    sql_condition = []
    logical_operator = "AND"
    if len(filter) > 0:
        for item in filter:
            field = item["field"]
            operator = item["condition"]
            value = item["value"]
            if (field == 'loai_san_pham' 
                or field == 'don_vi_tinh'
                or field == 'loai_giam_gia'
                or field == 'thoi_gian_bao_hanh'
            ):
                field = f"{field}.ten" 
            if operator == 'contains':
                sql_condition.append(f""" {field} LIKE '%{value}%' """)
            elif operator == 'notcontains':
                sql_condition.append(f""" {field} NOT LIKE '%{value}' """)
            elif operator == 'startswith':
                sql_condition.append(f""" {field} LIKE '{value}%' """)
            elif operator == 'endswith':
                sql_condition.append(f""" {field} LIKE '%{value}' """)
            elif operator == '=':
                sql_condition.append(f""" {field} = '{value}' """)
            elif operator == '<>':
                sql_condition.append(f""" {field} <> '{value}' """)
            elif operator == '<':
                sql_condition.append(f""" {field} < {0 if value == '' else value} """)
            elif operator == '>':
                sql_condition.append(f""" {field} > {0 if value == '' else value} """)
            if operator == '<=':
                sql_condition.append(f""" {field} <= {0 if value == '' else value} """)
            if operator == '>=':
                sql_condition.append(f""" {field} >= {0 if value == '' else value} """)
    if not sql_condition:
        return f"WHERE {table+'.' if table else ''}deleted_at IS NULL" 
    print("logical_operator:", logical_operator)
    print("sql_condition:", sql_condition)
    return " WHERE " + f" {logical_operator} ".join(sql_condition) + f" AND {table+'.' if table else ''}deleted_at IS NULL"

# view-nhan-vien -> view 
def get_word_before_dash(str):
    result = ''
    for c in str:
        if(c == '-'):
            return result
        result = result + c

    return result