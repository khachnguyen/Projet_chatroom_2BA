import pickle, socket, struct, sys, threading

SERVERADDRESS = (socket.gethostname(), 5000)
ls_users = {}

class Server():

    def __init__(self):
        self.__server = socket.socket()
        try:
            self.__server.bind(SERVERADDRESS)
        except socket.error:
            print('Bind raté {}'.format(socket.error))

        self.__server.listen()
    def run(self):
        print( "Ecoute ... {}".format(SERVERADDRESS))
        while True:
            client, addr = self.__server.accept()
            th = ThreadClient(client, addr)
            th.start()
            client.send("Accueil".encode())

    def exit(self):
        self.__server.close()


class ThreadClient(threading.Thread):
    def __init__(self, connection, addr):
        threading.Thread.__init__(self)
        self.connection = connection
        self.addr = addr
        self.commands = {
            '/list': self._list,
            '/addPseudo': self._addPseudo,
        }

    def run(self):
        ls_users[self.addr] = [self.connection, "", "active"]
        while True:
            data = self.connection.recv(1024).decode()
            if data[0] == "/":
                line = data.rstrip() + ' '
                commande = line[:line.index(' ')]
                param = line[line.index(' ')+1:].rstrip()
                params = [param, self.addr]
                if commande in self.commands:
                    try:
                        self.commands[commande](self.connection) if param == '' else self.commands[commande](params)
                    except Exception as e:
                        print("Erreur pendant l'éxécution de la commande")

                else:
                    print('Commande introuvable :', commande)
            elif not data:
                break
            else:
                message = "{}> {}".format(ls_users[self.addr][1], data)
                print(message)
                for cle in ls_users:
        	         if cle != self.addr:
        	            ls_users[cle][0].send(message.encode())

    def _addPseudo(self, params):
        print("ceci est un", params)
        ls_users[params[1]][1] = params[0]
        msg = "{} vient de se connecter".format(params[0])
        for cle in ls_users:
             if cle != self.addr:
                ls_users[cle][0].send(msg.encode())

    def _list(self, client):
        users = ""
        for x in ls_users:
            print (x,"yooo", ls_users)
            users += "- {} - IP : {} - Port : {}\n".format(ls_users[x][1], x[0],x[1])
        self.connection.send(('Il y a actuellement {} connecté'.format(len(ls_users))).encode())
        self.connection.send(users.encode())


if __name__ == '__main__':
    Server().run()
