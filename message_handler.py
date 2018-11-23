from Crypto.PublicKey import RSA
from base64 import b64decode, b64encode


class MessageHandler:
    def __init__(self, con, bsize, pubkey, prvkey):
        self.con = con
        self.bsize = bsize
        self.con.send(pubkey)
        con_key = self.con.recv(self.bsize)
        self.con_key = RSA.importKey(con_key)
        self.prvkey = RSA.importKey(prvkey)

    def receive_message(self):
        data = ''
        cycles = self.con.recv(self.bsize).decode("utf-8")
        if cycles == '':
            return ''
        cycles = int(cycles)
        while cycles > 0:
            chunk = self.con.recv(self.bsize).decode("utf-8")
            data += chunk
            cycles -= 1

        # don't touch before it
        data = b64decode(data)
        data = self.prvkey.decrypt(data)
        return data.decode('utf-8')

    def send_message(self, data):
        print("Data:", data)
        data = self.con_key.encrypt(data.encode('utf-8'), 32)[0]
        # base64encode data
        data = b64encode(data)

        # actual starts here, don't touch after it
        cycles = (len(data) // self.bsize) + 1
        cyc_strl = len(str(cycles))
        load = str(cycles)
        for i in range(cyc_strl, self.bsize):
            load += ' '
        try:
            self.con.send(load.encode("utf-8"))
        except BrokenPipeError:
            print("BrokenPipeError detected")
            return
        offset = 0
        while cycles > 0:
            try:
                self.con.send(
                    data[offset: offset + self.bsize])
            except BrokenPipeError:
                print("BrokenPipeError detected")
                break
            offset += self.bsize
            cycles -= 1

    def close(self):
        self.con.close()

    def encrypt(self):
        pass

    def decrypt(self, data):
        return data
