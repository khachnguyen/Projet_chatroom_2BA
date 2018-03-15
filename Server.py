import pickle, socket, struct, sys, threading
#/join_server DESKTOP-P9NPJL4 5000
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
            client.send("AccueilServer".encode())

    def exit(self):
        self.__server.close()


class ThreadClient(threading.Thread):
    def __init__(self, connection, addr):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__addr = addr
        self.__commands = {
            '/list': self._list,
            '/addPseudo': self._addPseudo,
            '/quit': self._quit,
        }

    def run(self):
        ls_users[self.__addr] = [self.__connection, ""]
        while True:
            data = self.__connection.recv(1024).decode()
            if data[0] == "/":
                line = data.rstrip() + ' '
                commande = line[:line.index(' ')]
                param = line[line.index(' ')+1:].rstrip()
                params = [param, self.__addr]
                if commande in self.__commands:
                    try:
                        self.__commands[commande](self.__connection) if param == '' else self.__commands[commande](params)
                    except Exception as e:
                        print("Erreur pendant l'éxécution de la commande")
                else:
                    print('Commande introuvable :', commande)
            else:
                message = "[{}] : {}".format(ls_users[self.__addr][1], data)
                print(message)
                for user in ls_users:
        	         if user != self.__addr:
        	            ls_users[user][0].send(message.encode())

    def _addPseudo(self, params):
        ls_users[params[1]][1] = params[0]
        msg = "Connexion de {} ".format(params[0])
        for user in ls_users:
             if user != self.__addr:
                ls_users[user][0].send(msg.encode())

    def _list(self, client):
        users = ""
        for x in ls_users:
            users += "- {} - IP : {} - Port : {}\n".format(ls_users[x][1], x[0],x[1])
        self.__connection.send(('Il y a actuellement {} connecté'.format(len(ls_users))).encode())
        self.__connection.send(users.encode())
        
    def _quit(self, pseudo):
        for user in ls_users:
            if ls_users[user][1] == pseudo[0]:
                self.__connection.send(("Deconnexion en cours...").encode())
                del ls_users[user]
                for us in ls_users:
                    print("HELLOE TOI", len(ls_users))
                    ls_users[us][0].send(("{} s'est déconnecté ".format(pseudo[0])).encode())

        
        


if __name__ == '__main__':
    Server().run()