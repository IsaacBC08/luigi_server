import http.server
import socketserver
import json

# Define el puerto en el que quieres que el servidor escuche
PORT = 8000
last_key = None

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Sirve el archivo HTML
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("index.html", "r") as file:
                self.wfile.write(file.read().encode('utf-8'))
        else:
            # Responder con la última tecla recibida
            response = {
                "status": "ok",
                "last_key": last_key
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        global last_key
        # Establecer la longitud del contenido
        content_length = int(self.headers['Content-Length'])
        # Leer el cuerpo de la solicitud
        post_data = self.rfile.read(content_length)
        # Parsear el JSON recibido
        key_data = json.loads(post_data)
        key = key_data.get('key')

        # Manejar la tecla recibida (puedes agregar más lógica aquí)
        print(f"Tecla recibida: {key}")
        last_key = key

        # Responder con un mensaje JSON
        response = {
            "status": "ok",
            "key_received": key
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

# Crea una instancia del servidor
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("Servidor web básico corriendo en el puerto", PORT)
    # Pon el servidor en funcionamiento y mantenlo funcionando hasta que se interrumpa con Ctrl+C
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("^C recibido, cerrando el servidor...")
        httpd.server_close()
