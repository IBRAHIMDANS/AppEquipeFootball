from time import strftime

import MySQLdb
from datetime import datetime
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen


class DbCon:

    def __init__(self):
        #self.db = MySQLdb.connect(user="football", passwd="password", db="e4_football")
        self.db = MySQLdb.connect(user="158371_football", passwd="password", db="kivystudient_kivy", host="mysql-kivystudient.alwaysdata.net")
        self.c = self.db.cursor()

    def Joueur(self,equip):
        self.c.execute("SELECT j.J_Nom FROM joueur j JOIN equipe e ON j.Id_Equipe=e.Id_Equipe WHERE j.J_Status='Titulaire' and e.E_Nom= '%s'" % equip)
        values = [row[0] for row in self.c]
        return values

    def JoueurAjoutBut(self,joueur):
        print("ooo",joueur)
        self.c.execute("UPDATE statistiques s JOIN joueur j ON s.Id_Statistique=j.Id_Statistique SET s.S_But=s.S_But+1 WHERE j.J_Nom='%s'" % joueur)      
        self.db.commit()

    def JoueurDiminueBut(self,joueur):
        self.c.execute("UPDATE statistiques s JOIN joueur j ON s.Id_Statistique=j.Id_Statistique SET s.S_But=s.S_But-1 WHERE j.J_Nom='%s' and s.S_But!=0" % joueur)      
        self.db.commit()

    def Equipe(self, search=""):
        self.c.execute("SELECT E_Nom FROM equipe")
        values = [row[0] for row in self.c]
        return values

    def ConnexionArbitreNom(self, search=""):
        self.c.execute("SELECT A_Nom FROM arbitre")
        values = [row[0] for row in self.c]
        return values

    def ConnexionArbitrePasswd(self, search=""):
        self.c.execute("SELECT A_Mdp FROM arbitre")
        values = [row[0] for row in self.c]
        return values


class ConnexionScreen(Screen):

    def login(self):

        db = DbCon()
        usernameArbitre = db.ConnexionArbitreNom()
        passorwdArbitre = db.ConnexionArbitrePasswd()

        for i in range(0, len(usernameArbitre)):

            if self.ids.username.text == usernameArbitre[i] and self.ids.passwd.text == passorwdArbitre[i]:
                print("Connexion Reussie")
                self.manager.current = "equip"
                self.ids.username.text = ""
                self.ids.passwd.text = ""


class EquipScreen(Screen):

    equipDomicile = ObjectProperty()
    equipExterieur = ObjectProperty()
    nomEquipDom = StringProperty()
    nomEquipExt = StringProperty()

    def getEquipDom(self):
        return self.nomEquipDom

    def getEquipExt(self):
        return self.nomEquipExt

    def checking(self):

        #db = DbCon()
        self.manager.get_screen("ecran").start()
        self.manager.get_screen("ecran").startEcranScreen()

    def on_select_left(self,data):
        print(data.text)
        self.nomEquipDom=data.text
        self.manager.get_screen("ecran").setEquipDom(self.nomEquipDom)
        print(self.getEquipDom())
        #print(data.ids)

    def on_select_right(self,data):
        print(data.text)
        self.nomEquipExt=data.text
        self.manager.get_screen("ecran").setEquipExt(self.nomEquipExt)

    def __init__(self, *args, **kwargs):
        super(EquipScreen, self).__init__(*args, **kwargs)

        db = DbCon()

        listEquipe = db.Equipe()

        dropdown = DropDown()
        dropdown2 = DropDown()

        for i in range(0, len(listEquipe)):
            btn = Button(text=str(listEquipe[i]), size_hint_y=None, height=30)
            btn2 = Button(text=str(listEquipe[i]), size_hint_y=None, height=30)

            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            btn2.bind(on_release=lambda btn2: dropdown2.select(btn2.text))

            dropdown.add_widget(btn)
            dropdown2.add_widget(btn2)

        mainbutton = Button(text='Equipe Domicile')
        mainbutton2 = Button(text='Equipe Exterieur')

        mainbutton.bind(on_release=dropdown.open)
        mainbutton2.bind(on_release=dropdown2.open)

        print("debut")

        dropdown.bind(on_select=lambda instance, x: self.on_select_left(mainbutton))
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        

        print("milieu")

        dropdown2.bind(on_select=lambda instance, x: self.on_select_right(mainbutton2))
        dropdown2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))

        print("fin")

        self.equipDomicile.add_widget(mainbutton)
        self.equipExterieur.add_widget(mainbutton2)
        #print("self.ids={}".format(self.ids))




class EcranScreen(BoxLayout, Screen):

    i = 0
    liste = []
    liste.append(0)
    liste.append(0)
    zer = False
    text = str(0)
    nomEquipDom = StringProperty()
    nomEquipExt = StringProperty()

    joueurEquipDom = StringProperty()
    joueurEquipExt = StringProperty()

    score_dom = NumericProperty(0)
    score_ext = NumericProperty(0)

    buteurDomicile = ObjectProperty()
    buteurExterieur = ObjectProperty()

    db = DbCon()
    #test = db.get_rows("")
    #test = test[0][1]

    def __init__(self, *args, **kwargs):
        super(EcranScreen, self).__init__(*args, **kwargs)
        #self.nomEquipDom=self.manager.get_screen("equip").getEquipDom()
        #self.nomEquipExt=self.manager.get_screen("equip").getEquipExt()
        #print(self.manager.get_screen("equip").getEquipDom())
        #print(self.nomEquipExt)
        text = str(self.i)
        #self.start()
        

    def startEcranScreen(self):
        JoueurDom = DbCon().Joueur(self.nomEquipDom)
        print("JoueurDom")
        JoueurExt = DbCon().Joueur(self.nomEquipExt)
        dropdown = DropDown()
        dropdown2 = DropDown()

        for i in range(1, len(JoueurDom)):
            btn = Button(text=str(JoueurDom[i]), size_hint_y=None, height=30)

            btn.bind(on_release=lambda btn: dropdown.select(btn.text))

            dropdown.add_widget(btn)

        for i in range(1, len(JoueurExt)):
            btn2 = Button(text=str(JoueurExt[i]), size_hint_y=None, height=30)

            btn2.bind(on_release=lambda btn2: dropdown2.select(btn2.text))

            dropdown2.add_widget(btn2)

        mainbutton = Button(text='Buteur Domicile')
        mainbutton2 = Button(text='Buteur Exterieur')

        mainbutton.bind(on_release=dropdown.open)
        mainbutton2.bind(on_release=dropdown2.open)

        dropdown.bind(on_select=lambda instance, x: self.on_select_left(mainbutton))
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        dropdown2.bind(on_select=lambda instance, x: self.on_select_right(mainbutton2))
        dropdown2.bind(on_select=lambda instance, x: setattr(mainbutton2, 'text', x))

        self.buteurDomicile.add_widget(mainbutton)
        self.buteurExterieur.add_widget(mainbutton2)

    def setEquipDom(self,equip):
        self.nomEquipDom=equip

    def setEquipExt(self,equip):
        self.nomEquipExt=equip

    def start(self):
        Clock.schedule_interval(self.my_callback, 1)

    def my_callback(self, dt):
        self.i = self.i + 1
        if self.zer == True:
            if self.i == 60:
                self.liste[0] = self.liste[0] + 1
                self.i = 0

        self.zer = True

        self.liste[1] = self.i
        self.ids.time2.text = ""
        self.ids.time2.text = '%s : %s' % (str(self.liste[0]), str(self.i))

        #print(str(self.liste))

    def augmenterDom(self):
        if self.joueurEquipDom != "":
            self.score_dom += 1
            button = Button(text='My first button')
            DbCon().JoueurAjoutBut(self.joueurEquipDom)
            print("joueur :")
            print(self.joueurEquipDom)
            self.manager.get_screen("stat").addListeDom(self.joueurEquipDom)

        # self.add_widget(button)

    def diminuerDom(self):
        if self.joueurEquipDom != "":
            if self.score_dom > 0:
                self.score_dom -= 1
                self.db.JoueurDiminueBut(self.joueurEquipDom)
                self.manager.get_screen("stat").delListeDom()

    def augmenterExt(self):
        if self.joueurEquipExt != "":
            self.score_ext += 1
            self.db.JoueurAjoutBut(self.joueurEquipExt)
            self.manager.get_screen("stat").addListeExt(self.joueurEquipExt)

    def diminuerExt(self):
        if self.joueurEquipExt != "":
            if self.score_ext > 0:
                self.score_ext -= 1
                self.db.JoueurDiminueBut(self.joueurEquipExt)
                self.manager.get_screen("stat").delListeExt()

    def reinit(self):
        self.score_dom = 0
        self.score_ext = 0
        print("pré-fin")
        self.manager.get_screen("stat").start(self.nomEquipDom, self.nomEquipExt)

    def on_select_left(self,data):
        print(data.text)
        self.joueurEquipDom=data.text

    def on_select_right(self,data):
        print(data.text)
        self.joueurEquipExt=data.text

class StatScreen(BoxLayout, Screen):

    listeDom = {}
    listeExt = {}
    compteurDom=0
    compteurExt=0

    def __init__(self, *args, **kwargs):
        super(StatScreen, self).__init__(*args, **kwargs)

    def addListeDom(self,nomJoueur):
        self.listeDom[self.compteurDom]={}
        self.listeDom[self.compteurDom]["nom"]=nomJoueur
        self.compteurDom+=1
        #listeDom[compteurDom]["minutes"]=minutes

    def delListeDom(self):
        print(self.compteurDom)
        del self.listeDom[self.compteurDom-1]

    def addListeExt(self,nomJoueur):
        self.listeExt[self.compteurExt]={}
        self.listeExt[self.compteurExt]["nom"]=nomJoueur
        self.compteurExt+=1
        #listeExt[compteurExt]["minutes"]=minutes

    def delListeExt(self):
        print(self.compteurExt)
        del self.listeExt[self.compteurExt-1]

    def start(self,equipDom, equipExt):
        print("fin")
        print(equipDom)
        print(self.listeDom)
        print(equipExt)
        print(self.listeExt)
        self.ids.idDom.text=equipDom
        self.ids.idExt.text=equipExt
        listeDomChaine=""
        for i in range (0,self.compteurDom):
            listeDomChaine=listeDomChaine+self.listeDom[i]["nom"]+"\n"

        self.ids.listeDom.text=listeDomChaine

        listeExtChaine=""
        for i in range (0,self.compteurExt):
            listeExtChaine=listeExtChaine+self.listeExt[i]["nom"]+"\n"

        self.ids.listeExt.text=listeExtChaine
        #self.add_widget(Label(text="blabla"))
        #self.add_widget(Label(text="blabla"))


class ScreenManagement(ScreenManager):
    pass


class MyApp(App):

    def build(self):

        root = ScreenManager()
        #root.add_widget(ConnexionScreen(name="connexion"))
        root.add_widget(EquipScreen(name="equip"))
        root.add_widget(EcranScreen(name="ecran"))
        root.add_widget(StatScreen(name="stat"))

        return root


if __name__ == '__main__':
    MyApp().run()
