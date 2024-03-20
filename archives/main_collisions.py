from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from math import pi, sin, cos

class Pynard(ShowBase):
    def __init__(self): #Initialisation
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle('Pynard')
        props.setSize(1200,650)
        props.set_cursor_hidden(True)
        self.disable_mouse()

        base.win.requestProperties(props)
        
        maptest = self.loader.loadModel("../models/maps/labyrinth_colored.glb", noCache=True) #modèle de la map
        maptest.reparentTo(self.render)
        maptest.setPos(-70,0,0)

        self.perso = self.loader.loadModel("../models/chars/test_char.glb", noCache=True) #modèle du perso
        self.perso.reparentTo(self.render)
        self.perso.setPos(0, 0, 0)
        self.perso.setH(0)
        
        self.camera.reparentTo(self.render)
        self.camera.setPos(0, -40, 10)
        self.camera.setH(0)

        self.camera_check = self.loader.loadModel("../models/chars/test_char.glb", noCache=True) #crée un objet invisible qui sert de repère à la caméra
        self.camera_check.reparentTo(self.render)
        self.camera_check.hide()
        self.camera_check.setPos(0, -40, 0)
        self.camera_check.setH(0)


        #initialisation des variables   
        self.vitesse = 15
        self.dist = self.camera.getY() - self.perso.getY() #distance entre caméra et perso (important pour tourner la caméra)

        self.angleXY = 0
        self.angleZ = 0

        self.reset_cam = False

        self.saut = False

        self.pression_cam_gauche = False #indique si la caméra tourne vers la gauche
        self.pression_cam_droite = False #indique si la caméra tourne vers la droite


        # Collisions 
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.setHorizontal(True)
        base.cTrav.setRespectPrevTransform(True)
    
        # avec perso
        colliderNode = CollisionNode("player")
        colliderNode.addSolid(CollisionSphere(0, 0, 1, 1))
        collider = self.perso.attachNewNode(colliderNode)

        self.pusher.addCollider(collider, self.perso)
        self.cTrav.addCollider(collider, self.pusher)

        #avec cam
        colliderNode_camera = CollisionNode("camera")
        colliderNode_camera.addSolid(CollisionSphere(0,0,0,10))
        collider_camera = self.camera.attachNewNode(colliderNode_camera)
        collider_camera.setPos(0,0,0)

        self.pusher.addCollider(collider_camera, self.camera)
        self.cTrav.addCollider(collider_camera, self.pusher)
        
        #avec map
        colliderNode_labyrinth = CollisionNode("labyrinth")
        colliderNode_labyrinth.addSolid(CollisionBox(0, 50, 50, 50))
        collider_labyrinth = maptest.attachNewNode(colliderNode_labyrinth)
        collider_labyrinth.setPos(0,0,5)
        
        
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

    def mouvement_cam(self): #méthode qui gère les mouvements de la caméra et de son repère
        self.camera_check.setPos(self.camera.getPos())
        self.camera.setFluidX(self.perso.getX() + (sin(self.angleXY) * + self.dist)) #caméra tourne autour du personnage
        self.camera.setFluidY(self.perso.getY() + (cos(self.angleXY) * + self.dist))
        self.camera_check.setFluidX(self.perso.getX() + (sin(self.angleXY) * + self.dist)) #le repère de la caméra tourne autour du personnage de la même manière
        self.camera_check.setFluidY(self.perso.getY() + (cos(self.angleXY) * + self.dist))


    def update(self, task): #on met à jour ce qu'il se passe à chaque frame
        dt = globalClock.getDt()

        #4 directions
        if self.control["haut"]:
            self.perso.setY(self.perso, self.vitesse * dt) #perso avance devant son orientation, soit vers l'avant
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.mouvement_cam()

        if self.control["gauche"]:
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.angleXY -= 0.035
                self.perso.setH(self.perso, 2) #perso tourne 90° à gauche
                self.mouvement_cam()
                self.pression_cam_gauche = True
                self.pression_cam_droite = False
            elif self.pression_cam_gauche == False:
                self.angleXY -= 0.035 #vitesse de tour
                self.mouvement_cam()
                
        if self.control["droite"]:
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.angleXY += 0.035
                self.perso.setH(self.perso, - 2) #perso tourne 90° à droite
                self.mouvement_cam()
                self.pression_cam_gauche = False
                self.pression_cam_droite = True
            elif self.pression_cam_droite == False:
                self.angleXY += 0.035 #vitesse de tour
                self.mouvement_cam()


        #saut
        if self.control["saut"]:
            if self.perso.getZ() < 0.5: #on vérifie que le perso est sur le sol
                self.saut = True
            
        if self.saut == True:
            self.perso.setZ(self.perso, 0.5) #le perso monte 
        else :
            if self.perso.getZ()>=0.5 : #le perso descent s'il n'est pas sur le sol
                self.perso.setZ(self.perso, -0.5) 

        if self.perso.getZ() > 10: #le saut s'arrête quand le perso atteint sa hauteur max
            self.saut = False


        #caméra
        if self.control_camera["camera_haut"] and self.angleZ > -0.5: #on limite l'angle de la caméra
            self.angleZ -=0.01 #vitesse de tour

        if self.control_camera["camera_bas"] and self.camera.getZ() >= self.perso.getZ(): #on limite l'angle de la caméra
            self.angleZ +=0.01 #vitesse de tour

        self.camera.setFluidZ(sin(self.angleZ) * self.dist)
        self.camera.lookAt(self.perso) #caméra regarde vers le perso

        print(self.camera.getPos())
        print(self.camera_check.getPos())
        return task.cont

        

Game = Pynard()
Game.run()