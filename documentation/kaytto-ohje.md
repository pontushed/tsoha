# Asennus- ja käyttöohje

## Käyttöohje

Ennen kirjautumista voit selata tapahtumia etusivulta sekä Events-sivulta. Tapahtumasta saat tarkempaa tietoa napauttamalla tapahtuman nimeä.
Kirjautumisen (tai rekisteröitymisen) jälkeen voit liittyä/poistua tapahtumista, lisätä oman tapahtuman tai tapahtumapaikan sekä kirjoittaa kysymyksiä tai kommentteja tapahtumien yhteyteen. Tapahtuman järjestäjänä voit poistaa oman tapahtumasi sekä moderoida kommentteja. Oman profiilisivusi löydät oikeasta yläkulmasta.

Pääkäyttäjänä voit myös hallinnoida käyttäjiä sekä poistaa muiden käyttäjien kommentteja, tapahtumia sekä hallinnoida tapahtumapaikkoja.

### Etusivu
Sivulla listataan tapahtumat, joissa on osallistujia.

### Events-sivu
Sivulla listataan kaikki tapahtumat, jotka eivät ole vielä päättyneet. Voit liittyä tapahtumaan suoraan painamalla "Join Event"-nappulaa. Jos olet jo liittynyt, voit poistua painamalla "Leave event". Napauttamalla tapahtuman nimeä pääset tapahtuman sivulle, jossa näet osallistujat sekä voit lisätä kommentin tai kysymyksen.

#### Uuden tapahtuman lisääminen

Kirjautuneena käyttäjänä voit lisätä tapahtuman. Mene Events-sivulle ja napauta "Organize a new event".
Täytä kaikki kohdat. Jos tapahtumapaikkaa ei löydy listasta, voit lisätä uuden valitsemalla "Create a new venue" tapahtumapaikkavalinnasta ja täyttämällä tarvittavat tiedot.
Aikatiedot tulee kirjoittaa muodossa PP.KK.VVVV TT:MM.

### Venues-sivu

Kirjautuneena käyttäjänä voit lisätä tapahtumapaikan. Voit myös muokata tapahtumapaikan tietoja. Pääkäyttäjät voivat poistaa tapahtumapaikkoja, jolloin myös kaikki niihin liittyvät tapahtumat poistetaan.

### My Profile-sivu

Kirjauteena käyttäjänä näet täältä omat tietosi.

## Asennus paikallisesti

**Asentaminen**

```bash
$ git clone https://github.com/pontushed/tsoha
$ cd tsoha
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

**Käynnistäminen**
```bash
(venv)$ python run.py
```

**Käyttäminen**

Mene selaimella osoitteeseen http://localhost:5000
Alkutilanteessa sovelluksessa ei ole mitään tietoja, joten siirry selaimella osoitteeseen http://localhost:5000/init . Sovellus alustetaan testidatalla, eli parilla käyttäjällä ja tapahtumalla.
Voit kirjautua käyttäjänä 'admin', salasana 'admin'.


## Asennus Herokuun

Sinulla pitää olla [heroku-cli](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) asennettuna. Aja seuraavat komennot hakemistossa, johon olet ladannut sovelluksen:
```bash
$ heroku create
$ git push heroku master
$ heroku ps:scale web=1
$ heroku open
```

Lisäohjeita saat [täältä](https://devcenter.heroku.com/articles/getting-started-with-python)
