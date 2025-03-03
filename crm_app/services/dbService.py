from crm_app.services.helpers import *
from crm_app import db
from sqlalchemy import text
import math

def excute_select_data(table: str, str_get_column :str, filter, limit, page, sort, order, query_join:str = None):

    build_where = build_where_query(filter=filter) if filter else ''
    limit = int(limit) if limit else None
    page = int(page) if page else None
    skip = int(limit) * (int(page) - 1) if limit and page else 0
    
    opt_order = f" {order.upper()} " if order else "" 
    build_sort = f" ORDER BY {sort} {opt_order} " if sort else ""
    build_limit = f" LIMIT {limit}" if limit else ""
    build_offset = f" OFFSET {skip}" if limit and page else ""

    query_get_time = f"{table}.created_at as CreatedAt, {table}.updated_at as UpdatedAt, {table}.deleted_at as DeletedAt" if query_join else 'created_at as CreatedAt, updated_at as UpdatedAt, deleted_at as DeletedAt '

    query = text(f"""
                SELECT {table+'.' if query_join else '' }id as ID, {str_get_column}, {query_get_time}
                FROM {table}
                {query_join}
                {build_where}
                {build_sort}
                {build_limit}
                {build_offset}
            """)
    data = [dict(row) for row in db.session.execute(query).mappings().fetchall()]
    print("data:", data)
    total_count_query = text(f"SELECT COUNT(*) AS total FROM {table} {build_where}")
    total_count = db.session.execute(total_count_query).scalar()
    total_page = math.ceil(total_count / limit) if limit else 1

    response_data = {"data": data, "total_page": total_page}
    return response_data
