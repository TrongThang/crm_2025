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
            if table == 'san_pham' and field == 'ten':
                field = f"san_pham.ten"

            if (field == 'loai_san_pham' 
                or field == 'don_vi_tinh'
                or field == 'loai_giam_gia'
                or field == 'thoi_gian_bao_hanh'
                or field == 'nha_phan_phoi'
                or field == 'kho'
                or field == 'chuc_vu'
            ):
                field = f"{field}.ten" 

            # if operator == 'contains':
            #     sql_condition.append(f""" {field} IS NOT NULL AND {field} LIKE '%{value}%' """)
            # elif operator == 'notcontains':
            #     sql_condition.append(f""" {field} IS NOT NULL AND {field} NOT LIKE '%{value}' """)
            # elif operator == 'startswith':
            #     sql_condition.append(f""" {field} IS NOT NULL AND {field} LIKE '{value}%' """)
            # elif operator == 'endswith':
            #     sql_condition.append(f""" {field} IS NOT NULL AND {field} LIKE '%{value}' """)
            if operator == 'contains':
                if value:  # Nếu có giá trị tìm kiếm, thì loại bỏ NULL
                    sql_condition.append(f""" ({field} IS NOT NULL AND {field} LIKE '%{value}%') """)
                else:  # Nếu không có giá trị, lấy tất cả (kể cả NULL)
                    sql_condition.append(f""" ({field} LIKE '%%' OR {field} IS NULL) """)
            elif operator == 'notcontains':
                if value:
                    sql_condition.append(f""" ({field} IS NOT NULL AND {field} NOT LIKE '%{value}%') """)
                else:
                    sql_condition.append(f""" ({field} NOT LIKE '%%') """)  
            elif operator == 'startswith':
                if value:
                    sql_condition.append(f""" ({field} IS NOT NULL AND {field} LIKE '{value}%') """)
                else:
                    sql_condition.append(f""" ({field} LIKE '%%' OR {field} IS NULL) """)
            elif operator == 'endswith':
                if value:
                    sql_condition.append(f""" ({field} IS NOT NULL AND {field} LIKE '%{value}') """)
                else:
                    sql_condition.append(f""" ({field} LIKE '%%' OR {field} IS NULL) """)
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
    print('sql_condition:', sql_condition)
    if not sql_condition:
        print('sql_condition')
        return f"WHERE {table+'.'}deleted_at IS NULL" 
    print("logical_operator:", logical_operator)
    print("sql_condition:", sql_condition)
    return " WHERE " + f" {logical_operator} ".join(sql_condition) + f" AND {table+'.'}deleted_at IS NULL"

# view-nhan-vien -> view 
def get_word_before_dash(str):
    result = ''
    for c in str:
        if(c == '-'):
            return result
        result = result + c

    return result