from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from math import *

class Pynard(ShowBase):

    def __init__(self): #Initialisation
        ShowBase.__init__(self)
        props = WindowProperties()
        props.setTitle('Test gravité')
        props.setSize(1200,650)
        props.set_cursor_hidden(True)
        self.disable_mouse()

        base.win.requestProperties(props)

        self.maptest = self.loader.loadModel("../models/maps/Village de départ.glb", noCache=True) #modèle de la map
        self.maptest.reparentTo(self.render)
        self.maptest.setPos(0,0,0)

        self.perso = self.loader.loadModel("../models/chars/test_char.glb", noCache=True) #modèle du perso
        self.perso.reparentTo(self.render)
        self.perso.setPos(0, 0, 0)
        self.perso.setH(0)
        
        self.camera.reparentTo(self.render)
        self.camera.setPos(30, 0, 5)
        self.camera.setH(0)


        #initialisation des variables   
        self.vitesse = 0 #vitesse du perso

        self.speedcap = 15 #limite de vitesse du perso

        self.distance = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2 + (self.perso.getZ() - self.camera.getZ())**2) #distance entre caméra et personnage

        self.mouvement = False #si le perso bouge

        self.mouvement_cam = False #si la caméra monte ou descent

        self.reset_cam = False #si la caméra se reset

        self.reset_cam_counter = 0 #compteur avant de pouvoir reset la caméra
        
        self.saut = False #si le perso est en plein saut


        # Collisions 
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.grav = CollisionHandlerGravity()

        base.cTrav.setRespectPrevTransform(True)
    
        # avec perso
        colliderNode = CollisionNode("perso")
        colliderNode.addSolid(CollisionBox(0, 1.2, 1.2, 0.8))
        collider = self.perso.attachNewNode(colliderNode)
        collider.setPos(0,0,1.2)

        colliderNode2 = CollisionNode("perso2")
        colliderNode2.addSolid(CollisionBox(0, 1, 1, 0.01))
        collider2 = self.perso.attachNewNode(colliderNode2)
        collider2.setPos(0,0,-0.1)

        collider.show()
        collider2.show()

        self.pusher.addCollider(collider, self.perso)
        self.cTrav.addCollider(collider, self.pusher)
        self.grav.addCollider(collider2, self.perso)
        self.cTrav.addCollider(collider2,self.grav)

        #avec cam
        colliderNode_camera = CollisionNode("camera")
        colliderNode_camera.addSolid(CollisionBox(0, 1, 1, 1))
        collider_camera = self.camera.attachNewNode(colliderNode_camera)
        collider_camera.setPos(0,0,1)

        self.pusher.addCollider(collider_camera, self.camera)
        self.cTrav.addCollider(collider_camera, self.pusher)

        #avec map
        colliderNode_sol = CollisionNode("sol")
        colliderNode_sol.addSolid(CollisionBox(0, 150, 170, 10))
        collider_sol = self.maptest.attachNewNode(colliderNode_sol)
        collider_sol.setPos(0, 0, -10)
        collider_sol.show()

        colliderNode_mur1 = CollisionNode("mur1")
        colliderNode_mur1.addSolid(CollisionBox(0, 1, 170, 10))
        collider_mur1 = self.maptest.attachNewNode(colliderNode_mur1)
        collider_mur1.setPos(150, 0, 10)
        collider_mur1.show()

        colliderNode_mur2 = CollisionNode("mur2")
        colliderNode_mur2.addSolid(CollisionBox(0, 1, 170, 10))
        collider_mur2 = self.maptest.attachNewNode(colliderNode_mur2)
        collider_mur2.setPos(-150, 0, 10)
        collider_mur2.show()

        colliderNode_mur3 = CollisionNode("mur3")
        colliderNode_mur3.addSolid(CollisionBox(0, 170, 1, 10))
        collider_mur3 = self.maptest.attachNewNode(colliderNode_mur3)
        collider_mur3.setPos(0, 170, 10)
        collider_mur3.show()

        colliderNode_mur4 = CollisionNode("mur4")
        colliderNode_mur4.addSolid(CollisionBox(0, 160, 1, 10))
        collider_mur4 = self.maptest.attachNewNode(colliderNode_mur4)
        collider_mur4.setPos(0, -170, 10)
        collider_mur4.show()

        colliderNode_cube = CollisionNode("cube")
        colliderNode_cube.addSolid(CollisionBox(0, 5, 5, 2))
        collider_cube = self.maptest.attachNewNode(colliderNode_cube)
        collider_cube.setPos(10, 10, 2)
        collider_cube.show() 

        colliderNode_cube2 = CollisionNode("cube2")
        colliderNode_cube2.addSolid(CollisionBox(0, 5, 5, 5))
        collider_cube2 = self.maptest.attachNewNode(colliderNode_cube2)
        collider_cube2.setPos(20, 10, 5)
        collider_cube2.show() 

        #controles PERSO
        self.control = { #dictionnaire des variables utilisées pour les inputs du perso
            "haut" : False,
            "bas" : False,
            "gauche" : False,
            "droite" : False,
            "saut" : False,
            "sprint" : False
        }

        self.accept("z", self.etat_touche, ["haut", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-z", self.etat_touche, ["haut", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("z-up", self.etat_touche, ["haut", False]) #variable qui devient fausse si la touche est relachée

        self.accept("s", self.etat_touche, ["bas", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-s", self.etat_touche, ["bas", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("s-up", self.etat_touche, ["bas", False]) #variable qui devient fausse si la touche est relachée

        self.accept("q", self.etat_touche, ["gauche", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-q", self.etat_touche, ["gauche", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("q-up", self.etat_touche, ["gauche", False]) #variable qui devient fausse si la touche est relachée

        self.accept("d", self.etat_touche, ["droite", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-d", self.etat_touche, ["droite", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("d-up", self.etat_touche, ["droite", False]) #variable qui devient fausse si la touche est relachée

        self.accept("space", self.etat_touche, ["saut", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-space", self.etat_touche, ["saut", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("space-up", self.etat_touche, ["saut", False]) #variable qui devient fausse si la touche est relachée

        self.accept("shift", self.etat_touche, ["sprint", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-up", self.etat_touche, ["sprint", False]) #variable qui devient fausse si la touche est relachée

        #controles CAMERA
        self.control_camera = { #dictionnaire des variables utilisées pour les inputs de la caméra
            "camera_haut" : False,
            "camera_bas" : False,
            "camera_gauche" : False,
            "camera_droite" : False,
            "reset_camera" : False
        }

        self.accept("arrow_up", self.etat_touche, ["camera_haut", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-arrow_up", self.etat_touche, ["camera_haut", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("arrow_up-up", self.etat_touche, ["camera_haut", False]) #variable qui devient fausse si la touche est relachée

        self.accept("arrow_down", self.etat_touche, ["camera_bas", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-arrow_down", self.etat_touche, ["camera_bas", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("arrow_down-up", self.etat_touche, ["camera_bas", False]) #variable qui devient fausse si la touche est relachée

        self.accept("arrow_left", self.etat_touche, ["camera_gauche", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-arrow_left", self.etat_touche, ["camera_gauche", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("arrow_left-up", self.etat_touche, ["camera_gauche", False]) #variable qui devient fausse si la touche est relachée

        self.accept("arrow_right", self.etat_touche, ["camera_droite", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-arrow_right", self.etat_touche, ["camera_droite", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("arrow_right-up", self.etat_touche, ["camera_droite", False]) #variable qui devient fausse si la touche est relachée

        self.accept("r", self.etat_touche, ["reset_camera", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-r", self.etat_touche, ["reset_camera", True]) #obligé de créer une nouvelle commande parce que shift + une touche est considéré comme un input différent
        self.accept("r-up", self.etat_touche, ["reset_camera", False]) #variable qui devient fausse si la touche est relachée

        self.taskMgr.add(self.update, "update")


    def etat_touche(self, touche, etat): #on vérifie l'état des touches
        self.control[touche] = etat 
        self.control_camera[touche] = etat


    def update(self, task): #on met à jour ce qu'il se passe à chaque frame
        dt = globalClock.getDt()
        
        #perso

        #4 directions
        if self.control["gauche"]: #si touche assignée à "gauche" pressée
            self.mouvement = True
            if not self.control["droite"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 90) #perso tourne 90° à gauche
                     
        if self.control["droite"]: #si touche assignée à "droite" pressée
            self.mouvement = True
            if not self.control["gauche"] and not self.control["haut"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() - 90) #perso tourne 90° à droite

        if self.control["haut"]: #si touche assignée à "haut" pressée
            self.mouvement = True
            if not self.control["gauche"] and not self.control["droite"] and not self.control["bas"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH()) #perso tourne dans le même sens que la caméra
                if self.distance > 29.9 : #camera avance avec le perso si elle n'est pas trop proche de lui
                    self.camera.setY(self.camera, self.vitesse * dt) 
                
        if self.control["bas"]: #si touche assignée à "bas" pressée
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

        #saut
        if self.control["saut"]: #si touche assignée à "saut" pressée
            if self.grav.isOnGround() == True: #si le perso est sur le sol
                self.saut = True
                
        if self.saut == True:
            if self.grav.getVelocity() < 0.4: #si la vitesse verticale est inférieure à 0.4
                self.grav.setVelocity(self.grav.getVelocity() + 0.03) #augmenter la vitesse
            else:
                self.saut = False
        else:
            if self.grav.isOnGround() == False: #si le perso n'est pas sur le sol
                self.grav.setVelocity(self.grav.getVelocity() - 0.03) #diminuer la vitesse
            else:
                self.perso.setFluidZ(self.perso, -0.5) #diminuer la hauteur du perso constamment (gravité)
                
        self.perso.setFluidZ(self.perso, 0.1 + self.grav.getVelocity()) #change la hauteur du perso en fonction de la vitesse verticale

        #sprint
        if self.control["sprint"]: #si touche assignée à "sprint" pressée
            self.speedcap = 30
        else : 
            self.speedcap = 15

        #acceleration
        if self.mouvement == True: #si le perso est censé bouger
            if self.vitesse < self.speedcap :
                self.vitesse = self.vitesse + 0.5
            else : 
                self.vitesse = self.vitesse - 0.5
        else :
            if self.vitesse > 0:
                self.vitesse = self.vitesse - 0.5
        
        self.perso.setY(self.perso, self.vitesse * dt) #le perso avance selon son orientation


        #caméra 
        if self.control_camera["camera_haut"] and self.camera.getZ() < self.perso.getZ() + 14 : #on limite la hauteur du mouvement de la caméra si touche assignée à "camera_haut" pressée
            '''and self.mouvement == False : #aurait empêché la changement de la hauteur de la caméra si le perso bouge''' 
            self.camera.setFluidZ(self.camera, 1)
            self.mouvement_cam = True

        if self.control_camera["camera_bas"] and self.camera.getZ() > self.perso.getZ() - 4.5 : #on limite la hauteur du mouvement de la caméra si touche assignée à "camera_bas" pressée
            '''and self.mouvement == False : #aurait empêché la changement de la hauteur de la caméra si le perso bouge''' 
            self.camera.setFluidZ(self.camera, -1)
            self.mouvement_cam = True

        if self.control_camera["camera_gauche"] and self.distance < 40 : #si touche assignée à "camera_gauche" pressée et si la distance entre camera et perso n'est pas trop grande
            self.camera.setFluidX(self.camera, -1.5) #la caméra bouge vers sa propre gauche
                
        if self.control_camera["camera_droite"] and self.distance < 40 : #si touche assignée à "camera_droite" pressée et si la distance entre camera et perso n'est pas trop grande
            self.camera.setFluidX(self.camera, 1.5) #la caméra bouge vers sa propre droite
            
        if self.control_camera["reset_camera"] and self.reset_cam == False : #remet la caméra à sa place
            self.camera.setPos(self.perso.getPos()) #téléporte la caméra sur le perso
            self.camera.setH(self.perso, 0) #donne à la caméra la même orientation qu'au perso
            self.camera.setFluidY(self.camera, - 30) #recule la caméra derrière le perso
            self.reset_cam = True

        if self.reset_cam == True :
            self.reset_cam_counter = self.reset_cam_counter + 1 #compteur avant le prochain reset de la caméra possible
            if self.reset_cam_counter == 60 : #60 pour 1 seconde
                self.reset_cam_counter = 0 #on remet le compteur à 0
                self.reset_cam = False 

        '''if self.mouvement == True and self.mouvement_cam == False : #remet la caméra à sa hauteur initiale si le personnage bouge et qu'elle n'est pas utilisée
            if self.camera.getZ() > self.perso.getZ() + 5.5 :
                self.camera.setFluidZ(self.camera, -0.1)
            elif self.camera.getZ() < self.perso.getZ() + 4.5 :
                self.camera.setFluidZ(self.camera, 0.1)'''

        if self.distance < 29.5 : #empêche la caméra d'être trop proche du personnage
            self.camera.setFluidY(self.camera, -0.1) 
            if self.distance < 10 :
                self.perso.hide() #rend le perso invisible si la caméra est trop proche
            else:
                self.perso.show() #rend le perso à nouveau visible si la caméra est assez loin

        elif self.distance > 35 : #empêche la caméra d'être trop loin du personnage
            self.camera.setFluidY(self.camera, 0.5) 

        if self.camera.getZ() > self.perso.getZ() + 15 : #empêche la caméra d'être trop haute par rapport au perso
            self.camera.setFluidZ(self.camera, -0.135)

        elif not self.control_camera["camera_bas"] and self.camera.getZ() < self.perso.getZ() + 5 : #empêche la caméra d'être trop basse par rapport au perso
            self.camera.setFluidZ(self.camera, 0.05)


        self.distance = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2 + (self.perso.getZ() - self.camera.getZ())**2) #distance entre caméra et personnage
        self.camera.lookAt(self.perso) #caméra regarde vers le perso
        self.mouvement = False


        

        print(self.grav.isOnGround())
        print(self.grav.getVelocity())

        return task.cont
       

Game = Pynard()
Game.run()