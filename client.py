from socket import socket, AF_INET, SOCK_STREAM
from message_handler import MessageHandler
from string_match import match
from rsa_ops import init_rsa


class Client:
    def __init__(self, server_adr, bsize=1024):
        self.server_adr = server_adr  # a tuple
        self.bsize = bsize
        self.pubkey, self.privkey = init_rsa()

    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(self.server_adr)
        print("Client started")
        mh = MessageHandler(sock, self.bsize, self.pubkey, self.privkey)
        print("Enter command after the PocketDB > prompt. Enter .exit to exit")
        while True:
            print("PocketDB > ", end='')
            command = input().strip()
            if command == ".q":
                mh.send_message("\n")
                break
            if command.startswith("filter"):
                mh.send_message("select")
                data = mh.receive_message()
                lines = data.split("\n")
                lines = lines[1:-1]
                words = [i.strip() for i in lines]
                target = command.split()[1:]
                target = ' '.join(target)
                rst = []
                words.pop()
                for word in words:
                    if match(target, word.split(',')[1].strip()):
                        rst.append(word)
                print(">Matched results:")
                print(rst)
                continue
            mh.send_message(command)
            data = mh.receive_message()
            if data == "\n\n\n":
                break
            print(data)
        print("Database connection closed")


if __name__ == '__main__':
    client = Client(('127.0.0.1', 9001))
    client.run()
