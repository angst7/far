from random import random, randrange

class MobFlags:
    UNDEFINED  = 0
    
    AGGRESSIVE = 1
    SENTINAL   = 2
    
    ISNPC      = 3
    WIMPY      = 4
    
class AffectFlags:
    UNDEFINED     = 0
    
    SENSE_LIFE    = 1
    SENSE_HIDDEN  = 2
    
    SEE_INVISIBLE = 3
    NIGHT_VISION  = 4
    
    FLYING        = 5

class Attack(object):
    def __init__(self, dice, sides, use):
        self.dice = dice
        self.sides = sides
        self.use = use
        
    def roll(self):
        total = 0
        for i in range(1, dice):
            if self.sides > 1:
                total += randrange(1, self.sides, 1)
            else:
                total += 1
            
        return total

class NPC(object):
    def __init__(self, number, name, desc, level, hp, attacks, mobile):
        self.number = number
        self.name = name
        self.desc = desc
        self.level = level
        self.maxhp = hp
        self.hp = hp
        self.attacks = attacks
        self.mobile = mobile
        self.room = None

    def goto(self, room):
        if self.room != None:
            self.room.npc_left(self)
        self.room = room
        self.room.npc_entered(self)

    def walk(self):
        if random() > 0.8:
            if len(self.room.exits) > 1:
                destination = randrange(0,len(self.room.exits)-1,1)
            else:
                destination = 0
            self.goto(self.room.exits[destination].room)
            print "%s taks a walk." % self.name

class Player(object):
    def __init__(self, connection):
        self.connection = connection
        self.messages = []
        self.exit = False
        self.fighting = False
        self.identified = False
        self.name = "DummyPlayer"
        self.room = None

    def addmessage(self, m):
        self.messages.append("%s\r\n" % m)
        
    def combat(self):
        self.addmessage('Pow!')
        
    def look(self):
        self.addmessage("[ROOMINFO]|%d|%s|%s" % (self.room.number, self.room.short_description, self.room.long_description))
        for e in self.room.exits:
            self.addmessage("[EXITINFO]|%d|%d" % (e.direction, e.room.number))
            
        for m in self.room.mobs:
            self.addmessage("[MOBINFO]|%d|%s" % (m.number, m.name))
            
        for p in self.room.players:
            if p != self:
                self.addmessage("[PLAYERINFO]|%s" % (p.name))
        
    def goto(self, room):
        if self.room != None:
            self.room.player_left(self)
        self.room = room
        self.room.player_entered(self)
        self.look()
