from crm_app.services.helpers import *
from crm_app import db
from sqlalchemy import text
from flask import make_response
import math
from crm_app import redis_client
from crm_app.docs.containts import get_error_response, ERROR_CODES

def excute_select_data(table: str, str_get_column :str, filter = None, limit = None, page = None, sort = None, order = None, query_join:str = None):
    build_where = build_where_query(filter=filter, table=table) if filter else f"WHERE {table}.deleted_at IS NULL"
    limit = int(limit) if limit else None
    page = int(page) if page else None
    skip = int(limit) * (int(page) - 1) if limit and page else 0
    
    opt_order = f" {order.upper()} " if order else "" 
    build_sort = f" ORDER BY {table}.{sort} {opt_order} " if sort else ""
    build_limit = f" LIMIT {limit}" if limit else ""
    build_offset = f" OFFSET {skip}" if limit and page else ""

    query_get_time = f"{table}.created_at as CreatedAt, {table}.updated_at as UpdatedAt, {table}.deleted_at as DeletedAt" 
    query_get_id_table = text(f"""
        SELECT DISTINCT {table}.id
        FROM {table}
        {'' if query_join is None else query_join}
        {build_where}
        {build_sort}
        {build_limit}
        {build_offset}
    """)
    print(query_get_id_table)
    result_ids = [row[0] for row in db.session.execute(query_get_id_table).fetchall()]
    print('result_ids:',result_ids)
    query = text(f"""
                SELECT {table+'.' if query_join is not None else '' }id as ID, {str_get_column}, {query_get_time}
                FROM {table}
                {'' if query_join is None else query_join}
                WHERE {table}.id  IN ({','.join(map(str, result_ids))})
            """)
    print("query:",query)
    data = [dict(row) for row in db.session.execute(query).mappings().fetchall()]

    total_count_query = text(f"SELECT COUNT(*) AS total FROM {table} {'' if query_join is None else query_join} {build_where}")
    total_count = db.session.execute(total_count_query).scalar()
    total_page = math.ceil(total_count / int(limit)) if limit else 1

    response_data = {"data": data, "total_page": total_page}
    return response_data

def check_reference_existence(model, column_name, value, error_code):
    if model.query.filter_by(**{column_name: value}, deleted_at=None).first():
        return make_response(get_error_response(error_code), 401)
    return None
    