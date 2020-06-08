# Kehityspäiväkirja

#### 8.6.2020

Tein autorisoinnin valmiiksi. Lisäsin sivun, jolta näkee oman profiilin tiedot. Autorisointia tarvitaan tällä hetkellä vain Venues-kohteen poistoon. Se onnistuu, jos kuuluu rooliin "admin".
Lisäsin validointia lähes kaikkiin lomakkeisiin. Aloitin tekemään keskusteluominaisuutta. Tapahtumasta voi avata oman sivun, johon tulee siihen liittyvät kommentit.

#### 1.6.2020

Lisäsin yhteenvetokyselyn etusivulle. Se näyttää suositut tapahtumat, eli tapahtumat, joissa on osallistujia.
Etusivulta voi myös suoraan liittyä tai poistua tapahtumasta, jos on kirjautunut sisään.
Lisäsin suojauksen, että vain tapahtuman luoja voi muokata tai poistaa tapahtuman.
Lisäsin myös varmistuksen poistojen yhteyteen. Tapahtumapaikan poisto poistaa kaikki siihen liitetyt tapahtumat!



#### 31.5.2020

Lisäsin ajan validoinnin "Organize new event"-lomakkeeseen. Alku- ja lopetusajan pitää olla tulevaisuudessa ja lopetusajan pitää olla alkuajan jälkeen.

Huomasin bugin, jossa uutta tapahtumaa lisättäessä venue-lista ei vastannut tietokannan tietoja. Tämä johtui siitä, että täydensin selectboxin valinnat forms.py:ssä olevalla kutsulla ja tämä ei toimi hyvin.
```python
class EventForm(FlaskForm):
  ...
  venue = SelectField("Event venue", choices=Venue.query.all(), coerce=int)
  ...
```
Siirsin nyt tietokantahaun views.py-tiedostoon ja siirrän tiedon lomakkeen luonnin jälkeen lomakkeelle muodossa
```python
    venueChoices = [
        (v.id, (v.name + " (" + v.location + ")")) for v in Venue.query.all()
    ]
    eventForm = EventForm()
    eventForm.venue.choices = venueChoices
```

forms.py:ssä muutin lomakkeen luonnin seuraavaksi:
```python
class EventForm(FlaskForm):
  ...
  venue = SelectField("Event venue", coerce=int)
  ...
```

#### 25.5.2020

Tein osan 3 etapit valmiiksi. Sovellukseen voi rekisteröityä, jonka jälkeen voi luoda tapahtumia ja tapahtumapaikkoja. Rekisteröitymislomakkeessa on validointi, joka tarkastaa mm. ettei samannimisiä tai samalla sähköpostiosoitteella olevia käyttäjiä löydy. Events-tauluun on nyt CRUD-toiminnot.


#### 17.5.2020

Isompi päivitys. Tein osan 2 valmiiksi sekä myös myöhempiä osioita. Dokumentaatiota on päivitetty. Tein kaikkiin luokkiin pohjat valmiiksi, joten tietokanta vastaa jo projektin tämänhetkistä suunnitelmaa. Ulkoasu on toteutettu Bulma.io-tyylikirjastolla. Tein käyttäjän autentikoinnin ja polkujen suojausta. Käyttäjän salasana tallennetaan Bcrypt-kirjastolla tietokantaan. Käyttöliittymässä on valikkopohja ja responsiivinen ulkoasu. Sovellus toimii Herokussa PostgreSQL-tietokannalla.

#### 11.5.2020

Loin projektin pohjan, tietokantakaavion ja kansiorakenteen. Ensimmäinen commit ja Heroku-integraatio "Hello world"-tyyppisenä.
