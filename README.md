# Solsystem modell

Enkel to-dimensjonal modell av solsystemet vårt. Progrmammet er laget for å svare på problemstillingen:
**"Hvordan påvirker Neptun Uranus' bane?"**.
___

## Innhold

* [Installasjon](#Installasjon)
* [Bruk](#Bruk)
* [Teknologi](#Teknologi)
* [Lisens](#Lisens)

___

## Installasjon

Last ned prosjektet fra GitHub og kjør main.py i en Python IDE.

___

## Bruk

Programmet brukes for å analysere numerisk og visuelt hvordan solsystemet vårt fungerer. Det er mulig å legge til flere
planeter og endre på deres masse, radius, startposisjon, startfart og farge. Det er også mulig å endre på tidssteg og
tidsstegsantall. Programmet kan også brukes til å simulere andre systemer enn solsystemet vårt, for eksempel et
dobbeltstjernesystem.

Spesefikt brukes programmet i nåverende tilstand for å analysere hvordan Neptun påvirker Uranus og banen dens. Dette
gjøres ved å kjøre to simuleringer samtidig: en med Neptun og en uten. Deretter sammenlignes resultatene fra de to
simuleringene ved å plotte banene til Uranus i et koordinatsystem.
___

## Teknologi

Prosjektet er laget med:

* Python 3.9.1
* Pygame 2.0.1
* Numpy 1.19.5
* Matplotlib 3.3.4

___

## Lisens
MIT License

Copyright (c) 2023 Johannes Aamot-Skeidsvoll

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.