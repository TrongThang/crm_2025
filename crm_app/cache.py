import redis
import time 


r = redis.Redis(host='localhost', port=6379)

r.set("Viet Nam", "Ho Chi Minh City")

r.mset( {"f1": 'abc',
    "f2": 'nn',
    "f3": 'as'},)


VietNam_capital = r.get("Viet Nam")
print(VietNam_capital)
print(r.get("f1"))
print(r.get("f2"))

r.psetex("Germany", 5000, "100ms")

if (r.exists("f3")):
    print(r.get("f3"))
else:
    print("Không tìm thấy redis")

time.sleep(2)
