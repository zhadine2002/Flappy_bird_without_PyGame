from tkinter import *
import random
import os
from PIL import ImageTk, Image                                              #initialisation
delai = 20                                      #delai en ms
SCORE = -1                                      #initialisation du score
jeu = Tk()                                       #création de la fenetre
jeu.resizable(width = False, height = False)                 #bloquer la taille de la fenetre
jeu.title("Flappy Dino")                                #titre du jeu
jeu.geometry('550x700')                                  #taille de la fenetre
w = Canvas(jeu, width=1366, height=768)                   #arriere plan
Image = ImageTk.PhotoImage(Image.open("paysage.jpg"))     #ajouter limage a larriere plan
w.create_image(0, 0, anchor=NW, image=Image)
w.pack()
DINO_Y = 200                                    #initialisation de la position du dinosaure
obstacle = 550                                     #initialisation de la position de l'obstacle
trou = 0                                        #initialisation entre les  obstacles
NOW_PAUSE = False                                   #freeze
meilleur_score = 0
if os.path.isfile("meilleur_score.txt"):                   ##enregistrement du meilleure score dans un fichier texte
	fichierdescore = open('meilleur_score.txt')            #ouvrir le fichier
	meilleur_score = int(fichierdescore.read())
	fichierdescore.close()
else:
	fichierdescore = open('meilleur_score.txt', 'w')
	fichierdescore.write(str(meilleur_score))
	fichierdescore.close()
dinoImg = PhotoImage(file="dino.gif")               #importation de l'image du dinosaure
dino = w.create_image(100, DINO_Y, image=dinoImg)    #creation de l'objet
up_count = 0
endRectangle = endBest = endScore = None
obstacle_du_haut = w.create_rectangle(obstacle, 0, obstacle + 100, trou, fill="lime green", outline="#74BF2E")    #obstacle du haut
obstacle_du_bas = w.create_rectangle(obstacle, trou + 200, obstacle + 100, 700, fill="lime green", outline="#74BF2E")     #obstacle du bas
score_w = w.create_text(15, 45, text="0", font='Impact 60', fill='#ffffff', anchor=W)                  #texte 'meilleure score'
def position_trou():            #positionnement du trou
	global trou
	global SCORE
	SCORE += 1
	w.itemconfig(score_w, text=str(SCORE))   #Pour remplacer le texte par le score
	trou = random.randint(50, 500)                       #position aléatoire du trou
	if SCORE + 1 % 7 == 0 and SCORE != 0:
		delai-=1
position_trou()
def recommencer_le_jeu():     #fonction pour recommencer le jeu
	global obstacle
	global DINO_Y
	global SCORE
	global NOW_PAUSE
	global delai
	DINO_Y = 200                #initialisation des cordonnées
	obstacle = 550
	SCORE = -1
	delai = 20
	NOW_PAUSE = False
	w.delete(endScore)                         #supprimer tout
	w.delete(endRectangle)
	w.delete(endBest)
	position_trou()
	jeu.after(delai, mouvement_en_bas)
	jeu.after(delai, mouvement_des_obstacles)
	jeu.after(delai, detection_de_Collision)
def mouvement_en_haut(event = None):              #mouvement_en_haut
	global DINO_Y
	global up_count
	global NOW_PAUSE
	if NOW_PAUSE == False:
		DINO_Y -= 20
		if DINO_Y <= 0:
			DINO_Y = 0
		w.coords(dino, 100, DINO_Y)
		if up_count < 5:
			up_count += 1
			jeu.after(delai, mouvement_en_haut)
		else: up_count = 0
	else:
		recommencer_le_jeu()
def mouvement_en_bas():               #mouvement_en_bas
	global DINO_Y
	global NOW_PAUSE
	DINO_Y += 8
	if DINO_Y >= 700:
		DINO_Y = 700
	w.coords(dino, 100, DINO_Y)
	if NOW_PAUSE == False:
		jeu.after(delai,mouvement_en_bas)
def mouvement_des_obstacles():              #mouvement des obstacles
	global obstacle
	global trou
	global NOW_PAUSE
	obstacle -= 5
	w.coords(obstacle_du_haut, obstacle, 0, obstacle + 100, trou)
	w.coords(obstacle_du_bas, obstacle, trou + 200, obstacle + 100, 700)
	if obstacle < -100:
		obstacle = 550
		position_trou()
	if NOW_PAUSE == False:
		jeu.after(delai, mouvement_des_obstacles)      #after pour l'animation
def fin_de_jeu():                                         # fenetre du fin de jeu
	global endRectangle
	global endScore
	global endBest
	endRectangle = w.create_rectangle(0, 0, 550, 700, fill='#4EC0CA')
	endScore = w.create_text(15, 200, text="Your score: " + str(SCORE), font='Impact 50', fill='#ffffff', anchor=W)
	endBest = w.create_text(15, 280, text="Best score: " + str(meilleur_score), font='Impact 50', fill='#ffffff', anchor=W)
def detection_de_Collision():
	global NOW_PAUSE                #variable global
	global meilleur_score           #....
	if (obstacle < 150 and obstacle + 100 >= 55) and (DINO_Y < trou + 45 or DINO_Y > trou + 175):     #condition de collision
		NOW_PAUSE = True                                               # arret de jeu
		if SCORE > meilleur_score:
			meilleur_score = SCORE
			fichierdescore = open('meilleur_score.txt', 'w')
			fichierdescore.write(str(meilleur_score))                  #enregistrement et lécriture du nouveau score
			fichierdescore.close()
		fin_de_jeu()
	if NOW_PAUSE == False:                                         #sinon le jeu continue normalement
		jeu.after(delai, detection_de_Collision)
jeu.after(delai, mouvement_en_bas)
jeu.after(delai, mouvement_des_obstacles)
jeu.after(delai, detection_de_Collision)
jeu.bind("<space>", mouvement_en_haut)              #relier le boutton d'espace avec le mouvement en haut avec  ''bind''
jeu.mainloop()
