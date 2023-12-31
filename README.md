# Solsystem modell

Enkel to-dimensjonal modell av solsystemet vårt. Progrmammet er laget for å svare på problemstillingen:
**"Hvordan påvirker Neptun Uranus' bane?"**.

Programmet kan starte en solsystem simulasjon fra en vilkårlig dato med ekte data.
___

## Innhold

* [Installasjon](#Installasjon)
* [Bruk](#Bruk)
* [Teknologi](#Teknologi)

___

## Installasjon

Last ned prosjektet fra GitHub og kjør main.py i en Python IDE. Endre instillinger for blant annent zoom nivå,
simulasjonsfart og debug modus i `config.py`.

___

## Bruk

Programmet brukes for å analysere numerisk og visuelt hvordan solsystemet vårt fungerer. Det er mulig å legge til flere
planeter og endre på deres masse, radius, startposisjon, startfart og farge. Det er også mulig å endre på tidssteg og
tidsstegsantall. Programmet kan også brukes til å simulere andre systemer enn solsystemet vårt, for eksempel et
dobbeltstjernesystem. Man kan egendefinere himmellegemer ved å lage en csv fil i data mappen. Hvis antall csv filer
endrer seg må man kanskje endre på `for` løkken i `main.py` for å få med alle filene og `utils.py` filen som leser fra
csv-filene.

Spesefikt brukes programmet i nåverende tilstand for å analysere hvordan Neptun påvirker Uranus og banen dens. Dette
gjøres ved å kjøre to simuleringer samtidig: en med Neptun og en uten. Deretter sammenlignes resultatene fra de to
simuleringene ved å plotte banene til Uranus i et koordinatsystem.
___

## Teknologi

Avhengigheter:
* Python 3.9.1
* Pygame 2.0.1
* Numpy 1.19.5
* Matplotlib 3.3.4
