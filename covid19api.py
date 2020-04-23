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

    def allData(self, country):
        m = self.muertos(country)
        r = self.recuperados(country)
        c = self.confirmados(country)
        
        fechas = list(map(lambda x: datetime.strptime(
            x, "%Y-%m-%dT%H:%M:%S%z").date(), m.Date))
        
        df = DataFrame(data = {"Muertos": m.Cases, "Recuperados": r.Cases, "Contagiados": c.Cases, "Fechas": fechas})

        return df

    def grafPais(self, country):
        data = self.allData(country)
        plt.figure(figsize=(15, 6))
        plt.stackplot(data.Fechas, data.Muertos, data.Recuperados, data.Contagiados, labels=[
                      "muertos", "recuperados", "confirmados"])
        plt.legend(loc='upper left')

    # compara los paises desde el dia 0 en adelante
    def compararPaises(self, countries, countriesData, n):
        fig, (ax0, ax1, ax2) = plt.subplots(
            3, 1, figsize=(15, 12), sharex=True)
        ax0.set_title("Contagiados")
        ax1.set_title("Muertos")
        ax2.set_title("Recuperados")
        for data in countriesData:
            ndata = min(len(data), n)
            ax0.plot(range(ndata), data.Contagiados[0:ndata])
            ax1.plot(range(ndata), data.Muertos[0:ndata])
            ax2.plot(range(ndata), data.Recuperados[0:ndata])
        ax0.legend(countries, loc='upper left')
        ax1.legend(countries, loc='upper left')
        ax2.legend(countries, loc='upper left')
