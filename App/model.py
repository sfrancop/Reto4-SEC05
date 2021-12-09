"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

#•••••••••••••••••••••••••••••••••••••••••
#   Importaciones.
#•••••••••••••••••••••••••••••••••••••••••

from os import access, name
from sys import path

from prettytable.prettytable import NONE
from DISClib.DataStructures.arraylist import iterator
from DISClib.DataStructures.chaininghashtable import defaultcompare, get
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from DISClib.ADT import orderedmap as om
from DISClib.ADT.graph import gr
from DISClib.Utils import error as error
import requests
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT import stack
from prettytable import PrettyTable
from math import radians, cos, sin, asin, sqrt
from DISClib.Algorithms.Graphs import scc

#•••••••••••••••••••••••••••••••••••••••••
#   Inicializacion del analizador.
#•••••••••••••••••••••••••••••••••••••••••

def newAnalyzer():

    """ 

        Inicializa el analyzer y sus estructuras de datos.

    """
    
    analyzer = {
            "noDirectedGraph": None,
            "directedGraph": None,
            "airportsFull": None,
            "routesFull": None,
            "worldCities": None,
            "airportDestinations": None,
            'paths': None,
            "noDirectedGraphAdded": None,
            "citiesByASCII": None,
            "IATA_name": None,
            "name_IATA": None,
            "airportInfoByIATA": None,
            'components': None,
            "airportsByCity": None
    }
    
    analyzer["airportsFull"] = lt.newList("ARRAY_LIST")
    analyzer["routesFull"] = lt.newList("ARRAY_LIST")
    analyzer["worldCities"] = lt.newList("ARRAY_LIST")



    analyzer["airportDestinations"] = mp.newMap(
                                                numelements=14000,
                                                maptype='PROBING',
                                                comparefunction=None
                                                )
    
    analyzer["directedGraph"] = gr.newGraph(
                                                datastructure='ADJ_LIST',
                                                directed=True,
                                                size=14000,
                                                comparefunction=None
                                        )

    analyzer["noDirectedGraph"] = gr.newGraph(
                                                datastructure='ADJ_LIST',
                                                directed=False,
                                                size=14000,
                                                comparefunction=None
                                        )

    analyzer["noDirectedGraphAdded"] = mp.newMap(
                                                numelements=14000,
                                                maptype='PROBING',
                                                comparefunction=None
                                        )

    analyzer["citiesByASCII"] = mp.newMap(
                                                numelements=14000,
                                                maptype='PROBING',
                                                comparefunction=None
                                        )

    analyzer["IATA_name"] = mp.newMap(
                                                numelements=14000,
                                                maptype='PROBING',
                                                comparefunction=None
                                        )

    analyzer["name_IATA"] = mp.newMap(
                                                numelements=14000,
                                                maptype='PROBING',
                                                comparefunction=None
                                        )

    analyzer["airportInfoByIATA"] = mp.newMap(
                                                numelements=14000,
                                                maptype='PROBING',
                                                comparefunction=None
                                        )

    analyzer["airportsByCity"] = mp.newMap(
                                                numelements=14000,
                                                maptype='PROBING',
                                                comparefunction=None
                                        )

    return analyzer

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones de consulta.
#•••••••••••••••••••••••••••••••••••••••••

def reqOne(analyzer):

        """
        
                Responde al requerimiento 1.

        """

        graph = analyzer["directedGraph"]
        airportsInfoMap = analyzer["airportInfoByIATA"]
        airportsIATAs = gr.vertices(graph)
        data = lt.newList("ARRAY_LIST")

        for i in lt.iterator(airportsIATAs):

                airportData = {
                                "IATA": None,
                                "name": None,
                                "inBound": None,
                                "outBound": None,
                                "connections": None,
                                "city": None,
                                "country": None
                        }

                airportData["IATA"] = i
                airportData["name"] = me.getValue(mp.get(analyzer["IATA_name"], i)) 
                airportData["inBound"] = gr.indegree(graph, i)
                airportData["outBound"] = gr.outdegree(graph, i)
                airportData["connections"] = gr.indegree(graph, i) + gr.outdegree(graph, i)
                airportData["country"] = (me.getValue(mp.get(airportsInfoMap, i)))["country"]
                airportData["city"] = (me.getValue(mp.get(airportsInfoMap, i)))["city"]

                lt.addLast(data, airportData)
        
        data = sortByConnections(data)

        outPut = PrettyTable(["Name",
                            "City",
                            "Country",
                            "IATA",
                            "Connections",
                            "Inbound",
                            "Outbound"])

        for i in range(1, 6):
                airport = lt.getElement(data, i)
                outPut.add_row ([
                                airport["name"],
                                airport["city"],
                                airport["country"],
                                airport["IATA"],
                                airport["connections"],
                                airport["inBound"],
                                airport["outBound"],
                                ])

        return f"\nTop most connected airports: \n{outPut}\n"

def reqTwo(analyzer, IATA1, IATA2):

        """

                Responde al requerimiento 2.

        """

        output = {
                        "components": None,
                        "number": None,
                        "connected": None
                }

        graph = analyzer["directedGraph"]
        IATA_name = analyzer["IATA_name"]
        IATA1Name = me.getValue(mp.get(IATA_name, IATA1))
        IATA2Name = me.getValue(mp.get(IATA_name, IATA2))

        components = scc.KosarajuSCC(graph)
        number = scc.connectedComponents(components)
        connected = scc.stronglyConnected(components, IATA1, IATA2)

        output["components"] = components
        output["number"] = number
        output["connected"] = connected

        finalOutput = f"\n- Number of scc in airport route network: {output['number']}\n- Does the {IATA1Name} and the {IATA2Name} belong together? {output['connected']}\n"

        return finalOutput

def reqThree(analyzer, departureCity, destinationCity):

        """

                Responde al requerimiento 3.

        """

        # Se obtiene el mapa que guarda las ciudades con nombre similares.
        citiesByASCII = analyzer["citiesByASCII"]

        # Se obtiene la lista de las ciudades que poseen nombres similares
        # a la ciudad de partida ingresada por el ususario.
        posibleDepartureCitiesList = me.getValue(
                                                        mp.get(
                                                                citiesByASCII, 
                                                                departureCity)
                                                )

        # Se obtiene la lista de las ciudades que poseen nombres similares
        # a la ciudad de destino ingresada por el ususario.

        posibleDestinationCitiesList = me.getValue(
                                                        mp.get(
                                                                citiesByASCII,
                                                                destinationCity)
                                                )

        print(f"\nThere are {lt.size(posibleDepartureCitiesList)} departure cities posibilities, this is the list:\n")

        # Retorna la lista de ciudades de partida con nombres similares a
        # la ingresada por el ususario.
        departureCityPosition = 1
        for i in lt.iterator(posibleDepartureCitiesList):
                print(f"{departureCityPosition}, {i['city']}, {i['country']}, {i['lat']}, {i['lng']}")
                departureCityPosition += 1

        # Le pide al usuario seleccionar alguna de las ciudades motradas.
        departureCityPosition = int(input("\nSelect one by number: "))

        # Selecciona de la lista de posibles ciudades el mapa de la ciudad
        # elegida por el usuario.
        departureCityMap = lt.getElement(
                                                posibleDepartureCitiesList,
                                                departureCityPosition
                                        )

        print(f"\nThere are {lt.size(posibleDestinationCitiesList)} destination cities posibilities, this is the list:\n")

        # Retorna la lista de ciudades de destino con nombres similares a
        # la ingresada por el ususario.
        destinationCityPosition = 1
        for i in lt.iterator(posibleDestinationCitiesList):
                print(f"{destinationCityPosition}. {i['city']}, {i['country']}, {i['lat']}, {i['lng']}")
                destinationCityPosition += 1

        # Le pide al usuario seleccionar alguna de las ciudades motradas.
        destinationCityPosition = int(input("\nSelect one by number: "))

        # Selecciona de la lista de posibles ciudades el mapa de la ciudad
        # elegida por el usuario.
        destinationCityMap = lt.getElement(
                                                posibleDestinationCitiesList,
                                                destinationCityPosition
                                        )
        
        # Se remplazan los nombres de las ciudades insertadas por el
        # usuario por los nombres exactos de las ciudades elegidas.
        #departureCity = departureCityMap["city"]
        #destinationCity = destinationCityMap["city"]

        airportsByCity = analyzer["airportsByCity"]

        pathList = lt.newList("ARRAY_LIST")
        counter = 1
        output = None
        graph = analyzer["directedGraph"]

        airportInfoByIATA = analyzer["airportInfoByIATA"]

        if not mp.contains(airportsByCity, departureCity):
                output = "No airports found in departure city."

        elif not mp.contains(airportsByCity, destinationCity):
                output = "No airports found in destination city."

        else:
                # Se extrae la latitud y longitud de la ciudad de partida.
                departureCityLatitude = departureCityMap["lat"]
                departureCityLongitude = departureCityMap["lng"]

                # Se extrae la latitud y longitud de la ciudad de destino.
                destinationCityLatitude = destinationCityMap["lat"]
                destinationCityLongitude = destinationCityMap["lng"]

                # Se extrae la lista de aerpouertos que se necuentran en
                # las ciudades de partide y de destino.
                airportsDepartureCityList = me.getValue(mp.get(airportsByCity, departureCity))
                airportsDestinationCityList = me.getValue(mp.get(airportsByCity, destinationCity))

                # Se crea una nueva lista donde cada elemento sera un
                # diccionario, cada diccionario está formado por dos
                # llaves, una llamda IATA, donde se encuentra el IATA
                # del aeropuerto, y otro llamada distance, donde se
                # se encuentra la distance entre los puntos geograficos
                # de la ciudad y el aeropuerto.
                airportsDepartureCityDistancesList = lt.newList("ARRAY_LIST")
                airportsDestinationCityDistancesList = lt.newList("ARRAY_LIST")

                # Se insertan los datos en la lista de aeropuertos de 
                # partida.
                for i in lt.iterator(airportsDepartureCityList):

                        airportIATA = i["IATA"]
                        airportLatitude = float(i["Latitude"])
                        airportLongitude = float(i["Longitude"])

                        distance = haversine(airportLatitude, airportLongitude, departureCityLatitude, departureCityLongitude)

                        info = {
                                "IATA": airportIATA,
                                "distance": distance
                        }

                        lt.addLast(airportsDepartureCityDistancesList, info)

                # Se insertan los datos en la lista de aeropuertos de 
                # destino.
                for i in lt.iterator(airportsDestinationCityList):

                        airportIATA = i["IATA"]
                        airportLatitude = float(i["Latitude"])
                        airportLongitude = float(i["Longitude"])

                        distance = haversine(airportLatitude, airportLongitude, destinationCityLatitude, destinationCityLongitude)

                        info = {
                                "IATA": airportIATA,
                                "distance": distance
                        }

                        lt.addLast(airportsDestinationCityDistancesList, info)

                # Se ordenan ambas listas por el valor de distancia que hay 
                # en cada diccionario.
                airportsDepartureCityDistancesList = sortByDistance(airportsDepartureCityDistancesList)
                airportsDestinationCityDistancesList = sortByDistance(airportsDestinationCityDistancesList)

                pos = lt.size(airportsDepartureCityDistancesList)
                departureAirport = None
                departureAirportIATA = None
                while pos >= 1:
                        departureAirport = lt.getElement(airportsDepartureCityDistancesList, pos)
                        departureAirportIATA = departureAirport["IATA"]
                        if gr.containsVertex(graph, departureAirportIATA) and gr.outdegree(graph, departureAirportIATA) != 0:
                                break
                        else:
                                pos -= 1

                pos = lt.size(airportsDestinationCityDistancesList)
                destinationAirport = None
                destinationAirportIATA = None
                while pos >= 1:
                        destinationAirport = lt.getElement(airportsDestinationCityDistancesList, pos)
                        destinationAirportIATA = destinationAirport["IATA"]
                        if gr.containsVertex(graph, destinationAirportIATA) and gr.indegree(graph, departureAirportIATA) != 0:
                                break
                        else:
                                pos -= 1

                destinationAirport = lt.getElement(airportsDestinationCityDistancesList, lt.size(airportsDestinationCityDistancesList))
                destinationAirportIATA = destinationAirport["IATA"]

                # Se calculan los caminos de costos minimos que hay
                # para ir desde el aeropuerto de salida hasta
                # cualquier otro aeropuerto del grafo.
                minimumCostPaths(
                                        analyzer,
                                        departureAirportIATA
                                )

                # Se calcula el camino directo o las escalas para ir
                # del aeropuerto de partida al de destino.
                path = minimumCostPath(
                                        analyzer,
                                        destinationAirportIATA
                                        )

                # Añade el/los camino(s) del recorrido a un nuevo arreglo.
                if path is not None:
                    pathlen = stack.size(path)
                    print('\nEl camino es de longitud: ' + str(pathlen))
                    while (not stack.isEmpty(path)):
                        stop = stack.pop(path)
                        lt.addLast(pathList, stop)

                # Se incializa una variable para calcular la distancia
                # aerea total del recorrido.
                routeDistance = 0

                # Se crea una tabla para mostrar el recrrido de la ruta.
                pathTable = PrettyTable([
                                                "Airport A",
                                                "Airport B",
                                                "Distance"
                                        ])
                
                # Se suma la distancia total del recorrido y se añaden
                # los recorridos a las tablas a mostrar.
                while counter <= lt.size(pathList):

                        distancee = lt.getElement(
                                                        pathList,
                                                        counter
                                                )['weight']

                        routeDistance += distancee

                        pathTable.add_row(
                                                [
                                                        lt.getElement(
                                                                        pathList,
                                                                        counter
                                                                )['vertexA'],

                                                        lt.getElement(
                                                                        pathList,
                                                                        counter
                                                                )['vertexB'],
                                                        
                                                        distancee
                                                ]
                                        )

                        counter += 1

                # Se obtiene la latitud y longitud del aeropuerto de salida.
                departureAirportLatitude = (me.getValue(mp.get(airportInfoByIATA, departureAirportIATA)))["latitude"]
                departureAirportLongitude = (me.getValue(mp.get(airportInfoByIATA, departureAirportIATA)))["longitude"]

                # Se obtiene la latitud y longitud del aeropuerto de destino.
                destinationAirportLatitude = (me.getValue(mp.get(airportInfoByIATA, destinationAirportIATA)))["latitude"]
                destinationAirportLongitude = (me.getValue(mp.get(airportInfoByIATA, destinationAirportIATA)))["longitude"]

                # Calcula la distancia entre el punto geografico del aeropuerto de salida
                # y el punto geografico de la ciudad de salida.
                distanceBetweenDepartureCityAndDepartureAirport = haversine(departureAirportLatitude, departureAirportLongitude, departureCityLatitude, departureAirportLongitude)
                
                # Calcula la distancia entre el punto geografico del aeropuerto de destino
                # y el punto geografico de la ciudad de destino.
                distanceBetweenDestinationCityAndDestinationAirport = haversine(destinationAirportLatitude, destinationAirportLongitude, destinationCityLatitude, departureCityLongitude)

                # Se obtiene el nombre del aeropuerto de salida y de destino.
                departureAirportName = (me.getValue(mp.get(airportInfoByIATA, departureAirportIATA)))["name"]
                destinationAirportName = (me.getValue(mp.get(airportInfoByIATA, destinationAirportIATA)))["name"]

                # Se formatea la salida final de la función.
                output = f"\nDeparture Airport: {departureAirportName}\nDestination Airport: {destinationAirportName}\n\nRuta:\n{pathTable}\n\nTotal route distance: {routeDistance} kilometers\nDistance between departure city and departure airport: {distanceBetweenDepartureCityAndDepartureAirport} miles\nDistance between destination city and destination airport: {distanceBetweenDestinationCityAndDestinationAirport}miles\n"

        return output

def reqFive(analyzer, IATA):

        graph = analyzer["directedGraph"]
        airportInfoByIATA = analyzer["airportInfoByIATA"]

        affected = gr.adjacents(graph, IATA)

        table = PrettyTable(["IATA",
                            "Name",
                            "City",
                            "Country"
                            ])

        pos = [1, 2, 3, lt.size(affected)-2, lt.size(affected)-1, lt.size(affected)]

        for i in pos:

                IATA = lt.getElement(affected, i)
                airportInfo = me.getValue(mp.get(airportInfoByIATA, IATA))

                table.add_row ([
                                        airportInfo["IATA"],
                                        airportInfo["name"],
                                        airportInfo["city"],
                                        airportInfo["country"]
                                ])

        output = f"\nThere are {lt.size(affected)} airports affected by the removal of {IATA}.\n\nThe first and las three affected aiports are:\n\n{table}\n\n"
        return output

def reqSix(analyzer, departureCity, destinationCity):

        """

                Responde al requerimiento 6.

        """

        # Se obtiene el mapa que guarda las ciudades con nombre similares.
        citiesByASCII = analyzer["citiesByASCII"]

        # Se obtiene la lista de las ciudades que poseen nombres similares
        # a la ciudad de partida ingresada por el ususario.
        posibleDepartureCitiesList = me.getValue(
                                                        mp.get(
                                                                citiesByASCII, 
                                                                departureCity)
                                                )

        # Se obtiene la lista de las ciudades que poseen nombres similares
        # a la ciudad de destino ingresada por el ususario.

        posibleDestinationCitiesList = me.getValue(
                                                        mp.get(
                                                                citiesByASCII,
                                                                destinationCity)
                                                )

        print(f"\nThere are {lt.size(posibleDepartureCitiesList)} departure cities posibilities, this is the list:\n")

        # Retorna la lista de ciudades de partida con nombres similares a
        # la ingresada por el ususario.
        departureCityPosition = 1
        for i in lt.iterator(posibleDepartureCitiesList):
                print(f"{departureCityPosition}, {i['city']}, {i['country']}, {i['lat']}, {i['lng']}")
                departureCityPosition += 1

        # Le pide al usuario seleccionar alguna de las ciudades motradas.
        departureCityPosition = int(input("\nSelect one by number: "))

        # Selecciona de la lista de posibles ciudades el mapa de la ciudad
        # elegida por el usuario.
        departureCityMap = lt.getElement(
                                                posibleDepartureCitiesList,
                                                departureCityPosition
                                        )

        print(f"\nThere are {lt.size(posibleDestinationCitiesList)} destination cities posibilities, this is the list:\n")

        # Retorna la lista de ciudades de destino con nombres similares a
        # la ingresada por el ususario.
        destinationCityPosition = 1
        for i in lt.iterator(posibleDestinationCitiesList):
                print(f"{destinationCityPosition}. {i['city']}, {i['country']}, {i['lat']}, {i['lng']}")
                destinationCityPosition += 1

        # Le pide al usuario seleccionar alguna de las ciudades motradas.
        destinationCityPosition = int(input("\nSelect one by number: "))

        # Selecciona de la lista de posibles ciudades el mapa de la ciudad
        # elegida por el usuario.
        destinationCityMap = lt.getElement(
                                                posibleDestinationCitiesList,
                                                destinationCityPosition
                                        )

        # Se extrae la latitud y longitud de la ciudad de partida.
        departureCityLatitude = departureCityMap["lat"]
        departureCityLongitude = departureCityMap["lng"]

        # Se extrae la latitud y longitud de la ciudad de destino.
        destinationCityLatitude = destinationCityMap["lat"]
        destinationCityLongitude = destinationCityMap["lng"]

        # Se obtiene el codigo de acceso de para poder consultar la API.
        acessToken = getAcessToken()

        # Se incializa una nueva estructura de datos para guardar la
        # información consultada en la API.
        APIData = {
                        "departureData": None,
                        "destinatioData": None
                }

        # Se guarda la información de aeropuertos cercanos al punto
        # geografico de partida retornado por la API.
        APIData["departureData"] = queryAPI(
                                                departureCityLatitude,
                                                departureCityLongitude,
                                                acessToken
                                        )["data"]
        
        # Se guarda la información de aeropuertos cercanos al punto
        # geografico de destino retornado por la API.
        APIData["destinatioData"] = queryAPI(
                                                destinationCityLatitude,
                                                destinationCityLongitude,
                                                acessToken
                                        )["data"]

        # Se inicializan variables y/o asignan para usarlas mas
        # adelante.
        path = None
        answer = None
        pathList = lt.newList("ARRAY_LIST")
        counter = 1
        departureData = APIData["departureData"]
        destinatioData = APIData["destinatioData"]

        # Retorna una respuesta para toda la funcion en caso de
        # que no la API no encuentre aeropuertos en la ubicación
        # de partida dada por el usuario.
        if len(departureData) == 0:
                answer = "No airports found in departure city."

        # Retorna una respuesta para toda la funcion en caso de
        # que no la API no encuentre aeropuertos en la ubicación
        # de destino dada por el usuario.
        elif len(destinatioData) == 0:
                answer = "No airports found in destination city."
        
        # En caso de que la API si encuentre aeropuertos tanto en 
        # la ubicación de destino como de salida, se hace continua
        # con la función.
        else: 
                # Se obtiene el IATA del aeropuesto de salida.
                departureAirportIATA = departureData[0]["iataCode"]

                # Se obtiene el IATA del aeropuesto de destino.
                destinationAirportIATA = destinatioData[0]["iataCode"]

                # Se calculan los caminos de costos minimos que hay
                # para ir desde el aeropuerto de salida hasta
                # cualquier otro aeropuerto del grafo.
                minimumCostPaths(
                                        analyzer,
                                        departureAirportIATA
                                )

                # Se calcula el camino directo o las escalas para ir
                # del aeropuerto de partida al de destino.
                path = minimumCostPath(
                                        analyzer,
                                        destinationAirportIATA
                                        )

                # Añade el/los camino(s) del recorrido a un nuevo arreglo.
                if path is not None:
                    pathlen = stack.size(path)
                    print('El camino es de longitud: ' + str(pathlen))
                    while (not stack.isEmpty(path)):
                        stop = stack.pop(path)
                        lt.addLast(pathList, stop)

                # Se incializa una variable para calcular la distancia
                # aerea total del recorrido.
                routeDistance = 0

                # Se crea una tabla para mostrar el recrrido de la ruta.
                pathTable = PrettyTable([
                                                "Airport A",
                                                "Airport B",
                                                "Distance"
                                        ])
                
                # Se suma la distancia total del recorrido y se añaden
                # los recorridos a las tablas a mostrar.
                while counter <= lt.size(pathList):

                        distancee = lt.getElement(
                                                        pathList,
                                                        counter
                                                )['weight']

                        routeDistance += distancee

                        pathTable.add_row(
                                                [
                                                        lt.getElement(
                                                                        pathList,
                                                                        counter
                                                                )['vertexA'],

                                                        lt.getElement(
                                                                        pathList,
                                                                        counter
                                                                )['vertexB'],
                                                        
                                                        distancee
                                                ]
                                        )

                        counter += 1

                # Se obtiene la latitud y longitud del aeropuerto de salida.
                departureAirportLatitude = departureData[0]["geoCode"]["latitude"]
                departureAirportLongitude = departureData[0]["geoCode"]["longitude"]

                # Se obtiene la latitud y longitud del aeropuerto de destino.
                destinationAirportLatitude = destinatioData[0]["geoCode"]["latitude"]
                destinationAirportLongitude = destinatioData[0]["geoCode"]["longitude"]

                # Calcula la distancia entre el punto geografico del aeropuerto de salida
                # y el punto geografico de la ciudad de salida.
                distanceBetweenDepartureCityAndDepartureAirport = haversine(departureAirportLatitude, departureAirportLongitude, departureCityLatitude, departureAirportLongitude)
                
                # Calcula la distancia entre el punto geografico del aeropuerto de destino
                # y el punto geografico de la ciudad de destino.
                distanceBetweenDestinationCityAndDestinationAirport = haversine(destinationAirportLatitude, destinationAirportLongitude, destinationCityLatitude, departureCityLongitude)

                # Se obtiene el nombre del aeropuerto de salida y de destino.
                departureAirportName = APIData['departureData'][0]['name']
                destinationAirportName = APIData['destinatioData'][0]['name']

                # Se formatea la salida final de la función.
                answer = f"\nDeparture Airport: {departureAirportName}\nDestination Airport: {destinationAirportName}\n\nRuta:\n{pathTable}\n\nTotal route distance: {routeDistance} kilometers\nDistance between departure city and departure airport: {distanceBetweenDepartureCityAndDepartureAirport} miles\nDistance between destination city and destination airport: {distanceBetweenDestinationCityAndDestinationAirport}miles\n"

        return answer

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones para cargar los datos en el Analyzer.
#•••••••••••••••••••••••••••••••••••••••••

def addAirporttFullRow(analyzer, row):

        """

                Añade cada fila del archivo "airports_full"
                como elemento a un arreglo que se encuentra
                como valor del analizador en la llave 
                "airportsFull".

        """

        list = analyzer["airportsFull"]

        lt.addLast(
                        list,
                        row
                )

        return analyzer

def addRoutesFullRow(analyzer, row):

        """

                Añade cada fila del archivo "routes_full"
                como elemento a un arreglo que se encuentra
                como valor del analizador en la llave 
                "routesFull".

        """

        list = analyzer["routesFull"]

        lt.addLast(
                        list,
                        row
                )

        return analyzer

def addworldCitiesRow(analyzer, row):

        """

                Añade cada fila del archivo "worldcities"
                como elemento a un arreglo que se encuentra
                como valor del analizador en la llave 
                "worldCities".

        """

        list = analyzer["worldCities"]

        lt.addLast(
                        list,
                        row
                )

        return analyzer

def addAirportDestinationkeys(analyzer, row):

        """

                Añade como llave el IATA de un aeropuerto a
                un mapa y como valor un arreglo vacio, donde
                se almacenará mas adelante en otra funcion
                los IATA de los aeropuertos a los que desde
                el aeropuerto que se encuentro en la llave se
                puede ir.

        """

        map = analyzer["airportDestinations"]   
        airportIATA = row["IATA"]

        mp.put(
                map, airportIATA,
                lt.newList("ARRAY_LIST")
        )

def addAirport(analyzer,row):

        """
        
                Añade como vertices los IATAS de los
                aeropuertos al grafo dirigido.

        """
        
        graph = analyzer["directedGraph"]
        airportIATA = row["IATA"]
        try:
                if not gr.containsVertex(
                                                graph, 
                                                airportIATA
                                        ):

                        gr.insertVertex(
                                                graph,
                                                airportIATA
                                        )
                return analyzer
        except Exception as exp:
                error.reraise(
                                exp,
                                'model:addairport'
                        ) 

def addAirportDestinationValuesaAndConnections(analyzer, row):

        """

                Añade los destinos al mapa de los destinos
                de los aeropuertos, adicionalmente, crea
                las conexiones dirigidas en el grafo
                dirigido entre los aeropuertos y añade
                como peso sus distancias.

        """

        map = analyzer["airportDestinations"]   
        departureAirportIATA = row["Departure"]
        destinationAirportIATA = row["Destination"]
        distance = float(row["distance_km"])

        list = me.getValue(
                                mp.get(
                                        map, 
                                        departureAirportIATA
                                )
                        )

        if lt.isPresent(
                                list,
                                destinationAirportIATA
                        ) == 0:

                lt.addLast(
                                list,
                                destinationAirportIATA
                        )

                gr.addEdge(
                                analyzer['directedGraph'],
                                departureAirportIATA,
                                destinationAirportIATA,
                                distance
                        )

def addAirpotCommonDestination(analyzer, row):

        """
        
                Se carga la informacion al grafo no dirigido, el
                cual contiene como vertices loa IATAS de los
                aeropuertos y se crea un enlace unicamente entre
                los aeropuertos que se tienen como destino.

        """

        addedMap = analyzer["noDirectedGraphAdded"]

        departureAirportIATA = row["Departure"]
        destinationAirportIATA = row["Destination"]

        if not mp.contains(
                                addedMap,
                                departureAirportIATA
                        ):

                mp.put(
                        addedMap,
                        departureAirportIATA,
                        lt.newList("ARRAY_LIST")
                )

        if not mp.contains(
                                addedMap,
                                destinationAirportIATA
                        ):

                mp.put(
                        addedMap,
                        destinationAirportIATA,
                        lt.newList("ARRAY_LIST")
                )

        distance = float(row["distance_km"])

        airportDestinationsMap = analyzer["airportDestinations"]

        departureAirportAirportDestinationsList = me.getValue(
                                                                mp.get(
                                                                        airportDestinationsMap, 
                                                                        departureAirportIATA
                                                                )
                                                        )

        destinationAirportAirportDestinationsList = me.getValue(
                                                                mp.get(
                                                                        airportDestinationsMap,
                                                                        destinationAirportIATA
                                                                )
                                                        )
        
        graph = analyzer["noDirectedGraph"]

        if lt.isPresent(
                        me.getValue(
                                        mp.get(
                                                addedMap,
                                                departureAirportIATA
                                        )
                                ), 
                        destinationAirportIATA
                ) == 0 and lt.isPresent(
                                        me.getValue(
                                                        mp.get(
                                                                addedMap,
                                                                destinationAirportIATA
                                                        )
                                                ), 
                                        departureAirportIATA
                                ) == 0:

                if lt.isPresent(
                                departureAirportAirportDestinationsList, 
                                destinationAirportIATA
                                ) != 0 and lt.isPresent(
                                                        destinationAirportAirportDestinationsList, 
                                                        departureAirportIATA
                                                        ) != 0:
                        try:
                                if not gr.containsVertex(
                                                                graph,
                                                                departureAirportIATA
                                                        ):
                                        gr.insertVertex(
                                                        graph,
                                                        departureAirportIATA
                                                )

                                if not gr.containsVertex(
                                                                graph,
                                                                destinationAirportIATA
                                                        ):
                                        gr.insertVertex(
                                                        graph,
                                                        destinationAirportIATA
                                                )
                                gr.addEdge(
                                                graph,
                                                departureAirportIATA,
                                                destinationAirportIATA,
                                                distance
                                        )
                                lt.addLast(
                                                me.getValue(
                                                                mp.get(
                                                                        addedMap, 
                                                                        departureAirportIATA
                                                                )
                                                        ), 
                                                destinationAirportIATA)

                                lt.addLast(
                                                me.getValue(
                                                                mp.get(
                                                                        addedMap,
                                                                        destinationAirportIATA
                                                                )
                                                        ), 
                                                departureAirportIATA
                                        )
                                return analyzer
                        except Exception as exp:
                                error.reraise(exp, 'model:addairpotcommondestination')

def addCity(analyzer, row):

        """
        
                Añade en una misma lista las ciudades
                que tienen nombres similares. Esta lista
                es valor de la llave, la cual es el ascii
                de la ciudad, que se encuentra en un map.

        """

        city = row["city_ascii"]
        map = analyzer["citiesByASCII"]

        mapCity = {
                        "city": row["city"],
                        "city_ascii": row["city_ascii"],
                        "lat": row["lat"],
                        "lng": row["lng"],
                        "country": row["country"],
                        "iso2": row["iso2"],
                        "iso3": row["iso3"],
                        "admin_name": row["admin_name"],
                        "capital": row["capital"],
                        "population": row["population"],
                        "id": row["id"]
                }

        if not mp.contains(
                                map, 
                                city
                        ):
                mp.put(
                        map,
                        city,
                        lt.newList("ARRAY_LIST")
                )
                lt.addLast(
                                me.getValue(
                                                mp.get(
                                                        map,
                                                        city
                                                )
                                        ), 
                                mapCity
                        )
        else:
                lt.addLast(
                                me.getValue(
                                                mp.get(
                                                        map,
                                                        city
                                                )
                                        ), 
                                mapCity
                        )

def addIATA_nameRelations(analyzer, row):

        IATA_nameRelationMap = analyzer["IATA_name"]
        name_IATARelationMap = analyzer["name_IATA"]

        IATA = row["IATA"] 
        name = row["Name"]

        mp.put(IATA_nameRelationMap, IATA, name)
        mp.put(name_IATARelationMap, name, IATA)

        return analyzer

def addAirportInfo(analyzer, row):

        map = analyzer["airportInfoByIATA"]

        data = {
                        "name": row["Name"],
                        "city": row["City"],
                        "country": row["Country"],
                        "IATA": row["IATA"],
                        "latitude": row["Latitude"],
                        "longitude": row["Longitude"]
        }

        mp.put(map, row["IATA"], data)

        return analyzer

def addAirportByCity(analyzer, row):

        map = analyzer["airportsByCity"]
        city = row["City"]

        if not mp.contains(map, city):

                mp.put(
                        map, 
                        city, 
                        lt.newList("ARRAY_LIST")
                )

                airportsList = me.getValue(mp.get(map, city))
                lt.addLast(airportsList, row)

        else:
                airportsList = me.getValue(mp.get(map, city))
                lt.addLast(airportsList, row)

        return analyzer

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones para consultar la API.
#•••••••••••••••••••••••••••••••••••••••••

def getAcessToken():

        """

                https://docs.python-requests.org/en/latest/
                https://developers.amadeus.com/self-service/apis-docs/guides/authorization-262

                Obtiene el codigo de acceso para poder consultar la API
                Amadeus.
        
        """



        url="https://test.api.amadeus.com/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data ={
                "grant_type": "client_credentials", 
                "client_id": "R26UdEoEUobh9EpW6ECoCUA5QAOcr9Kz",
                "client_secret": "lIogqm05SknXsOA7"
        }

        r = requests.post(      'https://test.api.amadeus.com/v1/security/oauth2/token',
                                headers=headers,
                                data=data
                        )

        return (r.json()["access_token"])

def queryAPI(latitude, longitude, acessToken):

        """
        
                # https://developers.amadeus.com/self-service/category/air/api-doc/airport-nearest-relevant/api-reference

                Consulta en la API Amadeus los aeropuertos
                cercanos a la ubicación geografica dada.

        """

        access_token = acessToken

        headers = {
                        "Authorization": "Bearer " + access_token
                }

        params = {
                        "latitude": float(latitude),
                        "longitude": float(longitude),
                        "radius": 500
                }

        r = requests.get(
                                'https://test.api.amadeus.com/v1/reference-data/locations/airports',
                                headers=headers,
                                params=params
                        )

        return r.json()

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones adicionales.
#•••••••••••••••••••••••••••••••••••••••••

def minimumCostPaths(analyzer, initialAirport):

    """

        Calcula los caminos de costo mínimo desde el aeropuerto
        inicial a todos los demas aeropuertos del grafo.
    
    """

    analyzer['paths'] = djk.Dijkstra(
                                        analyzer["directedGraph"],
                                        initialAirport
                                )

def minimumCostPath(analyzer, destAirport):

    """

    Retorna el camino de costo minimo entre el aeropuerto
    de inicio y el aeropuerto de destino. Se debe ejecutar
    primero la funcion minimumCostPaths.

    """

    path = djk.pathTo(
                        analyzer['paths'],
                        destAirport
                )

    return path

def haversine(lat1, lon1, lat2, lon2): 

        """
        
                Cálcula la distancia terrestre entre
                dos puntos geograficos.

        """

        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        R = 3959.87433 # this is in miles. For Earth radius in kilometers use 6372.8 km
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
        c = 2*asin(sqrt(a)) 
        return R * c

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones de comparacion.
#•••••••••••••••••••••••••••••••••••••••••

def compareConnections(airport1, airport2):

    """
        Compara dos numeros.
    """

    return(airport1["connections"] > airport2["connections"])

def compareDistances(distance1, distance2):
        return(distance1["distance"] > distance2["distance"])

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones de ordenamiento.
#•••••••••••••••••••••••••••••••••••••••••

def sortByConnections(data):

    """
        Ordena una lista por la cantidad de conecciones.
    """

    return sa.sort(data, compareConnections)

def sortByDistance(data):
        return sa.sort(data, compareDistances)