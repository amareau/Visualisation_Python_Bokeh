## Importation des modules
import pandas
import json
import ast
from pyproj import Proj, transform 
from bokeh.plotting import figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.layouts import widgetbox, row, column, gridplot
from bokeh.models import HoverTool, ColumnDataSource, LinearColorMapper, LabelSet, ColorBar, BasicTicker
from bokeh.models.widgets import *
from bokeh.palettes import magma, viridis, inferno
from bokeh.io import curdoc
from math import pi
from bokeh.transform import cumsum

## Définition des fonctions MAJ
def MAJ_slider_graph1(attr,old,new):
    Age_choisi = liste_age[radio1_Age.active]
    Annee_choisi = '('+ str(slider1_Annee.value) + '|nom_pays)'
    Niveau_choisi = liste_niveau[radio1_Niveau.active]
    
    g1.title.text = "Pourcentage de la population {} ans ayant été au {} en {} ".format(dict_age[Age_choisi], dict_niveau[Niveau_choisi], str(slider1_Annee.value))
    
    donnees_graphCarto = donnees.query("sex == 'T' and age ==@Age_choisi and niveau==@Niveau_choisi").filter(regex=Annee_choisi)
    donnees_graphCarto = donnees_graphCarto.merge(pays_countries, left_on="nom_pays", right_on="nom_pays")
    donnees_graphCarto.columns = ['valeur', 'nom_pays', 'name_country', 'coordx', 'coordy']
    dC = {'valeur':list(donnees_graphCarto.valeur), 'nom_pays':list(donnees_graphCarto.nom_pays), 'coordx':list(donnees_graphCarto.coordx), 'coordy':list(donnees_graphCarto.coordy)}
    sourceCarto.data = dC

def MAJ_radio_graph1(new):
    Age_choisi = liste_age[radio1_Age.active]
    Annee_choisi = '('+ str(slider1_Annee.value) + '|nom_pays)'
    Niveau_choisi = liste_niveau[radio1_Niveau.active]

    g1.title.text = "Pourcentage de la population {} ans ayant été au {} en {} ".format(dict_age[Age_choisi], dict_niveau[Niveau_choisi], str(slider1_Annee.value))
    
    donnees_graphCarto = donnees.query("sex == 'T' and age ==@Age_choisi and niveau==@Niveau_choisi").filter(regex=Annee_choisi)
    donnees_graphCarto = donnees_graphCarto.merge(pays_countries, left_on="nom_pays", right_on="nom_pays")
    donnees_graphCarto.columns = ['valeur', 'nom_pays', 'name_country', 'coordx', 'coordy']
    dC = {'valeur':list(donnees_graphCarto.valeur), 'nom_pays':list(donnees_graphCarto.nom_pays), 'coordx':list(donnees_graphCarto.coordx), 'coordy':list(donnees_graphCarto.coordy)}
    sourceCarto.data = dC
    
def MAJ_slider_graph2(attr,old,new):
    annee_choisie = str(slider2_Annee.value)
    dM=donnees2564.query('sex =="M"').filter(regex='({}|nom_pays)'.format(annee_choisie)).sort_values(by=[annee_choisie], ascending=0).head(10)
    dF=donnees2564.query('sex =="F"').filter(regex='({}|nom_pays)'.format(annee_choisie)).sort_values(by=[annee_choisie], ascending=0).head(10)
    
    PM=["{} : {}%".format(dM["nom_pays"].iloc[i],str(dM[annee_choisie].iloc[i])) for i in range(10)]
    PF=["{} : {}%".format(dF["nom_pays"].iloc[i],str(dF[annee_choisie].iloc[i])) for i in range(10)]

    df = {"F":[float(i) for i in dF[annee_choisie]],
         "M":[-float(i) for i in dM[annee_choisie]],
         "rang":range(1,11),
         "PM" : PM,
         "PF" : PF,
         "CF": magma(100)[55:95:4],
         "CM": viridis(100)[50:90:4],
         "citationM" : [-(dM[annee_choisie].iloc[i]+len(PM[i])*0.6)/2 for i in range(10)],
         "citationF" : [(dF[annee_choisie].iloc[i]-len(PF[i])*0.6)/2 for i in range(10)]}
    Source2.data = df
    
def MAJ_select_graph3(attr,old,new):
    Age_choisi = liste_age[radio3_Age.active]
    Niveau_choisi = liste_niveau[radio3_Niveau.active]
    Pays_choisi = select3_Pays.value
    
    g3.title.text = "Evolution du pourcentage de femmes et d'hommes {} ans ayant été au {} en/au {}".format(dict_age[Age_choisi],dict_niveau[Niveau_choisi], Pays_choisi)

    donnees_grapFM = donnees.query("sex != 'T' and age==@Age_choisi and nom_pays==@Pays_choisi and niveau==@Niveau_choisi").filter(regex='(sex|2018|2017|2016|2015|2014|2013|2012|2011|2010|2009|2008|2007|2006|2005|2004|2003|2002|2001|2000|1999|1998|1997|1996|1995|1994|1993|1992)').transpose()
    donnees_grapFM.columns = list(donnees_grapFM.iloc[0])
    donnees_grapFM = donnees_grapFM[1:]
    donnees_grapFM['annee'] = pandas.to_datetime(liste_annee)
    
    dFM = {'F':list(donnees_grapFM.F), 'M':list(donnees_grapFM.M), 'annee':list(donnees_grapFM.annee), 'annee2':liste_annee}
    SourceFM.data = dFM

def MAJ_radio_graph3(new):
    Age_choisi = liste_age[radio3_Age.active]
    Niveau_choisi = liste_niveau[radio3_Niveau.active]
    Pays_choisi = select3_Pays.value

    g3.title.text = "Evolution du pourcentage de femmes et d'hommes {} ans ayant été au {} en/au {}".format(dict_age[Age_choisi],dict_niveau[Niveau_choisi], Pays_choisi)    

    donnees_grapFM = donnees.query("sex != 'T' and age==@Age_choisi and nom_pays==@Pays_choisi and niveau==@Niveau_choisi").filter(regex='(sex|2018|2017|2016|2015|2014|2013|2012|2011|2010|2009|2008|2007|2006|2005|2004|2003|2002|2001|2000|1999|1998|1997|1996|1995|1994|1993|1992)').transpose()
    donnees_grapFM.columns = list(donnees_grapFM.iloc[0])
    donnees_grapFM = donnees_grapFM[1:]
    donnees_grapFM['annee'] = pandas.to_datetime(liste_annee)
    
    dFM = {'F':list(donnees_grapFM.F), 'M':list(donnees_grapFM.M), 'annee':list(donnees_grapFM.annee), 'annee2':liste_annee}
    SourceFM.data = dFM
    
def MAJ_slider_graph4(attr,old,new):
    lab = liste_equ_niveau
    couleurs = ['yellow',"orange", 'red']
    Age_choisi = liste_age[radio4_Age.active]
    Annee_choisi = '(niveau|' + str(slider4_Annee.value) + ')'
    
    g4F.title.text = "Femmes {} ans en {}".format(dict_age[Age_choisi],str(slider4_Annee.value))
    g4M.title.text = "Hommes {} ans en {}".format(dict_age[Age_choisi],str(slider4_Annee.value))
    g4T.title.text = "Femmes/Hommes {} ans en {}".format(dict_age[Age_choisi],str(slider4_Annee.value))

    donnees_grapFranceF = donnees.query("sex=='F' and age==@Age_choisi and nom_pays=='France'").filter(regex=Annee_choisi)
    donnees_grapFranceM = donnees.query("sex=='M' and age==@Age_choisi and nom_pays=='France'").filter(regex=Annee_choisi)
    donnees_grapFranceT = donnees.query("sex=='T' and age==@Age_choisi and nom_pays=='France'").filter(regex=Annee_choisi)
    donnees_grapFranceF.columns = ['Niveau','Valeur']
    donnees_grapFranceM.columns = ['Niveau','Valeur']
    donnees_grapFranceT.columns = ['Niveau','Valeur']
    
    camembertF = list(donnees_grapFranceF.Valeur)
    camembertF2 = [2*pi*i/sum(camembertF) for i in camembertF]
    camembertM = list(donnees_grapFranceM.Valeur)
    camembertM2 = [2*pi*i/sum(camembertM) for i in camembertM]
    camembertT = list(donnees_grapFranceT.Valeur)
    camembertT2 = [2*pi*i/sum(camembertT) for i in camembertT]
    
    df4 = {"Variable":lab, "PourcentageF":camembertF, "Pourcentage Femme 2":camembertF2, "PourcentageH":camembertM, "Pourcentage Homme 2":camembertM2, "PourcentageT":camembertT, "Pourcentage Tous 2":camembertT2, "couleur":couleurs}
    Source4.data = df4

def MAJ_radio_graph4(new):
    lab = liste_equ_niveau
    couleurs = ['yellow',"orange", 'red']
    Age_choisi = liste_age[radio4_Age.active]
    Annee_choisi = '(niveau|' + str(slider4_Annee.value) + ')'
    
    g4F.title.text = "Femmes {} ans en {}".format(dict_age[Age_choisi],str(slider4_Annee.value))
    g4M.title.text = "Hommes {} ans en {}".format(dict_age[Age_choisi],str(slider4_Annee.value))
    g4T.title.text = "Femmes/Hommes {} ans en {}".format(dict_age[Age_choisi],str(slider4_Annee.value))
    
    donnees_grapFranceF = donnees.query("sex=='F' and age==@Age_choisi and nom_pays=='France'").filter(regex=Annee_choisi)
    donnees_grapFranceM = donnees.query("sex=='M' and age==@Age_choisi and nom_pays=='France'").filter(regex=Annee_choisi)
    donnees_grapFranceT = donnees.query("sex=='T' and age==@Age_choisi and nom_pays=='France'").filter(regex=Annee_choisi)
    donnees_grapFranceF.columns = ['Niveau','Valeur']
    donnees_grapFranceM.columns = ['Niveau','Valeur']
    donnees_grapFranceT.columns = ['Niveau','Valeur']
    
    camembertF = list(donnees_grapFranceF.Valeur)
    camembertF2 = [2*pi*i/sum(camembertF) for i in camembertF]
    camembertM = list(donnees_grapFranceM.Valeur)
    camembertM2 = [2*pi*i/sum(camembertM) for i in camembertM]
    camembertT = list(donnees_grapFranceT.Valeur)
    camembertT2 = [2*pi*i/sum(camembertT) for i in camembertT]
    
    df4 = {"Variable":lab, "PourcentageF":camembertF, "Pourcentage Femme 2":camembertF2, "PourcentageH":camembertM, "Pourcentage Homme 2":camembertM2, "PourcentageT":camembertT, "Pourcentage Tous 2":camembertT2, "couleur":couleurs}
    Source4.data = df4


## Importation des données
donnees = pandas.read_csv("donneesEducation.csv",sep=",",na_values='NaN',skipinitialspace = True)

coordonnees = pandas.read_csv("coordonnees_pays.csv", sep=";", converters={'coordx':ast.literal_eval,'coordy':ast.literal_eval})

colonne_pays = ["nom_pays", "pays"]
pays = pandas.read_excel("nomenclature.xls",sheet_name='Pays',names = colonne_pays, header = None)

colonne_niveau = ["niveau", "équivalence"]
NiveauEduc = pandas.read_excel("nomenclature.xls",sheet_name="Niveau d'éducation",names = colonne_niveau, header = None)

fp = open("countries.geojson","r",encoding='utf-8')
countries = json.load(fp)

## Traitement des données
liste_annee = [str(i) for i in range(2018,1991,-1)]
liste_sexe = list(pandas.Series(donnees.sex).unique())

# On remarque que dans la colonne niveau, il y a une erreur d'écriture pour le niveau 3-4.
print(list(pandas.Series(donnees.niveau).unique()))

# On décide d'uniformiser cette écriture par rapport aux autres niveaux.
donnees = donnees.replace('ED3_4','ED3-4')

# De plus, nous décidons d'enlever du tableau 'donnee' le niveau 'ED3-8' qui est la somme des niveaux 'ED3-4' et 'ED5-8'.
# Cette information n'apporte pas de plus value à la suite de notre étude et par conséquent, c'est une information "inutile" à garder dans le data-frame.
donnees = donnees.query("niveau != 'ED3-8'")
liste_niveau = list(pandas.Series(donnees.niveau).unique())
liste_equ_niveau = ['primaire ou moins (au maximum)','collège-lycée (au maximum)',"plus que le lycée"]
dict_niveau = {}
for i in range(len(liste_niveau)):
    dict_niveau[liste_niveau[i]]=liste_equ_niveau[i]


# On regarde la liste des pays présents dans le tableau de données 'pays'.
print(list(pandas.Series(pays.nom_pays).unique())) 

# On remarque qu'en plus des pays européens, il y a aussi des regroupements de pays (ex: 'Zone euro (17 pays)').
# Nous avons décidé de ne pas les garder pour la suite de notre application.
# Il faut donc les enlever du data frame 'pays' pour éviter de conserver des informations inutiles.
etats_a_enlever = ['Zone euro (17 pays)', 'Zone euro (18 pays)', 'Zone euro (19 pays)', 'Union européenne - 15 pays (1995-2004)', 'Union européenne - 27 pays (2007-2013)', 'Union européenne - 28 pays']

pays = pays.query('nom_pays !=@etats_a_enlever')
liste_pays = list(pandas.Series(pays.nom_pays).unique())

# On remarque aussi que dans la colonne 'age', il y a des séquences qui se chevauchent (ex:'Y45-64', 'Y45-54' et 'Y55-64').
# Nous avons décidé de garder seulement les catégories qui vont de 10 en 10 et 'Y25-64' pour la suite de notre application.
# Il faut donc les enlever du data frame 'donnees' pour éviter de conserver des informations inutiles.
ages_a_enlever = ['Y15-64', 'Y20-24', 'Y30-34', 'Y45-64']

donnees = donnees.query('age !=@ages_a_enlever')
liste_age = list(pandas.Series(donnees.age).unique())
liste_equ_age = ['entre 25 et 34','entre 25 et 64','entre 35 et 44','entre 45 et 54','entre 55 et 64']
dict_age = {}
for i in range(len(liste_age)):
    dict_age[liste_age[i]]=liste_equ_age[i]

# On crée un dataframe 'pays_countries' qui a pour colonne 'nom_pays' et 'name_country'. Il nous donne le nom anglais d'un nom français d'un pays et inversement.
# On fusionne le tableau 'pays_countries' et le tableau 'coordonnees'.
liste_paysEN = ['Austria', 'Belgium', 'Bulgaria', 'Switzerland', 'Cyprus', 'Czech Republic', 'Germany', 'Denmark', 'Estonia', 'Greece', 'Spain', 'Finland', 'France', 'Croatia', 'Hungary', 'Ireland', 'Iceland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Montenegro', 'Macedonia', 'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Serbia', 'Sweden', 'Slovenia', 'Slovakia', 'Turkey', 'United Kingdom']

pays_countries = pandas.DataFrame({'nom_pays': liste_pays, 'name_country': liste_paysEN})
pays_countries = pays_countries.merge(coordonnees, left_on="name_country", right_on="name_country")

# On fusionne le tableau 'donnees' et le tableau 'pays' pour ne pas seulement avoir l'identifiant du pays, mais son appelation entière.
donnees = donnees.merge(pays, left_on="pays", right_on="pays")

# On crée des data-frames dont chacun sera utilisé pour la création d'un des 4 graphes.
donneesFM = donnees.query("sex != 'T' and age=='Y25-34' and nom_pays=='France' and niveau=='ED3-4'").filter(regex='(sex|2018|2017|2016|2015|2014|2013|2012|2011|2010|2009|2008|2007|2006|2005|2004|2003|2002|2001|2000|1999|1998|1997|1996|1995|1994|1993|1992)').transpose()
donneesFM.columns = list(donneesFM.iloc[0])
donneesFM = donneesFM[1:]
donneesFM['annee'] = pandas.to_datetime(liste_annee)
donneesFM['annee2'] = liste_annee

donnees2564=donnees.query('niveau=="ED5-8" and age=="Y25-64"')

donneesFranceF = donnees.query("sex=='F' and age=='Y25-64' and nom_pays=='France'").filter(regex='(niveau|2018)')
donneesFranceM = donnees.query("sex=='M' and age=='Y25-64' and nom_pays=='France'").filter(regex='(niveau|2018)')
donneesFranceT = donnees.query("sex=='T' and age=='Y25-64' and nom_pays=='France'").filter(regex='(niveau|2018)')
donneesFranceF.columns = ['Niveau','Valeur']
donneesFranceM.columns = ['Niveau','Valeur']
donneesFranceT.columns = ['Niveau','Valeur']

# SourceT = ColumnDataSource(donneesT)
# Source5_8 = ColumnDataSource(donnees5_8)


## Création des widgets
div_niveau1 = Div(text="""<b>Choisir le niveau d'étude:<b>""")
div_age1 = Div(text="""<b>Choisir la tranche d'âge:<b>""")
div_niveau3 = Div(text="""<b>Choisir le niveau d'étude:<b>""")
div_age3 = Div(text="""<b>Choisir la tranche d'âge:<b>""")
div_age4 = Div(text="""<b>Choisir la tranche d'âge:<b>""")
div_titre4 = Div(text="""<b>Répartition du niveau d'études en France<b>""")

slider1_Annee = Slider(start = 1993, end = 2018, value=2018, title = "Choix de l'année", step = 1)
radio1_Age = RadioGroup(labels=liste_equ_age, active=1)
radio1_Niveau = RadioGroup(labels=liste_equ_niveau, active=2)

slider2_Annee = Slider(start = 1993, end = 2018, value=2018, title = "Choix de l'année", step = 1)

select3_Pays = Select(title="Choix du pays", value="France", options=liste_pays)
radio3_Age = RadioGroup(labels=liste_equ_age, active=0)
radio3_Niveau = RadioGroup(labels=liste_equ_niveau, active=1)

slider4_Annee = Slider(start = 1993, end = 2018, value=2018, title = "Choix de l'année", step = 1)
radio4_Age = RadioGroup(labels=liste_equ_age, active=1)


## Présentation
p = Paragraph(text="""Choix des données : Nous avons choisi de ne garder que les niveaux d'études
              suivants : ED1-2, ED3-4 et ED5-8 correspondant respectivement à «primaire ou moins»,
              «collège-lycée», «études supérieures». Au niveau des tranches d'âge, nous 
              conservons les suivantes 25-34, 25-64, 35-44, 45-54 et 55-64 afin d'éviter les séquences 
              qui se chevauchent. Pour le remplissage des cartes, nous avons eu besoin des coordonnées
              des frontières de chaque pays européens donc des données de taille importante. Afin
              d'éviter un temps de chargement très (trop) long de ces coordonnées, nous avons décidé
              de le faire en amont et d'ensuite exporter la dataframe que nous voulions obtenir vers 
              un fichier csv. De cette façon, nous avons pu obtenir des frontières nettes et un temps
              de chargement optimal. Pour obtenir la dataframe a exporté le programme a tourné pendant 
              une trentaine de minute, il était inenvisageable d'attendre tout ce temps lors de chaque
              lancement de notre application.""",
width=1500, height=60)


p1 = Paragraph(text="""Cartographie : L'utilisateur a plusieurs choix à faire 
               pour ce premier graphique : l'année, l'âge de la population 
               qu'il souhaite observer, et le niveau d'éducation qui l’intéresse.
               Cette cartographie permet de comparer entre chaque pays le pourcentage
               de la population choisie ayant le niveau d'étude sélectionné. Un code
               couleur permet de visualiser les pays ayant les parts les plus importantes
               jusqu'aux pays ayant les pourcentages les plus faibles. L'utilisateur peut
               également positionner le curseur de sa souris sur le pays qui l’intéresse
               pour avoir la valeur exacte de cette proportion observée.  """,
width=1500, height=50)

p2 = Paragraph(text="""Rang : Le deuxième graphique est une pyramide représentant les dix pays
               comprenant le plus de personnes âgées de 25 à 64 ans ayant effectué des
               études supérieures. C'est la catégorie « ED5-8 ». L'utilisateur à la
               possibilité de choisir l'année pour laquelle il souhaite connaître le
               classement. Cette pyramide met en comparaison ce rang pour les hommes
               et celui pour les femmes. Il permet de visualiser les pays où l'éducation
               est la plus haute et l'évolution du classement au cours du temps. Ce
               graphique nous permet également de comparer les pays et les pourcentages
               apparaissant dans les 10 premiers pays selon le sexe.""",
width=1500, height=50)

p3 = Paragraph(text="""Evolution : Ce troisième graphique représente l'évolution de la proportion
               de la population d'une âge et d'un pays donnés ayant le niveau d'étude
               sélectionné. L'utilisateur a donc trois choix à effectuer : pays, âge,
               niveau d'étude. Ce graphique permet de se rendre compte de l'évolution
               de l'éducation et de comparer celles- ci pour les hommes et les femmes.
               On va pouvoir constater que globalement, le niveau d'étude augmente : 
               La proportion de personnes suivants de plus hautes études augmentent, tandis
               que le pourcentage de personnes s'arrêtant à un plus bas niveau diminue.""",
width=1500, height=50)

p4 = Paragraph(text="""Répartition : Le quatrième graphique est formé de trois pie-charts : hommes,
               femmes, et les deux sexes confondus. Ces pie-charts représentent la part
               des trois niveaux d'étude dans la population du pays choisi. Le choix de
               l'année va permettre de voir clairement l'évolution de cette répartition
               au cours du temps.""",
width=1500, height=30)

layout0 = gridplot([[p],[p1],[p2],[p3],[p4]])
#curdoc().add_root(layout0)


## Graphique n°1 - Cartographie
donneesCarto = donnees.query("sex == 'T' and age =='Y25-64' and niveau=='ED5-8'").filter(regex='(2018|nom_pays)')
donneesCarto = donneesCarto.merge(pays_countries, left_on="nom_pays", right_on="nom_pays")
donneesCarto.columns = ['valeur', 'nom_pays', 'name_country', 'coordx', 'coordy']

mapper = LinearColorMapper(palette=inferno(256)[128:], low=donneesCarto["valeur"].min(), high=donneesCarto["valeur"].max())
color_bar = ColorBar(color_mapper=mapper, ticker=BasicTicker(), label_standoff=12, border_line_color=None, location=(0,0))

sourceCarto = ColumnDataSource(donneesCarto)

hover_tool1 = HoverTool(tooltips=[('Pays', '@nom_pays'),('Pourcentage', '@valeur{0.00 a} %')])

g1 = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", title="Pourcentage de la population entre 25 et 64 ans ayant été plus qu'au lycée en 2018", plot_width=700, plot_height=600)
g1.add_tile(CARTODBPOSITRON)
g1.patches(xs="coordx", ys="coordy", source = sourceCarto, line_color="white",line_width=1.5, fill_color={'field': 'valeur', 'transform': mapper})
g1.add_tools(hover_tool1)
g1.add_layout(color_bar, 'right')

slider1_Annee.on_change('value', MAJ_slider_graph1)
radio1_Age.on_click(MAJ_radio_graph1)
radio1_Niveau.on_click(MAJ_radio_graph1)

layout1 = row(column(slider1_Annee, div_age1, radio1_Age, div_niveau1, radio1_Niveau),g1)
# curdoc().add_root(layout1)


## Graphique n°2 - Rang
dM=donnees2564.query('sex =="M"').filter(regex='({}|nom_pays)'.format("2018")).sort_values(by=["2018"], ascending=0).head(10)
dF=donnees2564.query('sex =="F"').filter(regex='({}|nom_pays)'.format("2018")).sort_values(by=["2018"], ascending=0).head(10)

PM=["{} : {}%".format(dM["nom_pays"].iloc[i],str(dM["2018"].iloc[i])) for i in range(10)]
PF=["{} : {}%".format(dF["nom_pays"].iloc[i],str(dF["2018"].iloc[i])) for i in range(10)]

d = {"F":[float(i) for i in dF["2018"]],
    "M":[-float(i) for i in dM["2018"]],
    "rang":range(1,11),
    "PM" : PM,
    "PF" : PF,
    "CF": magma(100)[55:95:4],
    "CM": viridis(100)[50:90:4],
    "citationM" : [-(dM["2018"].iloc[i]+len(PM[i])*0.6)/2 for i in range(10)], #on considère qu'une lettre mesure 0.65 de largeur
    "citationF" : [(dF["2018"].iloc[i]-len(PF[i])*0.6)/2 for i in range(10)]}

Source2 = ColumnDataSource(d)

pyramide1 = figure(title="Rang des pays : pourcentage de personnes de 25 à 64 ans ayant fait des études supérieures",x_axis_label="Hommes",x_range=(-55, 0),y_range=(10.5,0.5), plot_width=600, plot_height=550)
pyramide1.hbar(y= "rang",height = 0.6,right=0,left = "M", color="CM",source = Source2)
pyramide1.yaxis.visible = False
citation= LabelSet(x="citationM",y="rang",text="PM",source=Source2,y_offset = -10)
pyramide1.add_layout(citation)
pyramide1.xaxis.major_label_overrides = dict((i,str(-i)) for i in range(-55,0,5))

pyramide2 = figure(x_axis_label="Femmes",x_range=(0, 55),y_range=(10.5,0.5), plot_width=600, plot_height=550)
pyramide2.hbar(y= "rang",height = 0.6,right="F",left = 0,color="CF", source = Source2)
citation= LabelSet(x="citationF",y="rang",text="PF",source=Source2,y_offset = -10)
pyramide2.add_layout(citation)
pyramide2.yaxis.ticker = [int(i) for i in range(1,11)]

slider2_Annee.on_change('value',MAJ_slider_graph2)
layout2 = gridplot([[slider2_Annee],[pyramide1,pyramide2]])
#curdoc().add_root(layout2)


## Graphique n°3 - Evolution
SourceFM = ColumnDataSource(donneesFM)
hover_tool3 = HoverTool(tooltips=[('Année', '@annee2'), ( 'Pourcentage Femme',   '@F{0.00 a} %'),( 'Pourcentage Homme',   '@M{0.00 a} %')])
g3 = figure(title = "Evolution du pourcentage de femmes et d'hommes entre 25 et 34 ans ayant été au collège (au maximum) en France", x_axis_type='datetime', plot_width=1000, plot_height=650)
g3.line(x="annee", y="F", source=SourceFM, color = '#CB3E71', legend = 'Femme',line_width=5)
g3.line(x="annee", y="M", source=SourceFM, color = '#20908C', legend = 'Homme',line_width=5)
g3.xaxis.axis_label = 'Année'
g3.yaxis.axis_label = 'Pourcentage (%)'
g3.legend.location="top_center"
g3.add_tools(hover_tool3)

select3_Pays.on_change('value',MAJ_select_graph3)
radio3_Age.on_click(MAJ_radio_graph3)
radio3_Niveau.on_click(MAJ_radio_graph3)

layout3 = row((column(select3_Pays, div_age3, radio3_Age, div_niveau3, radio3_Niveau)),g3)
# curdoc().add_root(layout3)


## Graphique n°4 - Répartition France
lab = liste_equ_niveau
couleurs = ['yellow',"orange", 'red']
camembertF = list(donneesFranceF.Valeur)
camembertF2 = [2*pi*i/sum(camembertF) for i in camembertF]
camembertM = list(donneesFranceM.Valeur)
camembertM2 = [2*pi*i/sum(camembertM) for i in camembertM]
camembertT = list(donneesFranceT.Valeur)
camembertT2 = [2*pi*i/sum(camembertT) for i in camembertT]

df2 = {"Variable":lab, "PourcentageF":camembertF, "Pourcentage Femme 2":camembertF2, "PourcentageH":camembertM, "Pourcentage Homme 2":camembertM2, "PourcentageT":camembertT, "Pourcentage Tous 2":camembertT2, "couleur":couleurs}

Source4 = ColumnDataSource(df2)

hover_tool_4F = HoverTool(tooltips=[( 'Pourcentage',   '@PourcentageF{0.00 a} %')])
hover_tool_4M = HoverTool(tooltips=[( 'Pourcentage',   '@PourcentageH{0.00 a} %')])
hover_tool_4T = HoverTool(tooltips=[( 'Pourcentage',   '@PourcentageT{0.00 a} %')])

g4F = figure(title = "Femmes entre 25 et 64 ans en 2018",plot_width=350, plot_height=350)
g4F.wedge(x=0, y=1, radius=0.7, start_angle=cumsum('Pourcentage Femme 2',include_zero=True), end_angle = cumsum('Pourcentage Femme 2'), line_color="white", fill_color='couleur', legend='Variable', source = Source4)
g4F.add_tools(hover_tool_4F)

g4M = figure(title = "Hommes entre 25 et 64 ans en 2018",plot_width=350, plot_height=350)
g4M.wedge(x=0, y=1, radius=0.7, start_angle=cumsum('Pourcentage Homme 2',include_zero=True), end_angle = cumsum('Pourcentage Homme 2'), line_color="white", fill_color='couleur', legend='Variable', source = Source4)
g4M.add_tools(hover_tool_4M)

g4T = figure(title = "Femmes/Hommes entre 25 et 64 ans en 2018",plot_width=350, plot_height=350)
g4T.wedge(x=0, y=1, radius=0.7, start_angle=cumsum('Pourcentage Tous 2',include_zero=True), end_angle = cumsum('Pourcentage Tous 2'), line_color="white", fill_color='couleur', legend='Variable', source = Source4)
g4T.add_tools(hover_tool_4T)

slider4_Annee.on_change('value',MAJ_slider_graph4)
radio4_Age.on_click(MAJ_radio_graph4)

layout4 = column(row((column(div_titre4, slider4_Annee, div_age4, radio4_Age, width=350)),g4T),row(g4F, g4M))
# curdoc().add_root(layout4)


## TabPanel
tab0 = Panel(child=layout0, title="Présentation")
tab1 = Panel(child=layout1, title="Cartographie")
tab2 = Panel(child=layout2, title="Rang")
tab3 = Panel(child=layout3, title="Evolution")
tab4 = Panel(child=layout4, title="Répartition en France")
tabs = Tabs(tabs = [tab0, tab1, tab2, tab3, tab4])

curdoc().add_root(tabs)