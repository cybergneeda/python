import os
import random
import math
WIDTH = 1200
HEIGHT = 800
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
SCALE = 12
class Coordinate:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
class Character:
    def __init__(self):
        self.symbol=None
        self.coords=None
        self.health=None
        self.is_alive=True
        self.miss_chance=10
   
    def set_coords(self,x,y):
        self.coords=Coordinate(x,y)
    
    def move(self,direction):
        
        if direction=='w' or direction=='W':
            self.coords.y-=1

        elif direction=='a' or direction=='A':
            self.coords.x-=1

        elif direction=='s' or direction=='S':
            self.coords.y+=1

        elif direction=='d' or direction=='D':
            self.coords.x+=1
       
class Playable_character(Character):
    def __init__(self):
        super().__init__()
        self.symbol="\u25cf"
        self.armor=0
        self.health=100
        self.damage=20
        self.damage_distribution=2
        self.attack_range=1
        self.ammo=0
        self.weapon=None
    
    def attack(self):
        return random.randrange(self.damage-self.damage_distribution,self.damage+self.damage_distribution)
     
class Monster(Character):
    def __init__(self):
        super().__init__()
        self.symbol="\u2735"
        self.damage=random.randrange(5,15)
        self.damage_distribution=random.randrange(1,self.damage//2)
        self.health=int(random.normalvariate(100,15))

    def set_coords(self, x1, x2, y1, y2):
        self.coords=Coordinate(random.randrange(x1+1,x2-1),random.randrange(y1+1,y2-1))
    
    def move(self, direction):
        if direction==0:
            self.coords.y-=1
        elif direction==1:
            self.coords.y+=1
        elif direction==2:
            self.coords.x-=1
        elif direction==4:
            self.coords.x+=1

    def attack(self):
        return random.randrange(self.damage-self.damage_distribution,self.damage+self.damage_distribution)       

class Item:
    def __init__(self,x,y):
        self.coords=Coordinate(x,y)
        self.id=random.randrange(4)
        if self.id==0:
            self.symbol='+'
        elif self.id==1:
            self.symbol="\u2699"
        elif self.id==2:
            self.symbol="\u2694"           
        else:
            self.symbol="\U0001f52b" 
          
class Field:
    def __init__(self):
        self.width=100
        self.height=31
        self.field=[[" "]*self.width for i in range(self.height)]
        self.corridor_zone=[]
        j=0
        while j<self.width:
            for i in range(self.height):
                self.field[i][j]="\u25A0"
            j+=self.width//3
        j=0
        while j<self.height:
            for i in range(self.width):
                self.field[j][i]="\u25A0"
            j+=self.height//3
        for i in range(5,26,10):
            for j in range(33,67,33):
                self.field[i][j]=" "  
                self.corridor_zone.append([i,j])
        for i in range(10,21,10):
            for j in range(16,83,33):
                self.field[i][j]=" "   
                self.corridor_zone.append([i,j])
        self.room_coords=[[1,32,1,9],[34,65,1,9],[67,98,1,9],[1,32,11,19],[34,65,11,19],[67,98,11,19],[1,32,21,29],[34,65,21,29],[67,98,21,29]]
    
    def pirnt_field(self):
        for i in range(self.height):
            for j in range(self.width):
                print(self.field[i][j], end=' ')
            print()
    
    def set_player(self,x,y,symbol):
        self.field[y][x]=symbol

    def set_monster(self,x,y,symbol):
        self.field[y][x]=symbol

    def set_item(self,x,y):
        item=Item(x,y)
        self.field[y][x]=item.symbol

    def clear_prev_pos(self,x,y):
        self.field[y][x]=' '
    
    def stare_at_wall(self,x,y,symbol):
        self.set_player(x,y,symbol)
        os.system('cls')
        
class Cycle:
    def __init__(self):
        self.message=[0,0]      
        self.field=Field()
        self.player=Playable_character()
        self.player.set_coords(16,9)
        self.field.set_player(self.player.coords.x,self.player.coords.y,self.player.symbol)
        self.room_is_clear=False
        self.corridor_check=False
        self.monster=Monster()
        self.monster.set_coords(self.field.room_coords[0][0],self.field.room_coords[0][1],self.field.room_coords[0][2],self.field.room_coords[0][3])
        self.field.set_monster(self.monster.coords.x,self.monster.coords.y,self.monster.symbol) 
        
                                                              
    def enter_new_room(self):
        self.corridor_check=False
        for i in range(9):            
            if self.player.coords.x>=self.field.room_coords[i][0] and self.player.coords.x<=self.field.room_coords[i][1]\
                and self.player.coords.y>=self.field.room_coords[i][2] and self.player.coords.y<=self.field.room_coords[i][3]:
                self.monster=Monster()
                self.monster.set_coords(self.field.room_coords[i][0],self.field.room_coords[i][1],self.field.room_coords[i][2],self.field.room_coords[i][3])
                self.field.set_monster(self.monster.coords.x,self.monster.coords.y,self.monster.symbol)               

    def enter_corridor_check(self):       
        for i in range(12):
            if self.player.coords.y==self.field.corridor_zone[i][0] and self.player.coords.x==self.field.corridor_zone[i][1]:
                self.corridor_check=True     
                self.monster.is_alive=False 
                self.field.field[self.monster.coords.y][self.monster.coords.x]=" "     

    def calc_range(self):
        return math.sqrt(pow(self.player.coords.x-self.monster.coords.x,2)+pow(self.player.coords.y-self.monster.coords.y,2))

    def calc_range_change(self,x_change,y_change):
        return (math.sqrt(pow(self.player.coords.x-self.monster.coords.x-x_change,2)+pow(self.player.coords.y-self.monster.coords.y-y_change,2))-\
                math.sqrt(pow(self.player.coords.x-self.monster.coords.x,2)+pow(self.player.coords.y-self.monster.coords.y,2)))

    def gen_monstr_dir(self):
        while True:
            self.monster_direction=random.randrange(4)
            if self.monster_direction==0 and self.calc_range_change(0,-1)<0:
                break
            elif self.monster_direction==1 and self.calc_range_change(0,1)<0:
                break
            elif self.monster_direction==2 and self.calc_range_change(-1,0)<0:
                break
            elif self.monster_direction==3 and self.calc_range_change(1,0)<0:
                break

    def monster_attack(self):
        number=random.randrange(100)
        if number<5:
            damage=random.randrange(1,10)
            self.monster.health-=damage
            if self.monster.health>0:
                self.message[0]=(f"Монстр критически промахнулся и получил {damage} урона, у него осталось {self.monster.health} здоровья")
            if self.monster.health<=0:
                self.monster.is_alive=False
                self.room_is_clear=True
                self.field.set_item(self.monster.coords.x,self.monster.coords.y)
                self.message[0]=(f"Монстр критически промахнулся, получил {damage} урона и погиб")
                   
        elif number>self.monster.miss_chance:
            if number>94:
                multiplier=random.randrange(100,250)/100
                damage=int(self.monster.attack()*multiplier)
            else:
                damage=self.monster.attack()
            if self.player.armor>damage:
                self.player.armor-=damage
            else:
                damage-=self.player.armor
                self.player.armor=0
                self.player.health-=damage
            if self.player.health<=0:            
                self.player.is_alive=False
            else:
                if number>90:
                    self.message[0]=(f"Вы получили критический урон в {damage} единиц")
                else:
                    self.message[0]=(f"Вы получили {damage} урона")
        else:
            self.message[0]=("Монстр промахнулся")      

    def player_attack(self):
        if self.player.attack_range>1:
            self.player.miss_chance=10+self.calc_range()*8
            self.player.ammo-=1
        if self.calc_range()<=self.player.attack_range and self.monster.health>0:      
            number=random.randrange(100)
            if number<5:
                damage=random.randrange(1,10)
                self.player.health-=damage
                if self.player.health<=0:            
                    self.player.is_alive=False
                else:
                    self.message[1]=(f"Вы критически промахнулись и получили {damage} урона")
                    
            elif number>self.player.miss_chance:    
                if number>94:
                    multiplier=random.randrange(100,250)/100
                    damage=int(self.player.attack()*multiplier)
                else:
                    damage=self.player.attack()
                self.monster.health-=damage
                if self.monster.health<=0:
                    self.monster.is_alive=False
                    self.room_is_clear=True
                    if number>90:
                        self.message[1]=(f"Вы нанесли {damage} критического урона и убили монстра")
                    else:
                        self.message[1]=(f"Вы нанесли {damage} урона и убили монстра")
                else:
                    if number>90:
                        self.message[1]=(f"Вы нанесли {damage} критического урона, у монстра осталось {self.monster.health} здоровья")   
                    else:
                        self.message[1]=(f"Вы нанесли {damage} урона, у монстра осталось {self.monster.health} здоровья")  
            else:
                self.message[1]=("Вы промахнулись")   
        else:
            self.message[1]=("Вы успешно атаковали пустоту")          
        if self.player.ammo==0:
            self.player.weapon=None
            self.player.attack_range=1
            self.player.miss_chance=10      
         
