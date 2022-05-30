from  vec import vec2D
import math
import pyxel
import numpy as np
import Body

# Global Constants
GRAV_CON = 0.001

class Sol:
    # All Body List
    bodies = []
    # Timestep
    tS = 0.0

    # Universe and Render Scale
    scale = 265.0 / 800.0
    # scale = 1.0

    def __init__(self):
        pyxel.init(int(800*self.scale),int(800*self.scale), "Sol System", fps=60)
        pyxel.load("stars.pyxres", tilemap=True)
                    
        # Init bodies and append to all body list
        Sol.Sun = Body.Body(100000000.0, vec2D(400.0, 400.0)*self.scale, 22.0*self.scale, vec2D(0.0, 0.0), vec2D(0.0, 0.0), 9)
        self.bodies.append(Sol.Sun)
        p1 = Body.Body(Sol.Sun.m*0.000003, vec2D(200.0, 400.0)*self.scale, 12*self.scale, vec2D(0.0, 315.0), vec2D(0.0, 0.0), 2)
        self.bodies.append(p1)
        p2 = Body.Body(Sol.Sun.m*0.000001, vec2D(700.0, 400.0)*self.scale, 8*self.scale, vec2D(0.0, -315.0), vec2D(0.0, 0.0), 5)
        self.bodies.append(p2)
        p3 = Body.Body(Sol.Sun.m*0.000001, vec2D(400.0, 300.0)*self.scale, 6*self.scale, vec2D(-315.0, 0.0), vec2D(0.0, 0.0), 8)
        self.bodies.append(p3)
        Sol.ship = Body.Body(1000, vec2D(400.0, 250.0)*self.scale, 0, vec2D(0.0, 0.0), vec2D(0.0, 0.0), 0)
        self.bodies.append(Sol.ship)

        # Variable Init
        Sol.dampToggle = False
        Sol.dampText = "OFF"
        Sol.dampFactor = 1.0
        Sol.shipThrust = 20.0
        Sol.menu = True
        Sol.scoreToggle = True
        Sol.score = 0

        pyxel.run(self.update, self.draw)
    
    # Runs every frame, draws when necessary
    def update(self):

        # Quit button
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Press Space To Start!
        if pyxel.btnp(pyxel.KEY_SPACE) and Sol.menu == True:
            Sol.menu = False
            if self.scale < 1:
                self.tS = 0.005
            else:
                self.tS = 0.01

        # Ship controller and damping
        if pyxel.btn(pyxel.KEY_UP):
            Sol.ship.v.y -= Sol.shipThrust
        if pyxel.btn(pyxel.KEY_DOWN):
            Sol.ship.v.y += Sol.shipThrust
        if pyxel.btn(pyxel.KEY_RIGHT):
            Sol.ship.v.x += Sol.shipThrust
        if pyxel.btn(pyxel.KEY_LEFT):
            Sol.ship.v.x -= Sol.shipThrust
        
        # Damp ship vel by factor
        Sol.ship.v *= Sol.dampFactor
        
        # Scoring System (WIP)
        # if pyxel.btnp(pyxel.KEY_UP, 30, 60) or pyxel.btnp(pyxel.KEY_DOWN, 30, 60) or pyxel.btnp(pyxel.KEY_LEFT, 30, 60) or pyxel.btnp(pyxel.KEY_RIGHT, 30, 60) and 0 < Sol.ship.pos.x < 400*self.scale and 0 < Sol.ship.pos.y < 400*self.scale:
        #     Sol.score += 100
            # Sol.score += int(Sol.ship.v.Mag)*int(vec2D(Sol.Sun.pos.x - Sol.ship.pos.x, Sol.Sun.pos.y - Sol.ship.pos.y).Mag)
        # Sol.score -= int(Sol.ship.v.Mag*self.tS)
        # if ((Sol.ship.pos.x <= Sol.Sun.pos.x + Sol.Sun.r) or (Sol.ship.pos.x > Sol.Sun.pos.x - Sol.Sun.r)) and ((Sol.ship.pos.x < Sol.Sun.pos.y + Sol.Sun.r) or (Sol.ship.pos.x > Sol.Sun.pos.y - Sol.Sun.r)):
        #     Sol.score = 0
        # Sol.score += 100

        # Damping factor w/ toggle
        if pyxel.btnp(pyxel.KEY_T):
            if Sol.dampToggle:
                Sol.dampToggle = False
                Sol.dampFactor = 1.0
                Sol.dampText = "OFF"
            else:
                Sol.dampToggle = True
                Sol.dampFactor = 0.95
                Sol.dampText = "ON"

        # Velocity and Positional limiters (so the ship doesnt fly too fast/far away)
        if Sol.ship.pos.x <= 0:
            Sol.ship.v.x *= 0.0
            Sol.ship.pos.x += 2
        if Sol.ship.pos.x >= 800*self.scale:
            Sol.ship.v.x *= 0.0
            Sol.ship.pos.x -= 2
        if Sol.ship.pos.y <= 0:
            Sol.ship.v.y *= 0.0
            Sol.ship.pos.y += 2
        if Sol.ship.pos.y >= 800*self.scale:
            Sol.ship.v.y *= 0.0  
            Sol.ship.pos.y -= 2

        # Update Velocity for every body in the list
        for body in self.bodies:
            for other in self.bodies:
                if(other != body):
                    sqD = (other.pos - body.pos).Mag
                    fMag = (other.pos - body.pos).Mag
                    fDir = vec2D((other.pos.x - body.pos.x)/fMag, (other.pos.y - body.pos.y)/fMag)
                    body.a = vec2D((fDir.x * GRAV_CON * other.m) / sqD, (fDir.y * GRAV_CON * other.m) / sqD)
                    body.v += body.a * self.tS

        # Update Position for every body in the list
        for Body in self.bodies:
            Body.pos += vec2D(Body.v.x*self.tS, Body.v.y*self.tS)
        Sol.ship.pos += vec2D(Sol.ship.v.x*self.tS, Sol.ship.v.y*self.tS)
    
    def draw(self):
        pyxel.cls(0)

        # Seed for star placement
        pyxel.rseed(1002)
        # Background star generation, pulls tilemaps from stars.pyxres
        for x in range(int(20*self.scale)):
            pyxel.blt(pyxel.rndi(0,int(799*self.scale)), pyxel.rndi(0,int(799*self.scale)), 0, 0, 0, 6, 6, colkey=0)
        for x in range(int(50*self.scale)):
            pyxel.blt(pyxel.rndi(0,int(799*self.scale)), pyxel.rndi(0,int(799*self.scale)), 0, 8, 0, 5, 5, colkey=0)
        for x in range(int(100*self.scale)):
            pyxel.blt(pyxel.rndi(0,int(799*self.scale)), pyxel.rndi(0,int(799*self.scale)), 0, 0, 8, 3, 3, colkey=0)

        # Draw Ship and Ship outline
        pyxel.blt(Sol.ship.pos.x-1, Sol.ship.pos.y-2, 0, 8, 8, 4, 5, colkey=0)
        pyxel.circb((Sol.ship.pos.x), (Sol.ship.pos.y-1), 3, 7)

        # Draw each body in bodies list on top of orbits
        for Body in self.bodies:

            # Circular Orbits (quick and dirty method)
            pyxel.circb(Sol.Sun.pos.x, Sol.Sun.pos.y, abs(pyxel.sqrt((Sol.Sun.pos.x-Body.pos.x)**2 + (Sol.Sun.pos.y-Body.pos.y)**2)), (Body.col-6)%16)
            
            # Draw Body
            pyxel.circ(Body.pos.x, Body.pos.y, Body.r, Body.col)
            # Body Outline
            pyxel.circb(Body.pos.x, Body.pos.y, Body.r, (Body.col-3)%16)

            # Elliptical Orbits attempt
            # pyxel.ellib(Body.pos.x, Body.pos.y, (abs(sqrt((400-Body.pos.x)**2 + (400-Body.pos.y)**2))), (abs(sqrt((400-Body.pos.x)**2 + (400-Body.pos.y)**2))), Body.col)

            # Trails attempt
            # pyxel.pset(Body.pos.x, Body.pos.y, Body.col)

        # UI
        # Menu
            if Sol.menu:
                pyxel.rect(280*self.scale, 50*self.scale, 80, 12, 0)
                pyxel.text(280*self.scale, 50*self.scale, "     Gravitas 2D\nPress Space to Start!", 7)
            # Elapsed frames
            if self.tS > 0.0:
                pyxel.rect(0,0, 800*self.scale, 6, 3)
                pyxel.text(0, 0, "Frame Count: " + str(pyxel.frame_count), 7)
                #Control Settings
                pyxel.text(800*self.scale-75, 0, "KEY T Damping: " + str(Sol.dampText), 7)
                # Score Display
                # pyxel.text(0,6, "Score: " + str(Sol.score), 3)

        # Reference Lines
        # pyxel.line(0,400,800,400,3)
        # pyxel.line(400,0,400,800,4)
        
Sol()
