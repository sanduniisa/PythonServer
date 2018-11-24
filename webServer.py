import socket
import threading


folder = 'SA_server'
host = 'localhost'
port = 8080


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def on():
    try:
        server_socket.bind((host, port))
        connection()

    except OSError:
        print("OSError")
        off()
        
def connection():
    server_socket.listen(1)  # number of invalid connections before termination
    while True:
        (client, address) = server_socket.accept()
        threading.Thread(target= r, args=(client,)).start()  # with threading
        


def r(client):  #r :client request function
    while True:
        
        info = client.recv(1024).decode()
        if not info:
            break
        
        print(info)

        try:
            f = info.split(' ')[1]  #split from the spaces
            if f == "/":   
                f = "/abc.html"

            p = folder + f  #p is the path of the file

            t = f.split('.')[1] #t is the type of the file

            a = open(p, 'rb') #rb:- read in bytes
            output = a.read()
            a.close()
            print("Your File is : " + p)
            c = message(200, t)  #header of the response
            print(c)

        

        except FileNotFoundError as e:

            p = folder + '/404.html'  #p is the path of the file

            t = f.split('.')[1] #t is the type of the file

            a = open(p, 'rb') #rb:- read in bytes
            output = a.read()
            a.close()
            print("Your File is : " + p)
            c = message(404, "html")  #header of the response
            print(c)

        except Exception as e:
            c = "HTTP/1.1 400 Bad Request\n\n"
            output = b"<html><body><center><h1>Bad Request</h1></center></body></html>"

            
            
        response = c.encode()
        response = response + output

        client.send(response)
        client.close()
        break

def message(msg_code, t):  #t is the type of the file
    
    head = ''
    if msg_code == 200:
        head = head + 'HTTP/1.1 200 OK\n'
        
    elif msg_code == 404:
        head = head + 'HTTP/1.1 404 Not Found\n'
        


    if t == 'jpg' or t == 'jpeg':
        head = head + 'Content-Type: image/jpeg\n'
        
    elif t == 'htm' or t == 'html':
             head = head + 'Content-Type: text/html\n'
        
    elif t == 'png':
        head = head + 'Content-Type: image/png\n'
        
        
    head = head + '\n'
    return head



def off():
    try:
        print("Server shutting down")
        server_socket.shutdown(socket.SHUT_RDWR)  #RDWR:- No reads/Writes
    except Exception:
        pass
        


on()
