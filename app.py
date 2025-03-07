from crm_app import app
from crm_app.helpers.redis import init_permissions_role_to_redis, init_role_employee_to_redis
from crm_app.helpers.redis import redis_client
from crm_app.routes.routes import register_routes, api_blueprint  
from crm_app.middlewares.check_permission import check_permission

with app.app_context():
    init_permissions_role_to_redis()
    init_role_employee_to_redis()
    redis_client.set("is_restart", 1)

app.before_request(check_permission)
api = register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5007, threaded=True)