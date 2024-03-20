from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from math import *

class Pynard(ShowBase):

    def __init__(self): #Initialisation
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle('Test nouvelle caméra')
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
        self.camera.setPos(30, 0, 5)
        self.camera.setH(0)


        #initialisation des variables   
        self.vitesse = 15  

        self.distance = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2 + (self.perso.getZ() - self.camera.getZ())**2) #distance entre caméra et personnage

        self.mouvement = False

        self.mouvement_cam = False

        self.reset_cam = False
        
        self.saut = False
        
        
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

        self.accept("r", self.etat_touche, ["reset_camera", True])
        self.accept("r-up", self.etat_touche, ["reset_camera", False])

        self.taskMgr.add(self.update, "update")


    def etat_touche(self, touche, etat): #on vérifie l'état des touches
        self.control[touche] = etat 
        self.control_camera[touche] = etat


    def update(self, task): #on met à jour ce qu'il se passe à chaque frame
        dt = globalClock.getDt()
        
        #4 directions
        if self.control["gauche"]:
            self.mouvement = True
            if not self.control["droite"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 90) #perso tourne 90° à gauche
                     
        if self.control["droite"]:
            self.mouvement = True
            if not self.control["gauche"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() - 90) #perso tourne 90° à droite

        if self.control["haut"]:
            self.mouvement = True
            if not self.control["gauche"] and not self.control["droite"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH()) #perso tourne dans le même sens que la caméra
                if self.distance > 29.9 : #camera avance avec le perso si elle n'est pas trop proche de lui
                    self.camera.setY(self.camera, self.vitesse * dt) 
                
        if self.control["bas"]:
            self.mouvement = True
            if not self.control["gauche"] and not self.control["droite"] and not self.control["haut"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 180) #perso regarde la caméra
                if self.distance < 30.1 : #camera recule avec le perso si elle n'est pas trop loin de lui
                    self.camera.setY(self.camera, - self.vitesse * dt)
                        

        #8 directions:
        if self.control["haut"] and self.control["gauche"]: #si avant et gauche pressés
            self.perso.setH(self.camera.getH() + 45) #le perso s'oriente vers l'avant-gauche

        if self.control["haut"] and self.control["droite"]: #si avant et droite pressés
            self.perso.setH(self.camera.getH() - 45) #le perso s'oriente vers l'avant-droit

        if self.control["bas"] and self.control["gauche"]: #si arrière et gauche pressés
            self.perso.setH(self.camera.getH() + 135) #le perso s'oriente vers l'arrière-gauche
             
        if self.control["bas"] and self.control["droite"]: #si arrière et droite pressés
            self.perso.setH(self.camera.getH() - 135) #le perso s'oriente vers l'arrière-droit

        if self.mouvement == True: #si le perso est censé bougé alors
            self.perso.setY(self.perso, self.vitesse * dt) #le perso avance selon son orientation

        #saut
        if self.control["saut"]:
            if self.saut == False: #on vérifie que le perso n'est pas déjà en train de sauter
                self.saut = True
                self.hauteur_saut = 0.4
            
        if self.saut == True:
            self.perso.setZ(self.perso.getZ() + self.hauteur_saut) #le perso monte chaque frame
            if self.hauteur_saut > -0.4:
                self.hauteur_saut = self.hauteur_saut - 0.01 #le perso redescent chaque frame jusqu'à sa hauteur initiale (à changer quand les collisions du sol seront faites)
            else :
                self.saut = False


        #caméra 
        if self.control_camera["camera_haut"] and self.camera.getZ() < self.perso.getZ() + 14: #on limite la hauteur du mouvement de la caméra
            self.camera.setFluidZ(self.camera, 1)
            self.mouvement_cam = True

        if self.control_camera["camera_bas"] and self.camera.getZ() > self.perso.getZ() - 4: #on limite la hauteur du mouvement de la caméra
            self.camera.setFluidZ(self.camera, -1)
            self.mouvement_cam = True

        if self.control_camera["camera_gauche"]:
            self.camera.setFluidX(self.camera, -1) #la caméra bouge vers sa propre gauche
                
        if self.control_camera["camera_droite"]:
            self.camera.setFluidX(self.camera, 1) #la caméra bouge vers sa propre droite
            
        if self.control_camera["reset_camera"]: #téléporte la caméra derrière le perso et à sa hauteur initiale
            self.camera.setPos(self.perso.getPos())
            self.camera.setH(self.perso, 0)
            self.camera.setFluidY(self.camera, - 30)

        if self.mouvement == True and self.mouvement_cam == False: #remet la caméra à sa hauteur initiale si le personnage bouge et qu'elle n'est pas utilisée
            if self.camera.getZ() > self.perso.getZ() + 0.5:
                self.camera.setFluidZ(self.camera, -0.1)
            elif self.camera.getZ() < self.perso.getZ() - 0.5:
                self.camera.setFluidZ(self.camera, 0.1)

        if self.distance < 29.5 : #empêche la caméra d'être trop proche du personnage
            self.camera.setFluidY(self.camera, -0.1) 

        elif self.distance > 35 : #empêche la caméra d'être trop loin du personnage
            self.camera.setFluidY(self.camera, 0.5) 

        if self.camera.getZ() > self.perso.getZ() + 15.5 : #empêche la caméra d'être trop haute par rapport au perso
            self.camera.setFluidZ(self.camera, -0.135)

        elif self.camera.getZ() < self.perso.getZ() - 5.5 : #empêche la caméra d'être trop basse par rapport au perso
            self.camera.setFluidZ(self.camera, 0.05)
        

        self.distance = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2 + (self.perso.getZ() - self.camera.getZ())**2) #distance entre caméra et personnage
        self.camera.lookAt(self.perso) #caméra regarde vers le perso
        self.mouvement = False


        return task.cont

        

Game = Pynard()
Game.run()