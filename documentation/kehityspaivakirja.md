# Kehityspäiväkirja

#### 25.5.2020

Tein osan 3 etapit valmiiksi. Sovellukseen voi rekisteröityä, jonka jälkeen voi luoda tapahtumia ja tapahtumapaikkoja. Rekisteröitymislomakkeessa on validointi, joka tarkastaa mm. ettei samannimisiä tai samalla sähköpostiosoitteella olevia käyttäjiä löydy. Events-tauluun on nyt CRUD-toiminnot.


#### 17.5.2020

Isompi päivitys. Tein osan 2 valmiiksi sekä myös myöhempiä osioita. Dokumentaatiota päivitetty. Tein kaikkiin luokkiin pohjat valmiiksi, joten tietokanta vastaa jo projektin tämänhetkistä suunnitelmaa. Ulkoasu on toteutettu Bulma.io-tyylikirjastolla. Tein käyttäjän autentikoinnin ja polkujen suojausta. Käyttäjän salasana tallennetaan Bcrypt-kirjastolla tietokantaan. Käyttöliittymässä on valikkopohja ja responsiivinen ulkoasu. Sovellus toimii Herokussa PostgreSQL-tietokannalla.

#### 11.5.2020

Loin projektin pohjan, tietokantakaavion ja kansiorakenteen. Ensimmäinen commit ja Heroku-integraatio "Hello world"-tyyppisenä.
