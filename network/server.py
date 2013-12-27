from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

class FarProtocol(LineReceiver):
    def __init__(self):
        pass
        
    def lineReceived(self, line):
        self.factory.parser(self, line)
        
    def connectionMade(self):
        self.factory.clientConnectionMade(self)
    def connectionLost(self, reason):
        self.factory.clientConnectionLost(self)
        
        
class FarFactory(ServerFactory):
    def __init__(self, game):
        self.game = game
        self.tickservice = task.LoopingCall(self.tick)
        self.tickservice.start(60)
        self.combatservice = task.LoopingCall(self.combat)
        self.combatservice.start(3)
        self.writeservice = task.LoopingCall(self.send_updates)
        self.writeservice.start(0.5)
    
    def clientConnectionMade(self, client):
        self.game.connection(client)
        print "Got connection."

    def clientConnectionLost(self, client):
        self.game.disconnection(client)
        print "Lost connection."
        
    def tick(self):
        self.game.tick()
        
    def combat(self):
        self.game.combat()
        
    def parser(self, client, line):
        print "Parsing %s" % line
        player = None
        for p in self.game.players:
            if p.connection == client:
               player = p
               
        if p == None:
            print "Couldnt find player."
        else:
            self.game.parser(player, line)
            self.send_player_messages(player)
           
    def send_player_messages(self, player):
        m = '\n'+' '.join(player.messages)
        player.connection.transport.write(m)
        player.messages = []
        
    def send_updates(self):
        for p in self.game.players:
            if len(p.messages) > 0:
                self.send_player_messages(p)
            if p.exit:
                p.connection.transport.loseConnection()
                
    protocol = FarProtocol
    
