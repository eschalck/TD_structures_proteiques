# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 14:15:22 2019

@author: Elsa
"""

#########################################
#                                       #
#   Autour des structures protéiques    #
#   Elsa Schalck                        #
#   IODAA AP_PROG 2019-2020             #
#   Programmation Orientée Objet        #
#                                       #
#########################################

import math
import matplotlib.pyplot as plt
import re
from mpl_toolkits.mplot3d import Axes3D


#EXERCICE 4

class AA(object):
    
    """
    Classe définissant un acide aminé caractérisé par :
    - sa nature
    - sa composition
    
    Methodes de la classe : 
    - addAtome : ajoute un atome à la composition de l'acide aminé. 
    - determineCentre : calcul du centre de gravité de l'acide aminé. 
    - determineRayon : calcul du rayon de l'acide aminé. 
    """

    def __init__(self, chaine):
        """
        Constructeur :
            - initialise un attribut nommé nature qui est une chaîne de caractères permettant d'identifier à quel acide aminé l'on fait référence. 
            - initialise un attribut nommé composition à la liste vide.
        
        chaine : string, chaîne de caractères permettant d'identifier à quel acide aminé l'on fait référence.
        """
        self.nature=chaine
        self.composition=[]
    
    def addAtome(self,lettres,valeur):
        """
        Méthode qui pour une instance donnée et un couple ('lettres', valeur) donné ajoute ce dernier à l'attribut composition.
        
        lettres : string, lettres de l'atome ajouté.
        valeur : list, position de l'atome dans l'espace (sous forme d'une liste de trois valeurs [x, y, z]).
        """
        self.composition=self.composition+[lettres]+[valeur]
    
    def determineCentre(self):
        """
        Méthode qui, pour une instance donnée calcule, étant donné sa composition connue, son centre de gravité et renseigne ainsi un attribut nommé centre.
        """
        self.centre=[0,0,0]
        n=int(len(self.composition)/2)
        for i in range(0,n):
            for j in range(0,3):    
                self.centre[j]=self.centre[j]+self.composition[i*2+1][j]
        for j in range(0,3):    
            self.centre[j]=self.centre[j]/n

    def determineRayon(self):
        """
        Méthode qui, pour une instance donnée, calcule à partir de sa composition connue son rayon comme étant la plus grande distance entre son centre et un de ses atomes et stocke cette information dans un attribut de même nom.
        """       
        self.rayon=0
        n=int(len(self.composition)/2)
        for k in range(0,n):
            distance=math.sqrt((self.composition[k*2+1][0]-self.centre[0])**2+(self.composition[k*2+1][1]-self.centre[1])**2+(self.composition[k*2+1][2]-self.centre[2])**2)
            if distance>self.rayon:
                self.rayon=distance


#EXERCICE 5


class ChaineProt(object):
    
    """
    Classe définissant une chaîne protéique caractérisée par :
        - son identifiant
        - les acides aminés qui la composent
    
    Méthodes de la classe :
        - addAd : ajoute un acide aminé à la chaîne protéique.
        - calculeHisto : calcule l'histogramme des acides aminés qui composent la chaîne protéique. 
        - traceHisto : affiche l'histogramme des acides aminés qui composent la chaîne protéique.
        - traceSquelette : affiche le graphique du squelette calcique de la chapine protéique. 
        - traceSpheres : affiche le graphique de la chaîne protéique où chaque acide aminé est représenté par une sphère (définie par le centre et le rayon de l'acide aminé). 
    """

    def __init__(self, valeur):
        """
        Constructeur :
            - initialise un attribut id à la valeur fournie en argument
            - initialise la liste des acide aminés qui composent la chaîne à la liste vide (attribut nommé aas).
        
        valeur : string, identifiant de la chaîne protéique. 
        """
        self.id=valeur
        self.aas=[]
    
    def addAa(self, instance):
        """
        Méthode qui pour une instance donnée et une instance de la classe AA ajoute cette dernière à l'attribut aas.
        
        instance: instance de la classe AA qui est ajoutée à l'attribut aas. 
        """
        self.aas=self.aas+[instance]

    def calculeHisto(self):
        """
        Méthode qui pour une instance donnée calcule l'histogramme des acides aminés qui la compose et enregistre le résultat dans un attribut nommé histo.
        """
        self.dico=dict()            #utilisation d'un dictionnaire
        n=len(self.aas)
        for k in range(0,n):
            if self.aas[k].nature in self.dico:
                for i in self.dico.keys():
                    if self.aas[k].nature==i:
                        self.dico[i]=self.dico[i]+1
            else:
                self.dico[self.aas[k].nature]=1

    #EXERCICE 7
    
    def traceHisto(self, figure=None, num_fig=0, axes=None):
        """
        Méthode qui pour une instance donnée permet d'afficher l'histogramme de l'attribut histo.
        
        Si l'histogramme fait partie d'une figure, alors les arguments optionnels suivants sont fournis à traceHisto : 
        - figure : figure, figure au sein de laquelle est tracé l'histogramme.
        - num_fig : int, numéro de l'emplacement de l'histogramme dans la figure.
        - axes : axes, list des subplots de la figure. 
        """
        #Si l'histogramme ne fait pas partie d'une figure déjà créée, on crée une figure
        if figure==None:
            self.fig=plt.figure(figsize=(10, 6))
            plt.title("Histogramme des acides aminés qui composent la chaîne "+str(self.id))
            plt.bar(self.dico.keys(),self.dico.values())
        #si l'histogramme fait partie d'une figure déjà créée, on l'ajoute à cette figure en tant que subplot. 
        else:
            self.fig=figure
            axes[num_fig].bar(self.dico.keys(),self.dico.values())
            axes[num_fig].title.set_text("Histogramme des acides aminés de la chaîne "+str(self.id))
            
        
    def traceSquelette(self, figure=0):
        """
        Méthode qui crée un graphique où chaque atome CA de chaque acide aminé présent dans la chaîne est représenté par un cercle et relié à ses homologues voisins dans la chaîne.
        
        Si le graphique fait partie d'une figure, alors l'argument optionnel suivant est fourni à traceSquelette : 
            - figure : figure, figure au sein de laquelle est tracé le graphique.
        --> : figure, si on travaille sur une figure déjà créée, on retourne la figure, pour pouvoir appeler plusieurs fois la fonction traceSquelette et ainsi ajouter les squelettes de plusieures chaînes protéiques.
        """
        #on note qu'il n'y a qu'un seul atome de Calcium par acide aminé, et que celui-ci se trouve toujours en 2ème position de la composition des acides aminés. 
        
        #Si le graphique ne fait pas partie d'une figure déjà créée, on crée la figure.
        if figure==0: 
            plt.figure(figsize=(10, 6))
            figure=plt.axes(projection='3d')
            figure.set_xlabel('x')
            figure.set_ylabel('y')
            figure.set_zlabel('z')
            plt.title("Squelette des atomes de Calcium des acides aminés de la chaîne "+str(self.id))
        
        #Sinon, on ajoute le graphique à la figure déjà créée. 
        else:
            plt.figure
        
        x=[]
        y=[]
        z=[]
        
        for i in range(0,len(self.aas)):
            for j in range(0,int(len(self.aas[i].composition)/2)):
                if self.aas[i].composition[2*j]=='CA':
                    x=x+[self.aas[i].composition[2*j+1][0]]
                    y=y+[self.aas[i].composition[2*j+1][1]]
                    z=z+[self.aas[i].composition[2*j+1][2]]
        figure.plot(x, y, z, linewidth=0.75)
        figure.scatter(x, y, z, label='CA de la chaîne '+str(self.id))
        figure.legend(loc=3)
        self.fig=figure
        
        if figure!=0:           #Si on travaille sur une figure déjà créée, on retourne la figure, pour pouvoir appeler plusieurs fois la fonction traceSquelette et ainsi ajouter les squelettes de plusieures chaînes protéiques. 
            return figure
        
        plt.show()

    def traceSpheres(self):
        """
        Méthode qui crée un graphique représentant une chaîne par des sphères dont le centre et le rayon sont donnés par les attributs de chaque acide aminé de la chaîne.
        """
        
        plt.figure(figsize=(10, 6))
        
        fig=plt.axes(projection='3d')
        fig.set_xlabel('x')
        fig.set_ylabel('y')
        fig.set_zlabel('z')
        
        x=[]
        y=[]
        z=[]
        size=[]
        
        for i in range(0,len(self.aas)):
            
            if len(self.aas[i].composition)!=0:  
        #on ne travaille que sur les aas dont les atomes sont renseignés, 
        #et donc pour lesquels on peut calculer le centre et le rayon.
                
                self.aas[i].determineCentre()
                x.append(self.aas[i].centre[0])
                y.append(self.aas[i].centre[1])
                z.append(self.aas[i].centre[2])
            
                self.aas[i].determineRayon()
                size.append(self.aas[i].rayon*100)
            
        
        fig.scatter(x, y, z, s=size, label='Acide Aminé')
        fig.legend()
        plt.title("Représentation de la chaîne "+str(self.id))
        plt.show()    
                
        
#EXERCICE 6

class PDB(object):
    
    """
    Classe définissant des fichiers d'extension ".pdb", caractérisés par : 
        - leur nom (sans l'extension ".pdb")
        - les chaines protéiques qui le composent, elles-mêmes consitués des acides aminés qui les composent, eux-mêmes constitués des atomes qui les composent. 
    """

    def __init__(self, fichier):
        """
        Constructeur qui prend en entrée un nom de fichier d'extension ".pdb", initialise un attribut name à la valeur du nom du fichier fournit sans son extension et un attribut nommé chaines qui stocke la liste des chaînes protéiques décrites dans le fichier.
        """
        self.name=fichier[:len(fichier)-4]
        
        f=open(fichier,"r")
        lines=f.readlines()
        f.close()
        
        self.chaines=[]
        
        for k in range(0,len(lines)):         
            
            #CREATION DES CHAINES PROTEIQUES ET AJOUT DES ACIDES AMINES
            
            if lines[k][0:6]=='SEQRES':         
            #les lignes commençant par SEQRES donnent la composition des chaînes protéiques. 
            #l'identifiant de la chaine protéique concernée par la ligne se trouve en position 12 de la chaine commençant par SEQRES.
                
                chaine=lines[k][19:-1].strip(' ')       #on récupère la liste des aas de la chaîne protéique
                chaine=chaine.split(' ')
                
                n=0
                for i in range (0,len(self.chaines)):
                    if self.chaines[i].id==lines[k][11]:       
                    #si la ligne concerne une chaîne protéique déjà crée
                        n=1
                        for j in range(0,len(chaine)): 
                            self.chaines[i].addAa(AA(chaine[j]))          #on crée les aas donnés par la ligne et on les ajoute à la chaîne protéique. 
                
                if n==0:
                #sinon on crée la chaîne protéique et on y ajout les aas donnés par la ligne.
                    self.chaines=self.chaines+[ChaineProt(lines[k][11])]
                    for j in range(0,len(chaine)):
                        self.chaines[-1].addAa(AA(chaine[j]))
            
            #AJOUT DES ATOMES AUX ACIDES AMINES DES CHAINES PROTEIQUES
            #Remarque : les lignes contenant ATOM sont en dessous des lignes contenant SEQRES dans le fichier pdb, donc les aas ont tous déjà été créés.
            #L'identifiant de la chaine se trouve en position 22 de la chaine commençant par ATOM.
            
            if lines[k][0:4]=='ATOM':
                position=lines[k][30:54].strip(' ')
                position=re.split('  | ',position)
                while len(position)>3:                     #si 3 espaces séparent les valeurs des positions : python crée un ou plusieurs élément(s) contenant juste un espace, qui sont supprimés.
                    position.remove('')
                position=[float(i) for i in position]

                for i in range (0,len(self.chaines)):
                    for j in range(0,len(self.chaines[i].aas)):
                        if self.chaines[i].id==lines[k][21] and j+1==int(lines[k][22:26].strip(' ')):
                            self.chaines[i].aas[j].addAtome(lines[k][12:16].strip(' '),position)
                                

    
    def afficheSynthese(self):
        """
        Méthode qui pour une instance donnée affiche dans la console son "nom", le nombre de chaînes qu'elle contient, le nombre d'acides aminés qu'elle contient et les histogrammes de composition par chaines précédés de l'identifiant de la chaîne.
        """ 
        print("Synthèse")
        
        #NOM
        print("Nom: ",self.name)
        #NOMBRE DE CHAINES
        print("Nombre de chaînes: ", len(self.chaines))
        
        #NOMBRE D'ACIDES AMINES 
        nb_aa=0         #compteur du nombre d'acides aminés
        for k in range (0,len(self.chaines)):
            nb_aa=nb_aa+len(self.chaines[k].aas)
        print("Nombre total d'acides aminés :", nb_aa)
        
        #HISTOGRAMMES PAR CHAINE 
        for k in range (0,len(self.chaines)):
            print("\nIdentifiant de la chaîne: ", self.chaines[k].id)
            self.chaines[k].calculeHisto()
            self.fig=plt.figure(k,figsize=(10, 6))              #on crée un attribut figure pour l'aa. 
            plt.bar(self.chaines[k].dico.keys(),self.chaines[k].dico.values())
            plt.show()
            
    def traceHisto(self, figure=None, axes=None):
        """
        Méthode qui pour une instance donnée permet de visualiser l'histogramme de l'attribut histo pour chacune de ses chaînes protéiques.
        
        Si les histogrammes font partie d'une figure, alors les arguments optionnels suivants sont fournis à traceHisto : 
            - figure : figure, figure au sein de laquelle est tracé l'histogramme.
            - axes : axes, list des subplots de la figure. 
        """
        
        if figure==None: 
        #Si les histogrammes ne font pas partie d'une figure déjà créée, on crée une figure.
            nb_fig=len(self.chaines)
            self.fig, axes=plt.subplots(nb_fig,1, figsize=(10, 15))
            plt.subplots_adjust(hspace=0.5)
            self.fig.suptitle("Histogrammes par chaîne des acides aminés qui composent les chaînes de la \n protéine "+str(self.name), fontsize=14)
                
        #Sinon, on rajoute les histogrammes à la figure déjà créée.
        else:                         
            self.fig=figure   
            
        for k in range(0,len(self.chaines)):
            self.chaines[k].calculeHisto()
            self.chaines[k].traceHisto(self.fig, k, axes)

            
            
    def traceSquelette(self, figure=None, axes=None):
        """
        Méthode qui pour une instance donnée crée un graphique où chaque squelette de chacune de ses chaînes protéiques est représenté par une couleur spécifique.
        
        Si le graphique fait partie d'une figure, alors les arguments optionnels suivants sont fournis à traceSquelette : 
            - figure : figure, figure au sein de laquelle est tracé le graphique.
            - axes : axes, list des subplots de la figure.
        """
        if figure==None:
        #Si le graphique ne fait pas partie d'une figure déjà créée, on crée une figure.
            plt.figure(figsize=(10, 6))
            self.fig=plt.axes(projection='3d')
            plt.title("Graphique des squelettes des chaînes de la protéine "+str(self.name))
        
            self.fig.set_xlabel('x')
            self.fig.set_ylabel('y')
            self.fig.set_zlabel('z')
            
            for k in range(0,len(self.chaines)):
                self.fig=self.chaines[k].traceSquelette(self.fig)
            plt.show()
        
        #Sinon, on rajoute le graphique a la figure déjà créée. 
        else:
            self.fig=figure
            for k in range(0,len(self.chaines)):                
                axes[-1]=self.chaines[k].traceSquelette(axes[-1])
                

    def  traceHistoGlob(self, figure=None, axes=None):
        """
        Méthode qui pour une instance donnée permet de visualiser l'histogramme des acides aminés contenus dans ses chaînes protéiques.
        
        Si le graphique fait partie d'une figure, alors les arguments optionnels suivants sont fournis à traceSquelette : 
            - figure : figure, figure au sein de laquelle est tracé le graphique.
            - axes : axes, list des subplots de la figure.
        """
        self.dico=dict()
        for k in range(0,len(self.chaines)):
            self.chaines[k].calculeHisto()
            for i in self.chaines[k].dico.keys():
                if i in self.dico.keys():
                    self.dico[i]=self.dico[i]+self.chaines[k].dico[i]
                else:
                    self.dico[i]=self.chaines[k].dico[i]
        
        if figure==None:
        #Si le graphique ne fait pas partie d'une figure déjà créée, on crée une figure.
            self.fig=plt.figure(figsize=(10, 6))
            plt.title("Histogramme des acides aminés qui composent les chaînes de la protéine "+str(self.name))
            plt.bar(self.dico.keys(),self.dico.values())
            plt.show()
        
        else:
        #Sinon, on rajoute le graphique a la figure déjà créée.
            self.fig=figure
            axes[-2].bar(self.dico.keys(),self.dico.values())

    def traceAll(self):
        """
        Méthode qui pour une instance donnée créer un graphique contenant les sous-graphiques implémentés.
        """
        
        self.figure, axes=plt.subplots(len(self.chaines)+2,1, figsize=(10, 25), gridspec_kw={'height_ratios': [1]*len(self.chaines)+[3]+[4]})
        axes[len(self.chaines)+1].remove()
        self.figure.add_subplot(len(self.chaines)+2,1,len(self.chaines)+1, projection='3d')
        axes=self.figure.axes
        plt.subplots_adjust(hspace=0.5)
        self.figure.suptitle("Protéine "+str(self.name), fontsize=16)
        axes[-2].title.set_text("Histogramme des acides aminés de la protéine")
        axes[-1].title.set_text("Graphique des squelettes des chaînes de la protéine")
        self.traceHisto(self.figure, axes)
        self.traceSquelette(self.figure, axes)
        self.traceHistoGlob(self.figure, axes)
        self.figure.subplots_adjust(top=0.95)
        

"""
CODE PRINCIPAL
"""
        
ala=AA('Ala')
print(ala.nature)
print(ala.composition)
ala.addAtome('N',[4,8,6])
print(ala.nature)
print(ala.composition)
ala.addAtome('C',[5,4,3])
print(ala.nature)
print(ala.composition)
ala.determineCentre()
print(ala.centre)
ala.determineRayon()
print(ala.rayon)
chaine_1=ChaineProt(1)
print(chaine_1.id)
print(chaine_1.aas)
chaine_1.addAa(ala)
print(chaine_1.id)
print(chaine_1.aas[0].nature)
met=AA('Met')
chaine_1.addAa(met)
chaine_1.addAa(met)
chaine_1.calculeHisto()
print(chaine_1.aas[1].nature)
print(chaine_1.dico)
test=PDB('1BRS.pdb')
print(test.chaines[0].aas[3].composition)
test.afficheSynthese()
test.chaines[3].calculeHisto()
test.chaines[3].traceHisto()
test.chaines[3].traceSquelette()
test.chaines[3].traceSpheres()
test.traceHisto()
test.traceSquelette()
test.traceHistoGlob()
test.traceAll()


"""
Aide fichiers .pdb : 
    https://www.wwpdb.org/documentation/file-format-content/format33/sect9.html#ATOM
    https://www.wwpdb.org/documentation/file-format-content/format33/sect3.html#SEQRES
"""