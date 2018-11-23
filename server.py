from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
# from subprocess import Popen, PIPE, STDOUT
import pexpect
from message_handler import MessageHandler
from rsa_ops import init_rsa


class Server:
    def __init__(self, ip, port, n_con, bsize=1024):
        self.ip = ip
        self.port = port
        self.n_con = n_con
        self.bsize = bsize
        self.pubkey, self.privkey = init_rsa()
        # print("pub:", self.pubkey)

    def show_attrs(self):
        print(self.ip, self.port, self.n_con)

    def handle_client(self, mh, child):
        while True:
            data = mh.receive_message().strip()
            if not data:
                print(">> Client disconnected")
                break
            print("Client says:", data)
            # qh = QueryHandler(data)
            # result = qh.run()
            # print("<> Data sent to query_handler and query ran")
            # res = p.communicate(input=data.encode("utf-8"))[0]
            # child.expect(b"db >*")
            child.sendline(data)
            if data == '.exit':
                mh.send_message("\n\n\n")
                print(">> Client closed the database connection")
                break
            child.expect(b"db >*")
            res = child.before
            print("Result obtained:", res)
            if res == b'':
                res = b'\n'
            mh.send_message(res.decode("utf-8"))
        mh.close()

    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self.ip, self.port))
        sock.listen(self.n_con)
        print("Starting db server..")
        # p = Popen(
        #    # ["./db_bin", "db.pocketdb"], stdin=PIPE, stdout=PIPE,
        #    # stderr=STDOUT
        # )
        while True:
            child = pexpect.spawn("./db_bin db.pocketdb")
            child.expect(b"db >*")
            print("Db server started")
            cl, addr = sock.accept()
            print(">> Connected to a new client")
            mh = MessageHandler(cl, self.bsize, self.pubkey, self.privkey)
            Thread(target=self.handle_client, args=(mh, child)).start()


if __name__ == '__main__':
    server = Server('127.0.0.1', 9001, 3)
    server.run()
