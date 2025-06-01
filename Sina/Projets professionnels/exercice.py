import socket, threading

msgSize = 1024
host = 'localhost'
portH = 50000
portC = 55000


class ClientServeur:
    def __init__(self):
        raise NotImplementedError

    def envoyerMsg(self):
        raise NotImplementedError
    
    def receiveMsg(self):
        raise NotImplementedError
    

class ClientServeurUDP(ClientServeur):
    def __init__(self, addrSrc:str = host, portSrc:int = portC):
        self.addrSrc = addrSrc
        self.portSrc = portSrc
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((addrSrc, portSrc))
        
    def envoyerMsg(self, msg, addrDst):
        self.socket.sendto(msg.encode(), addrDst)
        
    def receiveMsg(self):
        return self.socket.recvfrom(msgSize)
    

class EchoUDPServeur(ClientServeurUDP):
    def __init__(self, addrSrc:str = host, portSrc:int = portH):
        super().__init__(addrSrc, portSrc)
        self.clients = []

    def receiveMsg(self):
        msg, addrC = super().receiveMsg()
        print(f'Message de {addrC[0]}:{addrC[1]}')
        if not addrC in self.clients: 
            self.clients.append(addrC)
        msg = f'Echo de {self.addrSrc}:{self.portSrc} : {msg.decode()}'  
        self.envoyerMsg(msg)

    def envoyerMsg(self, msg):
        for client in self.clients:
            super().envoyerMsg(msg, client)    


class EchoUDPClient(ClientServeurUDP):
    def __init__(self, addrSrc:str = host, portSrc:int = portC, host:str = host, portH:int = portH):
        super().__init__(addrSrc, portSrc)
        self.serveur = (host, portH)

    def envoyerMsg(self, msg:str):
        super().envoyerMsg(msg, self.serveur)
    
    def receiveMsg(self):
        msg, _ = super().receiveMsg()
        print('\n'+ msg.decode())


class ServeurUDPMT(ClientServeurUDP):
    def __init__(self, addrSrc:str = host, portSrc:int = portH):
        super().__init__(addrSrc, portSrc)
        self.clients = []

    def receiveMsg(self):
        msg, addrC = super().receiveMsg()
        print(f'Message de {addrC[0]}:{addrC[1]}')
        if not addrC in self.clients: 
            self.clients.append(addrC)
        thread = threading.Thread(target=self.envoyerMsg, args=(msg.decode(),))
        thread.start()
        thread.join()

    def envoyerMsg(self, msg:str, addr:tuple):
        super().envoyerMsg(msg, addr)


class EchoUDPServeurMT(ServeurUDPMT):
    def envoyerMsg(self, msg:str):
        msg = f'{threading.current_thread().name} : {msg}'
        for client in self.clients:
            super().envoyerMsg(msg, client)
            

if __name__=='__main__':
    # serveur = EchoUDPServeur()
    serveur = EchoUDPServeurMT()
    def run():
        while True: serveur.receiveMsg()
    threading.Thread(target=run, daemon=True).start()
    input()
