    
# Projet_chatroom_2BA

Notre code permet de comuniquer via un serveur ains que vie le peer-to-peer via les protocols **UDP** et **TCP**
Série 6a binôme 4, Nguyen Khac Huy et Soysal Deniz

## Partie Client/Serveur

Nous avons utilisé le protocol **TCP**. 
Pour lancez la chatroom, lancez 

```
Server.py et Client.py
```


### Commandes

Pour rejoindre le serveur :

```
/join_server [ADRESSE IP SERVEUR] [PORT]
```

Pour envoyer un message via le serveur :

```
/send [MSG]
```

Pour récuperer la liste des personnes connectées au serveur :

```
/list
```

Pour quitter le serveur : 

```
/quit
```

Pour quitter le programme :

```
/exit
```

## Partie Peer-To-Peer

Nous avons utilisé le protocol **UDP**.
Pour lancez la chatroom, lancez 

```
Client.py
```

### Commandes

Pour rejoindre le client de quelqu'un :

```
/join_ip [ADRESSE IP] [PORT]
```

Pour envoyer un message directement :

```
/send_pv [MSG]
```
