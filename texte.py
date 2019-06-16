#! /usr/bin/env python3

#
# Génération de texte
# Copyright (C) 2019 Ewenak@github
#
# Génération de texte is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Génération de texte is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Génération de texte; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

#TODO phrases négatives

import random

#Données

# True : verbe transitif 
# False : verbe intransitif
verbes = {'manger': {'groupe': 1, 'radical': 'mang', 'transitif': True}, 
          'courir': {'groupe': 3, 'radical': 'cour', 'transitif': False},
          'dormir': {'groupe': 3, 'radical': 'dor', 'transitif': False}, 
          'marcher': {'groupe': 1, 'radical': 'march', 'transitif': False}, 
          'faire': {'groupe': 3, 'radical': 'fai','transitif': True},
          'fabriquer': {'groupe': 1, 'radical': 'fabriqu', 'transitif': True}, 
          'rigoler': {'groupe': 1, 'radical': 'rigol', 'transitif': False}, 
          'parler': {'groupe': 1, 'radical': 'parl', 'transitif': False}, 
          'boire': {'groupe': 3, 'radical': 'boi', 'transitif': True},
          'casser': {'groupe': 1, 'radical': 'cass', 'transitif': True}, 
          'applaudir': {'groupe': 2, 'radical': 'applaud', 'transitif': True},
          'être': {'groupe': 3, 'radical': '', 'transitif': True}}
verbes_transitifs = [ k for k, v in verbes.items() if v['transitif'] ]
conjugaisons = {
    'indicatif': {
        'présent' : {
            1: ['e', 'es', 'e', 'ons', 'ez', 'ent'],
            2: ['is', 'is', 'it', 'issons', 'issez', 'issent']
        },
        'imparfait': {
            1: ['ais', 'ais', 'ait', 'ions', 'iez', 'aient'],
            2: ['issais', 'issais', 'issait', 'issions', 'issiez', 'issaient']
        }
    }
}
conjug_3e = { 'boire': ['bois', 'bois', 'boit', 'buvons', 'buvez', 'boivent'],
              'courir': ['cours', 'cours', 'court', 'courons', 'courez', 'courent'],
              'dormir': ['dors', 'dors', 'dort', 'dormons', 'dormez', 'dorment'],
              'faire': ['fais', 'fais', 'fait', 'faisons', 'faites', 'font'],
              'être': ['suis', 'es', 'est', 'sommes', 'êtes', 'sont']}

noms = {'m': ['papier', 'ordinateur', 'mot', 'casse-croûte', 'véhicule', 'métier', 'verre', 'bois', 'boa', 'schtroumpf'], 
        'f': ['nourriture', 'couverture', 'arrivée', 'tente', 'voiture', 'nature']}
adjectifs = {'m':['noir', 'bleu', 'beau', 'rigolo', 'bizarre', 'breton', 'lumineux', 'grand', 'transparent', 'énorme', 
                  'schtroumpf'],
            'f':['noire', 'bleue', 'belle', 'rigolote', 'bizarre', 'bretonne', 'lumineuse', 'grande', 'transparente', 
                 'énorme', 'schtroumpf']}
adj_devant_nom = ['beau', 'grand', 'belle', 'grande']
adj_changeant_radical_voyelles = {'beau': 'bel', 'nouveau': 'nouvel', 'vieux': 'vieil'}
pronoms_personnels = {'je': 0, 'tu': 1, 'il': 2, 'elle': 2, 'nous': 3, 'vous': 4, 'ils': 5, 'elles': 5}
determinants = {'m':['le', 'un', 'mon', 'ce', 'notre', 'votre', 'son', 'ton', 'leur'],
                'f':['la', 'une', 'ma', 'cette', 'notre', 'votre', 'sa', 'ta', 'leur'],
                'pl':['les', 'des', 'mes', 'ces', 'nos', 'vos', 'ses', 'tes', 'leurs']}
adverbes = ['rapidement', 'bien', 'bruyamment', 'calmement', 'sans effort', 'schtroupfement']
prepositions_lieu = ['à', 'sur', 'dans']
voyelles = 'aeiouyéèà'
structures_phrase = [['sgn', 'v', 'adv'], ['sgn', 'v'], ['sgn', 'vt', 'gn'], ['sgn', 'vt', 'gn', 'adv'],
                     ['adv', ',', 'sgn','v'], ['pp', 'v'], ['pp', 'v', 'adv'], ['pp', 'vt', 'gn', 'adv'],
                     ['adv', ',', 'pp', 'vt', 'gn'], ['sgn', 'vt', 'gn', 'ccl'], ['pp', 'vt', 'gn', 'adv', 'ccl'], 
                     ['adv', ',', 'sgn', 'vt', 'gn', 'ccl'], ['v', '-', 'pp', 'adv', '?'], 
                     ['Est-ce que', 'sgn', 'v', '?']]
pluriel_en_als = ['aval', 'bal', 'banal', 'bancal', 'cal', 'carnaval', 'cérémonial', 'choral', 'étal', 'fatal', 'festival',
             'natal', 'naval', 'récital', 'régal', 'tonal', 'pal', 'val', 'virginal']
pluriel_en_aux = ['bail', 'corail', 'émail', 'gemmail', 'soupirail', 'travail', 'vantail', 'vitrail']
pluriel_en_eus_aus = ['bleu', 'émeu', 'landau', 'lieu', 'pneu', 'sarrau']
pluriel_en_oux = ['bijou', 'caillou', 'chou', 'genou', 'hibou', 'joujou', 'pou']

def pluriel(mot):
    '''La fonction pluriel prend en paramètre
    un adjectif ou un nom et le renvoie au pluriel'''
    if mot[-1] in 'szx':
        return mot
    elif (mot[-2:] in ['au', 'eu'] or mot in pluriel_en_oux) and (not mot in pluriel_en_eus_aus):
        return mot + 'x'
    elif mot[-2:] == 'al' and not mot in pluriel_en_als:
        return mot[:-2] + 'aux'
    elif mot in pluriel_en_aux:
        return mot[:-3] + 'aux'
    else:
        return mot + 's'

def groupe_nominal(det=None, nom=None, adj=None, genre=None, nombre=None):
    '''Renvoie un groupe nominal (gn) dont
    on peut spécifier certaines choses'''
    gn = []
    if genre is None:
        genre = random.choice(['f', 'm'])
    if nombre is None:
        nombre = random.choice(['s', 'p'])
    if det is None:
        det = random.choice(determinants[genre]) if nombre == 's' else random.choice(determinants['pl'])
    if adj is None:
        adj = random.choice(adjectifs[genre])
    if nom is None:
        nom = random.choice(noms[genre])
    #Pluriel
    if nombre == 'p':
        adj = pluriel(adj)
        nom = pluriel(nom)
    if adj in adj_devant_nom:
        gn = [det, adj, nom]
    else:
        gn = [det, nom, adj]
    
    #Correction de l'orthographe du déterminant en fonction du mot qu'il y a après
    if gn[1][0] in voyelles:
        if det in ('le', 'la'):
            gn[0] = "l'"
        elif det in ('ma', 'sa', 'ta'):
            gn[0] = det[:-1] + 'on'
        elif det == 'ce':
            gn[0] = 'cet'
            
    return {'contenu': gn, 'nombre': nombre, 'genre': genre, 'det': det, 'nom': nom, 'adj': adj}

def conjugaison(verbe, personne, temps='pi'): # pi = présent indicatif, imp = imparfait (indicatif)
    '''Conjugue le verbe passé en paramètre
    au temps et à la personne voulus'''
    if verbes[verbe]['groupe'] == 3:
        return conjug_3e[verbe][personne]
    cara_verbe = verbes[verbe]
    radical = cara_verbe['radical']
    groupe = cara_verbe['groupe']
    terminaison = conjugaisons['indicatif']['présent' if temps == 'pi' else 'imparfait'][groupe][personne]
    if groupe == 1:
        return radical + ('e' if (terminaison[0] in ['a', 'o', 'u'] and radical[-1] == 'g') else '') + terminaison
    elif groupe == 2:
        return radical + terminaison
    return f'[{verbe}]'

def complement_lieu(prep=None, gn=None):
    'Génère complément circonstanciel de temps'
    if prep is None:
        prep = random.choice(prepositions_lieu)
    if gn is None:
        gn = groupe_nominal()
    return {'contenu': [prep] + gn['contenu'], 'prep': prep, 'gn': gn}

def genere_phrase(structure=None, temps=None, sujet=None, verbe=None, cod=None, adv=None, ccl=None):
    'Génère une phrase'
    phrase = []
    if structure is None:
        structure_phrase = random.choice(structures_phrase)
    else:
        structure_phrase = structure
    if temps is None:
        temps = random.choice(['pi', 'imp'])
    personne = 2
    
    if verbe is None:
        verbe_infinitif = (random.choice([ v for v in verbes.keys() if not v == 'être']) if 'v' in structure_phrase
                           else random.choice(list(verbes_transitifs)))
    else:
        verbe_infinitif = verbe
    
    #Définition de la personne
    if sujet is None:
        if 'pp' in  structure_phrase:
            sujet = random.choice(list(pronoms_personnels.keys()))
            personne = pronoms_personnels[sujet]
        else:
            sujet = groupe_nominal()
    else:
        if isinstance(sujet, str):
            personne = pronoms_personnels[sujet]
        else: 
            if sujet['nombre'] == 's':
                personne = 2 
            else:
                personne = 5
    
    for nature in structure_phrase:
        if nature == 'pp':
            pp = sujet
            if pp == 'je' and verbe_infinitif[0] in voyelles:
                pp = "J'"
            phrase.append(pp)
        elif nature == 'sgn':
            if sujet is None:
                gn = groupe_nominal()
                sujet = gn
            else:
                gn = sujet
            if gn['nombre'] == 'p':
                personne = 5
            for m in gn['contenu']:
                phrase.append(m)
        elif nature == 'gn':
            if cod is None:
                gn = groupe_nominal()
            else:
                gn = cod
            for m in gn['contenu']:
                phrase.append(m)
        elif nature == 'v':
            phrase.append(conjugaison(verbe_infinitif, personne, temps))
        elif nature == 'vt':
            phrase.append(conjugaison(verbe_infinitif, personne, temps))
        elif nature == 'adv':
            adv = random.choice(adverbes) if adv is None else adv
            phrase.append(adv)
        elif nature == 'ccl':
            ccl = complement_lieu() if ccl is None else ccl
            for m in ccl['contenu']:
                phrase.append(m)
        elif nature == ',':
            phrase.append(',')
        elif nature == '?':
            phrase.append('?')
        elif nature == '-':
            if sujet[0] in voyelles:
                if conjugaison(verbe_infinitif, personne, temps)[-1] in 'dt':
                    phrase.append('-')
                else:
                    phrase.append('-t-')
            else:
                phrase.append('-')
        elif nature == 'Est-ce que':
            phrase.append('Est-ce que')

    return phrase

def finalise_phrase(phrase):
    if phrase[-1] == '?':
        return ' '.join(phrase).replace(' , ', ', ').replace("' ", "'").capitalize().replace(' - ', '-').replace(' -t- ', '-t-')
    else:
        return (' '.join(phrase).replace(' , ', ', ').replace("' ", "'") + '.').capitalize()

phrases = []
if __name__ == '__main__':
    for x in range(0, 100):
        phrase = genere_phrase()
        phrases.append(finalise_phrase(phrase))
        print(phrases[-1])