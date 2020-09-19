from myhandler.MyHandler import MyHandler
import socketserver

def create_httpserver():
    with socketserver.TCPServer(("", 80), MyHandler) as http:
        http.serve_forever()

if __name__ == "__main__":
    create_httpserver()