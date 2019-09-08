from collections import Iterable
import random
#When returning something, always use getter function
class Room:
    """stores information about the locations that the player and monster will
    be moving through

    attributes: name,room_num"""
    def __init__(self,name,room_num):
        """initializes self with the name and room number(room_num)

        Room,str,int->None"""
        self.name = name
        self.room_num = room_num
        self.__exits = set()
    def connect_to(self,other):
        """takes another Room or an iterable of Rooms and adds connections
        between them

        Room,Room->None"""
        if isinstance(other,Iterable):
            for room in other:
                room.__exits.add(self)
                self.__exits.add(room)
        else:
            other.__exits.add(self)
            self.__exits.add(other)
    def __repr__(self):
        """returns the Room in format 'Room(name,room_num)'

        Room->str"""
        
        return "Room("+repr(self.name)+", "+repr(self.room_num)+")"
        
    def get_exits(self):
        """returns the exit list of the Room

        Room -> set"""
        return self.__exits
    def is_connected_to(self,other):
        """returns True if there's a connection between two rooms

        Room,Room->Bool"""
        if isinstance(other.__exits,Iterable):
            if other in self.__exits:
                return True
        else:
            return False

    def get_exit_nums(self):#made this function to display valid exits for user
        """returns a string of numbers of connected rooms of Room

        Room -> str"""
        exit_nums = ''
        for room in self.get_exits():
            exit_nums = exit_nums + str(room.room_num)+','
        return exit_nums[:-1]
    
    def description(self):
        """returns a string representing a description of the Room

        Room ->str"""
        return "You are in "+str(self.name)+". Valid exits: "+\
               str(self.get_exit_nums())

#Creating Room objects
lab = Room('lab',1)
library = Room('library',2)
gym = Room('gym',3)
bathroom = Room('bathroom',4)
kitchen = Room('kitchen',5)
garage = Room('garage',6)
#Creating connections
lab.connect_to((library,bathroom,kitchen))
library.connect_to((kitchen,garage))
gym.connect_to((garage,lab,bathroom))
bathroom.connect_to((kitchen))
kitchen.connect_to((garage))

map_of_rooms = {lab,library,gym,bathroom,kitchen,garage}



class Command:
    """a command that stores action and destination

    attributes:action,destination"""
    def __init__(self,action,destination):
        """initializes self with action and destination

        Command, str, Room -> None"""
        self.action = action
        self.destination = destination

    def __repr__(self):
        """returns the Command in the format Command(action,destination)

        Command->str"""
        return 'Command('+repr(self.action)+', '+repr(self.destination)+')'

class Movable:
    """a class that represents objects and characters that have changeable
    locations."""
    def move_to(self,location):
        """sets the location

        Movable,str->None"""
        self.__location = location
        
    def __init__(self,room):
        """initializes self with a Room instance

        Movable,Room -> None"""
        self.move_to(room)

    def get_location(self):
        """returns the location of Movable

        Movable -> Room"""
        return self.__location
    
    def __repr__(self):
        """returns the Movable in the format Movable(Room)

        Movable -> str"""
        return 'Movable('+repr(self.get_location())+')'
    
    def update(self):
        """For subclasses of Movable, will move the object or get input from
        user. For simple Movable objects, doesn't do anything

        Movable->None"""
        pass 

class Wanderer(Movable):
    """things that move around randomly on their own

    attributes:is_awake"""
    def __init__(self,location=random.choice(list(map_of_rooms)),is_awake=True):
        """initializes self with room and awake status

        Wanderer,Room,Bool->None"""
        super().__init__(location)
        self.is_awake = is_awake

    def __repr__(self):
        """returns the Wanderer in the format Wanderer(room,is_awake)

        Wanderer->str"""
        return 'Wanderer('+repr(self.get_location())+', '+repr(self.is_awake)+')'

    def update(self):
        """check if the Wanderer is awake. If not, do nothing. If so, move
        the Wanderer to a random Room that is adjacent to current location
        and go to sleep

        Wanderer->None"""
        current_location = self.get_location()
        if self.is_awake:
            self.move_to(random.sample(current_location.get_exits(),1)[0])
            self.is_awake = False
        else:
            pass

monster = Wanderer()
IS_MONSTER_SHOT = False
#if multiple monster, add .is_shot attribute to Wanderer instance Monster

#making a copy of map_of_rooms excluding the Room monster is in
#(these are not necessary anymore because using a loop to check if they are
#spawn in the same room is much simpler)

#copy_of_map = set([lab,library,gym,bathroom,kitchen,garage])
#copy_of_map.remove(monster.get_location())
#rooms_for_player = copy_of_map

class Player(Movable):
    """represents player characters

    attribute:dart_num"""
    def __init__(self,dart_num,location = random.sample(map_of_rooms,1)[0]):
        """initializes Player with dart_num and location

        Player,int,Room->None"""
        self.dart_num = dart_num
        super().__init__(location)

    def shoot_into(self,target_room):
        """takes the target room and first decrease the number of darts by 1
        and if the monster is in target_room, the monster is shot and
        method returns True. If not, return False

        Player, Room -> Bool"""
        self.dart_num -= 1
        if target_room == monster.get_location():
            IS_MONSTER_SHOT = True
            return True
        else:
            return False
    def __repr__(self):
        """returns Player in format Player(dart_num,location)

        Player -> str"""
        return 'Player('+repr(self.dart_num)+","+repr(self.get_location())+')'
    def get_command(self):
        """communicate with the user to find out what user wants to do and
        returns an appropriate Command Object once a valid command has been
        entered

        Player -> Command"""
        print('What do you want to do?')
        print('(Enter "shoot into NUMBER" or "go to NUMBER")')
        user_command = input('> ')
        while True:
            if user_command[:10] == 'shoot into':#stuck when checking conditions
                if self.dart_num == 0:
                    print('No darts left.')
                    print('What do you want to do?')
                    print('(Enter "shoot into NUMBER" or "go to NUMBER")')
                    user_command = input('>')
                    continue
                elif int(user_command[11:]) not in range(1,7):
                    print("That's not a valid room number.")
                    print('What do you want to do?')
                    print('(Enter "shoot into NUMBER" or "go to NUMBER")')
                    user_command = input('> ')
                    continue
                elif user_command[11:] not in \
                     self.get_location().get_exit_nums():
                    print("You can't shoot into that room from here.")
                    print('What do you want to do?')
                    print('(Enter "shoot into NUMBER" or "go to NUMBER")')
                    user_command = input('> ')
                    continue
                else:
                    if user_command[11:] == '1':
                        return Command('shoot',lab)
                    elif user_command[11:] == '2':
                        return Command('shoot',library)
                    elif user_command[11:] == '3':
                        return Command('shoot',gym)
                    elif user_command[11:] == '4':
                        return Command('shoot',bathroom)
                    elif user_command[11:] == '5':
                        return Command('shoot',kitchen)
                    elif user_command[11:] == '6':
                        return Command('shoot',garage)
                    
            elif user_command[:5] == 'go to':
                if user_command[6:] not in '123456':
                    print("That's not a valid room number.")
                    print('What do you want to do?')
                    print('(Enter "shoot into NUMBER" or "go to NUMBER")')
                    user_command = input('> ')
                    continue
                elif user_command[6:] not in self.get_location().get_exit_nums():
                    print("You can't shoot into that room from here.")
                    print('What do you want to do?')
                    print('(Enter "shoot into NUMBER" or "go to NUMBER")')
                    user_command = input('> ')
                    continue
                else:
                    if user_command[6:] == '1':
                        return Command('move',lab)
                    elif user_command[6:] == '2':
                        return Command('move',library)
                    elif user_command[6:] == '3':
                        return Command('move',gym)
                    elif user_command[6:] == '4':
                        return Command('move',bathroom)
                    elif user_command[6:] == '5':
                        return Command('move',kitchen)
                    elif user_command[6:] == '6':
                        return Command('move',garage)
            else:
                print("That's not a valid command.")
                print('What do you want to do?')
                print('(Enter "shoot into NUMBER" or "go to NUMBER")')
                user_command = input('> ')
                continue
            
    def execute_command(self,command):
        """takes a Command object and carries out the corresponding action

        Player, Command -> None"""
        if command.action == 'move':
            if command.destination.room_num == 1:
                self.move_to(lab)
                print('You walk into room number 1.')
                if monster.get_location().is_connected_to(lab):
                    print('You can smell the monster; it must be nearby.')
            elif command.destination.room_num == 2:
                self.move_to(library)
                print('You walk into room number 2.')
                if monster.get_location().is_connected_to(library):
                    print('You can smell the monster; it must be nearby.')
            elif command.destination.room_num == 3:
                self.move_to(gym)
                print('You walk into room number 3.')
                if monster.get_location().is_connected_to(gym):
                    print('You can smell the monster; it must be nearby.')
            elif command.destination.room_num == 4:
                self.move_to(bathroom)
                print('You walk into room number 4.')
                if monster.get_location().is_connected_to(bathroom):
                    print('You can smell the monster; it must be nearby.')
            elif command.destination.room_num == 5:
                self.move_to(kitchen)
                print('You walk into room number 5.')
                if monster.get_location().is_connected_to(kitchen):
                    print('You can smell the monster; it must be nearby.')
            elif command.destination.room_num == 6:
                self.move_to(garage)
                print('You walk into room number 6.')
                if monster.get_location().is_connected_to(garage):
                    print('You can smell the monster; it must be nearby.')
        elif command.action == 'shoot':
            if command.destination.room_num == 1:
                self.shoot_into(lab)
                print('The gun goes *BANG*, and a dart flies into room 1.')
                if monster.get_location() != lab:
                    print("It doesn't sound like you hit anything.")
                    print('You can hear the monster moving about.')
                else:
                    IS_MONSTER_SHOT = True
            elif command.destination.room_num == 2:
                self.shoot_into(library)
                print('The gun goes *BANG*, and a dart flies into room 2.')
                if monster.get_location() != library:
                    print("It doesn't sound like you hit anything.")
                    print('You can hear the monster moving about.')
                else:
                    IS_MONSTER_SHOT = True
            elif command.destination.room_num == 3:
                self.shoot_into(gym)
                print('The gun goes *BANG*, and a dart flies into room 3.')
                if monster.get_location() != gym:
                    print("It doesn't sound like you hit anything.")
                    print('You can hear the monster moving about.')
                else:
                    IS_MONSTER_SHOT = True
            elif command.destination.room_num == 4:
                self.shoot_into(bathroom)
                print('The gun goes *BANG*, and a dart flies into room 4.')
                if monster.get_location() != bathroom:
                    print("It doesn't sound like you hit anything.")
                    print('You can hear the monster moving about.')
                else:
                    IS_MONSTER_SHOT = True
            elif command.destination.room_num == 5:
                self.shoot_into(kitchen)
                print('The gun goes *BANG*, and a dart flies into room 5.')
                if monster.get_location() != kitchen:
                    print("It doesn't sound like you hit anything.")
                    print('You can hear the monster moving about.')
                else:
                    IS_MONSTER_SHOT = True
            elif command.destination.room_num == 6:
                self.shoot_into(garage)
                print('The gun goes *BANG*, and a dart flies into room 6.')
                if monster.get_location() != garage:
                    print("It doesn't sound like you hit anything.")
                    print('You can hear the monster moving about.')
                else:
                    IS_MONSTER_SHOT = True


    def update(self):
        """displays the description of the Player's current Room

        Player -> str"""
        print(self.get_location().description())

player1 = Player(3)

while True:
    if player1.get_location().room_num == monster.get_location().room_num:
        player1 = Player(3)#always get stuck
        continue
    else:
        break
    
UPDATE_LIST = [player1,monster]
print("""Welcome to Monster Capture!

A wild monster is loose in the area, and it's your job to capture it without
getting eaten. Travel around the map, and when you have figured out which
room the monster is in, go to an adjacent room and shoot a tranquilizer 
dart into that room. If you hit the monster, you win! But be careful; you
only have two darts!

""")
print('You begin the game in room '+str(player1.get_location().room_num)+'.')
if player1.get_location().is_connected_to(monster.get_location()):
    print('You can smell the monster; it must be nearby.')

while True:
    if player1.get_location().room_num == monster.get_location().room_num and \
       IS_MONSTER_SHOT == False:
        print('The monster eats you! Game over.')
        break
    for movable in UPDATE_LIST:
        movable.update()
    if IS_MONSTER_SHOT == True:
        print('You hear a roar from the monster and a thump as it falls asleep.')
        print('Congratulations! You have captured the monster!')
        break
    player1.execute_command(player1.get_command())
