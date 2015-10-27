from random import random, randint, randrange

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
        print "Rolling %d die with %d sides" % (self.dice, self.sides)
        for i in range(1, self.dice+1):
            if self.sides > 1:		
                total += randint(1, self.sides)
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
        self.fighting = False
        self.mobile = mobile
        self.room = None
        self.target = None

    def goto(self, room):
        if self.room != None:
            self.room.npc_left(self)
        self.room = room
        self.room.npc_entered(self)

    def combat(self):
        if self.target is None:
            self.fighting = False
            return

        for a in self.attacks:
            damage = a.roll()
            self.target.addmessage("%s hits you for %d damage." % (self.name, damage))

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
        self.hp = 100
        self.room = None
        self.target = None
        self.attacks = [Attack(1, 5, 100)]

    def addmessage(self, m):
        self.messages.append("%s\r\n" % m)
        
    def combat(self):
        if self.target is None:
            self.addmessage("You arent fighting anyone!")
            self.fighting = False

        for a in self.attacks:
             damage = a.roll()
        if damage == 0:
            self.addmessage("You miss %s with your hit." % self.target.name)
        else:
            self.addmessage("You hit %s for %d points." % (self.target.name, damage))

    def stats(self):
        fight = "No One"
        if self.fighting:
            fight = self.target.name

        self.addmessage("You are %s, you have %d hit points, and are currently fighting %s." % (self.name, self.hp, fight))

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
