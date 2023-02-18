from app.google_sheets import views
from pathlib import Path

static_dir = Path(Path().absolute(), 'static')

# настраиваем пути, которые будут вести к нашей странице
def setup_routes(app):
   app.router.add_get("/", views.index)
   app.router.add_get("/sign-in/", views.sign_in)
   app.router.add_post("/sign-in/", views.sign_in)
   app.router.add_get("/logout/", views.logout)
   app.router.add_get('/dashboard/', views.dashboard)
   app.router.add_get('/connection-types/', views.connection_types)
   app.router.add_get('/hard-connection-type/', views.hard_connection_type)
   app.router.add_post('/hard-connection-type/', views.hard_connection_type)
   app.router.add_get('/dashboard/metrika/', views.metrika)
   app.router.add_get('/dashboard/analytics/', views.analytics)
   app.router.add_post('/dashboard/metrika/new-connection/', views.metrila_new_connection)
   app.router.add_post('/dashboard/analytics/new-connection/', views.analytics_new_connection)
   app.router.add_static('/static/', path=static_dir, name='static')