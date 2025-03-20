from flask import make_response
from crm_app.services.dbService import get_error_response, excute_select_data
from crm_app.docs.containts import ERROR_CODES
from crm_app.services.HoaDonXuatKhoService import get_hoa_don_xuat_kho
from crm_app.services.HoaDonNhapKhoService import get_hoa_don_nhap_kho
import math

def get_cong_no_khach_hang(limit, page, sort, order):
    filter = '[{"field": "con_lai", "condition": ">", "value": 0}]'
    print('limit:',limit)
    result = get_hoa_don_xuat_kho(filter=filter, limit=limit, page=page, sort=sort, order=order)
    print(result)
    if result.status_code != 200:
        return result
    
    dict_khach_hang = (result.json)["data"]["data"]
    grouped_data = {}
    print("dict_khach_hang:", dict_khach_hang)
    for item in dict_khach_hang:
        print("item:",item.get("khach_hang_id"))
        khach_hang_id = item.get("khach_hang_id")

        if khach_hang_id not in grouped_data:
            grouped_data[khach_hang_id] = {
                "khach_hang_id": item.get("khach_hang_id"),
                "khach_hang": item.get("khach_hang"),
                "tong_tien": 0,
                "tra_truoc": 0,
                "con_lai": 0,
                "tong_hoa_don": 0
            }

        grouped_data[khach_hang_id]["tong_tien"]    += item.get("tong_tien")
        grouped_data[khach_hang_id]["tra_truoc"]    += item.get("tra_truoc")
        grouped_data[khach_hang_id]["con_lai"]      += item.get("con_lai")
        grouped_data[khach_hang_id]["tong_hoa_don"] += 1
    
    result_list = list(grouped_data.values())
    total_page = math.ceil(len(result_list) / int(limit)) if limit else 1

    response_data = {
        "data": result_list,
        "total_page": total_page
    }
    return get_error_response(ERROR_CODES.SUCCESS, result=response_data)

def get_cong_no_nha_phan_phoi(limit, page, sort, order):
    filter = '[{"field": "con_lai", "condition": ">", "value": 0}]'
    limit = limit if limit else 0
    result = get_hoa_don_nhap_kho(filter=filter, limit=limit, page=page, sort=sort, order=order)
    print(result)
    if result.status_code != 200:
        return result
    
    dict_nha_phan_phoi = (result.json)["data"]["data"]
    grouped_data = {}
    for item in dict_nha_phan_phoi:
        print("item:",item.get("nha_phan_phoi_id"))
        nha_phan_phoi_id = item.get("nha_phan_phoi_id")
        if nha_phan_phoi_id is not None:
            if nha_phan_phoi_id not in grouped_data:
                grouped_data[nha_phan_phoi_id] = {
                    "nha_phan_phoi_id": item.get("nha_phan_phoi_id"),
                    "nha_phan_phoi": item.get("nha_phan_phoi"),
                    "tong_tien": 0,
                    "tra_truoc": 0,
                    "con_lai": 0,
                    "tong_hoa_don": 0
                }

            grouped_data[nha_phan_phoi_id]["tong_tien"]    += item.get("tong_tien")
            grouped_data[nha_phan_phoi_id]["tra_truoc"]    += item.get("tra_truoc")
            grouped_data[nha_phan_phoi_id]["con_lai"]      += item.get("con_lai")
            grouped_data[nha_phan_phoi_id]["tong_hoa_don"] += 1
    
    result_list = list(grouped_data.values())
    total_page = math.ceil(len(result_list) / limit) if limit else 1

    response_data = {
        "data": result_list,
        "total_page": total_page
    }
    return get_error_response(ERROR_CODES.SUCCESS, result=response_data)