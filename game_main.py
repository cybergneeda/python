import pygame
import sys
from game_logic import *
WIDTH = 1200
HEIGHT = 800
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
SCALE = 12
def main():
    item_taken=False
    displacement=0
    cycle=Cycle()
    def print_status():
        text1=f1.render(f"Здоровье: {cycle.player.health}",True,WHITE)
        text2=f1.render(f"Броня: {cycle.player.armor}",True,WHITE)
        text3=f1.render(f"Оружие: {cycle.player.weapon} Аmmo: {cycle.player.ammo}",True,WHITE)
        text4=f1.render(f"Урон: {cycle.player.damage-cycle.player.damage_distribution}-{cycle.player.damage+cycle.player.damage_distribution}",True,WHITE)
        screen.blit(text1,(10,380))
        screen.blit(text2,(10,410))
        screen.blit(text3,(10,440))
        screen.blit(text4,(10,470))
        pygame.display.update()
    def print_message(message,displacement):
        text1=f1.render(message,True,WHITE)
        screen.blit(text1,(10,500+displacement))
        pygame.display.update()

    pygame.init()
    
    class Sprite(pygame.sprite.Sprite):
        def __init__(self,x,y,filename) :
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load(filename).convert_alpha()
            self.rect=self.image.get_rect(
            center=(x,y))
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('kill them all')
    sprite1=Sprite(16.5*SCALE,9.5*SCALE,"C:\qwe\Okayeg.png")
    sprite2=Sprite(SCALE*(cycle.monster.coords.x+0.5),SCALE*(cycle.monster.coords.y+0.5),"C:\qwe\pepega.png") 
    clock=pygame.time.Clock()
    f1=pygame.font.Font(None,36)  
    
    while True:                           
        clock.tick(FPS)           
        while cycle.player.is_alive: 
            action=0         
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()   
                if event.type==pygame.KEYDOWN: 
                    displacement=0           
                    if (event.key==pygame.K_UP) and (cycle.field.field[cycle.player.coords.y-1][cycle.player.coords.x]=="\u25A0" or cycle.field.field[cycle.player.coords.y-1][cycle.player.coords.x]=="\u2735") or\
                    (event.key==pygame.K_LEFT) and (cycle.field.field[cycle.player.coords.y][cycle.player.coords.x-1]=="\u25A0" or cycle.field.field[cycle.player.coords.y][cycle.player.coords.x-1]=="\u2735") or\
                    (event.key==pygame.K_DOWN) and (cycle.field.field[cycle.player.coords.y+1][cycle.player.coords.x]=="\u25A0" or cycle.field.field[cycle.player.coords.y+1][cycle.player.coords.x]=="\u2735") or\
                    (event.key==pygame.K_RIGHT) and (cycle.field.field[cycle.player.coords.y][cycle.player.coords.x+1]=="\u25A0" or cycle.field.field[cycle.player.coords.y][cycle.player.coords.x+1]=="\u2735"):
                        cycle.field.stare_at_wall(cycle.player.coords.x,cycle.player.coords.y,cycle.player.symbol)  
                        continue
                        
                    if event.key==pygame.K_r:              
                        cycle.player_attack()
                        print_message(cycle.message[1],displacement)
                        displacement+=30
                        pygame.time.delay(3000)
                    else:
                        cycle.field.clear_prev_pos(cycle.player.coords.x,cycle.player.coords.y)                            
                        if event.key==pygame.K_UP:
                            action='w'
                            sprite1.rect.y-=SCALE
                        elif event.key==pygame.K_LEFT:
                            action='a'
                            sprite1.rect.x-=SCALE
                        elif event.key==pygame.K_DOWN:
                            action='s'
                            sprite1.rect.y+=SCALE
                        elif event.key==pygame.K_RIGHT:
                            action='d'
                            sprite1.rect.x+=SCALE
                        
                        pygame.time.delay(1000)
                        pygame.display.update()  
                        cycle.player.move(action)                   
                        if cycle.field.field[cycle.player.coords.y][cycle.player.coords.x]=="+":
                            cycle.player.health=100
                            item_taken=True
                        elif cycle.field.field[cycle.player.coords.y][cycle.player.coords.x]=="\u2699":
                            cycle.player.armor+=25
                            item_taken=True
                        elif cycle.field.field[cycle.player.coords.y][cycle.player.coords.x]=="\u2694":
                            cycle.player.damage=40
                            cycle.player.weapon="Меч"
                            cycle.player.ammo=0
                            cycle.player.damage_distribution=5
                            item_taken=True
                        elif cycle.field.field[cycle.player.coords.y][cycle.player.coords.x]=="\U0001f52b":
                            cycle.player.damage=60
                            cycle.player.damage_distribution=10
                            cycle.player.attack_range=10
                            cycle.player.ammo+=10
                            cycle.player.weapon="Пистолет"
                            item_taken=True
                        if cycle.corridor_check:
                            cycle.enter_new_room()   
                            sprite2=Sprite(SCALE*(cycle.monster.coords.x+0.5),SCALE*(cycle.monster.coords.y+0.5),"C:\qwe\pepega.png")     
                            item_taken=False
                        cycle.field.set_player(cycle.player.coords.x,cycle.player.coords.y,cycle.player.symbol)                         
                        cycle.enter_corridor_check()
                        if cycle.corridor_check:
                            item_taken=True
                    if cycle.monster.is_alive:
                        if cycle.calc_range()<=1:
                            cycle.monster_attack()   
                            print_message(cycle.message[0],displacement)     
                            pygame.time.delay(3000)          
                        else:
                            cycle.gen_monstr_dir()                         
                            cycle.field.clear_prev_pos(cycle.monster.coords.x,cycle.monster.coords.y)
                            cycle.monster.move(cycle.monster_direction)                           
                            if cycle.monster_direction==0:
                                sprite2.rect.y-=SCALE
                            elif cycle.monster_direction==1:
                                sprite2.rect.y+=SCALE
                            elif cycle.monster_direction==2:
                                sprite2.rect.x-=SCALE
                            else:
                                sprite2.rect.x+=SCALE
                            cycle.field.set_monster(cycle.monster.coords.x,cycle.monster.coords.y,cycle.monster.symbol)
                    else:                       
                        screen.fill(BLACK)
                        if cycle.room_is_clear:
                            cycle.field.set_item(cycle.monster.coords.x,cycle.monster.coords.y)
                            if cycle.field.field[cycle.monster.coords.y][cycle.monster.coords.x]=='+':
                                item_file_name="C:\qwe\healka.png"
                            elif cycle.field.field[cycle.monster.coords.y][cycle.monster.coords.x]=='\u2699':
                                item_file_name="C:\qwe\Bronya.png"
                            elif cycle.field.field[cycle.monster.coords.y][cycle.monster.coords.x]=='\u2694':
                                item_file_name="C:\qwe\me4.png"
                            else:
                                item_file_name="C:\qwe\gun.png"
                            sprite2=Sprite(SCALE*(cycle.monster.coords.x+0.5),SCALE*(cycle.monster.coords.y+0.5),item_file_name)
                            cycle.room_is_clear=False
                    screen.fill(BLACK)
                    for i in range(31):
                        for j in range(100): 
                            if cycle.field.field[i][j]=="\u25A0":
                                pygame.draw.rect(screen, WHITE,(j*SCALE,i*SCALE,SCALE,SCALE))
                    screen.blit(sprite1.image,sprite1.rect)
                    if item_taken==False:
                        screen.blit(sprite2.image,sprite2.rect)
                     
                    pygame.display.flip()
                    pygame.display.update()                                                  
                    print_status()
        print_message("Ваша жизнь закончилась в подземелье.",displacement)
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        sys.exit() 
main()