
class Direction(object):
    UNDEFINED = 0
    NORTH = 1
    SOUTH = 2
    EAST  = 3
    WEST  = 4
    UP    = 5
    DOWN  = 6
    
    STRINGS = {0: 'Undefined', 1: 'North', 2: 'South', 3: 'East', 4: 'West', 5: 'Up', 6: 'Down'}
    
    def tostring(self, direction):
        if direction == '1':
            return 'North'
        if direction == '2':
            return 'South'
        if direction == '3':
            return 'East'
        if direction == '4':
            return 'West'
        if direction == '5':
            return 'Up'
        if direction == '6':
            return 'Down'

class Exit(object):
    def __init__(self, direction, room):
        self.direction = direction
        self.room = room
        self.door = False
        self.closed = False
        self.locked = False
	self.key = 0
        self.pickproof = False
	self.secret = False
        

class Room(object):
    def __init__(self, number, sdesc, ldesc):
        self.number = number
        self.short_description = sdesc
        self.long_description = ldesc
        self.exits = []
        self.players = []
        self.mobs = []
        
    def player_entered(self, player):
        for p in self.players:
            p.addmessage("[PLAYERENTERED]|%s" % player.name)
        self.players.append(player)
        
    def player_left(self, player):
        self.players.remove(player)
        for p in self.players:
            p.addmessage("[PLAYERLEFT]|%s" % player.name)
        
    def npc_entered(self, npc):
        for p in self.players:
            p.addmessage("[MOBENTERED]|%s" % npc.name)
        self.mobs.append(npc)
    
    def npc_left(self, npc):
        self.mobs.remove(npc)
        for p in self.players:
            p.addmessage("[MOBLEFT]|%s" % npc.name)
        
    def connect_room(self, direction, room):
        removeexit = None
        for e in self.exits:
            if e.direction == direction:
                removeexit = e
                
        if removeexit != None:
            self.exits.remove(removeexit)
            
        self.exits.append(Exit(direction, room))
        
