from locust import HttpUser, task, between

# class WebsiteUser(HttpUser): # Usuario
#     wait_time = between(2, 5) # tiempo de accion del usuario, entre 5 y 15 seg aleatorio

#     @task # cada funcion decorada con task es una tarea que va a realizar nuestro user
#     def index(self):
#         self.client.get("/")

#     # en esa task se indica un "peso", 
#     # por lo que esta tarea es dos veces mas probable de ejecutarse cmo accion del usuario que la que por defecto no tiene nada () y equivale a 1
#     @task(2) 
#     def about(self):
#         self.client.get("/contacto")

class AuthenticatedUser(HttpUser):
    def on_start(self):
        """Ejecutado cuando un Locust comienza a correr."""
        self.client.post("/login", {"username": "jzuazo", "password": "123456"})

    def on_stop(self):
        """Ejecutado cuando un Locust termina de correr (se desconecta)."""
        self.client.post("/logout")

    @task
    def my_task(self):
        self.client.get("/perfil")