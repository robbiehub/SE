from math import sqrt
##### Distancia Euclidiana #####
"""
Regresa un puntuaje de similaridad para una persona1 y una persona2 basado en la distancia
Parametros:
    prefs - Un diccionario con personas y sus puntuajes en diferentes objetos.
    person1, person2 - La personas que se van a comparar.
"""
def sim_distance(prefs,person1,person2):
    # Crea una lista vacia
    si={}

    #Aqui busca que objetos tienen en comun.
    for item in prefs[person1]:
        if item in prefs[person2]:
            #Si tienen un objeto en comun se agrega a la lista con el valor 1.
            si[item]=1

    # Si no tienen un objeto en comun, regresa 0
    if len(si)==0: return 0

    # Aqui suma los cuadrados de la diferencias de las personas
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                        for item in prefs[person1] if item in prefs[person2]])
    return 1/(1 + sum_of_squares)

##### Pearson Correlation Score#####
"""
Esta funcion regresa la correlacion de Pearson entre dos personas.
Parametros:
    prefs - Un diccionario con personas y sus preferencias
    p1, p2 - Personas a comparar
"""
def sim_pearson(prefs,p1,p2):
    # Consigue una lista con los objetos en comun
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1

    # Cuenta los objetos en comun
    n=len(si)

    # Si no tienen algo en comun regresa 0
    if n==0: return 0

    # Suma las preferencias de cada persona
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    # Suma el cuadrado de cada preferencia de cada persona
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

    # Suma el producto de preferencias de dos personas.
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # Calcula la correlacion de Pearson
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    r=num/den
    return r

##### Calificar criticos #####
"""
Funcion que regresa personas con gustos similares
Parametros:
    prefs - Diccionario con personas y sus preferencias
    person - Persona a comparar
    Opcionales:
        n - Numero de resultados deseados, por default es 5
        similarity = Metodo de comparacion, por default es Pearson
"""
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    # Crea una lista con las personas y que tan similares son con la persona deseada.
    scores=[(similarity(prefs,person,other),other)
                for other in prefs if other!=person]

    # Organiza la lista para que los que tengan un score alto queden primero
    scores.sort( )
    scores.reverse( )
    return scores[0:n]

##### Recomendaciones #####
"""
Funcion que regresa recomendaciones para una persona utilizando una normal con peso
basada en las preferncias de otras personas.

Parametros:
    prefs - Diccionario con personas y sus preferncias
    person - Persona a la que le vamos a recomendar
    [Opcional] similarity - Metodo de comparacion, por default es Pearson
"""
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    #Inicia la comparacion entre las personas
    for other in prefs:
        # Evitar que 'person' se compare con si mismo
        if other==person: continue

        # Obtiene que tan similar es 'other' con 'person'
        sim=similarity(prefs,person,other)

        # Ignora puntuajes de 0 o menor
        if sim<=0: continue

        for item in prefs[other]:
            # Solo toma en cuenta objetos que 'person' no tiene
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * Score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim

                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim

    # Crea una lista normalizada
    rankings=[(total/simSums[item],item) for item,total in totals.items( )]

    # Regresa la lista organizada
    rankings.sort()
    rankings.reverse()
    return rankings

##### Swapperino #####
#En esta funcion se cambia la lista de criticos por una lista de peliculas.
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person
            result[item][person]=prefs[person][item]
    return result

##### Construir un dataset para comparar items #####
"""
Funcion que regresa un diccionario de objetos que muestra que otros objetos son similares a el.
Parametros:
    prefs - Diccionario con personas y sus preferencias
"""
def calculateSimilarItems(prefs,n=10):
    result={}

    # Invierte el diccionario para que se centrada en los objetos y no en las personas.
    itemPrefs=transformPrefs(prefs)
    c=0

    for item in itemPrefs:
        # La variable c es usada para dar informacion del status para datasets grandes
        c+=1
        # Imprime un status si es necesario
        if c%100==0: print "%d / %d" % (c,len(itemPrefs))
        # Busca otros objetos similares
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result

"""
Recomienda objetos usando el dataset de la funcion anterior.
Parametros:
    prefs - Diccionario con personas y sus preferncias
    itemMatch - Diccionario con objetos y sus objetos que son similares
    user - Persona a la que le vamos a recomendar
"""
def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}

    # Obtiene los objetos que el usuario ha calificado para comparar
    for (item,rating) in userRatings.items( ):

        # Busca objetos similares
        for (similarity,item2) in itemMatch[item]:
            # Ignora objetos que el usuario ya ha calificado
            if item2 in userRatings: continue

            # Weighted sum of rating times similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating

            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity

    # Divide each total score by total weighting to get an average
    rankings=[(score/totalSim[item],item) for item,score in scores.items( )]

    # Return the rankings from highest to lowest
    rankings.sort( )
    rankings.reverse( )
    return rankings



# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}
