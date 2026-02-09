import os
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        mime_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.ico': 'image/x-icon',
            '.svg': 'image/svg+xml',
        }

        # Получаем путь к запрашиваемому файлу
        path = self.path

        # Если запрашивается корневой путь, отдаём contacts.html
        if path == '/':
            path = '/contacts.html'

        try:
            # Определяем расширение файла
            _, ext = os.path.splitext(path)
            content_type = mime_types.get(ext.lower(), 'text/plain')

            # Открываем и читаем файл
            file_path = '.' + path  # Добавляем точку для относительного пути

            # Проверяем, существует ли файл
            if not os.path.exists(file_path):
                self.send_error(404, "File not found")
                return

            with open(file_path, 'rb') as file:
                content = file.read()

            # Отправляем успешный ответ
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            # Отправляем содержимое файла
            self.wfile.write(content)

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
