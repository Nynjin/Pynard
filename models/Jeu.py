from direct.showbase.ShowBase import ShowBase #Bibliothèque permettant de créer la fenêtre Panda3D
from panda3d.core import * #Bibliothèque permettant de gérer les éléments sdu jeu
from math import *
# from direct.task import Task
# import gltf #Bibliothèque permettant d'importer des fichiers glb (fichiers 3D)

class ConcatenageStudio(ShowBase):

    def __init__(self): #Initialisation
        ShowBase.__init__(self)

        # Configuration de la fenêtre
        props = WindowProperties()
            #Nom de la fenêtre
        props.setTitle("Projet NSI")
            #Taille de la fenêtre
        props.setSize(1200,650)
            #Position de la fenêtre
        props.setOrigin(100,100)
            #Gestion souris
        props.setCursorHidden(True) #Affichage de la souris
        self.disableMouse() #Gestion caméra libre avec souris
        #Appliquer les proprétés
        self.win.requestProperties(props)
        #Gestion propriétés GLTF
        # gltf.patch_loader(self.loader)

#Propriétés de collision 
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.grav = CollisionHandlerGravity()
        base.cTrav.setRespectPrevTransform(True)

#Gestion objets (modèle + collision)

    # Village vide
        #Modèle
        self.maptest = self.loader.loadModel("maps/Village de départ.glb") #Importation
        self.maptest.reparentTo(self.render) #Charger le modèle
        self.maptest.setPos(0,0,0) #Posistion du modèle

        #Collisions
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

    #Personnage
        #Modèle
        self.perso = self.loader.loadModel("chars/canard.glb") #modèle du perso
        self.perso.setScale(1.9)
        self.perso.reparentTo(self.render)
        self.perso.setPos(0, 0, 0)
        self.perso.setH(0)

        #Collisions
        colliderNode = CollisionNode("perso")
        colliderNode.addSolid(CollisionBox(0, 1.2, 1.2, 0.8))
        collider = self.perso.attachNewNode(colliderNode)
        collider.setPos(0,0,1.2)
        collider.show()
    
    #Arbres
        #Modèle1
        self.arbre1 = self.loader.loadModel("obj/arbre1.glb") #modèle du perso
        self.arbre1.setScale(0.5)
        self.arbre1.reparentTo(self.render)
        self.arbre1.setPos(15, 32, 0)
        self.arbre1.setH(0)

        #Collisions1
        colliderNode_arbre1 = CollisionNode("arbre1")
        colliderNode_arbre1.addSolid(CollisionBox(0, 4, 3.8, 20))
        collider_arbre1 = self.maptest.attachNewNode(colliderNode_arbre1)
        collider_arbre1.setPos(self.arbre1.getX()-2.5, self.arbre1.getY()+1, -1)
        collider_arbre1.show()


        #Modèle2
        self.arbre2 = self.loader.loadModel("obj/arbre2.glb") #modèle du perso
        self.arbre2.setScale(2.5)
        self.arbre2.reparentTo(self.render)
        self.arbre2.setPos(36, 24, 0)
        self.arbre2.setH(0)

        #Collisions2
        colliderNode_arbre2 = CollisionNode("arbre2")
        colliderNode_arbre2.addSolid(CollisionBox(0, 4, 3.8, 20))
        collider_arbre2 = self.maptest.attachNewNode(colliderNode_arbre2)
        collider_arbre2.setPos(self.arbre2.getX()-2.5, self.arbre2.getY()+1, -1)
        collider_arbre2.show()

        #Modèle3 (Angle route)
        self.arbre3 = self.loader.loadModel("obj/arbre2.glb") #modèle du perso
        self.arbre3.setScale(2.9)
        self.arbre3.reparentTo(self.render)
        self.arbre3.setPos(120, 115, -0.4)
        self.arbre3.setH(26)

        #Collisions3
        colliderNode_arbre3 = CollisionNode("arbre3")
        colliderNode_arbre3.addSolid(CollisionBox(0, 4, 3.8, 20))
        collider_arbre3 = self.maptest.attachNewNode(colliderNode_arbre3)
        collider_arbre3.setPos(self.arbre3.getX()-3, self.arbre3.getY()+1, -1)
        collider_arbre3.setH(26)
        collider_arbre3.show()

        #Modèle4
        self.arbre4 = self.loader.loadModel("obj/arbre1.glb") #modèle du perso
        self.arbre4.setScale(0.5)
        self.arbre4.reparentTo(self.render)
        self.arbre4.setPos(-28, 2, 0)
        self.arbre4.setH(0)

        #Collisions4
        colliderNode_arbre4 = CollisionNode("arbre1")
        colliderNode_arbre4.addSolid(CollisionBox(0, 4, 3.8, 20))
        collider_arbre4 = self.maptest.attachNewNode(colliderNode_arbre4)
        collider_arbre4.setPos(self.arbre4.getX()-2.5, self.arbre4.getY()+1, -1)
        collider_arbre4.show()



    #Maisons
        #Modèle1
        self.maison1 = self.loader.loadModel("obj/maison.glb") #modèle du perso
        self.maison1.setScale(2)
        self.maison1.reparentTo(self.render)
        self.maison1.setPos(22, -75, -0.4)
        self.maison1.setH(90)

        #Collisions1
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


        #Modèle2
        self.maison2 = self.loader.loadModel("obj/maison2.glb") #modèle du perso
        self.maison2.setScale(2)
        self.maison2.reparentTo(self.render)
        self.maison2.setPos(-32, 57, -0.4)
        self.maison2.setH(90)

        #Collisions2
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


    #Garages
        #Modèle1
        self.garage1 = self.loader.loadModel("obj/garage.glb") #modèle du perso
        self.garage1.setScale(2.5)
        self.garage1.reparentTo(self.render)
        self.garage1.setPos(57, -139, -0.4)
        self.garage1.setH(20+90)

        #Collisions1
        colliderNode_garage1 = CollisionNode("garage1")
        colliderNode_garage1.addSolid(CollisionBox(0, 13, 13, 13.2))
        collider_garage1 = self.maptest.attachNewNode(colliderNode_garage1)
        collider_garage1.setPos(self.garage1.getX(), self.garage1.getY(), -1)
        collider_garage1.setH(20+90)
        collider_garage1.show()

        #Modèle2
        self.garage2 = self.loader.loadModel("obj/garage.glb") #modèle du perso
        self.garage2.setScale(2.5)
        self.garage2.reparentTo(self.render)
        self.garage2.setPos(-69, 135, -0.4)
        self.garage2.setH(90)

        #Collisions2
        colliderNode_garage2 = CollisionNode("garage2")
        colliderNode_garage2.addSolid(CollisionBox(0, 13, 13, 13.2))
        collider_garage2 = self.maptest.attachNewNode(colliderNode_garage2)
        collider_garage2.setPos(self.garage2.getX(), self.garage2.getY(), -1)
        collider_garage2.setH(90)
        collider_garage2.show()


    #Bancs
        #Modèle1
        self.banc1 = self.loader.loadModel("obj/banc.glb") #modèle du perso
        self.banc1.setScale(3.2)
        self.banc1.reparentTo(self.render)
        self.banc1.setPos(119, -41, -0.4)
        self.banc1.setH(0)

        #Collisions1
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

        #Modèle2
        self.banc2 = self.loader.loadModel("obj/banc.glb") #modèle du perso
        self.banc2.setScale(3.2)
        self.banc2.reparentTo(self.render)
        self.banc2.setPos(119, 10, -0.4)
        self.banc2.setH(0)

        #Collisions2
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


        #Modèle3
        self.banc3 = self.loader.loadModel("obj/banc.glb") #modèle du perso
        self.banc3.setScale(3.2)
        self.banc3.reparentTo(self.render)
        self.banc3.setPos(119, 61, -0.4)
        self.banc3.setH(0)

        #Collisions3
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
        self.voiture1 = self.loader.loadModel("obj/voiture.glb") #modèle du perso
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

    #Ennemi 
        #Modèle
        self.ennemi = self.loader.loadModel("chars/grenouille.glb") #modèle du perso
        self.ennemi.setScale(0.5)
        self.ennemi.reparentTo(self.render)
        self.ennemi.setPos(-6,-46, 0)

        #Collisions
        colliderNode_ennemi = CollisionNode("ennemi")
        colliderNode_ennemi.addSolid(CollisionBox(0, 1, 1, 1))
        collider_ennemi = self.ennemi.attachNewNode(colliderNode_ennemi)
        collider_ennemi.setPos(0,0,1)


    #Pancarte
        #Modèle
        self.pancarte = self.loader.loadModel("obj/pancarte.glb") #modèle du perso
        self.pancarte.setScale(2.8)
        self.pancarte.reparentTo(self.render)
        self.pancarte.setPos(119, 155, 0.5)
        self.pancarte.setH(0)

        #Collisions
        colliderNode_pancarte = CollisionNode("pancarte")
        colliderNode_pancarte.addSolid(CollisionBox(0, 2, 1, 8))
        collider_pancarte = self.maptest.attachNewNode(colliderNode_pancarte)
        collider_pancarte.setPos(self.pancarte.getX()+1.6, self.pancarte.getY(), -1)
        collider_pancarte.setH(0)
        collider_pancarte.show()

    #Barrières
        #Modèle
        self.barriere1 = self.loader.loadModel("obj/barriere8.glb") #modèle du perso
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
        self.barriere2 = self.loader.loadModel("obj/barriere3.glb") #modèle du perso
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
        self.barriere3 = self.loader.loadModel("obj/barriere3.glb") #modèle du perso
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
        self.barriere4 = self.loader.loadModel("obj/barriere3.glb") #modèle du perso
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
        self.barriere5 = self.loader.loadModel("obj/barriere3.glb") #modèle du perso
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
        self.barriere6 = self.loader.loadModel("obj/barriere8.glb") #modèle du perso
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
        self.barriere7 = self.loader.loadModel("obj/barriere3.glb") #modèle du perso
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
        self.barriere8 = self.loader.loadModel("obj/barriere3.glb") #modèle du perso
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



#Gestion Caméra
    #Creation de l'entité caméra
        self.camera.reparentTo(self.render)
        self.camera.setPos(50, 0, 5)
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
        self.speedcap = 15 #limite de vitesse du perso
        self.distance = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2 + (self.perso.getZ() - self.camera.getZ())**2)#distance entre caméra et personnage
        self.mouvement = False #si le perso bouge
        self.mouvement_cam = False #si la caméra monte ou descent
        self.reset_cam = False #si la caméra se reset
        self.reset_cam_counter = 0 #compteur avant de pouvoir reset la caméra
        self.saut = False #si le perso est en plein saut
        self.attaque_ennemi = True
        self.stop_attaque_ennemi_temps = 0
        self.ennemi_charge = 0

        colliderNode2 = CollisionNode("perso2")
        colliderNode2.addSolid(CollisionBox(0, 0.7, 0.7, 0.01))
        collider2 = self.perso.attachNewNode(colliderNode2)
        collider2.setPos(0,0,0)
        collider2.show()


        self.pusher.addCollider(collider, self.perso)
        self.cTrav.addCollider(collider, self.pusher)
        self.grav.addCollider(collider2, self.perso)
        self.cTrav.addCollider(collider2, self.grav)


        self.pusher.addCollider(collider_ennemi, self.ennemi)
        self.cTrav.addCollider(collider_ennemi, self.pusher)

        #controles PERSO
        self.control = { #dictionnaire des variables utilisées pour les inputs du perso
            "haut": False,
            "bas": False,
            "gauche": False,
            "droite": False,
            "saut": False,
            "sprint": False
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
                if self.distance > 29.9: #camera avance avec le perso si elle n'est pas trop proche de lui
                    self.camera.setY(self.camera, self.vitesse * dt) 
                
        if self.control["bas"]: #si touche assignée à "bas" pressée
            self.mouvement = True
            if not self.control["gauche"] and not self.control["droite"] and not self.control["haut"]: #si uniquement cette direction est pressée
                self.perso.setH(self.camera.getH() + 180) #perso regarde la caméra
                if self.distance < 30.1: #camera recule avec le perso si elle n'est pas trop loin de lui
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
                if self.grav.getVelocity() > - 0.5:
                    self.grav.setVelocity(self.grav.getVelocity() - 0.03) #diminuer la vitesse
            else:
                self.perso.setFluidZ(self.perso, -0.5) #diminuer la hauteur du perso constamment (gravité)
                
        self.perso.setFluidZ(self.perso, 0.1 + self.grav.getVelocity()) #change la hauteur du perso en fonction de la vitesse verticale
        print(self.perso.getPos())

        #sprint
        if self.control["sprint"]: #si touche assignée à "sprint" pressée
            self.speedcap = 30
        else: 
            self.speedcap = 15

        #acceleration
        if self.mouvement == True: #si le perso est censé bouger
            if self.vitesse < self.speedcap:
                self.vitesse = self.vitesse + 0.5
            else: 
                self.vitesse = self.vitesse - 0.5
        else:
            if self.vitesse > 0:
                self.vitesse = self.vitesse - 0.5
        
        self.perso.setY(self.perso, self.vitesse * dt) #le perso avance selon son orientation


        #caméra 
        if self.control_camera["camera_haut"] and self.camera.getZ() < self.perso.getZ() + 14: #on limite la hauteur du mouvement de la caméra si touche assignée à "camera_haut" pressée
            self.camera.setFluidZ(self.camera, 1)
            self.mouvement_cam = True

        if self.control_camera["camera_bas"] and self.camera.getZ() > self.perso.getZ() - 4.5: #on limite la hauteur du mouvement de la caméra si touche assignée à "camera_bas" pressée
            self.camera.setFluidZ(self.camera, -1)
            self.mouvement_cam = True

        if self.control_camera["camera_gauche"] and self.distance < 58: #si touche assignée à "camera_gauche" pressée et si la distance entre camera et perso n'est pas trop grande
            self.camera.setFluidX(self.camera, -1.5) #la caméra bouge vers sa propre gauche
                
        if self.control_camera["camera_droite"] and self.distance < 58: #si touche assignée à "camera_droite" pressée et si la distance entre camera et perso n'est pas trop grande
            self.camera.setFluidX(self.camera, 1.5) #la caméra bouge vers sa propre droite
            
        if self.control_camera["reset_camera"] and self.reset_cam == False: #remet la caméra à sa place
            self.camera.setPos(self.perso.getPos()) #téléporte la caméra sur le perso
            self.camera.setH(self.perso, 0) #donne à la caméra la même orientation qu'au perso
            self.camera.setFluidY(self.camera, - 30) #recule la caméra derrière le perso
            self.reset_cam = True

        if self.reset_cam == True:
            self.reset_cam_counter = self.reset_cam_counter + 1 #compteur avant le prochain reset de la caméra possible
            if self.reset_cam_counter == 60: #60 pour 1 seconde
                self.reset_cam_counter = 0 #on remet le compteur à 0
                self.reset_cam = False 

        if self.distance < 44.5: #empêche la caméra d'être trop proche du personnage
            self.camera.setFluidY(self.camera, -0.1) 
            if self.distance < 10:
                self.perso.hide() #rend le perso invisible si la caméra est trop proche
            else:
                self.perso.show() #rend le perso à nouveau visible si la caméra est assez loin

        elif self.distance > 50: #empêche la caméra d'être trop loin du personnage
            self.camera.setFluidY(self.camera, 0.5) 

        if self.camera.getZ() > self.perso.getZ() + 15: #empêche la caméra d'être trop haute par rapport au perso
            self.camera.setFluidZ(self.camera, -0.135)

        elif not self.control_camera["camera_bas"] and self.camera.getZ() < self.perso.getZ() + 5: #empêche la caméra d'être trop basse par rapport au perso
            self.camera.setFluidZ(self.camera, 0.05)


        self.distance = sqrt( (self.perso.getX() - self.camera.getX())**2 + (self.perso.getY() - self.camera.getY())**2 + (self.perso.getZ() - self.camera.getZ())**2) #distance entre caméra et personnage
        self.camera.lookAt(self.perso) #caméra regarde vers le perso
        self.mouvement = False


        #Gestion ennemi

        self.dist_horizontal_perso_ennemi = sqrt((self.perso.getX() - self.ennemi.getX())**2 + (self.perso.getY() - self.ennemi.getY())**2)
        self.dist_vertical_perso_ennemi = sqrt((self.perso.getZ() - self.ennemi.getZ())**2)

        '''if self.dist_horizontal_perso_ennemi < 20:
            if self.dist_horizontal_perso_ennemi < 2.5:
                self.attaque_ennemi = False
                
            if self.attaque_ennemi == True:
                self.ennemi.lookAt(self.perso)
                self.ennemi.setP(0)
                self.ennemi.setFluidY(self.ennemi, 0.2)

            if self.attaque_ennemi == False:
                self.ennemi.setFluidY(self.ennemi, -0.05)
                self.stop_attaque_ennemi_temps = self.stop_attaque_ennemi_temps + 1
                if self.stop_attaque_ennemi_temps == 60:
                    self.attaque_ennemi = True
                    self.stop_attaque_ennemi_temps = 0'''
            
        if self.dist_horizontal_perso_ennemi < 20:

            self.ennemi.lookAt(self.perso)
            self.ennemi.setP(0)
            
            if self.dist_horizontal_perso_ennemi > 2.5:
                if self.ennemi_charge == 0:
                    self.ennemi.setFluidY(self.ennemi, 0.2)

            else:
                if self.dist_vertical_perso_ennemi < 2:
                    self.attaque_ennemi = False

            if self.attaque_ennemi == False:
                self.ennemi_charge = self.ennemi_charge + 1
                if self.ennemi_charge < 60:
                    self.ennemi.setFluidY(self.ennemi, -0.05)
                elif self.ennemi_charge == 120:
                    self.ennemi_charge = 0
                    self.attaque_ennemi = True
                    
            #saut sur l'ennemi

        if self.dist_horizontal_perso_ennemi < 1.5 and self.dist_vertical_perso_ennemi < 2:
            self.ennemi.setPos(0,0,0)
            self.grav.setVelocity(self.grav.getVelocity()+1)

        
        return task.cont
       
Game = ConcatenageStudio()
Game.run()