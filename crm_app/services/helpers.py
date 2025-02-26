def build_where_query(filter):
    sql_condition = []
    logical_operator = "AND"
    for item in filter:
        if isinstance(item, list):
            field, operator, value = item
            if (field == 'loai_san_pham' 
                or field == 'don_vi_tinh'
                or field == 'loai_giam_gia'
                or field == 'thoi_gian_bao_hanh'
            ):
                field = f"{field}.ten" 
            elif field == 'ten':
                field = f"san_pham.{field}"

            if operator == 'contains':
                sql_condition.append(f" {field} LIKE '%{value}%' ")
            elif operator == 'notcontains':
                sql_condition.append(f" {field} NOT LIKE '%{value}'")
            elif operator == 'startswith':
                sql_condition.append(f" {field} LIKE '{value}%'")
            elif operator == 'endswith':
                sql_condition.append(f" {field} LIKE '%{value}'")
            elif operator == '=':
                sql_condition.append(f" {field} = '{value}'")
            elif operator == '<>':
                sql_condition.append(f" {field} <> '{value}'")
            elif operator == '<':
                sql_condition.append(f" {field} < {value}")
            elif operator == '>':
                sql_condition.append(f" {field} > {value}")
            if operator == '<=':
                sql_condition.append(f" {field} <= {value}")
            if operator == '>=':
                sql_condition.append(f" {field} >= {value}")
        elif isinstance(item, str):
            logical_operator = item.upper()

    return " WHERE " + f" {logical_operator} ".join(sql_condition)

