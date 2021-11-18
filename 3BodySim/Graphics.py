import pygame
from pygame import  gfxdraw

import numpy as np
import random

from Sim import Body, Simulation, Trajectory
from Color import *

class Visualizer:
    isActive = True
    VecLen = 40

    def __init__(self, width, height):
        #initialize Parameters
        self.width = width
        self.height = height
        self.isActive = True

        #initialize pygame window
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pass

    def Line(self, pos : list, color = WHITE, width = 2):
        if len(pos) >= 2:
            pygame.draw.lines(self.screen, color, closed=False, width = width, points=pos)

    def AALine(self, pos : list, color = WHITE):
        if len(pos) >= 2:
            pygame.draw.aalines(self.screen, color = color, closed=False, points=pos)

    def Triangle(self, pos : np.array, theta = 0, radius = 5, color = WHITE):
        poss = []
        alpha = theta
        for i in range(1, 4):
            poss.append((pos[0] + np.cos(alpha) * radius, pos[1] + np.sin(alpha) * radius))
            alpha += np.pi * 2 / 3

        pygame.draw.polygon(self.screen, color = color, points=poss)
    
    def ArrowPoints(self, points, width = 2, tSize = 5, color = WHITE):
        points = [p - Simulation.ORIGIN for p in points]

        tail = points[-2]
        head = points[-1]

        self.Line(points, color=color, width=width)
        diff = np.subtract(head, tail)
        diff = diff / np.linalg.norm(diff)
        theta = np.arccos(diff[0])

        self.Triangle(head, theta=theta, radius=tSize, color=color)

    def DrawBody(self, b: Body, color = WHITE, fillingColor = -1, origin = None):
        p = b.virtualPos

        if(type(origin) != None):
            p = np.subtract(p, origin)

        gfxdraw.aacircle(self.screen, int(p[0]), int(p[1]), b.radius, color)
        if b.DrawInner:
            gfxdraw.filled_circle(self.screen, int(p[0]), int(p[1] ), b.radius, fillingColor)

    def DrawVec(self, pos, vel, width = 2, color=WHITE):
        d = vel / np.linalg.norm(vel)
        self.ArrowPoints([pos, pos + d * Visualizer.VecLen], width=width, color=color)
    
    def DrawBg(self, stars):
        self.screen.fill(BLACK)
        for s in stars.stars:
            if self.isInWindow(s.pos):
                self.DrawBody(s, fillingColor=WHITE, origin=Simulation.ORIGIN)

    def DrawTrajectroy(self, t : Trajectory, color = WHITE, width = 2):
        self.AALine(t.points, color = color)

    def Draw(self):
        #Update the screen
        pygame.display.flip()
        pygame.transform.smoothscale(self.screen, (self.width / 10, self.height / 10))


    def isInWindow(self, pos):
        return (0 <= pos[0] - Simulation.ORIGIN[0] < self.width and 0 <= pos[1] - Simulation.ORIGIN[1] < self.height)

    def DrawSim(self, s):
        for b in s.Bodies:
            self.DrawTrajectroy(b.Traj)

        for b in s.Bodies:
            if(self.isInWindow(b.virtualPos)):
                Vvel = np.subtract(b.virtualPos, b.PrevVirtualPos)
                self.DrawVec(b.virtualPos, Vvel, color=VELL_COLOR)
                self.DrawVec(b.virtualPos, np.subtract(Vvel, b.PrevVirtualVel), color=ACC_COLOR)
                b.PrevVirtualVel = Vvel

        for b in s.Bodies:
            if(self.isInWindow(b.virtualPos)):
                self.DrawBody(b, color=b.color, fillingColor=b.color, origin=Simulation.ORIGIN)
    

    def HandleInput(self):
        #Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isActive = False

class Stars:
    def __init__(self, number : int, minR, maxR, vis:Visualizer, offset = 500) -> None:
        self.num = number
        self.minR = minR
        self.maxR = maxR

        self.GenerateStars(vis, offset)
        pass

    def GenerateStars(self, Vis : Visualizer, offset = 500):
        self.stars = []
        for _ in range(self.num):
            pos = np.array([random.randint(-offset, Vis.width+offset), random.randint(-offset, Vis.height+offset)])
            rad = int(random.random() * (self.maxR - self.minR) + self.minR)
            s = Body(rad, pos, [], DrawInner=True)
            self.stars.append(s)


if __name__ == '__main__':
        
    Vis = Visualizer(800, 800)

    stars = Stars(number=100, minR=1, maxR=5, vis = Vis)


    while(Vis.isActive):
        Vis.HandleInput()
        Vis.DrawBg(stars)

        Vis.Draw()



