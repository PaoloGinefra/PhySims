import numpy as np
from pygame import init
from Color import *

class Body:
    RADIUS_COEF = 1
    def __init__(self, mass, inital_position : np.array, initial_vel : np.array, DrawInner = False, color = BD_COLOR) -> None:
        self.mass = mass
        self.Ipos = inital_position
        self.Ivel = initial_vel

        self.pos = inital_position
        self.vel = initial_vel
        self.acc = np.array([0, 0], dtype=np.float64)

        self.radius = int(Body.RADIUS_COEF * mass)
        self.DrawInner = DrawInner

        self.id = -1
        self.color = color
        self.Traj = Trajectory()

        self.virtualPos = inital_position
        self.PrevVirtualPos = inital_position
        self.PrevVirtualVel = initial_vel
        pass

    def __str__(self):
        return f"Body n.{self.id}:\n\tmass:{self.mass}\n\tpos:{self.pos}\n\tvel:{self.vel}\n\tacc:{self.acc}"

class Simulation:
    G = 100000
    ORIGIN = np.array([0.0, 0.0])

    def __init__(self, dt : float, BufferSteps = 0) -> None:
        self.dt = dt
        self.Bodies = []
        self.Buffersteps = BufferSteps
        pass

    def AddBody(self, b : Body):
        b.id = len(self.Bodies)
        self.Bodies.append(b)

    def ComputeForce(self, b1 : Body, b2 : Body):
        distance = np.linalg.norm(b1.pos - b2.pos)
        vers = np.add(b1.pos, -b2.pos, dtype=np.float64) / distance

        F = Simulation.G / distance**2

        b1.acc = np.subtract(b1.acc, vers * F * b2.mass)
        b2.acc = np.add(b2.acc, vers * F * b1.mass)

    def ApplyForces(self):
        l = len(self.Bodies)

        for b in self.Bodies:
            b.acc = np.array([0, 0], dtype=np.float64)

        for i in range(l):
            for j in range(1, l - i):
                self.ComputeForce(self.Bodies[i], self.Bodies[i + j])

    def areColliding(self, a : Body, b : Body):
        d = np.subtract(a.pos, b.pos)
        dist = np.dot(d, d)
        limit = (a.radius + b.radius)**2
        return dist <= limit

    def Collision(self, a : Body, b : Body):
        M_Sum = (a.mass + b.mass)

        V_diff = np.subtract(a.vel, b.vel)
        P_diff = np.subtract(a.pos, b.pos)

        Vc = np.dot(V_diff, P_diff) / (np.dot(P_diff, P_diff))

        a.vel = np.add(a.vel, -2*b.mass/M_Sum * Vc * P_diff)
        b.vel = np.add(b.vel, 2*a.mass/M_Sum * Vc * P_diff)

    def HandleCollisions(self):
        l = len(self.Bodies)

        for i in range(l):
            for j in range(1, l - i):
                if(self.areColliding(self.Bodies[i], self.Bodies[i + j])):
                    self.Collision(self.Bodies[i], self.Bodies[i + j])


    def BodyStepVel(self, b : Body):
        b.vel = np.add(b.vel, b.acc * self.dt)

    def BodyStepPos(self, b : Body):
        b.pos = np.add(b.pos, b.vel * self.dt)

    def SaveState(self):
        for b in self.Bodies:
            b.Traj + (b.pos - Simulation.ORIGIN)

    def LoadState(self):
        for b in self.Bodies:
            b.PrevVirtualPos = b.virtualPos
            b.virtualPos = b.Traj.Read()

    def SimStep(self):
        #Simulation.ORIGIN = self.Bodies[0].pos - np.array([400, 400])
        self.ApplyForces()

        for b in self.Bodies:
            self.BodyStepVel(b)

        self.HandleCollisions()

        for b in self.Bodies:
            self.BodyStepPos(b)

    def PopulateBuffer(self):
        for _ in range(self.Buffersteps):
            self.SimStep()
            self.SaveState()


             
class Trajectory:
    def __init__(self) -> None:
        self.points = []
        pass

    def __add__(self, p : np.array):
        self.points.append(p)

    def Read(self):
        a = self.points[0]
        self.points = self.points[1:]
        return a
    

