import pickle, socket, struct, sys, threading
import traceback


class Client():

    def __init__(self, host="0.0.0.0", port=6000, pseudo="pseudo"):
        self.__socket = socket.socket()
        self.__socket.bind((host, port))
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
                    print("Erreukjhkhr")
            else:
                print('Commande inconnue:', command)
                
    def _client(self):
        print(self.__address)
        
    def _exit(self):
        self.__running = False
        self.__address = None
        self.__socket.close()
  
    def _quit(self):
        self.__address = None

    def _help(self):
        print("/list permet d'afficher la liste des clients connectés si vous êtes connectés au serveur\n/send permet d'envoyer un message\n/quit ==> Quitter le serveur\n/join permet de rejoindre le serveur ou de se connecter à un une autre personne grâce à l'adresse IP")

    def _list(self):
        self.__socket.send("/list".encode())

    def _join_server(self, param):
        if self.__pseudo == "pseudo":
            self.__pseudo = input("Choisi ton pseudo : ")

        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (tokens[0], int(tokens[1]))
                self.__socket.connect(self.__address)
                threading.Thread(target=self._receive).start()
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur de connection")

        self.__socket.send(('/addPseudo {}'.format(self.__pseudo)).encode())

    def _join_IP(self, param):
        tokens = param.split(' ')
        if len(tokens) == 2:
            try:
                self.__address = (tokens[0], int(tokens[1]))
                print('Connecté à {}:{}'.format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")
        
       
    def _send(self, param):
        if self.__address is not None:            
            try:
                message = param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent = self.__socket.send(message[totalsent:])
                    totalsent += sent
            except OSError:
                print("Erreur lors de l'Envoi du messagehhhh ")

    def _receive(self):
        while self.__running:
            try:
                data = self.__socket.recv(1024).decode()
                if data == "Accueil": 
                    print("Bienvenu dans le serveur {}".format(self.__pseudo))
                else :
                    print(data)
            except socket.timeout:
                traceback.print_exc()
            except OSError:
                traceback.print_exc()
                return





if __name__ == '__main__':
    if len(sys.argv) == 4:
        Client(sys.argv[1], int(sys.argv[2]),  sys.argv[3]).run()
    else:
        Client().run()