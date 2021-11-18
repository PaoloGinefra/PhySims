from Graphics import *
from Sim import * 

if __name__ == '__main__':
        
    Vis = Visualizer(800, 800)
    stars = Stars(number=100, minR=1, maxR=5, vis = Vis)

    Sim = Simulation(dt = 0.01, BufferSteps=500)

    b1 = Body(30, np.array([300, 400]), np.array([0, -50]), DrawInner= True)
    b2 = Body(20, np.array([500, 400]), np.array([0, 60]), DrawInner = True, color=(0, 255, 0))
    b3 = Body(10, np.array([400, 200]), np.array([10, 0]), DrawInner = True, color=(255, 0, 0))

    Sim.AddBody(b1)
    Sim.AddBody(b2)
    Sim.AddBody(b3)

    Sim.PopulateBuffer()

    while(Vis.isActive):
        Vis.HandleInput()

        Sim.SimStep()
        Sim.SaveState()
        Sim.LoadState()


        Vis.DrawBg(stars)
        Vis.DrawSim(Sim)

        Vis.Draw()
