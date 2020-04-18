from http import client
import json
from pandas import DataFrame
from matplotlib import pyplot as plt
from datetime import datetime

class Covid19():
    def __init__(self):
        self.__client = client.HTTPSConnection("api.covid19api.com")

        # obtiene los slugs por pais en un diccionario
        self.__client.request("GET", "/countries")
        countrylist = json.loads(self.__client.getresponse().read())
        countrydict = {}
        for country in countrylist:
            countrydict[country["Country"]] = country["Slug"]
        self._slugs = countrydict

    def __obtenerDatos(self, country, status):
        uri = "/total/dayone/country/" + \
            self._slugs[country] + "/status/" + status
        self.__client.request("GET", uri)
        return DataFrame(json.loads(self.__client.getresponse().read()))

    def confirmados(self, country):
        return self.__obtenerDatos(country, "confirmed")

    def recuperados(self, country):
        return self.__obtenerDatos(country, "recovered")

    def muertos(self, country):
        return self.__obtenerDatos(country, "deaths")

    def grafPais(self, country):
        m = self.muertos(country)
        r = self.recuperados(country)
        c = self.confirmados(country)
        fechas = list(map(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z").date(), m.Date))
        plt.figure(figsize=(9,8))
        plt.stackplot(fechas, m.Cases, r.Cases, c.Cases, labels=[
                      "muertos", "recuperados", "confirmados"])
        plt.legend(loc='upper right')
        
