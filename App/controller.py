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
 """

"""
    El controlador se encarga de mediar entre la vista y el modelo.
"""

#•••••••••••••••••••••••••••••••••••••••••
#   Importaciones.
#•••••••••••••••••••••••••••••••••••••••••

import config as cf
import model
import csv

#•••••••••••••••••••••••••••••••••••••••••
#   Inicializacion del analizador.
#•••••••••••••••••••••••••••••••••••••••••

def newAnalyzer():
    return model.newAnalyzer()

#•••••••••••••••••••••••••••••••••••••••••
#   Carga de datos al analizador.
#•••••••••••••••••••••••••••••••••••••••••

def loadData(analyzer, airportsFullFile, routesFullFile, worldCitiesFile):
    
    airportsFullFile = cf.data_dir + airportsFullFile
    airportsFullFile = csv.DictReader(
                                        open(
                                                airportsFullFile,
                                                encoding="utf-8"
                                            ),
                                        delimiter=","
                                )

    routesFullFile = cf.data_dir + routesFullFile
    routesFullFile = csv.DictReader(
                                    open(
                                            routesFullFile,
                                            encoding="utf-8"
                                        ), 
                                    delimiter=","
                                )

    worldCitiesFile = cf.data_dir + worldCitiesFile
    worldCitiesFile = csv.DictReader(
                                        open(
                                                worldCitiesFile,
                                                encoding="utf-8"
                                            ),
                                        delimiter=","
                                )

    for row in airportsFullFile:

        model.addAirporttFullRow(
                                    analyzer,
                                    row
                                )

        model.addAirport(
                            analyzer,
                            row
                        )

        model.addAirportDestinationkeys(
                                            analyzer,
                                            row
                                        )

        model.addIATA_nameRelations(
                                        analyzer,
                                        row
                                )

        model.addAirportInfo(
                                analyzer,
                                row
                            )

        model.addAirportByCity(
                                analyzer, 
                                row
                            )
        

    for row in routesFullFile:

        model.addRoutesFullRow(
                                analyzer,
                                row
                            )

        model.addAirportDestinationValuesaAndConnections(
                                                            analyzer,
                                                            row
                                                        )

        model.addAirpotCommonDestination(
                                            analyzer,
                                            row
                                        )

    for row in worldCitiesFile:

        model.addworldCitiesRow(
                                    analyzer,
                                    row
                                )

        model.addCity(
                        analyzer,
                        row
                    )

    return analyzer

#•••••••••••••••••••••••••••••••••••••••••
#   Funciones de consulta.
#•••••••••••••••••••••••••••••••••••••••••

def reqOne(analyzer):
    return model.reqOne(analyzer)

def reqTwo(analyzer, IATA1, IATA2):
    return model.reqTwo(analyzer, IATA1, IATA2)

def reqThree(analyzer, departureCity, destinationCity):
    return model.reqThree(analyzer, departureCity, destinationCity)

def reqFive(analyzer, IATA):
    return model.reqFive(analyzer, IATA)

def reqSix(analyzer, departureCity, destinationCity):
    return model.reqSix(
                        analyzer,
                        departureCity, 
                        destinationCity
                    )