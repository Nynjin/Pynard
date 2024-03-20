from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from math import pi, sin, cos

class Pynard(ShowBase):
    def __init__(self): #Initialisation
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle('Test collisions')
        props.setSize(1200,650)
        props.set_cursor_hidden(True)
        self.disable_mouse()

        base.win.requestProperties(props)
        
        maptest = self.loader.loadModel("../models/maps/labyrinth_colored.glb", noCache=True) #modèle de la map
        maptest.reparentTo(self.render)
        maptest.setPos(-50,0,0)

        self.perso = self.loader.loadModel("../models/chars/test_char.glb", noCache=True) #modèle du perso
        self.perso.reparentTo(self.render)
        self.perso.setPos(0, 0, 0)
        self.perso.setH(0)
        
        self.camera.reparentTo(self.render)
        self.camera.setPos(0, -40, 5)
        self.camera.setH(0)

        self.camera_check = self.loader.loadModel("../models/chars/test_char.glb", noCache=True) #crée un objet invisible qui sert de repère à la caméra
        self.camera_check.reparentTo(self.render)
        self.camera_check.hide()
        self.camera_check.setPos(1, -40, 5)
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
        colliderNode = CollisionNode("perso")
        colliderNode.addSolid(CollisionSphere(0, 0, 1, 1))
        collider = self.perso.attachNewNode(colliderNode)
        collider.setPos(0,0,0)

        self.pusher.addCollider(collider, self.perso)
        self.cTrav.addCollider(collider, self.pusher)

        #avec cam
        colliderNode_camera = CollisionNode("camera")
        colliderNode_camera.addSolid(CollisionBox(0,1,1,1))
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
            "bas" : False,
            "gauche" : False,
            "droite" : False,
            "saut" : False
        }

        self.accept("z", self.etat_touche, ["haut", True])
        self.accept("z-up", self.etat_touche, ["haut", False])

        self.accept("s", self.etat_touche, ["bas", True])
        self.accept("s-up", self.etat_touche, ["bas", False])

        self.accept("q", self.etat_touche, ["gauche", True])
        self.accept("q-up", self.etat_touche, ["gauche", False])

        self.accept("d", self.etat_touche, ["droite", True])
        self.accept("d-up", self.etat_touche, ["droite", False])

        self.accept("space", self.etat_touche, ["saut", True])
        self.accept("space-up", self.etat_touche, ["saut", False])

        #controles CAMERA
        self.control_camera = {
            "camera_haut" : False,
            "camera_bas" : False,
            "camera_gauche" : False,
            "camera_droite" : False,
            "reset_camera" : False
        }

        self.accept("arrow_up", self.etat_touche, ["camera_haut", True])
        self.accept("arrow_up-up", self.etat_touche, ["camera_haut", False])

        self.accept("arrow_down", self.etat_touche, ["camera_bas", True])
        self.accept("arrow_down-up", self.etat_touche, ["camera_bas", False])

        self.accept("arrow_left", self.etat_touche, ["camera_gauche", True])
        self.accept("arrow_left-up", self.etat_touche, ["camera_gauche", False])

        self.accept("arrow_right", self.etat_touche, ["camera_droite", True])
        self.accept("arrow_right-up", self.etat_touche, ["camera_droite", False])

        self.accept("i", self.etat_touche, ["reset_camera", True])
        self.accept("i-up", self.etat_touche, ["reset_camera", False])

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
        if self.control["gauche"]:
            if not self.control["droite"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 90) #perso tourne 90° à gauche
                self.perso.setY(self.perso, self.vitesse * dt)  #perso avance devant son orientation, soit vers la gauche
                if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                    self.mouvement_cam()
                     
        if self.control["droite"]:
            if not self.control["gauche"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() - 90) #perso tourne 90° à droite
                self.perso.setY(self.perso, self.vitesse * dt) #perso avance devant son orientation, soit vers la droite
                if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                    self.mouvement_cam()

        if self.control["haut"]:
            if not self.control["gauche"] and not self.control["droite"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH()) #perso tourne dans le même sens que la caméra
                self.perso.setY(self.perso, self.vitesse * dt) #perso avance devant son orientation, soit vers l'avant
                if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                    self.mouvement_cam()
                
        if self.control["bas"]:
            if not self.control["gauche"] and not self.control["droite"] and not self.control["haut"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 180) #perso regarde la caméra
                self.perso.setY(self.perso, self.vitesse * dt) #perso avance devant son orientation, soit vers la cam 
                if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                    self.mouvement_cam()
                

        #8 directions:
        if self.control["haut"] and self.control["gauche"]: #si avant et gauche pressés
            #perso
            self.perso.setH(self.camera.getH() + 45) #le perso s'oriente vers l'avant-gauche
            self.perso.setY(self.perso, self.vitesse * dt) #le perso avance selon son orientation
            #camera
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.mouvement_cam()

        if self.control["haut"] and self.control["droite"]: #si avant et droite pressés
            #perso
            self.perso.setH(self.camera.getH() - 45) #le perso s'oriente vers l'avant-droit
            self.perso.setY(self.perso, self.vitesse * dt) #le perso avance selon son orientation
            #camera
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.mouvement_cam()

        if self.control["bas"] and self.control["gauche"]: #si arrière et gauche pressés
            #perso
            self.perso.setH(self.camera.getH() + 135) #le perso s'oriente vers l'arrière-gauche
            self.perso.setY(self.perso, self.vitesse * dt) #le perso avance selon son orientation
            #camera
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.mouvement_cam()

        if self.control["bas"] and self.control["droite"]: #si arrière et droite pressés
            #perso
            self.perso.setH(self.camera.getH() - 135) #le perso s'oriente vers l'arrière-droit
            self.perso.setY(self.perso, self.vitesse * dt) #le perso avance selon son orientation
            #camera
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
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
        if self.angleXY > 6.2 or self.angleXY < -6.2: #reset l'angle permettant de tourner la caméra autour du perso
            self.angleXY = 0

        if self.control_camera["camera_haut"] and self.angleZ > -0.5: #on limite l'angle de la caméra
            self.angleZ -=0.04 #vitesse de tour

        if self.control_camera["camera_bas"] and self.camera.getZ() >= self.perso.getZ(): #on limite l'angle de la caméra
            self.angleZ +=0.04 #vitesse de tour

        if self.control_camera["camera_gauche"]:
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.angleXY += 0.06 #vitesse de tour
                self.mouvement_cam()
                self.pression_cam_gauche = True
                self.pression_cam_droite = False
            elif self.pression_cam_gauche == False:
                self.angleXY += 0.06 #vitesse de tour
                self.mouvement_cam()
                
        if self.control_camera["camera_droite"]:
            if abs(self.camera_check.getX()) - abs(self.camera.getX()) == 0: #vérifie si le repère de la caméra se trouve au même endroit que celle-ci
                self.angleXY -= 0.06 #vitesse de tour
                self.mouvement_cam()
                self.pression_cam_droite = True
                self.pression_cam_gauche = False
            elif self.pression_cam_droite == False:
                self.angleXY -= 0.06 #vitesse de tour
                self.mouvement_cam()

        if self.control_camera["reset_camera"]:
            self.angleXY = self.perso.getH() / -58 # -58 = 1 pour 'self.angleXY' permettant de tourner la caméra
            self.angleZ = self.perso.getZ()+10 / -43 # -43 = 1 pour 'self.angleZ' permettant de tourner la caméra
            self.camera.setFluidY(self.camera, 40)
            self.camera.setH(self.perso, 0)
            self.camera.setFluidY(self.camera, - 40)


        self.camera.setFluidZ(sin(self.angleZ) * self.dist)
        self.camera.lookAt(self.perso) #caméra regarde vers le perso
        self.camera_check.setFluidZ(sin(self.angleZ) * self.dist)
        self.camera_check.lookAt(self.perso) #caméra regarde vers le perso

        print(self.camera.getPos())
        print(self.camera_check.getPos())


        return task.cont

        

Game = Pynard()
Game.run()