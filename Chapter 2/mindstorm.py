#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 14:52:07 2017

@author: denniswang
"""
import turtle

def draw_square(some_turtle):
    some_turtle.shape("triangle")
    some_turtle.color("yellow")
    some_turtle.speed(6)
    side = 0
    while side < 4:
        some_turtle.fd(100)
        some_turtle.right(90)
        side += 1

def draw_circle(some_turtle):
    some_turtle.shape("turtle")
    some_turtle.color("black")
    some_turtle.speed(3)
    some_turtle.circle(100)

def draw_triangle(some_turtle):
    some_turtle.shape("square")
    some_turtle.color("green")
    some_turtle.speed(3)

    side = 0
    while side < 3:
        some_turtle.fd(100)
        some_turtle.left(120)
        side += 1

def draw_diamond(some_turtle):
    some_turtle.color("blue")
    some_turtle.speed(10)
    side = 0
    while side < 4:
        change_degree = (side % 2)  * 90 + 45
        some_turtle.fd(100)
        if side != 3:
            some_turtle.rt(change_degree)
        side += 1

def draw_art():
    window = turtle.Screen()
    window.bgcolor("red")
    brad = turtle.Turtle()
    # draw_diamond(brad)
    count = 0
    angel_change = 5
    while count < (180 / angel_change):
        draw_diamond(brad)
        brad.right(angel_change)
        count += 1

    brad.seth(270)
    brad.fd(350)
    

    window.exitonclick()


draw_art()

