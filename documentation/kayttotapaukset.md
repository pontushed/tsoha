# Sovelluksen käyttötapaukset

* Käyttäjä, joka ei ole kirjautunut sisään (vierailija) voi:
    - Selata tapahtumia etusivulla, muttei kommentoida eikä osallistua.

        Etusivulla näytetään yhteenvetokysely, joka näyttää tapahtumat ja osallistujamäärät:
        ```sql
        WITH t4 AS (
            SELECT t1.*, count(t2.user_id) participants FROM event t1
            INNER JOIN events_participants t2
            ON t2.event_id=t1.id
            GROUP BY t1.id
        )
        SELECT t3.name venue_name, t3.location venue_location, t4.*, account.full_name as organizer
        FROM venue t3 LEFT JOIN t4 ON t4.venue_id = t3.id
        INNER JOIN account ON t4.admin_id=account.id
        WHERE t4.end_time > date('now')
        ```
    - Selata tapahtumia Events-sivulla, muttei kommentoida eikä osallistua

        Events-sivulla näytetään, mitä tapahtumia on tulossa (end_time on tulevaisuudessa)

        ```sql
        SELECT t1.*, t2.full_name AS organizer, t3.name AS venue_name, t3.location AS venue_location
        FROM event t1
        INNER JOIN account t2 ON t1.admin_id=t2.id
        INNER JOIN venue t3 ON t1.venue_id=t3.id
        WHERE t1.end_time > date('now')
        ```

* Sisäänkirjautunut käyttäjä voi:
    - Osallistua tapahtumiin

        ```sql
        INSERT INTO events_participants (event_id,user_id) VALUES (1, 3)
        ```
    - Kirjoittaa tapahtumaan liittyvän kommentin tai kysymyksen

        ```sql
        INSERT INTO comments (event_id, author_id, comment) VALUES (3, 1, 'Onko ruokaa tarjolla?')
        ```

    - Nähdä muut osallistujat
    
        ```sql
        SELECT t1.full_name FROM account t1
        INNER JOIN events_participants t2 ON t2.user_id=t1.id WHERE t2.event_id=1
        ```
        
    - Luoda uuden tapahtuman

        ```sql
        INSERT INTO event (
            admin_id,
            name,
            info,
            venue_id,
            start_time,
            end_time
        ) VALUES (
            3,
            'Testitapahtuma',
            'Testataan jotain',
            1,
            '2020-06-04 12:00'
            '2020-06-04 16:00'
        )
        ```
    - Luoda uuden tapahtumapaikan

        ```sql
        INSERT INTO venue (
            name,
            location
        ) VALUES (
            'Gurula',
            'Exactum'
        )
        ```
    - Muokata omaa tapahtumaa

        ```sql
        UPDATE event SET
            name='Uusi nimi',
            info='Uusi info',
            start_time='2020-06-04 12:15'
            end_time='2020-06-04 16:15'
        WHERE id=14
        ```

    - Poistaa oman tapahtuman

        ```sql
        DELETE FROM event WHERE id=14
        ```

* Pääkäyttäjä voi:
    - Hallinnoida käyttäjiä

        ```sql
        DELETE FROM User WHERE id=14
        ```

        esim.
        ```sql
        UPDATE User SET email='uusi@email.fi' WHERE id=14
        ```

    - Muokata ja poistaa muiden käyttäjien tapahtumia ja poistaa kommentteja

         ```sql
        UPDATE event SET
            name='Uusi nimi',
            info='Uusi info',
            start_time='2020-06-04 12:15'
            end_time='2020-06-04 16:15'
        WHERE event_id=14
        ```

         ```sql
        DELETE FROM event WHERE id=14
        ```

         ```sql
        DELETE FROM comments WHERE id=33
        ```
    
    - Muokata ja poistaa tapahtumapaikkoja

        ```sql
        UPDATE Venue SET name='Gurula' WHERE id=1
        ```

        ```sql
        DELETE FROM Venue WHERE id=1
        ```