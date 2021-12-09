"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada.
"""

#•••••••••••••••••••••••••••••••••••••••••
#   Importaciones.
#•••••••••••••••••••••••••••••••••••••••••

from prettytable.prettytable import NONE
import config as cf
import sys
import controller
import model
from DISClib.ADT import list as lt
assert cf
import threading
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr

#•••••••••••••••••••••••••••••••••••••••••
#   Menu.
#•••••••••••••••••••••••••••••••••••••••••

def printMenu():
    print("\n1- Inicializar Analizador.")
    print("2- Cargar información.")
    print("3- Encontrar puntos de interconexión aérea.")
    print("4- Encontrar clústeresdetráfico aéreo.")
    print("5- Encontrar la ruta más corta entre ciudades.")
    print("6- Utilizar las millas de viajero.")
    print("7- Cuantificar el efecto de un aeropuerto cerrado.")
    print("8- Comparar con servicio WEB externo.")
    print("0- Salir\n")

#•••••••••••••••••••••••••••••••••••••••••
#   Incializacion de variables.
#•••••••••••••••••••••••••••••••••••••••••    

catalog = None
analyzer = None

#•••••••••••••••••••••••••••••••••••••••••
#   Rutas de archivos.
#•••••••••••••••••••••••••••••••••••••••••

airportsFullFile = 'Skylines primero/airports_full.csv'
routesFullFile = 'Skylines primero/routes_full.csv'
worldCitiesFile = 'Skylines primero/worldcities.csv'

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones de ejecución.
#•••••••••••••••••••••••••••••••••••••••••


def optionOne():
    return controller.newAnalyzer()

def optionTwo(analyzer):
    analyzer = controller.loadData(analyzer, airportsFullFile, routesFullFile, worldCitiesFile)
    return analyzer


def optionThree(analyzer):
    return controller.reqOne(analyzer)


def optionFour(analyzer):
    IATA1 = input("\nInsert the first Airport IATA: " )
    IATA2 = input("Insert the second Airport IATA: " )
    return controller.reqTwo(analyzer, IATA1, IATA2)


def optionFive(analyzer):
    departureCity = input("\nInsert the departure city: ")
    depstinationCity = input("Insert the destination city: ")
    return controller.reqThree(analyzer, departureCity, depstinationCity)

def optionSix(analyzer):
    return None

def optionSeven(analyzer):
    IATA = input("\nInsert the airport IATA: ")
    return controller.reqFive(analyzer, IATA)

def optionEight(analyzer):
    departureCity = input("\nInsert the departure city: ")
    depstinationCity = input("Insert the destination city: ")
    return controller.reqSix(analyzer, departureCity, depstinationCity)

#•••••••••••••••••••••••••••••••••••••••••
#   Ciclo de la aplicación.
#•••••••••••••••••••••••••••••••••••••••••

def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar: ')

        if int(inputs[0]) == 1:
            analyzer = optionOne()
            print("\nAnalyzer inicializado.\n")

        elif int(inputs[0]) == 2:
            analyzer = optionTwo(analyzer)

        elif int(inputs[0]) == 3:
            print(optionThree(analyzer))

        elif int(inputs[0]) == 4:
            print(optionFour(analyzer))

        elif int(inputs[0]) == 5:
            print(optionFive(analyzer))

        elif int(inputs[0]) == 6:
            print(optionSix(analyzer))

        elif int(inputs[0]) == 7:
            print(optionSeven(analyzer))

        elif int(inputs[0]) == 8:
            print(optionEight(analyzer))

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 30)
    thread = threading.Thread(target=thread_cycle)
    thread.start()