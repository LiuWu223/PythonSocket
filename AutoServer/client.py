import socket

def start_client():
    while 1:
        try:
            clients = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            # 设置超时时间，超时返回超时异常
            clients.settimeout(10)
            # 连接服务器
            server_ip = '192.168.3.121'
            try:
                clients.connect((server_ip,6565))
            except ConnectionRefusedError:
                print("服务器已断开，请重新启动服务器！")
                clients.close()
                break
            command = input("请输入")
            clients.sendall(command.encode())
            data = clients.recv(1024)
            # 数据编码根据实际情况改变，utf-8\gbk\等
            print(data.decode('utf-8'))
            clients.close()
        except socket.timeout:
            print("数据接收超时")
        except ConnectionResetError:
            print("与服务端已断开连接，检查服务端并重启服务端！！")
        continue
start_client()