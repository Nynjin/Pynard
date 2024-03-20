from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from math import sin

class Pynard(ShowBase):
    def __init__(self): #Initialisation
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle('Projet NSI')
        props.setSize(1200,650)
        props.set_cursor_hidden(True)
        self.disable_mouse()
        base.win.requestProperties(props)
        
        maptest = self.loader.loadModel("../models/maps/labyrinth_colored.glb", noCache=True) #modèle de la map
        maptest.reparentTo(self.render)
        maptest.setPos(0,40,0)

        self.perso = self.loader.loadModel("../models/chars/test_char.glb", noCache=True) #modèle du perso
        self.perso.reparentTo(self.render)
        self.perso.setPos(0, 0, 0)
        self.perso.setH(0)
        
        self.camera.reparentTo(self.perso)
        self.camera.setPos(0, -40, 10)
        self.camera.setH(0)
        
        #initialisation des variables   
        self.vitesse = 15
        self.dist = self.camera.getY() - self.perso.getY() #distance entre caméra et perso (important pour tourner la caméra)

        self.angleXY = 0
        self.angleZ = 0
        self.angle_actuel = 0

        self.reset_cam = False
        self.saut = False

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.setHorizontal(True)

        colliderNode = CollisionNode("player")
        # sphère de collision à coordonnées perso et de rayon 3
        colliderNode.addSolid(CollisionSphere(0, 0, 1, 1))
        collider = self.perso.attachNewNode(colliderNode)

        base.pusher.addCollider(collider, self.perso)
        base.cTrav.addCollider(collider, self.pusher)

        
        
        collider.show()

        colliderNode_labyrinth = CollisionNode("labyrinth")
        
        colliderNode_labyrinth.addSolid(CollisionBox(0, 20, 20, 20))
        collider_labyrinth = maptest.attachNewNode(colliderNode_labyrinth)
        collider_labyrinth.setPos(0,-20,0)
        
        
        #controles PERSO
        self.control = {
            "haut" : False,
            "gauche" : False,
            "droite" : False,
            "saut" : False
        }

        self.accept("z", self.etat_touche, ["haut", True])
        self.accept("z-up", self.etat_touche, ["haut", False])

        self.accept("q", self.etat_touche, ["gauche", True])
        self.accept("q-up", self.etat_touche, ["gauche", False])

        self.accept("d", self.etat_touche, ["droite", True])
        self.accept("d-up", self.etat_touche, ["droite", False])

        self.accept("space", self.etat_touche, ["saut", True])
        self.accept("space-up", self.etat_touche, ["saut", False])


        #contrôles CAMERA
        self.control_camera = {
            "camera_haut" : False,
            "camera_bas" : False,
        }

        self.accept("arrow_up", self.etat_touche, ["camera_haut", True])
        self.accept("arrow_up-up", self.etat_touche, ["camera_haut", False])

        self.accept("arrow_down", self.etat_touche, ["camera_bas", True])
        self.accept("arrow_down-up", self.etat_touche, ["camera_bas", False])


        self.taskMgr.add(self.update, "update")


    def etat_touche(self, touche, etat): #on vérifie l'état des touches
        self.control[touche] = etat 
        self.control_camera[touche] = etat


    def update(self, task): #on met à jour ce qu'il se passe à chaque frame
        dt = globalClock.getDt()

        #4 directions
        if self.control["gauche"]:
            if not self.control["droite"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 90) #perso tourne 90° à gauche
                self.perso.setY(self.perso, self.vitesse * dt)  #perso avance devant son orientation, soit vers la gauche
                self.camera.setX(self.camera, - self.vitesse * dt) #caméra avance à la même vitesse et dans la même direction 
                     
        if self.control["droite"]:
            if not self.control["gauche"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() - 90) #perso tourne 90° à droite
                self.perso.setY(self.perso, self.vitesse * dt) #perso avance devant son orientation, soit vers la droite
                self.camera.setX(self.camera, self.vitesse * dt) #caméra avance à la même vitesse et dans la même direction

        if self.control["haut"]:
            if not self.control["gauche"] and not self.control["droite"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH()) #perso tourne dans le même sens que la caméra
                self.perso.setY(self.perso, self.vitesse * dt) #perso avance devant son orientation, soit vers l'avant
                self.camera.setY(self.camera, self.vitesse * dt) #caméra avance à la même vitesse et dans la même direction
                
        if self.control["bas"]:
            if not self.control["gauche"] and not self.control["droite"] and not self.control["haut"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 180) #perso regarde la caméra
                self.perso.setY(self.perso, self.vitesse * dt) #perso avance devant son orientation, soit vers la cam 
                self.camera.setY(self.camera, - self.vitesse * dt) #caméra avance à la même vitesse et dans la même direction


        #saut
        if self.control["saut"]:
            if self.perso.getZ() < -10: #on vérifie que le perso est sur le sol
                self.saut = True
            
        if self.saut == True:
            self.perso.setFluidZ(self.perso, 0.5) #le perso monte 
        else :
            if self.perso.getZ()>=0 : #le perso descent s'il n'est pas sur le sol
                self.perso.setFluidZ(self.perso, -0.5) 

        if self.perso.getZ() > 10: #le saut s'arrête quand le perso atteint sa hauteur max
            self.saut = False


        #caméra
        if self.control_camera["camera_haut"] and self.angleZ > -0.5: #on limite l'angle de la caméra
            self.angleZ -=0.01 #vitesse de tour

        if self.control_camera["camera_bas"] and self.angleZ < 0.2: #on limite l'angle de la caméra
            self.angleZ +=0.01 #vitesse de tour

        self.perso.setY(40)
        self.camera.setZ(sin(self.angleZ) * self.dist)
        self.camera.lookAt(self.perso) #caméra regarde vers le perso

        return task.cont

        

Game = Pynard()
Game.run()