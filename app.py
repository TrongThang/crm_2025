from crm_app import app
from crm_app.helpers.redis import init_permissions_role_to_redis, init_role_employee_to_redis
from crm_app.helpers.redis import redis_client
from crm_app.routes.routes import register_routes, api_blueprint  
from crm_app.middlewares.check_permission import check_permission
import time
from crm_app import db

def wait_for_db():
    while True:
        try:
            db.session.execute('SELECT 1')
            print("MySQL connected")
            break
        except Exception as e:
            print(f"Waiting for MySQL: {e}")
            time.sleep(1)

with app.app_context():
    init_permissions_role_to_redis()
    init_role_employee_to_redis()
    redis_client.set("is_restart", 1)
    wait_for_db()

app.before_request(check_permission)
api = register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)