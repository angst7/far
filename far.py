from network.server import FarProtocol, FarFactory
from network.messages import Tag
from models.mob import Player, NPC, Attack
from models.world import Room, Exit, Direction
from twisted.internet import reactor, task
from copy import deepcopy
from guppy import hpy

class Game(object):
    def __init__(self):
        self.name = "FAR v0.01"
        self.players = []
        self.npcs = []
        self.mobs = []
        self.rooms = []
        self.commandtags = [Tag("[SAY]", self.saymsg), Tag("[QUIT]", self.quit), 
                            Tag("[FIGHT]", self.startfight), Tag("[FLEE]", self.stopfight),
                            Tag("[IDENTIFY]", self.identify), Tag("[LOOK]", self.look),
                            Tag("[EXITS]", self.exits), Tag("[MOVETO]", self.moveto),
                            Tag("[GO]",self.go)]
        self.exit = False
    
    def tick(self):
        #for player in self.players:
            #player.addmessage('Tick!')
        for room in self.rooms:
            for mob in room.mobs:
                if mob.mobile:
                    mob.walk()
        print "Tick"
	#print hpy().heap()
    
    def combat(self):
        for player in self.players:
            if player.fighting:
                player.combat()
    
    def connection(self, connect):
        p = Player(connect);
        p.addmessage('Welcome!')
        p.goto(self.rooms[1])
        self.players.append(p)
        
    def disconnection(self, connect):
        killplayer = None
        for p in self.players:
            if p.connection == connect:
                killplayer = p
        
        if killplayer == None:
            print "Could not find player"
        else:
            killplayer.room.player_left(killplayer)
            self.players.remove(killplayer)
    
    def saymsg(self, player, args):
        player.addmessage('You said: %s' % '|'.join(args))
        for p in self.players:
            if p != player:
                p.addmessage('%s: %s' % (player.name, ' '.join(args)))
    
    def quit(self, player, args):
        player.addmessage('Bye!');
        player.exit = True
        
    def startfight(self, player, args):
        player.addmessage("You attack!")
        player.fighting = True
                
    def stopfight(self, player, args):
        player.addmessage("You run like a little girl.")
        player.fighting = False
                    
    def identify(self, player, args):
        if len(args) == 1:
            player.name = args[0]
            player.identified = True
            player.addmessage("Welcome, %s" % player.name)
            
    def look(self, player, args):
        if len(args) == 0:
            player.look()
            #player.addmessage("[%d] %s\r\n%s" % (player.room.number,
            #                    player.room.short_description, 
            #                    player.room.long_description))
                    
    def moveto(self, player, args):
        if len(args) == 1:
            newroom = self.findroom(args[0])
            print "Player %s moving to [%s]%s" % (player.name, args[0], newroom.short_description)
            player.goto(newroom)
                    
    def go(self, player, args):
        if len(args) == 1:
            direction = int(args[0])
            dest = None
            for e in player.room.exits:
                if e.direction == direction:
                    dest = e.room
                    self.moveto(player, [dest.number])
            if dest == None:
                player.addmessage("[BADEXIT]")
            
    def exits(self, player, args):
        if len(args) == 0:
            for e in player.room.exits:
                player.addmessage("[%s] %s" % (Direction.STRINGS[e.direction], e.room.short_description))
                    
    def findroom(self, roomnum):
        for r in self.rooms:
            if r.number == int(roomnum):
                return r
        return self.rooms[0]
        
    def findnpc(self, npcnum):
        for n in self.npcs:
            if n.number == int(npcnum):
                return n
        return self.npcs[0]
                    
    def parser(self, player, line):
        parts = line.split('|')
        success = False
        for t in self.commandtags:
            if t.name == parts[0]:
                if len(parts) > 1:
                    p = parts[1:]
                else:
                    p = []
                t.action(player, p)
                success = True
        if (success == False):
            print 'No such tag'    

    def loadstatic(self):
        f = open('models/world1.txt','r')
        iterator = 0
        exits = []
        for line in f:
            if line[0] != "#":
                iterator += 1
                if iterator == 5:
                    print "Adding room: [%d] %s" % (rnum, sdesc)
                    self.rooms.append(Room(rnum, sdesc, ldesc))
                    iterator = 1
                if iterator == 1:
                    rnum = int(line)
                if iterator == 2:
                    sdesc = line.rstrip()
                if iterator == 3:
                    ldesc = line.rstrip()
                if iterator == 4:
                    direction = 1
                    for e in line.split('|'):
                        if int(e) > 0:
                            exits.append([rnum, direction, int(e)])
                        direction += 1
                
        for e in exits:
            fromroom = self.findroom(e[0])
            toroom = self.findroom(e[2])
            fromroom.connect_room(e[1], toroom)
            print "Adding exit from %s to %s" % (fromroom.number, toroom.number)

        f = open('models/mobs1.txt','r')
        iterator = 0
        attacks = []
        for line in f:
            if line[0] != "#":
                iterator += 1
                if iterator == 13:
                    print "Adding NPC: [%d] %s" % (number, name)
                    self.npcs.append(NPC(number, name, desc, level, hp, attacks, mobile))
                    iterator = 1
                if iterator == 1:
                    number = int(line)
                if iterator == 2:
                    name = line.rstrip()
                if iterator == 3:
                    desc = line.rstrip()
                if iterator == 4:
                    level = int(line)
                if iterator == 5:
                    hp = int(line)
                if iterator in range(6, 11):
                    dice = line.split('|')
                    if len(dice) == 3:
                        attacks.append(Attack(int(dice[0]), int(dice[1]), int(dice[2])))
                if iterator == 12:
                    if int(line) == 1:
                        mobile = True
                    else:
                        mobile = False

        f = open('models/populate1.txt', 'r')
        for line in f:
            data = line.split('|')
            if len(data) == 2:
                npcnum = int(data[0])
                roomnum = int(data[1])
                newmob = deepcopy(self.findnpc(npcnum))
                newmob.goto(self.findroom(roomnum))
                self.mobs.append(newmob)
                print "Placed [%d] %s in room %d" % (newmob.number, newmob.name, roomnum)

if __name__ == '__main__':

    g = Game()
    
    # Set up a few rooms and exits to connect them
    # this should go into a static load file
    
    g.rooms = [Room(0, 'Nowhere', 'This is nowhere, man.')] #,
               #Room(1, 'The Square', 'This is the center of town.', 
               #     [Exit(Direction.EAST, 2), Exit(Direction.WEST, 3)]), 
               #Room(2, 'Main Street', 'Walking along the main street', [Exit(Direction.WEST, 1)]),
               #Room(3, 'Main Street', 'Walking along the main street', [Exit(Direction.EAST, 1)])]
    
    g.loadstatic()
    
    reactor.listenTCP(4000, FarFactory(g))
    reactor.run()

