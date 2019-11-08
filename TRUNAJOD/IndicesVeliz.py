# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:34:13 2018

@author: Bruko
"""

import os
import re
import numpy as np
import pandas as pd
from math import log
from .Silabizator import Silabizer


def IndicesVeliz(doc):
    """ Entrega la lista de índices en un diccionario
      
    Argumentos:
        doc: texto tokenizado
        ver: verdadero si debe mostrar algo
    
    Salida:
        string: Agrega a [global html] una tabla con la salida de spacy
    """		
    frec = FrecuenciaCREA()
    dataFCI = ImagFamiConc()
    dtConju = CargarConjugaciones()

    doc = CorrectorDeArbol(doc, dtConju)

    salida = {
        "Promedio Longitud Palabras sílaba": NSilabas(doc) / NPalabras(doc),
        "Promedio Longitud Palabras letra": PromedioLongitudPalabras(doc),
        "Promedio Longitud Oracion": PromedioLongitudOracion(doc),
        "Promedio Longitud Cláusula": PromedioLongitudClausula(doc),
        "Densidad de Cláusula": Subordinacion(doc),
        "Palabras antes de la raíz": PalabrasAntesRoot(doc),
        "Densidad Número de 1,2 persona": PrimeraSegundaPersona(doc) / NPalabras(doc),
        "Densidad de la Frase Nominal": DensidadFraseNominal(doc),
        "Diversidad léxica MTLD": DiversidadLexicaMTLD(doc),
        "Similaridad Sintáctica": SimilaridadSintactica(doc),
        "Densidad Léxica": DensidadLexica(doc),
        "Índice de frecuencia": IndiceFrecuencia(doc, frec),
        "Palabras de conexión de base lógica": PalabrasConexion(doc),
        "Densidad de negación": DensidadDeNegacion(doc),
        "Verbos / Sustantivos": VerbosPorNombres(doc),
        "Disimilaridad PoS por oración": DisimiliradiadPoS(doc)
    }

    posL = ['NOUN|PROPN', 'NOUN', 'ADJ', 'ADV|ADP', 'VERB|AUX']
    for i in posL:
        salida["Densidad de " + i] = ProporcionPOS(doc, i)
        kwaList = ["concreteness", "imageability", "familiarity"]
        kwaValores = IndiceImagFamiConc(doc, dataFCI)

    i = 0
    for kwa in kwaList:
        salida[kwa] = kwaValores[i]
        i = i + 1

    return salida


def IndiceImagFamiConc(doc, dataFCI, ver=False):
    """ Índice de Imaginabilidad, Familiaridad o Concreción (IFC)

    Argumentos:
        doc : texto tokenizado
        dataset dataFCI: valor de IFC por palabra (global)
        bool ver: verdadero, muestra los detalles del cálculo

    Salida:
        float: promedio de IFC de cada sustantivo que tiene valor de concreción

    """

    n = [0, 0, 0]
    total = [0, 0, 0]
    ploce = ""
    aviso = False
    kwaList = ["concreteness", "imageability", "familiarity"]
    for token in doc:
        stro = ""
        aviso = False
        if (token.pos_ == "NOUN"):
            mot = token.lemma_
            i = 0
            for kwa in kwaList:
                ploc = dataFCI[dataFCI["word"] == mot.lower()][kwa]
                if (len(ploc) > 0) and (ploc.iloc[0] > 0):
                    n[i] = n[i] + 1
                    total[i] = total[i] + ploc.iloc[0]
                    ploce = round(ploc.iloc[0], 3)
                    aviso = True
                    stro = stro + "(" + kwa[0] + ": " + str(ploce) + ") "
                i += 1

        else:
            aviso = False
            ploc = 0
        MarcarTexto("Índice IFC", token, aviso, ver, stro)
    i = 0
    for kwa in kwaList:
        if n[i] > 0:
            total[i] = total[i] / n[i]
        else:
            total[i] = 0
        i = i + 1
    return total


def DistribucionPoS(doc):
    quoi = {}
    for token in doc:
        if token.pos_ not in quoi:
            quoi[token.pos_] = 0
        quoi[token.pos_] = quoi[token.pos_] + 1
    return quoi


def DisimiliradiadPoS(doc, ver=False):
    global html
    DistPoS = []
    Disimil = 0
    frases = []

    for sen in doc.sents:
        DistPoS.append(DistribucionPoS(sen))
        frases.append(sen)

    for i in range(len(DistPoS) - 1):
        b = DistPoS[i].copy()
        b.update(DistPoS[i + 1])
        dif = 0
        tot = 0
        for pos in b:
            if pos not in DistPoS[i]:
                vali = 0
            else:
                vali = DistPoS[i][pos]
            if pos not in DistPoS[i + 1]:
                vali1 = 0
            else:
                vali1 = DistPoS[i + 1][pos]

            dif = dif + abs(vali - vali1)
            tot = tot + vali + vali1
        Disimil = Disimil + dif / tot
        if(ver):
            html = html + "<br>Comparando <b> " + str(frases[i]) + "</b> con <b>" + str(frases[i + 1]) + "</b>: " + str(dif) + " / " + str(tot)
    if len(DistPoS) > 1:
        return Disimil / (len(DistPoS) - 1)
    else:
        return 0


def VerbosPorNombres(doc, ver=False):
    """ Entrega la división entre el total de verbos (VERB|AUX) por el
    total de nombres (NOUN|PROPN)

    Argumentos:
        doc : texto tokenizado
        bool ver: verdadero, muestra los detalles del cálculo

    Salida:
        float: verbos / nombres
    """
    nv = ProporcionPOS(doc, 'VERB|AUX', False)
    nn = ProporcionPOS(doc, 'NOUN|PROPN', False)
    if nn > 0:
        return (nv / nn)
    else:
        return 0


def DensidadDeNegacion(doc, ver=False):
    """ Entrega la proporción de palabras de negación


    Argumentos:
        doc :    texto tokenizado
        bool ver :    booleano que indica si quiere mostrarse el detalle

    Salida:
        float :    poporción palabras de negación

    """
    aviso = False
    k = 0
    n = 0
    for token in doc:
        if (token.pos_ != "PUNCT") and (token.pos_ != "SPACE"):
            n = n + 1
            if (
                    (token.lemma_.lower() == "no") or (token.lemma_.lower() == "ni") or 
                    (token.lemma_.lower() == "nunca") or (token.lemma_.lower() == "jamás") or
                    (token.lemma_.lower() == "jamás") or (token.lemma_.lower() == "tampoco") or
                    (token.lemma_.lower() == "nadie") or (token.lemma_.lower() == "nada") or
                    (token.lemma_.lower() == "ningún") or (token.lemma_.lower() == "ninguno") or
                    (token.lemma_.lower() == "ninguna")):

                aviso = True
                k = k + 1
            else:
                aviso = False

        MarcarTexto("Densidad de negación", token, aviso, ver, k)
    return k / n


def PrimeraSegundaPersona(doc, ver=False):
    """ Total de veros/adjetivos/etc en 1 o 2 persona en el texto

    Argumentos:
        doc: texto tokenizado
        bool ver: verdadero si muestra el análisis

    Salida:
        int : nº de palabras con etiqueta 1 o 2 personas

    """
    n = 0
    regexp = re.compile('Person=1|Person=2')
    for token in doc:
        if regexp.search(token.tag_):
            aviso = True
            n = n + 1
        else:
            aviso = False

        MarcarTexto("Número de 12 persona", token, aviso, ver, n)
    return n


def PalabrasConexion(doc, ver=False):
    """ Entrega la proporción de palabras de tipo y/o/ni/si


    Argumentos:
        doc :    texto tokenizado
        bool ver :    booleano que indica si quiere mostrarse el detalle

    Salida:
        float :    poporción palabras de conexión del texto

    """
    aviso = False
    k = 0
    n = 0
    for token in doc:
        if (token.pos_ != "PUNCT") and (token.pos_ != "SPACE"):
            n = n + 1
            if ((token.lemma_.lower() == "o") or (token.lemma_.lower() == "y") or (token.lemma_.lower() == "no") or (token.lemma_.lower() == "si")):
                aviso = True
                k = k + 1
            else:
                aviso = False

        MarcarTexto("Densidad de palabras de conexión", token, aviso, ver, k)
    return k / n


def VerMarcas(doc, ver=False):
    """ Entrega la salida de spacy de doc

    Argumentos:
        doc: texto tokenizado
        ver: verdadero si debe mostrar algo

    Salida:
        string: Agrega a [global html] una tabla con la salida de spacy
    """
    global html
    if ver:
        html = html + "<p><table class='table table-striped table-sm table-borderless'><tr><th>Texto<th>Lemma<th>POS<th>TAG<th>DEP<th>Padre<th>Hijos"
        for a in doc:
            html = html + "<tr><td>" + str(a.text) + "<td>" + str(a.lemma_) + "<td>" + str(a.pos_) + "<td><font size=1>" + str(a.tag_) + "</font><td>" + str(a.dep_) + "<td>" + str(a.head) + "<td>"
            for child in a.children:
                html = html + str(child) + ", "
        html = html + "</table>"
    else:
        for a in doc:
            print(a.text, a.pos_, a.tag_, a.dep_, [child for child in a.children])


def MarcarTexto(titulo, token, aviso, ver, n):
    """ Marca la palabra en negrita si aviso=True con el valor n
      
    Argumentos:
        string titulo: encabezado
        token: palabra que debe o no marcar
        bool aviso: verdadero si marca la palabra
        ver: verdadero si debe mostrar algo
        n: valor que escribe al lado en caso de aviso ser verdadero
    
    Salida:
        string: Agrega a [global html] la palabra token y la marca (en negrita) 
        si aviso es verdadero, agregándole también el valor n entre paréntesis
    """
    if ver:
        global html
        if (len(html)==0) or html[len(html)-1]==':':
            html = html + "<p>" + titulo + ":<br>"
        if hasattr(token, 'text'):
            toklen=token.text
        else:
            toklen=token
        if aviso:
            html = html + " <b>" + toklen + " (" + str(n) + ")</b>"
        else:
            html = html + " " + toklen


def NOraciones(doc, ver=False):
    """ Entrega el número de oraciones de un texto

    El número de oraciones se considera como el número total de 
    palabras que tengan la etiqueta ROOT como dependencia (dep)

    Argumentos:
        doc :    texto tokenizado
        ver :    booleano que indica si quiere mostrarse el detalle

    Salida:
        int : nº de oraciones
    """
    n=0
    for token in doc:
        if token.dep_=="ROOT":
            n=n+1
            aviso=True
        else:
            aviso=False
        #MarcarTexto("Número de oraciones",token,aviso,ver,n)
    return n

def NPalabras(doc):
    """ Entrega el número de palabras de un texto
    
    El número de palabras se considera como el número total de 
    tokens que identifica Spacy.
    
    Ejemplo:
        "Ella pidió entregárselo".    Cuenta 3 palabras
    
    
    Argumentos:
        doc :    texto tokenizado
    
    Salida:
        int : nº de palabras
    
    """
    n=0
    for token in doc:
        if (token.pos_!="PUNCT"):
            n=n+1
    return n


def CorrectorDeArbol(doc, dtConju, ver=False):
    """ Corrige el árbol que entrega Spacy
    
    Dado que Spacy subordina los adjetivos cuando están en conjunción,
    al corregir el arbol se obtiene que todos los adjetivos quedan subordinados
    
    Ejemplo:
        En "El extenso y poderoso imperio", spacy deja poderoso subordinado a extenso,
        luego de la corrección tanto extenso como poderoso quedan subordinados a imperio.
    
    
    Argumentos:
        doc :    texto tokenizado
    
    Salida:
        texto tokenizado corregido
    
    """
    # Primero marca perífrasis po!
    for token in doc:
        if token.pos_ == "VERB" or token.pos_ == "AUX":
            conjugado = Infinitivo(dtConju, token.text)
            if conjugado is not None:
                token.lemma_ = conjugado

    pi = open("{}/verbos_i.txt".format(os.path.dirname(os.path.realpath(__file__))), "r", encoding="utf-8").read().split('\n')
    pi[:] = [x.split(' ') for x in pi]
    pp = open("{}/verbos_p.txt".format(os.path.dirname(os.path.realpath(__file__))), "r", encoding="utf-8").read().split('\n')
    pp[:] = [x.split(' ') for x in pp]
    pg = open("{}/verbos_g.txt".format(os.path.dirname(os.path.realpath(__file__))), "r", encoding="utf-8").read().split('\n')
    pg[:] = [x.split(' ') for x in pg]

    doc = MarcarPerifrasis(doc, 'VerbForm=Inf', pi)
    doc = MarcarPerifrasis(doc, 'VerbForm=Ger', pg)
    doc = MarcarPerifrasis(doc, 'VerbForm=Part', pp)
    return doc


def Infinitivo(dtConju, conjugado):
    """ obtiene la forma infinitiva de un verbo (lemma)

    Argumentos:
        dtConju: lista de palabras del texto
        conjugado: verbo conjugado que quiere conocerse su forma en infinitiov

    Salida:
        string : forma infinitiva de un verbo de $conjugado

    """
    conjugado = conjugado.lower()
    for i in dtConju.keys():
        a = dtConju["infinitive"][dtConju[i] == conjugado]
        if len(a) > 0:
            return a.iloc[0]
    return None


def MarcarPerifrasis(doc, tipo, pi):
    """ Marca las palabras no-centrales de una perífrasis con perif en DEP.
    
    [ En desarrollo ]
    
    Argumentos:
        doc :    texto tokenizado
        int tipo:    tipo
        list pi: lista de perífrasis
    
    Salida:
        doc: nuevo texto tokenizado con los marcadores en las perífrasis
     
    """
    #infinitivo
    regexp = re.compile(tipo)
    for token in doc:
        if (token.pos_=="VERB") or (token.pos_=="AUX") or regexp.search(token.tag_):
            if regexp.search(token.tag_):
                for col in pi:
                    pos = token.i - len(col)
                    if(pos>=0):
                        falla = False
                        for ro in col:
                            #print(str(ro) + " vs " + str(doc[pos].lemma_) + " " + tipo)
                            if ro.lower()!=doc[pos].lemma_:
                                falla = True
                                break
                            pos = pos + 1
                        if not falla:
                            pos = token.i - len(col) +1
                            for k in range(len(col)):
                                doc[pos].tag_=doc[pos].tag_ + "|Perif"
                                pos = pos + 1

    return doc
    

def NClausulas(doc,ver=False):   ## VerbForm=Fin
    """ Entrega el número de cláusulas finitas de un texto
    
    El número de cláusulas finitas se considera como el número total de 
    palabras que sean verbos conjugados. 
    Es decir, que tengan la etiqueta VERB o AUX como POS, y que tengan 
    la expresión "VerbForm=Fin" en POS.
    
    Argumentos:
        doc :    texto tokenizado
        bool ver :    booleano que indica si quiere mostrarse el detalle
    
    Salida:
        int :    nº de clásulas finitas
     
    """
    n=0
    #regexp = re.compile('VerbForm=Inf|VerbForm=Ger|VerbForm=Part')
    regexp = re.compile('VerbForm=Fin')
    regexperif = re.compile('Perif')
    for token in doc:
        if ((token.pos_=="VERB") or (token.pos_=="AUX")) and not regexperif.search(token.tag_):
            #if not regexp.search(token.tag_):
            if regexp.search(token.tag_):
                aviso=True
                n=n+1
                #print(token.text)
            else:
                aviso=False
        else: 
            aviso=False
        #MarcarTexto("Número de cláusulas",token,aviso,ver,n)
    return n

def NClausulasInfinitas(doc,ver=False):   ## Cuenta verbos conjugados y sin conjugar pero no considera perífrasis: (he estado) cuenta una.
    """ Entrega el número de cláusulas finitas e infinitas de un texto
    
    Calcula el total de palabras que sean verbos conjugados o sin conjugar,
    y excluye los verbos que sean perífrasis.
    
    Argumentos:
        doc :    texto tokenizado
        bool ver :    booleano que indica si quiere mostrarse el detalle
    
    Salida:
        int :    nº de clásulas finitas e infinitas
        
    Ejemplo:
        "Ella ha estudiado", entrega 1
        "Ellas deben saber para dónde ir", entrega 2
     
    """
    n=0
    #regexp = re.compile('VerbForm=Inf|VerbForm=Ger|VerbForm=Part')
    regexp = re.compile('VerbForm')
    regexperif = re.compile('Perif')
    for token in doc:
        if ((token.pos_=="VERB") or (token.pos_=="AUX") ) and not regexperif.search(token.tag_):
            #if not regexp.search(token.tag_):
            if (token.dep_!="xcomp"):# and (token.dep_!="aux"):
                aviso=True
                n=n+1
                #print(token.text)
            else:
                aviso=False
        else: 
            aviso=False
        #MarcarTexto("Número de cláusulas infinitas",token,aviso,ver,n)
    return n

def PromedioLongitudOracion(doc):
    """ Entrega el largo, en palabras, medio de las oraciones
    
    Argumentos:
        doc :    texto tokenizado
    
    Salida:
        float :  palabras / nº oraciones

    """
    if NOraciones(doc)!=0:
        return (NPalabras(doc)/NOraciones(doc))
    else:
        return 0

def PromedioLongitudClausula(doc):
    """ Entrega el número de palabras por cláusulas finitas
    
    Argumentos:
        doc :    texto tokenizado
    
    Salida:
        float :  palabras / nº cláusulas finitas

    """
    if NClausulas(doc)!=0:
        return (NPalabras(doc)/NClausulas(doc))
    else:
        return 0

def PromedioLongitudPalabras(doc,ver=False):
    """ Entrega el número de palabras por cláusulas finitas
    
    Argumentos:
        doc :    texto tokenizado
    
    Salida:
        float :  palabras / nº cláusulas finitas

    """
    n=0
    l=0
    for token in doc:
        if (token.pos_!="PUNCT") and (token.pos_!="SPACE"):
            n=n+1
            l=l+len(token.text)
            if ver:
                print(token.text + " " + token.pos_ + " " + str(len(token.text)))
                
    return (l/n)

def ProporcionPOS(doc,tipo,ver=False):
    """ Entrega la proporcion de palabras con POS=[tipo] en el documento
    
    Argumentos:
        doc :    texto tokenizado
        string tipo: Part of speech, admite expresiones regulares, p.ej. VERB|AUX
    
    Salida:
        float :  palabras con etiqueta [tipo] / total palabras

    """
    regexp = re.compile(tipo)
    n=0
    l=0
    for token in doc:
        if (token.pos_!="PUNCT") and (token.pos_!="SPACE"):
            n=n+1
            if regexp.search(token.tag_):
                l=l+1
                aviso = True
            else:
                aviso = False
        else:
            aviso = False
        #MarcarTexto("Contar ",token,aviso,ver,l)
    return (l/n)

def Subordinacion(doc):
    """ Densidad de cláusulas
    
    Argumentos:
        doc :    texto tokenizado
        
    Salida:
        float :  nº de cláusulas / nº oraciones

    """
    if NOraciones(doc)>0:
        return (NClausulas(doc)/NOraciones(doc))
    else:
        return 0

def SimilaridadDosNodos(to1,to2,primera=False,ver=False):
    """ Similaridad entre dos nodos
    
    Argumentos:
        token to1, to2: Dos nodos en el árbol según la etiqueta head
        bool primera: verdado si se trata del nodo central
        bool ver: verdadero si muestra el análisis
        
    Salida:
        int :   Similaridad de los nodos (recursivo) de los hijos de to1 y 
                to2 que tienen la misma etiqueta.

    """
    buenas = 0
    total = 0
    lista1 = []
    lista2 = []
    global html
    
    if(primera):    #Si es la primera vez, compara las palabras antes de los hijos
        if (to1.pos_==to2.pos_):
            if(ver):
                html = html + "<br>1era coincide " + str(to1.text) + " - " + str(to2.text)
            buenas = buenas + 1
        else:
            return 0
    #if(ver):
        #html = html + "<br> estoy viendo " + str(to1.text) + " con " + str(to2.text)
    for child1 in to1.children:
        total = total + 1
        for child2 in to2.children:
            if (child1.pos_==child2.pos_) and (child1 not in lista1) and (child2 not in lista2):
                buenas = buenas + 1
                lista1.append(child1)
                lista2.append(child2)
                if(ver):
                    html = html + "<br>coincide " + str(child1.text) + " - " + str(child2.text)
                buenas = buenas + SimilaridadDosNodos(child1,child2,False,ver)
                #Ya no puede usar ni child1 ni child2
            #else:
                #if(ver):
                    #html = html + "<br> No pude revisar " + str(child1.text) + " con " + str(child2.text)
    return buenas
            
def SimilaridadSintactica(doc,ver=False):
    """ Promedio de similaridad sintáctica entre oraciones continguas en el texto
    
    Argumentos:
        token to1, to2: Dos nodos en el árbol según la etiqueta head
        bool primera: verdado si se trata del nodo central
        bool ver: verdadero si muestra el análisis
        
    Salida:
        int :   Similaridad de los nodos (recursivo) de los hijos de to1 y 
                to2 que tienen la misma etiqueta.

    """
    var1=[]
    var2=[]
    t = 0
    global html
    for sen in doc.sents:
        var1=sen
        if(len(var2)>0):
            #compara entre raices
            if(ver):
                html = html + "<br>Comparando <b> " + str(var1) + "</b> con <b>" + str(var2) + "</b>"
            palabrasComunes=SimilaridadDosNodos(var1.root,var2.root,True,ver)
            if(ver):
                html = html + "<br>Coincidieron " + str(palabrasComunes) + " palabras de " + str(len(var1)+len(var2)-palabrasComunes)
            t = t + palabrasComunes/(len(var1)+len(var2)-palabrasComunes)
        var2=sen
    if(len(list(doc.sents))>1):
        return (t/(len(list(doc.sents))-1))
    else:
        return 0

'''
def NVerbosNoConjugados(doc,ver=False):
    n=0
    regexp = re.compile('VerbForm=Inf|VerbForm=Ger|VerbForm=Part')
    regexperif = re.compile('Perif')
    for token in doc:
        if ((token.pos_=="VERB") or (token.pos_=="AUX")) and not regexperif.search(token.tag_):
            if regexp.search(token.tag_):
                aviso=True
                n=n+1
            else:
                aviso=False
        else: 
            aviso=False
        MarcarTexto("Verbos no conjugados",token,aviso,ver,n)
    return n
'''

def NNombres(doc,ver=False):
    """ Total de sustantivos en el texto
    
    Argumentos:
        doc: texto tokenizado
        bool ver: verdadero si muestra el análisis
        
    Salida:
        int : nº de palabras con etiqueta NOUN o PROPN (sustantivos comunes o propios)

    """
    n=0
    for token in doc:
        if (token.pos_=="NOUN") or (token.pos_=="PROPN"):
            aviso=True
            n=n+1
        else:
            aviso=False

        #MarcarTexto("Número de sustantivos",token,aviso,ver,n)
    return n


def NSilabas(doc,ver=False):
    """ Total de sílabas del texto
    
    Argumentos:
        doc: texto tokenizado
        bool ver: verdadero si muestra el análisis
        
    Salida:
        int : nº de sílabas de todo el texto

    """
    s = Silabizer()
    m=0
    n=0
    for token in doc:
        if (token.pos_!="PUNCT"):
            aviso=True
            n=len(s(str(token)))
            m = n + m
        else:
            aviso=False

        #MarcarTexto("Número de sustantivos",token,aviso,ver,n)
    return m

def DiversidadLexica(doc,ver=False):
    """ Diversidad Léxica à la trunajod.
    
    Argumentos:
        doc: texto tokenizado
        bool ver: verdadero si muestra el análisis
        
    Salida:
        int : promedio de palabras diferentes por cada bloque de [T] palabras

    """
    m=0 # palabras hasta T
    n=0 # suma de RTTs
    k=0 # cuantas pilas ha armado
    T=10
    lista = []
    for token in doc:
        if (token.pos_!="PUNCT"):
            m=m+1
            lista.append(token.lemma_)
        if (m==T):
            n=RTT(lista)
            lista=[]
            m=0
            k=k+1
    #if (m>0):
        #n=n+RTT(lista)
        #k=k+1
    #print(lista)
    if(k>0):
        return (n/k)
    else:
        return 0

def DiversidadLexicaMTLDunLado(dok,ver=False):
    """ Diversidad Léxica según MTLD desde atrás hacia adelante
    
    Argumentos:
        dok: texto tokenizado
        bool ver: verdadero si muestra el análisis
        
    Salida:
        float : tamaño promedio de trozos de texto con RTT = 0.72

    """
    f = 0   #faktor
    k = 0   #palabras totales
    lista = []
    for token in dok:
        lista.append(token)
        k=k+1
        valo = RTT(lista)
        if (valo<0.72):
            lista=[]
            f=f+1
        #MarcarTexto("Frecuencia",token,True,ver,round(valo,2))
    if (len(lista)>0):   #Qué hace con lo que sobra
        f=f+1-(RTT(lista)-0.72)/(0.28)
        k=k+1
    if (f>0):
        return (k/f)
    else:
        return 0

def DiversidadLexicaMTLD(doc,ver=False):
    """ Diversidad Léxica según MTLD desde atrás hacia adelante promediado con de adelante hacia atrás
    
    Argumentos:
        dok: texto tokenizado
        bool ver: verdadero si muestra el análisis
        
    Salida:
        float : índice de Diversidad Léxica MTLD

    """
    lista = []
    for token in doc:
        if (token.pos_!="PUNCT"):
            lista.append(token.lemma_)
    lista2=lista[::-1]
    return ((DiversidadLexicaMTLDunLado(lista,ver)+DiversidadLexicaMTLDunLado(lista2,False))/2)
    

def RTT(lista):
    """ type-token ratio
    
    Argumentos:
        lista: lista de palabras del texto
        
    Salida:
        float : fracción de palabras diferentes en el texto.

    """
    m=len(lista)
    npl=np.asarray(lista)
    return (len(np.unique(npl))/m)


def FrecuenciaCREA():
    """ Lista de pala

    Argumentos:
        lista: lista de palabras del texto

    Salida:
        data set : cada palabra con su frecuencia absoluta y normalizada según diccionario CREA de la RAE

    """
    dt = pd.read_csv(
        "{}/crea.csv".format(os.path.dirname(os.path.realpath(__file__))),
        delimiter='\t',
        encoding="latin-1",
        dtype={'Orden': np.float16, 'Mot': object, 'Frec.absoluta': object, 'Frec.normalizada': np.float16}
    )
    dt["Frec.absoluta"] = dt["Frec.absoluta"].apply(lambda x: x.replace(',', ''))
    dt["Frec.absoluta"] = dt["Frec.absoluta"].astype(int)
    return dt


def ImagFamiConc():
    """ Imaginabilidad, Familiaridad y Concreción de palabras

    Salida:
        dataset: Valor de Imaginabilidad, Familiaridad y Concreción según EsPal
        de todas las palabras que tienen valores en algunas de ellas.

    """
    dt = pd.read_csv("{}/ImagFamiConc.csv".format(os.path.dirname(os.path.realpath(__file__))))
    return dt


def CargarConjugaciones():
    """ carga el data frame para que pueda conjugar después

    Salida:
        dataset:lista de conjugaciones

    """
    dt = pd.read_csv("{}/conjugacionesLimpo.csv".format(os.path.dirname(os.path.realpath(__file__))))
    return dt


def FrecuenciaPalabra(mot, dt):
    """ Entrega la frecuencia normalizada de la palabra

    Argumentos:
        string mot: palabra
        dataset dt: datos de frecuencia por palabra
        
    Salida:
        float: frecuencia normalizada de la palabra según CREA

    """
    ploc = dt[dt["Mot"]==mot.lower()]["Frec.normalizada"]
    if(len(ploc)==0):
        return 0
    else:
        return(ploc.iloc[0])



def IndiceFrecuencia(doc,dt,ver=False): #El mínimo de la frecuencia
    """ Índice de frecuencia
    
    Argumentos:
        doc : texto tokenizado
        dataset dt: datos de frecuencia por palabra
        bool ver: verdadero, muestra los detalles del cálculo
        
    Salida:
        float: Por cada oración, toma la palabra con menor frecuencia y promedia sus log(frecuencia)

    """
    n=0
    total=0
    for sen in doc.sents:
        mini = 99999999999999
        for token in sen:
            if (token.pos_!="PUNCT"):
                frecok = FrecuenciaPalabra(token.text,dt)
                if (frecok<mini) and (mini>0):
                    mini = frecok
                aviso=True
            else:
                aviso=False
                frecok=""
           # MarcarTexto("Frecuencia",token,aviso,ver,frecok)
        if mini>0:
            total = total + log(mini,10)
            n = n + 1
    if n>0:
        return (total/n)
    else:
        return 0


def Concrecion():
    """ Concreción de palabras
    
    Salida:
        dataset: Valor de conreción según EsPal de todas las palabras del diccionario X (usado en trunajod 1.0)

    """
    dt=pd.read_csv("{}/concrecionTr.csv".format(os.path.dirname(os.path.realpath(__file__))), delimiter=',')
    return dt

def IndiceConcrecion(doc,dt,ver=False):
    """ Índice de concreción
    
    Argumentos:
        doc : texto tokenizado
        dataset dt: valor de concreción por palabra
        bool ver: verdadero, muestra los detalles del cálculo
    
    Salida:
        float: promedio de concreción de cada sustantivo que tiene valor de concreción

    """
    
    
    n=0
    total=0
    ploce=""
    for token in doc:
        if (token.pos_=="NOUN"):
            mot = token.lemma_
            #print(mot.lower())
            ploc = dt[dt["word"]==mot.lower()]["concreteness"]
            if (len(ploc)>0) and (ploc.iloc[0]>0):
                n=n+1
                #print(ploc.iloc[0])
                total = total + ploc.iloc[0]
                ploce=round(ploc.iloc[0],3)
                aviso=True
        else:
            aviso=False
            ploc=0
        #MarcarTexto("Frecuencia",token,aviso,ver,ploce)
    if n>0:
        return (total/n)
    else:
        return 0

def PalabrasAntesRoot(doc,ver=False):           ### Contar palabras antes del verbo principal (verbo conjugado más arriba) à confirmer (MV)
    """ Palabras antes de la raíz
    
    Argumentos:
        doc : texto tokenizado
        bool ver: verdadero, muestra los detalles del cálculo
    
    Salida:
        float: por cada oración cacula el número de palabras que están antes de la raíz, 
        en caso de que la raíz sea verbo. Sino, considera que la raíz es el verbo que está
        en la posición más alta del árbol.

    """
    # Si la raíz no es verbo/aux, entonces toma el verbo/aux el más alto
    
    suma = 0
    total=0
    for sen in doc.sents:
        #Revisa si en la oración 'sen' la raíz es o no verb
        esVerb = False
        mot = sen[0]
        mot2 = sen[0].head
        achei = False
        raiz = None
        while mot != mot2:
            mot=mot.head
            mot2=mot2.head
        if (mot.dep_ == "ROOT") and ((mot.pos_ == "VERB") or (mot.pos_ == "AUX")): # ¿El ROOT es un verbo?
            esVerb = True
            raiz = mot
        if esVerb == False:
            #Busca el verbo con mayor nivel
            achei = False
            for i in range(2,4):
                if achei == False:
                    for token in sen:
                        if (token.pos_=="VERB") or (token.pos_=="AUX"):
                            if Nivel(token.i,doc)==i:
                                raiz = token
                                achei = True
                                break
        
        motsAvant=0
        hay = False
        if 'raiz' in locals():
            aviso = False
            for token in sen:
                if (token==raiz) and (achei or esVerb):
                    hay = True
                    total=total+1
                    suma=suma+motsAvant
                    aviso=False
                else:
                    if (hay==False) and (token.pos_!="PUNCT") and (achei or esVerb):
                        motsAvant=motsAvant+1
                        aviso=True
                    else:
                        aviso=False
                
                #MarcarTexto("Palabras antes de la raíz",token,aviso,ver,motsAvant)
        else:
            suma = 0
    if(total>0):
        return (suma/total)
    else:
        return 0


def DensidadFraseNominal(doc,ver=False):    ### Contar hijos de NOUN y PROPN 
    """ Densidad de la frase nominal
    
    Argumentos:
        doc : texto tokenizado
        bool ver: verdadero, muestra los detalles del cálculo
    
    Salida:
        float: Por cada sustantivo cuenta sus modifcadores (hijos) que no sean del tipo
        cc (y,o) ni case. Entrega el número de modificadores totales / sustantivos totales

    """
    
    #diferentes de ADP y CC (otro: con o sin coordinados: conj)
    #Qué hacer con FN compuestas por más de un N
    nouns = NNombres(doc)
    hijos = 0
    for sen in doc.sents:
        for token in sen:
            if (token.head.pos_ == "NOUN") or (token.head.pos_ == "PROPN"):
                if ((token.text.upper() == 'AL') or (token.text.upper() == 'DEL')) or \
                   ((token.dep_ != "cc") and (token.dep_ != "case") and (token.pos_ != "PUNCT") and \
                   (token.head != token) and (token.dep_ != "cop")):  # and (token.dep_ != "conj") 
                    hijos = hijos + 1
                    aviso = True
                    #print(str(token) + " - " + str(token.head) + " - " + str(token.head.pos_))
                else:
                    aviso = False
            else:
                aviso = False
            #MarcarTexto("Densidad Frase Nominal",token,aviso,ver,hijos)
    if nouns==0:
        return 0
    else:
        return (hijos/nouns)
# contar adv, 
# comparar grafos


def DensidadLexica(doc,ver=False):
    """ Densidad léxica
    
    Argumentos:
        doc : texto tokenizado
        bool ver: verdadero, muestra los detalles del cálculo
    
    Salida:
        float: total de palabras de significado (verbos, adjetivos, sustantivos o adverbios) / total de palabras

    """
    return ProporcionPOS(doc,"VERB|AUX|ADJ|NOUN|PROPN|ADV")

    
#índice de inscrustación: profundiad del árbol

def GuardarHtml():
    global html
    file = open('trunajod.html', 'w+')
    file.write(html)
    file.close()
    
def MostrarHtml():
    global html
    print(html)

#Mide la profundidad del árbol, considerando los saltos entre NOUN y VERB/AUX





####  Otras funciones

def Nivel(i,doc):
    """ Nivel de la palabra
    
    Argumentos:
        doc : texto tokenizado
        int i: posición de la palabra en el texto
    
    Salida:
        int: En qué nivel del árbol se encuentra la palabra, donde 1 es cuando es raíz, 2 es hijo de la raíz, etc.

    """
    mot = doc[i]
    mot2 = doc[i].head
    n = 1
    while mot != mot2:
        mot=mot.head
        mot2=mot2.head
        n = n  + 1
    return n



