import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from MapTile import *
from Mob import Gomba, Turtle
from item import Mushroom, Flower
import collision
import server
from ball import Ball



name = "MainState"

Moblist = list()
itemlist = list()
itemlist_Flower = list()
boy = None
mapTile = None
Mob_Gomba = None
Mob_Tuttle = None

bool_all_tile = False
bool_all_tile2 = False
bool_jumpdown = True
# mapTile = MapTile()
# boy = Boy()

def collide(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def collideUpDown(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if bottom_a < top_b:
            return True
        else: return False
    else: return False

def collideUpDown_false(a, b):
    global bool_all_tile
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if bottom_a < top_b:
            bool_all_tile = True
        else: bool_all_tile = bool_all_tile or False
    else: bool_all_tile = bool_all_tile or False

def collidejump(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if top_a > bottom_b:
            return True
        else: return False
    else: return False

def collide_left(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if bottom_b < top_a < top_b or bottom_b < bottom_b < top_b:
        if right_a > left_b:
            return True
        else: return False
    else: return False

def collide_leftright(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if bottom_b < top_a < top_b or bottom_b < bottom_a< top_b:
        if left_b < right_a < right_b or left_b < left_a < right_b :
            return True
        else: return False
    else: return False

def collide_all(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < right_a < right_b:
        return 1
    elif left_b < left_a < right_b:
        return 2
    elif bottom_b < bottom_a < top_b:
        return 3
    elif bottom_b < top_a < top_b:
        return 4

def enter():
    global boy
    global mapTile
    global Moblist, Mob_Gomba, Mob_Tuttle
    boy = Boy()
    # grass = Grass()
    mapTile = MapTile()
    Mob_Gomba = Gomba()
    Mob_Tuttle = Turtle()
    Moblist.append(Mob_Gomba)
    Moblist.append(Mob_Tuttle)
    game_world.add_object(mapTile, 0)
    game_world.add_object(boy, 1)
    game_world.add_object(Mob_Gomba, 2)
    game_world.add_object(Mob_Tuttle, 2)




def exit():
    global boy, mapTile, Moblist
    del boy
    del mapTile
    del Moblist

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    global boy, mapTile, Mob_Gomba, Mob_Tuttle, bool_all_tile, bool_all_tile2, bool_jumpdown, Moblist, itemlist, itemlist_Flower
    for i in mapTile.Tilelist:
        i.MovingX = boy.getX()
    for i in itemlist:
        i.MovingX = boy.getX()
    for i in itemlist_Flower:
        i.MovingX = boy.getX()
    mapTile.set_movingX(boy.getX())
    Mob_Gomba.set_movingX(boy.getX())
    Mob_Tuttle.set_movingX(boy.getX())
    for game_object in game_world.all_objects():
        game_object.update()
    for i in mapTile.Tilelist:
        if i.collision >= 1:
            for j in Moblist:
                if collide(j, i):
                    if collideUpDown(j, i):
                        j.get_grabity(True)
                    j.collideUpDown_false(j, i)
                    if j.set_grabitycheck == False:
                        j.get_grabity(False)
            if collide(boy, i):
                if i.y < boy.plagY < i.y + 10:
                    if collidejump(boy, i):
                        boy.y -= 5
                        boy.get_booljump(True)
                        bool_jumpdown = False
                        boy.get_grabity(False)
                        if i.collision == 2:
                            i.collision = 1
                            i.type += 1
                            item_mushroom = Mushroom(i.x+30, i.y+30)
                            item_mushroom.MovingX = boy.getX()
                            itemlist.append(item_mushroom)
                            game_world.add_object(item_mushroom, 3)
                        if i.collision == 3:
                            i.collision = 1
                            i.type += 1
                            item_Flower = Flower(i.x+30, i.y+30)
                            item_Flower.MovingX = boy.getX()
                            itemlist_Flower.append(item_Flower)
                            game_world.add_object(item_Flower, 3)
                if collideUpDown(boy, i) and bool_jumpdown == True:
                    boy.get_grabity(True)
                collideUpDown_false(boy, i)
                if bool_all_tile == False:
                    boy.get_grabity(False)
                # if collide_left(boy, i):
                #     boy.get_bool_leftmove(True)
                #     boy.x -= 2
                bool_jumpdown = True
        else:
            collideUpDown_false(boy, i)
            if bool_all_tile == False:
                boy.get_grabity(False)
    for i in itemlist:
        if collide(boy, i):
            itemlist.remove(i)
            game_world.remove_object(i)
            boy.boolbig = True
    for i in itemlist_Flower:
        if collide(boy, i):
            itemlist_Flower.remove(i)
            game_world.remove_object(i)
            boy.boolFlower = True

    for j in Moblist:
        if collide(boy, j):
            if collide_all(boy, j) == 1:
                print('데미지')
            # if collide_leftright(boy, j):
                # print('데미지')
            # if collideUpDown(boy, j):
            #     j.booldeath = True
        if j.deathtime >= 10:
            Moblist.remove(j)
            game_world.remove_object(j)







    bool_all_tile = False



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







