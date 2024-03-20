from direct.showbase.ShowBase import ShowBase #Bibliothèque permettant de créer la fenêtre Panda3D
from panda3d.core import * #Bibliothèque permettant de gérer les éléments sdu jeu
from math import *

class Pynard(ShowBase):

    def __init__(self): #Initialisation
        ShowBase.__init__(self)

        # Configuration de la fenêtre
        props = WindowProperties()
            #Nom de la fenêtre
        props.setTitle("Test dash")
            #Taille de la fenêtre
        props.setSize(1200,650)
            #Position de la fenêtre
        props.setOrigin(100,100)
            #Gestion souris
        props.setCursorHidden(True) #Affichage de la souris
        self.disableMouse() #Gestion caméra libre avec souris
        #Appliquer les proprétés
        self.win.requestProperties(props)

#Propriétés de collision 
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.grav = CollisionHandlerGravity()
        base.cTrav.setRespectPrevTransform(True)

#Gestion objets (modèle + collision)
    # Village vide
        #Modèle
        self.maptest = self.loader.loadModel("../models/maps/Village de départ.glb", noCache=True) #Importation
        self.maptest.reparentTo(self.render) #Charger le modèle
        self.maptest.setPos(0,0,0) #Posistion du modèle

        #Collisions
        colliderNode_sol = CollisionNode("sol") #crée une collision
        colliderNode_sol.addSolid(CollisionBox(0, 150, 170, 10)) #ajoute un solide à la collision
        collider_sol = self.maptest.attachNewNode(colliderNode_sol) #attache la collision à l'objet
        collider_sol.setPos(0, 0, -9) #ajuste la position de la collision
        collider_sol.show() #rend la collision visible

        colliderNode_mur1 = CollisionNode("mur1")
        colliderNode_mur1.addSolid(CollisionBox(0, 1, 170, 20))
        collider_mur1 = self.maptest.attachNewNode(colliderNode_mur1)
        collider_mur1.setPos(150, 0, 20)
        collider_mur1.show()

        colliderNode_mur2 = CollisionNode("mur2")
        colliderNode_mur2.addSolid(CollisionBox(0, 1, 170, 20))
        collider_mur2 = self.maptest.attachNewNode(colliderNode_mur2)
        collider_mur2.setPos(-150, 0, 20)
        collider_mur2.show()

        colliderNode_mur3 = CollisionNode("mur3")
        colliderNode_mur3.addSolid(CollisionBox(0, 170, 1, 20))
        collider_mur3 = self.maptest.attachNewNode(colliderNode_mur3)
        collider_mur3.setPos(0, 170, 20)
        collider_mur3.show()

        colliderNode_mur4 = CollisionNode("mur4")
        colliderNode_mur4.addSolid(CollisionBox(0, 160, 1, 20))
        collider_mur4 = self.maptest.attachNewNode(colliderNode_mur4)
        collider_mur4.setPos(0, -170, 20)
        collider_mur4.show()

    #Plateformes
        #Collisions
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
    
    #Arbre1
        #Modèle
        self.arbre1 = self.loader.loadModel("../models/obj/arbre1.glb", noCache=True) #modèle du perso
        self.arbre1.setScale(0.5)
        self.arbre1.reparentTo(self.render)
        self.arbre1.setPos(15, 32, 0)
        self.arbre1.setH(0)

        #Collisions
        colliderNode_arbre1 = CollisionNode("arbre1")
        colliderNode_arbre1.addSolid(CollisionBox(0, 4, 3.8, 20))
        collider_arbre1 = self.maptest.attachNewNode(colliderNode_arbre1)
        collider_arbre1.setPos(self.arbre1.getX()-2.5, self.arbre1.getY()+1, -1)
        collider_arbre1.show()

    #Arbre2
        #Modèle
        self.arbre2 = self.loader.loadModel("../models/obj/arbre2.glb", noCache=True) #modèle du perso
        self.arbre2.setScale(2.5)
        self.arbre2.reparentTo(self.render)
        self.arbre2.setPos(36, 24, 0)
        self.arbre2.setH(0)

        #Collisions
        colliderNode_arbre2 = CollisionNode("arbre2")
        colliderNode_arbre2.addSolid(CollisionBox(0, 4, 3.8, 20))
        collider_arbre2 = self.maptest.attachNewNode(colliderNode_arbre2)
        collider_arbre2.setPos(self.arbre2.getX()-2.5, self.arbre2.getY()+1, -1)
        collider_arbre2.show()

    #Arbre3
        #Modèle
        self.arbre3 = self.loader.loadModel("../models/obj/arbre2.glb", noCache=True) #modèle du perso
        self.arbre3.setScale(2.9)
        self.arbre3.reparentTo(self.render)
        self.arbre3.setPos(120, 115, -0.4)
        self.arbre3.setH(26)

        #Collisions
        colliderNode_arbre3 = CollisionNode("arbre3")
        colliderNode_arbre3.addSolid(CollisionBox(0, 4, 3.8, 20))
        collider_arbre3 = self.maptest.attachNewNode(colliderNode_arbre3)
        collider_arbre3.setPos(self.arbre3.getX()-3, self.arbre3.getY()+1, -1)
        collider_arbre3.setH(26)
        collider_arbre3.show()

    #Maison
        #Modèle
        self.maison1 = self.loader.loadModel("../models/obj/maison.glb", noCache=True) #modèle du perso
        self.maison1.setScale(2)
        self.maison1.reparentTo(self.render)
        self.maison1.setPos(22, -75, -0.4)
        self.maison1.setH(90)

        #Collisions
        colliderNode_maison1 = CollisionNode("maison")
        colliderNode_maison1.addSolid(CollisionBox(0, 15, 15, 20))
        collider_maison1 = self.maptest.attachNewNode(colliderNode_maison1)
        collider_maison1.setPos(self.maison1.getX(), self.maison1.getY(), -1)
        collider_maison1.setH(0)
        collider_maison1.show()

        colliderNode_balcon = CollisionNode("balcon")
        colliderNode_balcon.addSolid(CollisionBox(0, 7, 3, 1.7))
        collider_balcon = self.maptest.attachNewNode(colliderNode_balcon)
        collider_balcon.setPos(self.maison1.getX()-3.8, self.maison1.getY()+18, 10.5)
        collider_balcon.setH(0)
        collider_balcon.show()

    #Maison2
        #Modèle
        self.maison2 = self.loader.loadModel("../models/obj/maison2.glb", noCache=True) #modèle du perso
        self.maison2.setScale(2)
        self.maison2.reparentTo(self.render)
        self.maison2.setPos(-32, 57, -0.4)
        self.maison2.setH(90)

        #Collisions
        colliderNode_maison2 = CollisionNode("maison2")
        colliderNode_maison2.addSolid(CollisionBox(0, 15, 15, 20))
        collider_maison2 = self.maptest.attachNewNode(colliderNode_maison2)
        collider_maison2.setPos(self.maison2.getX(), self.maison2.getY(), -1)
        collider_maison2.setH(0)
        collider_maison2.show()

        colliderNode_balcon2 = CollisionNode("balcon2")
        colliderNode_balcon2.addSolid(CollisionBox(0, 7, 3, 1.7))
        collider_balcon2 = self.maptest.attachNewNode(colliderNode_balcon2)
        collider_balcon2.setPos(self.maison2.getX()-3.8, self.maison2.getY()+18, 10.5)
        collider_balcon2.setH(0)
        collider_balcon2.show()

    #Garage1
        #Modèle
        self.garage1 = self.loader.loadModel("../models/obj/garage.glb", noCache=True) #modèle du perso
        self.garage1.setScale(2.5)
        self.garage1.reparentTo(self.render)
        self.garage1.setPos(57, -139, -0.4)
        self.garage1.setH(20+90)

        #Collisions
        colliderNode_garage1 = CollisionNode("garage1")
        colliderNode_garage1.addSolid(CollisionBox(0, 13, 13, 13.2))
        collider_garage1 = self.maptest.attachNewNode(colliderNode_garage1)
        collider_garage1.setPos(self.garage1.getX(), self.garage1.getY(), -1)
        collider_garage1.setH(20+90)
        collider_garage1.show()

    #Garage2
        #Modèle
        self.garage2 = self.loader.loadModel("../models/obj/garage.glb", noCache=True) #modèle du perso
        self.garage2.setScale(2.5)
        self.garage2.reparentTo(self.render)
        self.garage2.setPos(-69, 135, -0.4)
        self.garage2.setH(90)

        #Collisions
        colliderNode_garage2 = CollisionNode("garage2")
        colliderNode_garage2.addSolid(CollisionBox(0, 13, 13, 13.2))
        collider_garage2 = self.maptest.attachNewNode(colliderNode_garage2)
        collider_garage2.setPos(self.garage2.getX(), self.garage2.getY(), -1)
        collider_garage2.setH(90)
        collider_garage2.show()

    #Banc
        #Modèle
        self.banc1 = self.loader.loadModel("../models/obj/banc.glb", noCache=True) #modèle du perso
        self.banc1.setScale(3.2)
        self.banc1.reparentTo(self.render)
        self.banc1.setPos(119, -41, -0.4)
        self.banc1.setH(0)

        #Collisions
        colliderNode_banc1 = CollisionNode("banc")
        colliderNode_banc1.addSolid(CollisionBox(0, 3, 6.2, 4.3))
        collider_banc1 = self.maptest.attachNewNode(colliderNode_banc1)
        collider_banc1.setPos(self.banc1.getX(), self.banc1.getY(), -1)
        collider_banc1.setH(0)
        collider_banc1.show()

        colliderNode_haut_banc1 = CollisionNode("haut_banc1")
        colliderNode_haut_banc1.addSolid(CollisionBox(0, 1, 6.2, 7.5))
        collider_haut_banc1 = self.maptest.attachNewNode(colliderNode_haut_banc1)
        collider_haut_banc1.setPos(self.banc1.getX()-2, self.banc1.getY(), -1)
        collider_haut_banc1.setH(0)
        collider_haut_banc1.show()

    #Banc2
        #Modèle
        self.banc2 = self.loader.loadModel("../models/obj/banc.glb", noCache=True) #modèle du perso
        self.banc2.setScale(3.2)
        self.banc2.reparentTo(self.render)
        self.banc2.setPos(119, 10, -0.4)
        self.banc2.setH(0)

        #Collisions
        colliderNode_banc2 = CollisionNode("banc2")
        colliderNode_banc2.addSolid(CollisionBox(0, 3, 6.2, 4.3))
        collider_banc2 = self.maptest.attachNewNode(colliderNode_banc2)
        collider_banc2.setPos(self.banc2.getX(), self.banc2.getY(), -1)
        collider_banc2.setH(0)
        collider_banc2.show()

        colliderNode_haut_banc2 = CollisionNode("haut_banc2")
        colliderNode_haut_banc2.addSolid(CollisionBox(0, 1, 6.2, 7.5))
        collider_haut_banc2 = self.maptest.attachNewNode(colliderNode_haut_banc2)
        collider_haut_banc2.setPos(self.banc2.getX()-2, self.banc2.getY(), -1)
        collider_haut_banc2.setH(0)
        collider_haut_banc2.show()

    #Banc3
        #Modèle
        self.banc3 = self.loader.loadModel("../models/obj/banc.glb", noCache=True) #modèle du perso
        self.banc3.setScale(3.2)
        self.banc3.reparentTo(self.render)
        self.banc3.setPos(119, 61, -0.4)
        self.banc3.setH(0)

        #Collisions
        colliderNode_banc3 = CollisionNode("banc3")
        colliderNode_banc3.addSolid(CollisionBox(0, 3, 6.2, 4.3))
        collider_banc3 = self.maptest.attachNewNode(colliderNode_banc3)
        collider_banc3.setPos(self.banc3.getX(), self.banc3.getY(), -1)
        collider_banc3.setH(0)
        collider_banc3.show()

        colliderNode_haut_banc3 = CollisionNode("haut_banc3")
        colliderNode_haut_banc3.addSolid(CollisionBox(0, 1, 6.2, 7.5))
        collider_haut_banc3 = self.maptest.attachNewNode(colliderNode_haut_banc3)
        collider_haut_banc3.setPos(self.banc3.getX()-2, self.banc3.getY(), -1)
        collider_haut_banc3.setH(0)
        collider_haut_banc3.show()

    #Voitures
        #Modèle1
        self.voiture1 = self.loader.loadModel("../models/obj/voiture.glb", noCache=True) #modèle du perso
        self.voiture1.setScale(2)
        self.voiture1.reparentTo(self.render)
        self.voiture1.setPos(88, -129, 1.2)
        self.voiture1.setH(100)

        #Collisions1
        colliderNode_voiture1 = CollisionNode("garage1")
        colliderNode_voiture1.addSolid(CollisionBox(0, 3.8, 5.8, 6))
        collider_voiture1 = self.maptest.attachNewNode(colliderNode_voiture1)
        collider_voiture1.setPos(self.voiture1.getX()+1.2, self.voiture1.getY()+0.2, -1)
        collider_voiture1.setH(100)
        collider_voiture1.show()

    #Barrières
        #Modèle
        self.barriere1 = self.loader.loadModel("../models/obj/barriere8.glb", noCache=True) #modèle du perso
        self.barriere1.setScale(2.8)
        self.barriere1.reparentTo(self.render)
        self.barriere1.setPos(-16, -90, 0.2)
        self.barriere1.setH(90)

        #Collisions
        colliderNode_barriere1 = CollisionNode("barriere8")
        colliderNode_barriere1.addSolid(CollisionBox(0, 70, 1, 9))
        collider_barriere1 = self.maptest.attachNewNode(colliderNode_barriere1)
        collider_barriere1.setPos(self.barriere1.getX()+0.2, self.barriere1.getY(), -1)
        collider_barriere1.setH(90)
        collider_barriere1.show()

        #Modèle2
        self.barriere2 = self.loader.loadModel("../models/obj/barriere3.glb", noCache=True) #modèle du perso
        self.barriere2.setScale(2.8)
        self.barriere2.reparentTo(self.render)
        self.barriere2.setPos(13, -158, 0.2)
        self.barriere2.setH(0)

        #Collisions2
        colliderNode_barriere2 = CollisionNode("barriere3")
        colliderNode_barriere2.addSolid(CollisionBox(0, 27, 1, 9))
        collider_barriere2 = self.maptest.attachNewNode(colliderNode_barriere2)
        collider_barriere2.setPos(self.barriere2.getX()+0.2, self.barriere2.getY(), -1)
        collider_barriere2.setH(0)
        collider_barriere2.show()

        #Modèle3
        self.barriere3 = self.loader.loadModel("../models/obj/barriere3.glb", noCache=True) #modèle du perso
        self.barriere3.setScale(2.8)
        self.barriere3.reparentTo(self.render)
        self.barriere3.setPos(35, -118, 0.2)
        self.barriere3.setH(100)

        #Collisions3
        colliderNode_barriere3 = CollisionNode("barriere3")
        colliderNode_barriere3.addSolid(CollisionBox(0, 27, 1, 9))
        collider_barriere3 = self.maptest.attachNewNode(colliderNode_barriere3)
        collider_barriere3.setPos(self.barriere3.getX()+0.2, self.barriere3.getY(), -1)
        collider_barriere3.setH(100)
        collider_barriere3.show()

        #Modèle4
        self.barriere4 = self.loader.loadModel("../models/obj/barriere3.glb", noCache=True) #modèle du perso
        self.barriere4.setScale(2.8)
        self.barriere4.reparentTo(self.render)
        self.barriere4.setPos(30, -33, 0.2)
        self.barriere4.setH(90)

        #Collisions4
        colliderNode_barriere4 = CollisionNode("barriere3")
        colliderNode_barriere4.addSolid(CollisionBox(0, 27, 1, 9))
        collider_barriere4 = self.maptest.attachNewNode(colliderNode_barriere4)
        collider_barriere4.setPos(self.barriere4.getX()+0.2, self.barriere4.getY(), -1)
        collider_barriere4.setH(90)
        collider_barriere4.show()

        #Modèle5
        self.barriere5 = self.loader.loadModel("../models/obj/barriere3.glb", noCache=True) #modèle du perso
        self.barriere5.setScale(2.8)
        self.barriere5.reparentTo(self.render)
        self.barriere5.setPos(6, -12, 0.2)
        self.barriere5.setH(14)

        #Collisions5
        colliderNode_barriere5 = CollisionNode("barriere3")
        colliderNode_barriere5.addSolid(CollisionBox(0, 27, 1, 9))
        collider_barriere5 = self.maptest.attachNewNode(colliderNode_barriere5)
        collider_barriere5.setPos(self.barriere5.getX()+0.2, self.barriere5.getY(), -1)
        collider_barriere5.setH(14)
        collider_barriere5.show()

        #Modèle6
        self.barriere6 = self.loader.loadModel("../models/obj/barriere8.glb", noCache=True) #modèle du perso
        self.barriere6.setScale(2.8)
        self.barriere6.reparentTo(self.render)
        self.barriere6.setPos(-77, 68, 0.2)
        self.barriere6.setH(90)

        #Collisions6
        colliderNode_barriere6 = CollisionNode("barriere8")
        colliderNode_barriere6.addSolid(CollisionBox(0, 70, 1, 9))
        collider_barriere6 = self.maptest.attachNewNode(colliderNode_barriere6)
        collider_barriere6.setPos(self.barriere6.getX()+0.2, self.barriere6.getY(), -1)
        collider_barriere6.setH(90)
        collider_barriere6.show()

        #Modèle7
        self.barriere7 = self.loader.loadModel("../models/obj/barriere3.glb", noCache=True) #modèle du perso
        self.barriere7.setScale(2.8)
        self.barriere7.reparentTo(self.render)
        self.barriere7.setPos(12, 100, 0.2)
        self.barriere7.setH(90)

        #Collisions7
        colliderNode_barriere7 = CollisionNode("barriere3")
        colliderNode_barriere7.addSolid(CollisionBox(0, 27, 1, 9))
        collider_barriere7 = self.maptest.attachNewNode(colliderNode_barriere7)
        collider_barriere7.setPos(self.barriere7.getX()+0.2, self.barriere7.getY(), -1)
        collider_barriere7.setH(90)
        collider_barriere7.show()

        #Modèle8
        self.barriere8 = self.loader.loadModel("../models/obj/barriere3.glb", noCache=True) #modèle du perso
        self.barriere8.setScale(2.8)
        self.barriere8.reparentTo(self.render)
        self.barriere8.setPos(-50, -2, 0.2)
        self.barriere8.setH(0)

        #Collisions8
        colliderNode_barriere8 = CollisionNode("barriere3")
        colliderNode_barriere8.addSolid(CollisionBox(0, 27, 1, 9))
        collider_barriere8 = self.maptest.attachNewNode(colliderNode_barriere8)
        collider_barriere8.setPos(self.barriere8.getX()+0.2, self.barriere8.getY(), -1)
        collider_barriere8.setH(0)
        collider_barriere8.show()
    
    #Personnage
        #Modèle
        self.perso = self.loader.loadModel("../models/chars/canard.glb", noCache=True) #modèle du perso
        self.perso.reparentTo(self.render)
        self.perso.setPos(-100, 0, 10)
        self.perso.setH(0)

        #Collisions
        colliderNode = CollisionNode("perso")
        colliderNode.addSolid(CollisionBox(0, 2, 2, 2))
        collider = self.perso.attachNewNode(colliderNode)
        collider.setPos(0,0,2.5)
        collider.show()

        colliderNode2 = CollisionNode("perso2")
        colliderNode2.addSolid(CollisionBox(0, 0.5, 0.5, 0.01))
        collider2 = self.perso.attachNewNode(colliderNode2)
        collider2.setPos(0,0,0)
        collider2.show()

        #Gestion collisions
        self.pusher.addCollider(collider, self.perso)
        self.cTrav.addCollider(collider, self.pusher)
        self.grav.addCollider(collider2, self.perso)
        self.cTrav.addCollider(collider2, self.grav)
        
    #Ennemi 
        #Modèle
        self.ennemi = self.loader.loadModel("../models/chars/grenouille.glb", noCache=True) #modèle du perso
        self.ennemi.setScale(0.5)
        self.ennemi.reparentTo(self.render)
        self.ennemi.setPos(10, 0, 0)

        #Collisions
        colliderNode_ennemi = CollisionNode("ennemi")
        colliderNode_ennemi.addSolid(CollisionBox(0, 5, 5, 4))
        collider_ennemi = self.ennemi.attachNewNode(colliderNode_ennemi)
        collider_ennemi.setPos(0,2,4)
        collider_ennemi.show()

        #Gestion collisions
        self.pusher.addCollider(collider_ennemi, self.ennemi)
        self.cTrav.addCollider(collider_ennemi, self.pusher)

#Gestion Caméra
    #Creation de l'entité caméra
        self.camera.reparentTo(self.render)
        self.camera.setPos(30, 0, 14)
        self.camera.setH(0)
    #Gestion des collisions de la caméra
        colliderNode_camera = CollisionNode("camera")
        colliderNode_camera.addSolid(CollisionBox(0, 1, 1, 2))
        collider_camera = self.camera.attachNewNode(colliderNode_camera)
        collider_camera.setPos(0,0,1)
        self.pusher.addCollider(collider_camera, self.camera)
        self.cTrav.addCollider(collider_camera, self.pusher)

#Initialisation des variables   
        self.vitesse = 0 #vitesse du perso
        self.speedcap = 25 #limite de vitesse du perso
        self.distance = 50 #distance entre caméra et personnage
        self.distance_horizontale = 50 #distance horizontale entre caméra et perso
        self.mouvement = False #si le perso bouge
        self.gauche = False
        self.droite = False
        self.haut = False
        self.bas = False
        self.demi_tour = False
        self.mouvement_cam = False #si la caméra monte ou descent
        self.reset_cam = False #si la caméra se reset
        self.stop_reset_cam = False #la caméra ne peut pas se reset
        self.reset_cam_counter = 0 #compteur avant de pouvoir reset la caméra
        self.saut = False #si le perso est en plein saut
        self.double_saut = False #si le perso fait un double saut
        self.airdash = False #si le perso est en plein dash aérien
        self.airdash_stop = False #si le perso ne peut pas faire de dash aérien
        self.airdash_cooldown = 0 #temps d'attente avant un autre dash aérien
        self.gravité = 0.03 #acceleration verticale du perso
        self.acceleration = 1 #acceleration du perso
        self.points_de_vie = 3 #points de vie du perso
        self.attaque_ennemi = True #si l'ennemi
        self.ennemi_charge = 0 #temps d'attaque de l'ennemi
        self.invincibilite = 0 #temps de clignotement du perso
        self.invincibilite_compteur = 0 #temps d'invincibilité
        self.prise_de_degats = False #prise de dégat du perso

        #controles PERSO
        self.control = { #dictionnaire des variables utilisées pour les inputs du perso
            "haut": False,
            "bas": False,
            "gauche": False,
            "droite": False,
            "saut": False,
            "dash": False
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

        self.accept("shift", self.etat_touche, ["dash", True]) #variable qui devient vraie si la touche est pressée
        self.accept("shift-up", self.etat_touche, ["dash", False]) #variable qui devient fausse si la touche est relachée

        #controles CAMERA
        self.control_camera = { #dictionnaire des variables utilisées pour les inputs de la caméra
            "camera_haut": False,
            "camera_bas": False,
            "camera_gauche": False,
            "camera_droite": False,
            "reset_camera": False
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
        
    #Perso
        #4 directions
        if self.control["gauche"]: #si touche assignée à "gauche" pressée
            self.perso.setH(self.camera.getH() + 90) #perso tourne 90° à gauche
            if self.droite == True: #si le perso allait vers la droite
                self.demi_tour = True #le perso fait un demi-tour
            else:
                self.gauche = True #le perso va vers la gauche
                self.demi_tour = False #le perso arrête de faire un demi-tour
                self.mouvement = True #le perso est en mouvement
                     
        elif self.control["droite"]: #si touche assignée à "droite" pressée
            self.perso.setH(self.camera.getH() - 90) #perso tourne 90° à droite
            if self.gauche == True: #si le perso allait vers la gauche
                self.demi_tour = True #le perso fait un demi-tour 
            else:
                self.droite = True #le perso va vers la droite
                self.demi_tour = False #le perso arrête de faire un demi-tour
                self.mouvement = True #le perso est en mouvement

        elif self.control["haut"]: #si touche assignée à "haut" pressée  
            self.perso.setH(self.camera.getH()) #perso tourne dans le même sens que la caméra
            if self.bas == True: #si le perso allait vers l'arrière
                self.demi_tour = True #le perso fait un demi-tour
            else:
                self.haut = True #le perso va vers l'avant
                self.demi_tour = False #le perso arrête de faire un demi-tour
                self.mouvement = True #le perso est en mouvement
                
        elif self.control["bas"]: #si touche assignée à "bas" pressée
            self.perso.setH(self.camera.getH() + 180) #perso regarde la caméra
            if self.haut == True: #si le perso allait vers l'avant
                self.demi_tour = True #le perso fait un demi-tour
            else:
                self.bas = True #le perso va vers l'arrière
                self.demi_tour = False #le perso arrête de faire un demi-tour
                self.mouvement = True #le perso est en mouvement

        #8 directions:
        if self.control["haut"] and self.control["gauche"]: #si avant et gauche pressés
            self.perso.setH(self.camera.getH() + 45) #le perso s'oriente vers l'avant-gauche
            if self.droite == True and self.bas == True: #si le perso allait vers l'arrière-droit
                self.demi_tour = True #le perso fait un demi-tour
            else:
                self.gauche = True #le perso va à gauche
                self.haut = True #et vers l'avant
                self.mouvement = True #le perso est en mouvement
                self.demi_tour = False #le perso arrête de faire un demi-tour

        elif self.control["haut"] and self.control["droite"]: #si avant et droite pressés
            self.perso.setH(self.camera.getH() - 45) #le perso s'oriente vers l'avant-droit
            if self.gauche == True and self.bas == True: #si le perso allait vers l'arrière-gauche
                self.demi_tour = True #le perso fait un demi-tour
            else:
                self.droite = True #le perso va à gauche
                self.haut = True #et vers l'avant
                self.mouvement = True #le perso est en mouvement
                self.demi_tour = False #le perso arrête de faire un demi-tour
        
        elif self.control["bas"] and self.control["gauche"]: #si arrière et gauche pressés
            self.perso.setH(self.camera.getH() + 135) #le perso s'oriente vers l'arrière-gauche
            if self.droite == True and self.haut == True: #si le perso allait vers l'avant-droit
                self.demi_tour = True #le perso fait un demi-tour
            else:
                self.gauche = True #le perso va vers la gauche
                self.bas = True #et vers l'arrière
                self.mouvement = True #le perso est en mouvement
                self.demi_tour = False #le perso arrête de faire un demi-tour
             
        elif self.control["bas"] and self.control["droite"]: #si arrière et droite pressés
            self.perso.setH(self.camera.getH() - 135) #le perso s'oriente vers l'arrière-droit
            if self.gauche == True and self.haut == True: #si le perso allait vers l'avant-gauche
                self.demi_tour = True #le perso fait un demi-tour
            else:
                self.droite = True #le perso va vers la droite
                self.bas = True #et vers l'arrière
                self.mouvement = True #le perso est en mouvement
                self.demi_tour = False #le perso arrête de faire un demi-tour

        #saut
        if self.control["saut"]: #si touche assignée à "saut" pressée
            if self.grav.isOnGround() == True: #si le perso est sur le sol
                self.saut = True #le perso saute
                self.double_saut = True #le perso ne fait pas un double saut
            
            #double saut 
            else:
                if self.grav.getVelocity() < 0: #si le perso est en train de tomber
                    if self.double_saut == True: #si le perso peut faire un double saut
                        self.grav.setVelocity(0.5) #la hauteur du perso monte
                        self.double_saut = False #le perso a déjà fait un double saut

        if self.saut == True: #le perso saute
            if self.grav.getVelocity() < 0.4: #si la vitesse verticale est inférieure à 0.4
                self.grav.setVelocity(self.grav.getVelocity() + self.gravité) #augmenter la vitesse
            else:
                self.saut = False #le perso ne saute plus
        else:
            if self.grav.isOnGround() == False: #si le perso n'est pas sur le sol
                if self.grav.getVelocity() > - 0.5: #si la vitesse de chute du perso est supérieure à - 0.5
                    self.grav.setVelocity(self.grav.getVelocity() - self.gravité) #diminuer la vitesse
            else:
                self.perso.setFluidZ(self.perso, -0.5) #diminuer la hauteur du perso constamment (gravité)
                
        self.perso.setFluidZ(self.perso, 0.1 + self.grav.getVelocity()) #change la hauteur du perso en fonction de la vitesse verticale

        #dash
        if self.grav.isOnGround() == True: #si le perso est sur le sol
            self.airdash = False #le perso n'est plus en airdash
        if self.control["dash"]: #si touche assignée à "dash" pressée
            self.vitesse = 50 #augmente la vitesse
            self.speedcap = 50 #augmente la vitesse max
            if self.grav.isOnGround() == False: #si le perso n'est pas sur le son
                self.airdash = True #le perso fait un dash aérien

        #acceleration
        else:
            if self.speedcap > 25: #si le dash est activé
                self.speedcap = self.speedcap - 0.1 #diminue la vitesse max
            if self.mouvement == True: #si le perso est censé bouger
                if self.vitesse < self.speedcap: #si la vitesse est inférieure au maximum
                    if self.saut == False: #le perso n'accelère pas dans les airs
                        self.vitesse = self.vitesse + self.acceleration #augmente la vitesse petit à petit
                else: #si la vitesse dépasse le maximum
                    self.vitesse = self.vitesse - self.acceleration #diminue la vitesse petit à petit
            else: #si aucune touche de mouvement n'est pressée
                if self.grav.isOnGround() == True: #si le perso est sur le sol
                    self.vitesse = self.vitesse - self.acceleration*2#diminue la vitesse plus rapidement
                else: 
                    self.vitesse = self.vitesse - self.acceleration/2 #diminue la vitesse aérienne plus lentement
                if self.vitesse < 0: #si la vitesse est négative
                    self.vitesse = 0 #remet la vitesse à 0

            if self.demi_tour == False:
                self.perso.setFluidY(self.perso, self.vitesse * dt) #le perso avance selon son orientation
            else:
                self.perso.setFluidY(self.perso, - self.vitesse * dt)
                if self.vitesse < 5:
                    self.haut = False
                    self.bas = False
                    self.gauche = False
                    self.droite = False
                    self.demi_tour = False

    #caméra 
        if self.control_camera["camera_haut"]:
            if self.camera.getZ() < self.perso.getZ() + 14.5: #on limite la hauteur du mouvement de la caméra si touche assignée à "camera_haut" pressée
                self.camera.setFluidZ(self.camera, 1) #monte la caméra
                self.mouvement_cam = True #la caméra est en mouvement
            else:
                self.mouvement_cam = False #la caméra n'est pas en mouvement

        elif self.control_camera["camera_bas"]:
            if self.camera.getZ() > self.perso.getZ() - 4.5: #on limite la hauteur du mouvement de la caméra si touche assignée à "camera_bas" pressée
                self.camera.setFluidZ(self.camera, -1) #baisse la caméra
                self.mouvement_cam = True #la caméra est en mouvement
            else:
                self.mouvement_cam = False #la caméra n'est pas en mouvement
                
        else:
                self.mouvement_cam = False #la caméra n'est pas en mouvement

        if self.control_camera["camera_gauche"]: #si touche assignée à "camera_gauche" pressée 
            if self.distance < 55: #si la distance entre camera et perso n'est pas trop grande
                self.camera.setFluidX(self.camera, -1.5) #la caméra bouge vers sa propre gauche
            
        elif self.control_camera["camera_droite"]: #si touche assignée à "camera_droite" pressée
            if self.distance < 55: #si la distance entre camera et perso n'est pas trop grande
                self.camera.setFluidX(self.camera, 1.5) #la caméra bouge vers sa propre droite

        if self.control_camera["reset_camera"] and self.stop_reset_cam == False: #remet la caméra à sa place si elle le peut
            self.reset_cam = True #la caméra se reset
            self.stop_reset_cam = True #la caméra ne peut plus se reset
        
        if self.reset_cam == True: #si la caméra est en train de se reset
            self.camera.setPos(self.perso.getPos() + 14) #téléporte la caméra sur le perso
            self.camera.setH(self.perso, 0) #donne à la caméra la même orientation qu'au perso
            self.camera.setFluidY(self.camera, - 10) #recule la caméra derrière le perso
            self.reset_cam = False #la caméra a arrêté de se reset
        
        if self.stop_reset_cam == True: #si la caméra nep peut pas se reset
            self.reset_cam_counter = self.reset_cam_counter + 1 #compteur avant le prochain reset de la caméra possible
            if self.reset_cam_counter == 60: #60 pour 1 seconde
                self.reset_cam_counter = 0 #on remet le compteur à 0
                self.stop_reset_cam = False #la caméra peut à nouveau se reset

        if self.distance < 49: #empêche la caméra d'être trop proche du personnage
            self.camera.setP(0) #remet l'orientation de la caméra à 0
            if self.mouvement == False: #si le perso ne bouge pas
                self.camera.setFluidY(self.camera, - 0.3)  #fait reculer la caméra à une vitesse fixée
            else: #si le perso bouge
                self.camera.setFluidY(self.camera, - self.vitesse * dt) #fait reculer la caméra à la vitesse du perso
            self.camera.lookAt(self.perso) #la caméra regarde vers le perso
            if self.distance < 10: #si la distance est trop faible
                self.perso.hide() #rend le perso invisible si la caméra est trop proche
            else:
                self.perso.show() #rend le perso à nouveau visible si la caméra est assez loin

        elif self.distance > 51: #empêche la caméra d'être trop loin du personnage
            self.camera.setP(0) #remet l'orientation de la caméra à 0
            if self.mouvement == False: #si le perso ne bouge pas
                self.camera.setFluidY(self.camera, 0.3) #fait reculer la caméra à une vitesse fixée
            else: #si le perso bouge
                self.camera.setFluidY(self.camera, self.vitesse * dt) #fait avancer la caméra à la vitesse du perso
            self.camera.lookAt(self.perso) #la caméra regarde vers le perso

        if self.distance > 65: #si la caméra est bien trop loin du perso
            self.reset_cam = True #remet la caméra à sa place

        if self.camera.getZ() > self.perso.getZ() + 16: #si la caméra est trop haute par rapport au perso
            self.camera.setFluidZ(self.camera, -0.18) #la caméra descent

        elif self.camera.getZ() < self.perso.getZ() + 5:
            if self.camera.getZ() < self.perso.getZ() - 5: #si la caméra est trop basse par rapport au perso
                self.camera.setFluidZ(self.camera, 0.18) #monte la caméra
    
        self.distance = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2 + (self.perso.getZ() - self.camera.getZ())**2) #distance entre caméra et personnage
        self.distance_horizontale = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2) #distance horizontale entre perso et caméra
        self.camera.lookAt(self.perso) #caméra regarde vers le perso
        self.mouvement = False #le perso n'est plus en mouvement

    #Ennemi
        self.dist_horizontal_perso_ennemi = sqrt((self.perso.getX() - self.ennemi.getX())**2 + (self.perso.getY() - self.ennemi.getY())**2) #distance horizontale entre le perso et l'ennemi
        self.dist_vertical_perso_ennemi = sqrt((self.perso.getZ() - self.ennemi.getZ())**2) #distance verticale entre le perso et l'ennemi

        #attaque le perso
        if self.dist_horizontal_perso_ennemi < 50: #si le perso est assez proche de l'ennemi
            self.ennemi.lookAt(self.perso) #l'ennemi regarde vers le perso
            self.ennemi.setP(0) #remet l'orientation de l'ennemi à 0 (pour éviter qu'il s'incline verticalement)
            if self.dist_horizontal_perso_ennemi > 6: #si l'ennemi ne touche pas le perso
                if self.attaque_ennemi == True: #si l'ennemi peut attaquer le perso
                    self.ennemi.setFluidY(self.ennemi, 0.5) #l'ennemi avance vers le perso
            else: #si l'ennemi touche le perso
                if self.dist_vertical_perso_ennemi < 1: #si l'ennemi et le perso ont à peu près la même hauteur
                    if self.prise_de_degats == False: #si le perso n'est pas déjà en train de prendre des dégâts
                        self.points_de_vie = self.points_de_vie - 1 #le perso perd 1 point de vie
                        self.prise_de_degats = True #le perso est en train de prendre des dégâts
                        self.attaque_ennemi = False #l'ennemi ne peut plus attaquer le perso
            if self.attaque_ennemi == False: #si l'ennemi ne peut plus attaquer le perso
                self.ennemi_charge = self.ennemi_charge + 1 #le temps d'attente pour attaquer à nouveau augmente
                if self.ennemi_charge < 60: #pendant une seconde
                    self.ennemi.setFluidY(self.ennemi, -0.05) #l'ennemi recule lentement
                elif self.ennemi_charge == 120: #après 2 secondes
                    self.ennemi_charge = 0 #le temps d'attente revient à 0
                    self.attaque_ennemi = True #l'ennemi peut à nouveau attaquer

            #invincibilité
            if self.prise_de_degats == True: #si le perso est en train de prendre des dégâts
                self.attaque_ennemi = False #l'ennemi ne peut plus attaquer le perso
                if self.invincibilite_compteur < 3: #compteur du temps d'invincibilité
                    self.invincibilite = self.invincibilite + 1 #le compteur du temps de clignotement du perso augmente
                    if self.invincibilite == 10: #au bout d'1/10 seconde
                        self.perso.hide() #le perso est invisible
                    elif self.invincibilite == 40: #une demi-seconde plus tard
                        self.perso.show() #le perso redevient visible
                        self.invincibilite = 0 #le compteur de clignotement du perso revient à 0
                        self.invincibilite_compteur = self.invincibilite_compteur + 1 #le compteur du temps d'invincibilité augmente
                else:
                    self.invincibilite_compteur = 0 #le compteur du temps d'invincibilité se remet à 0
                    self.prise_de_degats = False #le perso n'est plus en train de prendre des dégâts

            #mort du perso
            if self.points_de_vie == 0: #si le perso n'a plus de points de vie
                self.perso.setPos(-100, 0, 0) #le perso revient à son point d'apparition
                self.reset_cam == True #la caméra revient à son point d'apparition
                self.points_de_vie = 3 #le perso a à nouveau tous ses points de vie
                    
        #saut sur l'ennemi
            if self.ennemi.getZ() + 4 < self.perso.getZ() < self.ennemi.getZ() + 20: #si le perso est au dessus de l'ennemi
                if self.dist_horizontal_perso_ennemi < 5 and self.dist_vertical_perso_ennemi < 5: #si le perso touche l'ennemi par le haut
                    self.ennemi.setPos(50, 50, 0) #téléporte l'ennemi à son point d'apparition
                    self.grav.setVelocity(0.5) #permet au perso de rebondir sur l'ennemi
                    self.airdash = False #le airdash est désactivé si le perso touche l'ennemi
                    self.double_saut = True #permet au perso de faire un double saut

        #attaque téléguidée
                if self.dist_horizontal_perso_ennemi < 20: #si le perso est assez proche de l'ennemi
                    if self.airdash == True and self.airdash_stop == False: #si le perso est en airdash
                        self.perso.lookAt(self.ennemi) #le perso regarde l'ennemi
                        self.perso.setFluidY(self.perso, self.vitesse * dt) #le perso va vers l'ennemi
                        self.perso.setP(0) #remet l'orientation du perso à la normale
                        if self.dist_horizontal_perso_ennemi < 6 and self.dist_vertical_perso_ennemi < 6: #si le perso touche l'ennemi
                            self.airdash_stop = True #le perso ne peut plus faire de dash aérien
        
        if self.airdash_stop == True: #si le perso ne peut plus faire de dash aérien
            self.airdash_cooldown = self.airdash_cooldown + 1 #le compteur avant de pouvoir refaire un dash aérien augmente
            if self.airdash_cooldown == 30: #si le temps est d'une demi seconde
                self.airdash_cooldown = 0 #le compteur revient à 0
                self.airdash_stop = False #le perso peut à nouveau faire un dash aérien

        return task.cont
       
Game = Pynard()
Game.run()