import socket
import subprocess
import zlwLog

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        locale_ip = s.getsockname()[0]
    except:
        locale_ip = ''
    finally:
        s.close()
    return locale_ip


# 服务端，执行命令端
def start_server(IP):
    log = zlwLog.logging_setting()
    while 1:
        # 创建socket对象
        servers = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将socket绑定到指定的地址和端口号
        servers.bind((IP, 6565))
        # 监听客户端链接操作
        servers.listen(1)
        log.info('等待用户接入....')
        client_socket, client_address = servers.accept()
        log.info('用户{}已接入'.format(client_address))
        data = client_socket.recv(1024)
        # 没有数据返回
        if not data:
            log.info('用户{}已关闭连接'.format(client_address))
            servers.close()
            continue
        try:
            result = subprocess.run(data.decode().split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
            cmds = ''
            for c in result.args: cmds += str(c) + ' '
            cmds = "[" + cmds + "]"
            log.info("用户{}-输入: {},输出: ->\n{}".format(client_address,cmds,result.stdout.decode('utf-8')))
            client_socket.sendall(result.stdout)
            servers.close()
        except subprocess.TimeoutExpired:
            log.error('此命令可能是一个终端命令，等待执行完成超过5s自动已自动退出！！！')
            client_socket.sendall('此命令可能是一个终端命令，等待执行完成超过5s自动已自动退出！！！'.encode())
            servers.close()
            continue
        except FileNotFoundError:
            log.error('命令错误，请查正重试！！')
            client_socket.sendall('命令错误，请查正重试！！'.encode())
            servers.close()
            continue


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    start_server(get_local_ip())
