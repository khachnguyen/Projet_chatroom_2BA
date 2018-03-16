import pickle, socket, struct, sys, threading

class Client():

    def __init__(self, host="0.0.0.0", port=6000, pseudo="pseudoAzErTy"):
        self.__socket = socket.socket()
        self.__socket.bind((host, port))
        self.__socket_UDP = socket.socket(type = socket.SOCK_DGRAM)
        self.__socket_UDP.bind((host, port))
        self.__pseudo = pseudo
        print('Écoute sur {}:{}'.format(host, port))

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join_server': self._join_server,
            '/join_ip' : self._join_IP,
            '/send': self._send,
            '/list': self._list,
            '/help': self._help,
            '/client' : self._client,
        }
        self.__running = True
        self.__address = None
        threading.Thread(target=self._receive_pv).start()
        while self.__running:
            line = sys.stdin.readline().rstrip() + ' '
            # Extract the command and the param
            command = line[:line.index(' ')]
            param = line[line.index(' ')+1:].rstrip()
            # Call the command handler
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Erreur")
            else:
                print('Commande inconnue:', command)
                
    def _client(self):
        print(self.__address)
        
    def _exit(self):
        self.__running = False
        self.__address = None
        self.__socket.close()
        self.__socket_UDP.close()
        
    def _quit(self):
        if self.__pseudo =='pseudoAzErTy' :
            self.__address = None
            print('Vous vous êtes deconnecté')
        else :
            self.__address = None
            self.__socket.send(('/quit {}'.format(self.__pseudo)).encode())
            self.__pseudo ='pseudoAzErTy'


    def _help(self):
        print("""\n/join_server [ADRESSE IP][PORT]permet de rejoindre le serveur\n
/join_ip [ADRESSE IP][PORT] permet de se connecter à un une autre personne\n
/send permet d'envoyer un message\n
/list permet d'afficher la liste des clients connectés si vous êtes connectés au serveur\n
/quit permet de quitter le serveur, la personne à qui vous vous etes connecté\n
/exit permet de quitter le programme\n
        """)

    def _list(self):
        self.__socket.send("/list ".encode())

    def _join_server(self, param):
        if self.__pseudo!= " ":
            self.__pseudo = input("Choisi ton pseudo : ")

        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (tokens[0], int(tokens[1]))
                self.__socket.connect(self.__address)
                threading.Thread(target=self._receive).start()
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur de connexion au serveur")

        self.__socket.send(('/addPseudo {}'.format(self.__pseudo)).encode())

    def _join_IP(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (tokens[0], int(tokens[1]))
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de la connexion")
        
       
    def _send(self, param):
        """check what protocol to use to send a message, UDP or TCP
        self.__pseudo is by default 'pseudoAzErTy' so if no connected to a server, it stays"""
        if self.__address is not None:           
            if self.__pseudo == 'pseudoAzErTy':
                try:
                    message = param.encode()
                    totalsent = 0
                    while totalsent < len(message):
                        sent = self.__socket_UDP.sendto(message[totalsent:], self.__address)
                        totalsent += sent
                except OSError:
                    print("Erreur lors de l'envoi du message ")
            else:
                try:
                    message = param.encode()
                    totalsent = 0
                    while totalsent < len(message):
                        sent = self.__socket.send(message[totalsent:])
                        totalsent += sent
                except OSError:
                    print("Erreur lors de l'envoi du message au serveur ")
             

    def _receive(self):
        """Function for receiving via a TCP""" 
        while self.__running:
            try:
                data = self.__socket.recv(1024).decode()
                if data == "AccueilServer": 
                    print("Bienvenu dans le serveur {}".format(self.__pseudo))
                else :
                    print(data)
            except socket.timeout:
                print("Vous avez été déconnecté")
                pass
            except OSError:
                return
                
    def _receive_pv(self):
        """Function for receiving via UDP"""
        while self.__running:
            try:
                data = self.__socket_UDP.recv(1024).decode()
                if data == "Accueil": 
                    print("Bienvenu dans le serveur {}".format(self.__pseudo))
                else :
                    print(data)
            except socket.timeout:
                print("Vous avez été déconnecté")
                pass
            except OSError:
                return



if __name__ == '__main__':
    if len(sys.argv) == 4:
        Client(sys.argv[1], int(sys.argv[2]),  sys.argv[3]).run()
    else:
        Client().run()