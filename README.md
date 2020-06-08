# Tapahtumakalenteri

#### Harjoitustyö - Tietokantasovellus - Alkukesä 2020

Sovelluksen avulla rekisteröityneet käyttäjät voivat selata, lisätä ja osallistua tapahtumiin sekä käydä keskustelua tapahtuman sivulla.

Käyttötapauksista löytyy tarkemmat kuvaukset [täältä.](documentation/kayttotapaukset.md)

## Sovellus Herokussa
[Avaa tästä](https://tsoha-pontushed.herokuapp.com) Kirjaudu sisään tunnuksella 'admin', salasana 'admin', tai rekisteröidy uutena käyttäjänä.

## Dokumentaatio

#### Asennus- ja käyttöohje

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
````


#### Tietokantakaavio:

![kaavio](documentation/tietokantakaavio.png)

#### Muu dokumentaatio

[Työaikakirjanpito](documentation/tyoaikakirjanpito.md)

[Kehityspäiväkirja](documentation/kehityspaivakirja.md)

[Create Table-lauseet](documentation/create-table-lauseet.md)
