# Totuuskortti: Älylä – synteettinen kaupungin arkkitehtuurimalli (testiversio)

Tämä kortti kertoo, mitä testiversioon (`alyla-arkkitehtuurimalli-testiversio.xml`, versio 1.1) on lisätty tarkoituksella ja mitä hyvän vastauksen pitäisi löytää.

**Sisältö:** Näin käytät korttia · 1. Mallin sisäiset epätäydellisyydet · 2. Istutetut puutteet · 3. Tarkoituksellisia erikoisuuksia · 4. Kohina · 5. Kysymykset ja vastaukset · Liitteet A–C

## Näin käytät korttia

**Testiversio = perusversio + istutetut puutteet + kohina.**

- **Mallin sisäinen epätäydellisyys (E)** on realistinen heikkous, joka on jo perusversiossa. Hyvä analyysi voi raportoida senkin.
- **Istutettu puute (P)** on tarkoituksella lisätty aukko, ristiriita tai mahdollinen ongelma. Hyvän analyysin pitäisi huomata se.
- **Kohina (N)** on tavallista epätäydellisyyttä, kuten puuttuva kuvaus. Hyvä vastaus sietää sen; se ei ole vastauksen virhe.
- **Kysymys (Q)** ja sen **odotettu vastaus (A)** kuuluvat yhteen: kysymykseen Q01 vastaa A01. Vastauksessa on kohdat, jotka hyvä vastaus huomioi ainakin, kohdat, jotka vastaus voi mainita lisäksi, ja kohdat, joita vastaus ei saa sisältää.

Vastaukset pisteytetään lomakkeella `alyla-arkkitehtuurimalli-testiversio-pisteytys.md`.

Mallin elementtien nimet, ominaisuudet ja tiedostonimet on kirjoitettu `näin`, jotta ne on helppo löytää Archista.

**Esimerkki.** Kysyt tekoälyltä kysymyksen Q02: "Kuka omistaa Kerro kartalla -järjestelmän?" Vastauksen A02 mukaan hyvä vastaus mainitsee ainakin, että omistajaa ei ole kirjattu. Jos tekoäly keksii omistajan, vastaus on virheellinen.

Maailman päivä on 1.11.2026. Käyttötapaukset (U01–U05) on kuvattu README-tiedostossa.

## 1. Mallin sisäiset epätäydellisyydet

Nämä ovat jo perusversiossa; niitä ei ole istutettu, vaan ne on laskettu mallista. Kaikki kohteet on lueteltu liitteessä A.

| Tunnus | Epätäydellisyys | Yhteenveto |
|---|---|---|
| E01 | Vanhentuneita ohjelmistoja | 7 ohjelmiston tuki on jo päättynyt ja 7 ohjelmiston päättyy kahden vuoden sisällä. |
| E02 | Pian päättyviä sopimuksia | 13 tietojärjestelmän sopimus päättyy viimeistään 30.6.2027. |
| E03 | Prosesseja ilman tietojärjestelmää | 3 prosessia ei tue yksikään tietojärjestelmä. |
| E04 | Tiedon käyttöä ilman kuvattua tietovirtaa | 13 tapausta, joissa järjestelmä käyttää toisen järjestelmän kirjoittamaa tietoa ilman kuvattua tietovirtaa. |
| E05 | Erillisiä varausjärjestelmiä | 4 erillistä varaus- tai ajanvarausjärjestelmää: `Eläinklinikka`, `Ohjaamo-ajanvaraus`, `Varaamo`, `Vuoro`. |
| E06 | Integraatioalustan ohjelmiston tuki päättyy | `Väylä Integrator 6`: tuki päättyy 30.6.2027. `Väylä` palvelee 40 tietojärjestelmää ja 40 tietovirtaa. |
| E07 | Suoria integraatioita | 19 tietovirtaa kulkee eri toimittajien järjestelmien välillä suoraan tai tiedostona, ei integraatioalustan kautta. |

## 2. Istutetut puutteet

| Tunnus | Puute | Käyttötapaukset |
|---|---|---|
| P01 | Tietojärjestelmältä puuttuu omistaja | U01, U03, U05 |
| P02 | Tietoaineistolta puuttuu omistaja | U03 |
| P03 | Mahdollinen päällekkäisyys asianhallinnassa | U02 |
| P04 | Poistuvalla järjestelmällä ei näy korvaajaa | U02, U04 |
| P05 | Uusi riippuvuus poistuvaan järjestelmään | U04, U05 |
| P06 | Tietovirta poistettuun järjestelmään | U03 |
| P07 | Henkilötietomerkintä on ristiriidassa | U03, U05 |
| P08 | Henkilötietoja EU/ETA-alueen ulkopuolella | U05 |
| P09 | Kriittinen järjestelmä poistuvalla alustalla | U04 |
| P10 | Tiedon lähdettä ei ole kuvattu | U03, U05 |
| P11 | Sama järjestelmä todennäköisesti kuvattu kahdesti | U02, U03 |
| P12 | Sama palvelu kahden yksikön vastuulla | U01, U02 |

### P01 Tietojärjestelmältä puuttuu omistaja

**Mitä mallissa on:** `Kerro kartalla` -osallistumisalustalle ei ole kirjattu omistajaa.

**Mitä hyvä vastaus voisi sanoa:**

- Toteaa, ettei omistajaa ole kirjattu, eikä arvaa sitä.
- Voi mainita, että järjestelmää käyttää `Maankäyttö ja kaavoitus`, ja ehdottaa omistajan nimeämistä.

**Periaate:** 10 Jokaisella tietojärjestelmällä on omistaja ja elinkaarisuunnitelma

### P02 Tietoaineistolta puuttuu omistaja

**Mitä mallissa on:** Henkilötietoja sisältävälle aineistolle `Kesätyösetelitiedot` ei ole kirjattu omistajaa.

**Mitä hyvä vastaus voisi sanoa:**

- Toteaa, ettei aineistolle ole kirjattu omistajaa.
- Huomauttaa, että aineisto sisältää henkilötietoja, joten omistajuus on erityisen tärkeä.

**Periaate:** 8 Tiedolla on omistaja ja laatuvastuu

### P03 Mahdollinen päällekkäisyys asianhallinnassa

**Mitä mallissa on:** `Ympäristönsuojelu` käyttää omaa `Ympäristöasiat`-järjestelmää, joka kirjaa samaa asiarekisteriä kuin kaupunkiyhteinen `Diaari`.

**Mitä hyvä vastaus voisi sanoa:**

- Huomaa, että kaksi järjestelmää kirjaa samaa asiarekisteriä.
- Esittää asian mahdollisena päällekkäisyytenä: yksikön oma järjestelmä voi olla perusteltu, mutta periaatteen 01 mukaan perustelu pitäisi kirjata.

**Periaate:** 1 Yhteiset ratkaisut ennen yksikkökohtaisia

### P04 Poistuvalla järjestelmällä ei näy korvaajaa

**Mitä mallissa on:** `Tonttipalvelu` on merkitty poistuvaksi 30.6.2027. Se tukee prosesseja `Tonttien luovutus` ja `Maanhankinta ja maankäyttösopimukset`, eikä mikään suunniteltu järjestelmä ole tulossa tilalle.

**Mitä hyvä vastaus voisi sanoa:**

- Toteaa, ettei korvaajaa näy mallissa. Korvaaja olisi toinen aktiivinen tai suunniteltu järjestelmä, joka tukee samoja prosesseja.
- Huomaa, että `Maanhankinta ja maankäyttösopimukset` jää kokonaan ilman järjestelmää.
- Mainitsee, että `Tonttipalvelu` toimii lisäksi ohjelmistoilla, joiden tuki on päättynyt.

**Periaate:** 10 Jokaisella tietojärjestelmällä on omistaja ja elinkaarisuunnitelma

### P05 Uusi riippuvuus poistuvaan järjestelmään

**Mitä mallissa on:** `Tonttihaku`-palvelusta on vuonna 2026 rakennettu uusi tietovirta poistuvaan `Tonttipalvelu`-järjestelmään.

**Mitä hyvä vastaus voisi sanoa:**

- Tunnistaa uuden riippuvuuden poistuvaan järjestelmään, mikä on periaatteen 13 vastaista.
- Huomaa, että `Tonttipalvelu`-järjestelmän poistuminen katkaisee myös tonttihaun.

**Periaate:** 13 Ei uusia riippuvuuksia poistuviin järjestelmiin ja teknologioihin

### P06 Tietovirta poistettuun järjestelmään

**Mitä mallissa on:** `Tilakone`-järjestelmästä kulkee mallin mukaan tietovirta `Tilavaraus Classic` -järjestelmään, joka poistettiin käytöstä 31.8.2025.

**Mitä hyvä vastaus voisi sanoa:**

- Huomaa, ettei poistettuun järjestelmään voi kulkea tietoa.
- Pitää molemmat tiedot esillä ja ehdottaa kuvauksen tarkistamista.

### P07 Henkilötietomerkintä on ristiriidassa

**Mitä mallissa on:** `Lukudiplomi` lukee aineistoa `Oppilastiedot`, mutta järjestelmän henkilötietomerkintä (`personal_data`) on `false`.

**Mitä hyvä vastaus voisi sanoa:**

- Huomaa ristiriidan merkinnän ja tiedon käytön välillä, kun se selvittää henkilötietojen käsittelyä.

**Periaate:** 18 Tietoturva ja tietosuoja sisäänrakennettuina

### P08 Henkilötietoja EU/ETA-alueen ulkopuolella

**Mitä mallissa on:** Oppimissovellus `Englantikeidas` toimii alustalla `Oppimissovelluksen pilvipalvelu (Yhdysvallat)` ja lukee aineistoa `Oppilastiedot`.

**Mitä hyvä vastaus voisi sanoa:**

- Löytää sovelluksen.
- Toteaa, että lasten henkilötietoja käsitellään EU/ETA-alueen ulkopuolella, mikä on periaatteen 19 vastaista.

**Periaate:** 19 Henkilötiedot käsitellään EU/ETA-alueella

### P09 Kriittinen järjestelmä poistuvalla alustalla

**Mitä mallissa on:** Alusta `Tietokantaklusteri Quarry` on merkitty poistuvaksi 31.3.2027, ja kriittinen `Lupakone` toimii sen varassa.

**Mitä hyvä vastaus voisi sanoa:**

- Kytkee alustan poistumisen rakennuslupien käsittelyyn.
- Huomaa, että `Lupakone`-järjestelmän muutkin ohjelmistot ovat vanhentuneita.

**Periaate:** 15 Teknologioiden elinkaari hallitaan

### P10 Tiedon lähdettä ei ole kuvattu

**Mitä mallissa on:** `Pysäköintivahti` käyttää aineistoa `Henkilöiden perustiedot`, mutta mallissa ei ole kuvattu, mistä se tiedon saa.

**Mitä hyvä vastaus voisi sanoa:**

- Huomaa, että tiedon lähde puuttuu kuvauksesta.
- Ei pidä tätä välttämättä virheenä: tieto voidaan hakea esimerkiksi kansallisen palvelun käyttöliittymän kautta. Ehdottaa tarkistusta.
- Huomaa, että väestötietojen muutoksen vaikutusarvio voisi ohittaa järjestelmän.

**Periaate:** 11 Integraatiot integraatioalustan kautta

### P11 Sama järjestelmä todennäköisesti kuvattu kahdesti

**Mitä mallissa on:** Kuntatekniikan katuomaisuuden hallinta on kuvattu kahtena järjestelmänä: `Infrakone` ja `Infra-kone 2`.

**Mitä hyvä vastaus voisi sanoa:**

- Epäilee kaksoiskuvausta: sama toimittaja, käyttötarkoitus ja prosessi.
- Ei laske niitä kahdeksi järjestelmäksi ilman tarkistusta.

### P12 Sama palvelu kahden yksikön vastuulla

**Mitä mallissa on:** Sekä Tilahallinnon prosessi `Tilojen vuokraus ja varaukset` että Liikuntapaikkojen prosessi `Liikuntapaikkojen vuorojen jako ja varaukset` toteuttavat palvelun `Tilojen vuokraus ja tilavaraukset`.

**Mitä hyvä vastaus voisi sanoa:**

- Nimeää molemmat yksiköt ja prosessit.
- Kytkee asian siihen, että varauksiin on useita erillisiä järjestelmiä.

**Periaate:** 4 Palvelut suunnitellaan asiakkaan tarpeista lähtien

## 3. Tarkoituksellisia erikoisuuksia

Nämä voivat näyttää virheiltä, mutta ne ovat tarkoituksellisia.

- Kansallisilla palveluilla sekä konserniyhtiöiden ja hyvinvointialueen järjestelmillä ei ole kaupungin omistajaa. Niillä on ulkoinen tarjoaja.
- Konserniyhtiöiden ja hyvinvointialueen sisäistä rakennetta ei kuvata. Mallissa näkyvät vain niiden palvelut, järjestelmät ja yhteydet kaupunkiin.
- Omistajaroolit ovat toimialatasolla, esimerkiksi `Tietojärjestelmäomistaja, Sivistys`. Henkilön nimi on roolin ominaisuudessa `holder`.
- Järjestelmän vastuuyksikkö on se yksikkö, jota järjestelmä palvelee.
- Noin 145 pientä järjestelmää on kuvattu kevyemmin: kuvauksena on järjestelmän tyyppi, ja toimittaja on usein pieni yritys.
- Yksiköiden omat rekisterit (toimittaja "Kaupunki (oma)") sijaitsevat tiedostopalvelimella.
- Integraatioalusta `Väylä` ja `Kansallinen tiedonvälityskerros` palvelevat järjestelmiä, joiden tietovirrat kulkevat niiden kautta. Tietovirran reitti on ominaisuudessa `via`.
- Integraationäkymissä sama järjestelmä voi näkyä kahdesti, jotta kaikki tietovirrat kulkevat vasemmalta oikealle.
- Säädökset perustuvat todelliseen lainsäädäntöön yleisellä tasolla, mutta eivät välttämättä heijasta oikeaa todellisuutta.

## 4. Kohina

Kohina on levitetty malliin satunnaisesti, ja jokainen muutos on kirjattu kohinalokiin (`alyla-arkkitehtuurimalli-testiversio-kohinaloki.csv`). Kohina ei koske istutettujen puutteiden kohteita.

| Tunnus | Kohina | Määrä | Mitä se tarkoittaa vastauksille |
|---|---|---|---|
| N01 | Vahvistamatta yli kaksi vuotta | 180 | Vastaus voi todeta tiedon mahdollisesti vanhentuneeksi. Ei virhe. |
| N02 | Puuttuva kuvaus tai toimittaja | 25 | Vastaus ei voi kertoa puuttuvaa tietoa. Ei virhe, jos vastaus ei keksi sitä. |
| N03 | Roolin haltija puuttuu | 1 | Rooli on olemassa, mutta sen haltijaa ei tiedetä. |
| N04 | Pienjärjestelmä kuvattu kahdesti | 3 | Vastaus voi luetella järjestelmän kahdesti; hyvä vastaus huomaa kaksoiskuvauksen. |
| N05 | Moduuli kuvattu omana järjestelmänä | 2 | Vastaus voi esittää moduulin erillisenä järjestelmänä. |
| N06 | Irrallinen järjestelmä ilman suhteita | 6 | Järjestelmä ei löydy suhteita seuraamalla; se löytyy vain nimellä tai luettelosta. |

## 5. Kysymykset ja vastaukset

Kysymykset ilman vastauksia ovat tiedostossa `alyla-arkkitehtuurimalli-testiversio-kysymykset.md`. Vastaukset on laskettu ennen kohinaa; kaikki vastauksiin kuuluvat kohteet on lueteltu liitteessä C.

Aikaan sidotut vastaukset lasketaan maailman päivästä 1.11.2026. Jos vastaus käyttää todellista päivämäärää ja kertoo sen, sekin hyväksytään.

**Mikään vastaus ei saa:**

- Keksiä puuttuvaa tietoa, kuten omistajaa, kuvausta tai toimittajaa.
- Esittää istutettua puutetta kohinana tai sivuuttaa sitä mahdollisena kohinana. Kohina ei koske istutettujen puutteiden kohteita.

| Kysymys | Käyttötapaus | Istutetut puutteet |
|---|---|---|
| Q01 Mitkä tietojärjestelmät tukevat varhaiskasvatushakemusten käsittelyä, ja kuka niistä vastaa? | U01 | – |
| Q02 Kuka omistaa Kerro kartalla -järjestelmän? | U01 | P01 |
| Q03 Mitä prosesseja, palveluja ja tietojärjestelmiä Rakennusvalvonnan organisaatiomuutos koskee? | U01 | – |
| Q04 Missä on päällekkäisiä tietojärjestelmiä samaan käyttötarkoitukseen? | U02 | P03, P11 |
| Q05 Mitkä prosessit ovat ilman tietojärjestelmätukea? | U02 | – |
| Q06 Mitkä poistuvat tietojärjestelmät tukevat yhä prosesseja, ja onko niille korvaaja? | U02 | P04, P05 |
| Q07 Mitä tiedämme Rakennusvalvonnan tietojärjestelmistä, ja missä tiedot ovat puutteellisia tai ristiriitaisia? | U03 | P09 |
| Q08 Mistä tietojärjestelmistä ja tietoaineistoista puuttuu omistaja? | U03 | P01, P02 |
| Q09 Missä mallin tiedot ovat keskenään ristiriidassa? | U03 | P06, P07, P10, P11 |
| Q10 Mikä Kaupunkiympäristössä vaatii uusimista kahden vuoden sisällä? | U04 | P04, P09 |
| Q11 Mitkä tietojärjestelmät ovat riippuvaisia ohjelmistoista, joiden tuki on jo päättynyt? | U04 | – |
| Q12 Mitä seuraa, jos integraatioalusta Väylän ohjelmiston tuki päättyy? | U04 | – |
| Q13 Mitä digipalvelulain saavutettavuusvaatimusten muutos koskee, ja kenelle siitä pitää kertoa? | U05 | – |
| Q14 Missä henkilötietoja käsitellään EU/ETA-alueen ulkopuolella? | U05 | P08 |
| Q15 Jos väestötietojen toimitus kansallisesta väestötietojärjestelmästä muuttuu, mihin kaupungin järjestelmiin se vaikuttaa? | U05 | P10 |

### Q01 Mitkä tietojärjestelmät tukevat varhaiskasvatushakemusten käsittelyä, ja kuka niistä vastaa?

*U01 Neuvonta ja viestintä*

*Tulkinta:* Järjestelmät, jotka tukevat prosessia `Varhaiskasvatushakemusten käsittely ja sijoittaminen`, ja niiden omistajaroolit. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A01**

Hyvä vastaus huomioi ainakin:

- [ ] 2 järjestelmää: `Vaka-Reppu` (`Tietojärjestelmäomistaja, Sivistys`); `Vaka-Reppu Asiointi` (`Tietojärjestelmäomistaja, Sivistys`).

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Vaka-Reppu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Vaka-Reppu Asiointi`: toimittaja puuttuu; vastaus ei voi kertoa toimittajaa

### Q02 Kuka omistaa Kerro kartalla -järjestelmän?

*U01 Neuvonta ja viestintä*

*Tulkinta:* Järjestelmälle kirjattu omistajarooli. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A02**

Hyvä vastaus huomioi ainakin:

- [ ] Omistajaa ei ole kirjattu.
- [ ] Järjestelmää käyttää `Maankäyttö ja kaavoitus`.

Vastaus voi mainita lisäksi:

- [ ] Ehdottaa omistajaa käyttäjän perusteella, kun se esitetään ehdotuksena eikä tosiasiana.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Maankäyttö ja kaavoitus`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

### Q03 Mitä prosesseja, palveluja ja tietojärjestelmiä Rakennusvalvonnan organisaatiomuutos koskee?

*U01 Neuvonta ja viestintä*

*Tulkinta:* Rakennusvalvontaan kohdistetut prosessit, niiden toteuttamat palvelut sekä järjestelmät, jotka tukevat näitä prosesseja tai palvelevat yksikköä. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A03**

Hyvä vastaus huomioi ainakin:

- [ ] Prosessit (5): `Rakennus- ja huoneistotietojen ylläpito`, `Rakennus- ja toimenpidelupien käsittely`, `Rakennustyön aikainen valvonta ja katselmukset`, `Rakennusvalvonta`, `Rakentamisen neuvonta ja ennakko-ohjaus`.
- [ ] Palvelut (3): `Rakennus- ja toimenpideluvat`, `Rakennustyön valvonta ja katselmukset`, `Rakentamisen neuvonta`.
- [ ] Tietojärjestelmät (8): `Kansallinen lupapalvelu`, `Kansallinen rakennetun ympäristön tietojärjestelmä`, `Kartta-apu`, `Kuittiskanneri`, `Lupakone`, `Piirustusarkisto`, `Uutiskirjetyökalu`, `Verkkokauppa Mini`.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Kansallinen lupapalvelu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Kartta-apu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Kuittiskanneri`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi; kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Lupakone`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Piirustusarkisto`: kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Uutiskirjetyökalu`: järjestelmällä ei ole suhteita, joten sitä ei löydä suhteita seuraamalla

### Q04 Missä on päällekkäisiä tietojärjestelmiä samaan käyttötarkoitukseen?

*U02 Nykytila-analyysi*

*Tulkinta:* Järjestelmät, jotka palvelevat samaa käyttötarkoitusta. Samaa tietoa kirjoittavat muut parit (7) ovat todennäköisesti luontevaa työnjakoa, esimerkiksi verkkoasiointi ja sen taustajärjestelmä: `Hankinta- ja sopimustiedot`: `Sopimus+`, `Tarjouspalvelu`; `Kantakartta ja paikkatietoaineistot`: `Karttakone`, `Mittaus Pro`; `Myyntilaskut ja saatavat`: `Kassa`, `Raita`; `Tiedonhallintamalli`: `Arkiva TOS`, `Arkki`; `Tilatiedot ja tilavaraukset`: `Tilakone`, `Varaamo`; `Tontti- ja maanvuokrasopimukset`: `Tonttihaku`, `Tonttipalvelu`; `Varhaiskasvatuksen asiakastiedot`: `Vaka-Reppu`, `Vaka-Reppu Asiointi`. Niiden nostaminen tarkistettaviksi ei ole virhe. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A04**

Hyvä vastaus huomioi ainakin:

- [ ] Todennäköinen kaksoiskuvaus: `Infrakone` ja `Infra-kone 2` (P11).
- [ ] Erilliset varausjärjestelmät: `Eläinklinikka`, `Ohjaamo-ajanvaraus`, `Varaamo`, `Vuoro` (E05).
- [ ] Mahdollinen päällekkäisyys: `Ympäristöasiat` kirjaa samaa asiarekisteriä kuin kaupunkiyhteinen `Diaari` (P03). Yksikön oma järjestelmä voi olla perusteltu; hyvä vastaus nostaa asian esiin, ei tuomitse sitä.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Arkiva TOS`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Diaari`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Eläinklinikka`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Ohjaamo-ajanvaraus`: kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Sopimus+`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Tilatiedot ja tilavaraukset`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Vaka-Reppu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Vaka-Reppu Asiointi`: toimittaja puuttuu; vastaus ei voi kertoa toimittajaa
- `Varaamo`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Varhaiskasvatuksen asiakastiedot`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

### Q05 Mitkä prosessit ovat ilman tietojärjestelmätukea?

*U02 Nykytila-analyysi*

*Tulkinta:* Prosessiryhmien alaiset prosessit. Prosessiryhmiä ei lasketa, koska tietojärjestelmät tukevat prosesseja eivätkä ryhmiä. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A05**

Hyvä vastaus huomioi ainakin:

- [ ] 3 prosessia: `Oikaisuvaatimusten ja valitusten käsittely`, `Opinto-ohjaus ja jatko-opintoihin ohjaus`, `Poikkeamis- ja suunnittelutarveasioiden käsittely`.

### Q06 Mitkä poistuvat tietojärjestelmät tukevat yhä prosesseja, ja onko niille korvaaja?

*U02 Nykytila-analyysi*

*Tulkinta:* Korvaaja tarkoittaa toista aktiivista tai suunniteltua järjestelmää, joka tukee samoja prosesseja kuin poistuva järjestelmä. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A06**

Hyvä vastaus huomioi ainakin:

- [ ] `Tonttipalvelu` poistuu 30.6.2027. Mallissa ei ole järjestelmää, joka tukisi samoja prosesseja.
- [ ] Prosessi `Maanhankinta ja maankäyttösopimukset` jää kokonaan ilman järjestelmää.
- [ ] Prosessi `Tonttien luovutus` jää järjestelmien `Tilausportaali`, `Tonttihaku` varaan.

Vastaus voi mainita lisäksi:

- [ ] `Tonttihaku` ei ole korvaaja: se on kytketty poistuvaan `Tonttipalvelu`-järjestelmään uudella tietovirralla 4.5.2026, ja poisto katkaisee sen (P05).

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Tilausportaali`: järjestelmällä ei ole suhteita, joten sitä ei löydä suhteita seuraamalla

### Q07 Mitä tiedämme Rakennusvalvonnan tietojärjestelmistä, ja missä tiedot ovat puutteellisia tai ristiriitaisia?

*U03 Tietoaukot ja ristiriidat*

*Tulkinta:* Järjestelmät, jotka palvelevat Rakennusvalvontaa. Puutteellisuus ja ristiriitaisuus näkyvät tässä elinkaaritiedoissa: vanhentuneissa ohjelmistoissa ja poistuvissa alustoissa. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A07**

Hyvä vastaus huomioi ainakin:

- [ ] `Lupakone` (Rakennusvalvonnan lupa- ja valvontajärjestelmä): `Pohjola Linux 7` tuki päättyi 30.6.2024; alusta `Tietokantaklusteri Quarry` poistuu 31.3.2027.
- [ ] `Piirustusarkisto` (Rakennuslupapiirustusten sähköinen arkisto): `Polaris SQL 2016` tuki päättyi 14.7.2026.
- [ ] Yksikön pienjärjestelmät `Kartta-apu`, `Kuittiskanneri`, `Uutiskirjetyökalu`, `Verkkokauppa Mini` on kuvattu kevyemmin: kuvauksena on järjestelmän tyyppi. Niissä ei ole elinkaaripuutteita.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Kartta-apu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Kuittiskanneri`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi; kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Lupakone`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Piirustusarkisto`: kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Quarry Database 12c`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Uutiskirjetyökalu`: järjestelmällä ei ole suhteita, joten sitä ei löydä suhteita seuraamalla
- `Windows-palvelinympäristö`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

### Q08 Mistä tietojärjestelmistä ja tietoaineistoista puuttuu omistaja?

*U03 Tietoaukot ja ristiriidat*

*Tulkinta:* Tietojärjestelmät ja tietoaineistot, joilla ei ole omistajaa eikä ulkoista tarjoajaa. Kansallisilla palveluilla ja konserniyhtiöiden järjestelmillä on ulkoinen tarjoaja, joten niiltä ei puutu omistajaa. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A08**

Hyvä vastaus huomioi ainakin:

- [ ] `Kerro kartalla` (tietojärjestelmä)
- [ ] `Kesätyösetelitiedot` (tietoaineisto)

Vastaus voi mainita lisäksi:

- [ ] Ehdottaa omistajaa käyttäjän perusteella, kun se esitetään ehdotuksena eikä tosiasiana.

### Q09 Missä mallin tiedot ovat keskenään ristiriidassa?

*U03 Tietoaukot ja ristiriidat*

*Tulkinta:* Ristiriita tarkoittaa, että mallin kaksi tietoa eivät voi olla yhtä aikaa totta, esimerkiksi tietovirta poistettuun järjestelmään tai henkilötietomerkintä, joka ei vastaa käytettyä aineistoa. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A09**

Hyvä vastaus huomioi ainakin:

- [ ] Tietovirta `Tilakone` → `Tilavaraus Classic`, vaikka `Tilavaraus Classic` on poistettu käytöstä (P06).
- [ ] `Lukudiplomi` käyttää aineistoa `Oppilastiedot`, mutta on merkitty henkilötiedottomaksi (P07).
- [ ] `Infrakone` ja `Infra-kone 2` kuvaavat todennäköisesti samaa järjestelmää (P11).

Vastaus voi mainita lisäksi:

- [ ] `Pysäköintivahti` käyttää aineistoa `Henkilöiden perustiedot`, mutta lähdettä ei ole kuvattu (P10).
- [ ] Muut tapaukset, joissa järjestelmä käyttää toisen järjestelmän kirjoittamaa tietoa ilman kuvattua tietovirtaa (E04).

### Q10 Mikä Kaupunkiympäristössä vaatii uusimista kahden vuoden sisällä?

*U04 Elinkaari ja tekninen velka*

*Tulkinta:* Järjestelmät, jotka tukevat Kaupunkiympäristön yksiköiden prosesseja. Kaksi vuotta lasketaan maailman päivästä eli 1.11.2028 asti. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A10**

Hyvä vastaus huomioi ainakin:

- [ ] Paikkatietojärjestelmien alusta: `Geomatica Server 10` ja `OpenRel 12` vanhenevat; niitä käyttävät `Infrakone`, `Kaavakone`, `Karttakone`, `Kiinteistö+`, `Älylän karttapalvelu`.
- [ ] `Lupakone` toimii vanhentuneilla ohjelmistoilla ja poistuvalla alustalla `Tietokantaklusteri Quarry` (P09).
- [ ] `Tonttipalvelu` poistuu, ja se toimii ohjelmistoilla, joiden tuki on päättynyt (P04).
- [ ] Yhteensä 20 järjestelmällä on teknologia- tai elinkaaririski ja 23 järjestelmän sopimus päättyy. Täysi lista on liitteessä.

Vastaus voi mainita lisäksi:

- [ ] Muut liitteen C kohteet, kuten yksittäisten järjestelmien vanhenevat ohjelmistot ja päättyvät sopimukset.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Aurausseuranta`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Eläinklinikka`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Kartta-apu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Kirjanpitoapu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Kuittiskanneri`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi; kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Kulku`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Lupakone`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Piirustusarkisto`: kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Quarry Database 12c`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Rakennusautomaatio`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Uutiskirjetyökalu`: järjestelmällä ei ole suhteita, joten sitä ei löydä suhteita seuraamalla
- `Windows-palvelinympäristö`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Ympäristö+`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Älylän karttapalvelu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

### Q11 Mitkä tietojärjestelmät ovat riippuvaisia ohjelmistoista, joiden tuki on jo päättynyt?

*U04 Elinkaari ja tekninen velka*

*Tulkinta:* Järjestelmät, jotka toimivat ohjelmistoilla, joiden toimittajan tuki on päättynyt ennen maailman päivää 1.11.2026. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A11**

Hyvä vastaus huomioi ainakin:

- [ ] `Fenestra Server 2012 R2`: tuki päättyi 10.10.2023; käyttävät `Tonttipalvelu`.
- [ ] `Pohjola Linux 7`: tuki päättyi 30.6.2024; käyttävät `Lupakone`.
- [ ] `Polaris SQL 2014`: tuki päättyi 9.7.2024; käyttävät `Tonttipalvelu`.
- [ ] `OpenRel 12`: tuki päättyi 14.11.2024; käyttävät `Infrakone`, `Kaavakone`, `Karttakone`, `Kiinteistö+`, `Älylän karttapalvelu`.
- [ ] `Automaatio BMS 5`: tuki päättyi 31.12.2025; käyttävät `Kulku`, `Rakennusautomaatio`.
- [ ] `Sisältöhallinta Kaari 9`: tuki päättyi 30.4.2026; käyttävät `Sisänet`.
- [ ] `Polaris SQL 2016`: tuki päättyi 14.7.2026; käyttävät `Lukkari`, `Mittaus Pro`, `Piirustusarkisto`, `Reppu`, `Tuki-Reppu`.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Kulku`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Lupakone`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Piirustusarkisto`: kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Rakennusautomaatio`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Reppu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Älylän karttapalvelu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

### Q12 Mitä seuraa, jos integraatioalusta Väylän ohjelmiston tuki päättyy?

*U04 Elinkaari ja tekninen velka*

*Tulkinta:* Järjestelmät, joita `Väylä` palvelee (Serving-suhde Väylästä tietojärjestelmään), ja tietovirrat, joiden ominaisuuden `via` arvo on `vayla`. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A12**

Hyvä vastaus huomioi ainakin:

- [ ] `Väylä Integrator 6`: tuki päättyy 30.6.2027.
- [ ] `Väylä` palvelee 40 tietojärjestelmää, ja sen kautta kulkee 40 tietovirtaa.
- [ ] Niistä 4 on ilmoituksia kansallisiin palveluihin: `Vaka-Reppu` → `Kansallinen varhaiskasvatuksen tietovaranto`; `Reppu` → `Kansallinen opintotietovaranto`; `Lupakone` → `Kansallinen rakennetun ympäristön tietojärjestelmä`; `Kaavakone` → `Kansallinen rakennetun ympäristön tietojärjestelmä`.
- [ ] Riski: lakisääteiset ilmoitukset voivat katketa, jos alustaa ei päivitetä ajoissa.

Vastaus ei saa:

- [ ] Väittää, ettei Väylän kautta kulkevia tietovirtoja voi tunnistaa. Reitti on tietovirran ominaisuudessa `via`.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Kansallinen opintotietovaranto`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Lupakone`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Reppu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Vaka-Reppu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

### Q13 Mitä digipalvelulain saavutettavuusvaatimusten muutos koskee, ja kenelle siitä pitää kertoa?

*U05 Muutosten vaikutukset*

*Tulkinta:* Kohteet, jotka mallissa toteuttavat digipalvelulain (Realization). Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A13**

Hyvä vastaus huomioi ainakin:

- [ ] 17 kohdetta, jotka digipalvelulaki sääntelee. Vastaus ryhmittelee ne omistajan mukaan, koska omistajille pitää kertoa muutoksesta:
- [ ] `Palveluomistaja, Konsernihallinto`: `Sähköinen asiointi kaupungin verkkopalvelussa`
- [ ] `Tietojärjestelmäomistaja, Elinvoima`: `Työtä Älylässä`, `Visit Älylä`
- [ ] `Tietojärjestelmäomistaja, Kaupunkiympäristö`: `Korjaa kaupunki`, `Reittiopas`, `Tonttihaku`, `Varaamo`, `Älylän karttapalvelu`
- [ ] `Tietojärjestelmäomistaja, Konsernihallinto`: `Asiointi`, `Diaari Julkaisu`, `Palautepolku`, `Valtuustolive`, `Älylä-botti`, `Älylä.fi`
- [ ] `Tietojärjestelmäomistaja, Sivistys`: `Reppu Koti`, `Vaka-Reppu Asiointi`, `Vuoro`

Vastaus voi mainita lisäksi:

- [ ] Asukkaille näkyvät tietojärjestelmät, joita ei ole kytketty digipalvelulakiin, ja suositus tarkistaa ne.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Palautepolku`: kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta
- `Reppu Koti`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Vaka-Reppu Asiointi`: toimittaja puuttuu; vastaus ei voi kertoa toimittajaa
- `Varaamo`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Älylän karttapalvelu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

### Q14 Missä henkilötietoja käsitellään EU/ETA-alueen ulkopuolella?

*U05 Muutosten vaikutukset*

*Tulkinta:* Järjestelmät, joiden alusta sijaitsee EU/ETA-alueen ulkopuolella ja jotka käsittelevät henkilötietoja: järjestelmä on merkitty henkilötietoja käsitteleväksi tai se käyttää henkilötietoja sisältävää aineistoa. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A14**

Hyvä vastaus huomioi ainakin:

- [ ] `Englantikeidas` toimii alustalla `Oppimissovelluksen pilvipalvelu (Yhdysvallat)` ja käyttää aineistoa `Oppilastiedot` (P08).
- [ ] Koskee lasten henkilötietoja ja on periaatteen 19 vastaista.

### Q15 Jos väestötietojen toimitus kansallisesta väestötietojärjestelmästä muuttuu, mihin kaupungin järjestelmiin se vaikuttaa?

*U05 Muutosten vaikutukset*

*Tulkinta:* Järjestelmät, jotka saavat väestötietoja kansallisesta väestötietojärjestelmästä tietovirtojen kautta. Jos vastaus kertoo käyttävänsä toista perusteltua tulkintaa, sekin hyväksytään.

**A15**

Hyvä vastaus huomioi ainakin:

- [ ] Tietovirtojen kautta: `Diaari`, `Reppu`, `Vaka-Reppu`.

Vastaus voi mainita lisäksi:

- [ ] `Pysäköintivahti` käyttää aineistoa `Henkilöiden perustiedot`, mutta sen lähdettä ei ole kuvattu (P10). Pelkkiä tietovirtoja seuraamalla se jäisi huomaamatta.

**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:

- `Diaari`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Reppu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi
- `Vaka-Reppu`: vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi

## Liite A. Mallin sisäiset epätäydellisyydet kokonaisuudessaan

### E01 Vanhentuneita ohjelmistoja

Jo päättynyt tuki on periaatteen 15 (Teknologioiden elinkaari hallitaan) vastaista.

- `Fenestra Server 2012 R2`: tuki päättyi 10.10.2023; käyttävät `Tonttipalvelu`
- `Pohjola Linux 7`: tuki päättyi 30.6.2024; käyttävät `Lupakone`
- `Polaris SQL 2014`: tuki päättyi 9.7.2024; käyttävät `Tonttipalvelu`
- `OpenRel 12`: tuki päättyi 14.11.2024; käyttävät `Infrakone`, `Kaavakone`, `Karttakone`, `Kiinteistö+`, `Älylän karttapalvelu`
- `Automaatio BMS 5`: tuki päättyi 31.12.2025; käyttävät `Kulku`, `Rakennusautomaatio`
- `Sisältöhallinta Kaari 9`: tuki päättyi 30.4.2026; käyttävät `Sisänet`
- `Polaris SQL 2016`: tuki päättyi 14.7.2026; käyttävät `Lukkari`, `Mittaus Pro`, `Piirustusarkisto`, `Reppu`, `Tuki-Reppu`
- `Javelin Runtime 8`: tuki päättyy 31.12.2026; käyttävät `Lupakone`
- `Geomatica Server 10`: tuki päättyy 31.12.2026; käyttävät `Infrakone`, `Kaavakone`, `Karttakone`, `Kiinteistö+`, `Älylän karttapalvelu`
- `Fenestra Server 2016`: tuki päättyy 12.1.2027; käyttävät `Lukkari`, `Mittaus Pro`, `Piirustusarkisto`, `Reppu`, `Tuki-Reppu`
- `Quarry Database 12c`: tuki päättyy 31.3.2027; käyttävät `Lupakone`
- `Väylä Integrator 6`: tuki päättyy 30.6.2027; käyttävät `Väylä`
- `OpenRel 15`: tuki päättyy 11.11.2027; käyttävät `Kuntanäkymä`
- `Dotframe 4.8`: tuki päättyy 11.1.2028; käyttävät `Diaari`, `Diaari Kokous`, `Kaavapiirtäjä`, `Laskentamestari`, `Liikennemalli`, `Lukkari`, `Malli 3D`, `Mittaus Pro`, `Määrälaskenta`, `Piirto CAD`, `Piirustusarkisto`, `Pistepilvi`, `Rakenne-analyysi`, `Reppu`, `Tietomallikatselin`, `Tuki-Reppu`

### E02 Pian päättyviä sopimuksia

- `Reppu`: sopimus päättyy 6.12.2026
- `Kotopolku`: sopimus päättyy 30.12.2026
- `IP-haku`: sopimus päättyy 2.1.2027
- `Eläinklinikka`: sopimus päättyy 14.2.2027
- `Polku`: sopimus päättyy 16.2.2027
- `Aurausseuranta`: sopimus päättyy 21.2.2027
- `Karttakone`: sopimus päättyy 27.2.2027
- `Arkiva TOS`: sopimus päättyy 14.4.2027
- `Päiväkirja`: sopimus päättyy 28.4.2027
- `Turva`: sopimus päättyy 5.5.2027
- `Kiinteistö+`: sopimus päättyy 18.5.2027
- `Reppu Koti`: sopimus päättyy 18.5.2027
- `Pysäköintivahti`: sopimus päättyy 8.6.2027

### E03 Prosesseja ilman tietojärjestelmää

- `Oikaisuvaatimusten ja valitusten käsittely`
- `Opinto-ohjaus ja jatko-opintoihin ohjaus`
- `Poikkeamis- ja suunnittelutarveasioiden käsittely`

### E04 Tiedon käyttöä ilman kuvattua tietovirtaa

Ei välttämättä virhe: tieto voidaan saada myös muuta kautta. Istutettu puute P10 on näistä merkittävin ja kuvattu erikseen.

- `Oppiva` käyttää aineistoa `Henkilöstön perustiedot`; tietovirtaa sen kirjoittajista (`Pallas`) ei ole kuvattu
- `Sijoittumispalvelu` käyttää aineistoa `Kantakartta ja paikkatietoaineistot`; tietovirtaa sen kirjoittajista (`Karttakone`, `Mittaus Pro`) ei ole kuvattu
- `Elinvoimamittari` käyttää aineistoa `Yritysten perustiedot`; tietovirtaa sen kirjoittajista (`Kansallinen yritystietojärjestelmä`) ei ole kuvattu
- `Palveluseuranta` käyttää aineistoa `Työnhakija-asiakastiedot`; tietovirtaa sen kirjoittajista (`Kansallinen työllisyyden asiakastietojärjestelmä`, `Polku`) ei ole kuvattu
- `Älylän karttapalvelu` käyttää aineistoa `Kaava-aineistot`; tietovirtaa sen kirjoittajista (`Kaavakone`) ei ole kuvattu
- `Kiinteistö+` käyttää aineistoa `Kaava-aineistot`; tietovirtaa sen kirjoittajista (`Kaavakone`) ei ole kuvattu
- `Reittiopas` käyttää aineistoa `Joukkoliikenteen linja- ja lipputiedot`; tietovirtaa sen kirjoittajista (`Lippu`) ei ole kuvattu
- `Kulku` käyttää aineistoa `Henkilöstön perustiedot`; tietovirtaa sen kirjoittajista (`Pallas`) ei ole kuvattu
- `Kyyti` käyttää aineistoa `Osoitetiedot`; tietovirtaa sen kirjoittajista (`Karttakone`) ei ole kuvattu
- `Pallas Itsepalvelu` käyttää aineistoa `Henkilöstön perustiedot`; tietovirtaa sen kirjoittajista (`Pallas`) ei ole kuvattu
- `Kansallinen ympäristövalvonnan tietojärjestelmä` käyttää aineistoa `Ympäristölupa- ja valvontatiedot`; tietovirtaa sen kirjoittajista (`Ympäristö+`) ei ole kuvattu
- `Lukudiplomi` käyttää aineistoa `Oppilastiedot`; tietovirtaa sen kirjoittajista (`Reppu`) ei ole kuvattu
- `Englantikeidas` käyttää aineistoa `Oppilastiedot`; tietovirtaa sen kirjoittajista (`Reppu`) ei ole kuvattu

### E05 Erillisiä varausjärjestelmiä

Realistinen tilanne: yksiköt ovat hankkineet omia varaustyökalujaan. Liittyy istutettuun puutteeseen P12.

- `Eläinklinikka`: Eläinlääkäripalvelujen potilas- ja ajanvarausjärjestelmä
- `Ohjaamo-ajanvaraus`: Nuorten ohjauspalvelujen ajanvaraus
- `Varaamo`: Tilojen sähköinen varaus
- `Vuoro`: Liikuntapaikkojen vuorovaraus

### E06 Integraatioalustan ohjelmiston tuki päättyy

- `Arkiva`
- `Asiointi`
- `Avain IAM`
- `Avustus`
- `Budjetti Pro`
- `Diaari`
- `Hyvä-kirjaus`
- `Infrakone`
- `Kaavakone`
- `Kansallinen lupapalvelu`
- `Kansallinen opintotietovaranto`
- `Kansallinen rakennetun ympäristön tietojärjestelmä`
- `Kansallinen varhaiskasvatuksen tietovaranto`
- `Kansallinen yhteishakupalvelu`
- `Kassa`
- `Katulupa`
- `Korjaa kaupunki`
- `Kotopolku`
- `Kuntahaku`
- `Kuntanäkymä`
- `Kurssi`
- `Kyyti`
- `Lippu`
- `Lupakone`
- `Opiskeluhuollon potilastietojärjestelmä`
- `Oppimo`
- `Palautepolku`
- `Pallas`
- `Polku`
- `Pysäköintivahti`
- `Päiväkirja`
- `Raita`
- `Reppu`
- `Sopimus+`
- `Tilakone`
- `Toimittajarekisteri`
- `Tukipolku`
- `Vaka-Reppu`
- `Varaamo`
- `Vuorolista`

### E07 Suoria integraatioita

Periaate 11 edellyttää integraatioalustaa. Poikkeamispäätökset kuvataan vaiheessa 2.

- `Avain IAM` → `Stratus Hakemisto`: Käyttäjätunnukset ja ryhmät (suora)
- `Vahti` → `Palvelupyyntö`: Tietoturvahälytykset (suora)
- `Reppu` → `IP-haku`: Oppilastiedot (tiedosto)
- `Vaka-Reppu` → `Setelipalvelu`: Palvelusetelipäätökset (tiedosto)
- `Setelipalvelu` → `Raita`: Palveluntuottajien maksuaineisto (tiedosto)
- `Älylä.fi` → `Älylä-botti`: Verkkosisällöt (suora)
- `Tapahtumat` → `Visit Älylä`: Tapahtumatiedot (suora)
- `Lupakone` → `Piirustusarkisto`: Hyväksytyt lupapiirustukset (suora)
- `Kiinteistö+` → `Tonttipalvelu`: Kiinteistötiedot (suora)
- `Tonttipalvelu` → `Raita`: Maanvuokrien laskutusaineisto (tiedosto)
- `Vuoro` → `Raita`: Vuorojen laskutusaineisto (tiedosto)
- `Rakennusautomaatio` → `Energiaseuranta`: Kulutusmittaukset (suora)
- `Kirjo` → `Raita`: Asiakasmaksut (tiedosto)
- `Kirjo` → `E-kirjasto`: Asiakkaiden tunnistetiedot (suora)
- `Kirjo` → `Omatoimi`: Kirjastokorttitiedot (suora)
- `Vesi- ja energialaskutus` → `Raita`: Laskutuksen kirjanpitoaineisto (tiedosto)
- `Asukashallinta` → `Kuntanäkymä`: Asuntotilastot (tiedosto)
- `Perintäpalvelu` → `Raita`: Perintätilitykset (tiedosto)
- `Tonttihaku` → `Tonttipalvelu`: Tonttihakemukset (suora)

## Liite B. Istutettujen puutteiden kohteet

| Tunnus | Kohteet mallissa (nimi ja tunniste) |
|---|---|
| P01 | `Kerro kartalla` (APP-0061) |
| P02 | `Kesätyösetelitiedot` (DAT-0081) |
| P03 | `Ympäristönsuojelu` (ACT-0060), `Ympäristöasiat` (APP-0299), `Asiarekisteri ja asiakirjat` (DAT-0001), `Kehä Systemsin pilvipalvelu` (NOD-0020), `Ympäristölupien ja -ilmoitusten käsittely` (PRC-0058) |
| P04 | `Tonttipalvelu` (APP-0063) |
| P05 | `Tonttipalvelu` (APP-0063), `Tonttihaku` (APP-0064) |
| P06 | `Tilakone` (APP-0078), `Tilavaraus Classic` (APP-0300) |
| P07 | `Lukudiplomi` (APP-0154), `Oppilastiedot` (DAT-0065) |
| P08 | `Englantikeidas` (APP-0140), `Oppilastiedot` (DAT-0065), `EU/ETA-alueen ulkopuolinen pilvialue` (LOC-0005), `Muut toimittajien SaaS-palvelut EU/ETA` (NOD-0032), `Oppimissovelluksen pilvipalvelu (Yhdysvallat)` (NOD-0038) |
| P09 | `Tietokantaklusteri Quarry` (NOD-0005) |
| P10 | `Pysäköintivahti` (APP-0073), `Henkilöiden perustiedot` (DAT-0027) |
| P11 | `Kuntatekniikka` (ACT-0062), `Infra-kone 2` (APP-0301), `Katu- ja viheromaisuustiedot` (DAT-0048), `Paikkatietopalvelinympäristö` (NOD-0006), `Katujen ja väylien ylläpito` (PRC-0063) |
| P12 | `Liikuntapaikkojen vuorojen jako ja varaukset` (PRC-0109), `Tilojen vuokraus ja tilavaraukset` (SRV-0059) |

## Liite C. Vastauksiin kuuluvat kohteet

### A01

- `Vaka-Reppu`: `Tietojärjestelmäomistaja, Sivistys`
- `Vaka-Reppu Asiointi`: `Tietojärjestelmäomistaja, Sivistys`

### A02

- `Kerro kartalla`: omistajaa ei ole kirjattu; käyttäjä `Maankäyttö ja kaavoitus`

### A03

- `Kansallinen lupapalvelu`: ulkoinen tarjoaja `Kansallinen ympäristökeskus`
- `Kansallinen rakennetun ympäristön tietojärjestelmä`: ulkoinen tarjoaja `Kansallinen ympäristökeskus`
- `Kartta-apu`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Kuittiskanneri`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Lupakone`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Piirustusarkisto`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Uutiskirjetyökalu`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Verkkokauppa Mini`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`

### A04

- Mahdollinen päällekkäisyys, `Asiarekisteri ja asiakirjat`: `Diaari`, `Ympäristöasiat`
- Mahdollinen päällekkäisyys, `Katu- ja viheromaisuustiedot`: `Infra-kone 2`, `Infrakone`
- Mahdollinen päällekkäisyys, varausjärjestelmät: `Eläinklinikka`, `Ohjaamo-ajanvaraus`, `Varaamo`, `Vuoro`
- Luontevaa työnjakoa, `Hankinta- ja sopimustiedot`: `Sopimus+`, `Tarjouspalvelu`
- Luontevaa työnjakoa, `Kantakartta ja paikkatietoaineistot`: `Karttakone`, `Mittaus Pro`
- Luontevaa työnjakoa, `Myyntilaskut ja saatavat`: `Kassa`, `Raita`
- Luontevaa työnjakoa, `Tiedonhallintamalli`: `Arkiva TOS`, `Arkki`
- Luontevaa työnjakoa, `Tilatiedot ja tilavaraukset`: `Tilakone`, `Varaamo`
- Luontevaa työnjakoa, `Tontti- ja maanvuokrasopimukset`: `Tonttihaku`, `Tonttipalvelu`
- Luontevaa työnjakoa, `Varhaiskasvatuksen asiakastiedot`: `Vaka-Reppu`, `Vaka-Reppu Asiointi`

### A05

- `Oikaisuvaatimusten ja valitusten käsittely`
- `Opinto-ohjaus ja jatko-opintoihin ohjaus`
- `Poikkeamis- ja suunnittelutarveasioiden käsittely`

### A06

- `Tonttipalvelu` → `Maanhankinta ja maankäyttösopimukset`; muut tukevat järjestelmät: ei yhtään
- `Tonttipalvelu` → `Tonttien luovutus`; muut tukevat järjestelmät: `Tilausportaali`, `Tonttihaku`

### A07

- `Kartta-apu` (Yksikön SaaS-pientyökalu): ei elinkaaripuutteita
- `Kuittiskanneri` (Yksikön SaaS-pientyökalu): ei elinkaaripuutteita
- `Lupakone` (Rakennusvalvonnan lupa- ja valvontajärjestelmä): `Pohjola Linux 7` tuki päättyi 30.6.2024; alusta `Tietokantaklusteri Quarry` poistuu 31.3.2027
- `Piirustusarkisto` (Rakennuslupapiirustusten sähköinen arkisto): `Polaris SQL 2016` tuki päättyi 14.7.2026
- `Uutiskirjetyökalu` (Yksikön SaaS-pientyökalu): ei elinkaaripuutteita
- `Verkkokauppa Mini` (Yksikön SaaS-pientyökalu): ei elinkaaripuutteita

### A08

- `Kerro kartalla` (tietojärjestelmä)
- `Kesätyösetelitiedot` (tietoaineisto)

### A09

- Tietovirta `Tilakone` → `Tilavaraus Classic`, vaikka `Tilavaraus Classic` on poistettu käytöstä (P06)
- `Lukudiplomi` käyttää aineistoa `Oppilastiedot`, mutta on merkitty henkilötiedottomaksi (P07)
- `Infrakone` ja `Infra-kone 2` kuvaavat todennäköisesti samaa järjestelmää (P11)
- `Pysäköintivahti` käyttää aineistoa `Henkilöiden perustiedot` ilman kuvattua lähdettä (P10)

### A10

- `Aurausseuranta`: sopimus päättyy 21.2.2027
- `Eläinklinikka`: sopimus päättyy 14.2.2027
- `Huoltokirja`: sopimus päättyy 2.7.2027
- `Infrakone`: `Geomatica Server 10` tuki 31.12.2026; `OpenRel 12` tuki 14.11.2024
- `Kaavakone`: `Geomatica Server 10` tuki 31.12.2026; `OpenRel 12` tuki 14.11.2024
- `Kaavapiirtäjä`: `Dotframe 4.8` tuki 11.1.2028; sopimus päättyy 9.5.2027
- `Kartta-apu`: sopimus päättyy 16.2.2027
- `Karttakone`: `Geomatica Server 10` tuki 31.12.2026; `OpenRel 12` tuki 14.11.2024; sopimus päättyy 27.2.2027
- `Kiinteistö+`: `Geomatica Server 10` tuki 31.12.2026; `OpenRel 12` tuki 14.11.2024; sopimus päättyy 18.5.2027
- `Kirjanpitoapu`: sopimus päättyy 3.1.2028
- `Kuittiskanneri`: sopimus päättyy 27.8.2028
- `Kulku`: `Automaatio BMS 5` tuki 31.12.2025
- `Laskentamestari`: `Dotframe 4.8` tuki 11.1.2028
- `Liikennemalli`: `Dotframe 4.8` tuki 11.1.2028
- `Lippu`: sopimus päättyy 19.6.2028
- `Lupakone`: `Pohjola Linux 7` tuki 30.6.2024; `Quarry Database 12c` tuki 31.3.2027; `Javelin Runtime 8` tuki 31.12.2026; alusta `Tietokantaklusteri Quarry` poistuu 31.3.2027
- `Malli 3D`: `Dotframe 4.8` tuki 11.1.2028
- `Mittaus Pro`: `Fenestra Server 2016` tuki 12.1.2027; `Polaris SQL 2016` tuki 14.7.2026; `Dotframe 4.8` tuki 11.1.2028
- `Määrälaskenta`: `Dotframe 4.8` tuki 11.1.2028; sopimus päättyy 15.8.2027
- `Piirto CAD`: `Dotframe 4.8` tuki 11.1.2028; sopimus päättyy 13.12.2026
- `Piirustusarkisto`: `Fenestra Server 2016` tuki 12.1.2027; `Polaris SQL 2016` tuki 14.7.2026; `Dotframe 4.8` tuki 11.1.2028; sopimus päättyy 1.2.2028
- `Pistepilvi`: `Dotframe 4.8` tuki 11.1.2028
- `Pysäköintivahti`: sopimus päättyy 8.6.2027
- `Rakenne-analyysi`: `Dotframe 4.8` tuki 11.1.2028; sopimus päättyy 6.4.2028
- `Rakennusautomaatio`: `Automaatio BMS 5` tuki 31.12.2025; sopimus päättyy 6.4.2028
- `Sähköinen ovikoodi`: sopimus päättyy 12.9.2028
- `Sähköinen vieraskirja`: sopimus päättyy 18.4.2027
- `Tiedostonjako`: sopimus päättyy 22.9.2028
- `Tietomallikatselin`: `Dotframe 4.8` tuki 11.1.2028
- `Tonttipalvelu`: `Fenestra Server 2012 R2` tuki 10.10.2023; `Polaris SQL 2014` tuki 9.7.2024; järjestelmä poistuu 30.6.2027
- `Uutiskirjetyökalu`: sopimus päättyy 26.9.2028
- `Verkkokauppa Mini`: sopimus päättyy 29.10.2028
- `Ympäristö+`: sopimus päättyy 12.2.2028
- `Ympäristöasiat`: sopimus päättyy 31.3.2028
- `Älylän karttapalvelu`: `Geomatica Server 10` tuki 31.12.2026; `OpenRel 12` tuki 14.11.2024

### A11

- `Fenestra Server 2012 R2`: tuki päättyi 10.10.2023; käyttävät `Tonttipalvelu`
- `Pohjola Linux 7`: tuki päättyi 30.6.2024; käyttävät `Lupakone`
- `Polaris SQL 2014`: tuki päättyi 9.7.2024; käyttävät `Tonttipalvelu`
- `OpenRel 12`: tuki päättyi 14.11.2024; käyttävät `Infrakone`, `Kaavakone`, `Karttakone`, `Kiinteistö+`, `Älylän karttapalvelu`
- `Automaatio BMS 5`: tuki päättyi 31.12.2025; käyttävät `Kulku`, `Rakennusautomaatio`
- `Sisältöhallinta Kaari 9`: tuki päättyi 30.4.2026; käyttävät `Sisänet`
- `Polaris SQL 2016`: tuki päättyi 14.7.2026; käyttävät `Lukkari`, `Mittaus Pro`, `Piirustusarkisto`, `Reppu`, `Tuki-Reppu`

### A12

- `Väylä Integrator 6` → `Väylä`
- `Vaka-Reppu` → `Kansallinen varhaiskasvatuksen tietovaranto`: Varhaiskasvatustiedot
- `Reppu` → `Kansallinen opintotietovaranto`: Opinto- ja arviointitiedot
- `Lupakone` → `Kansallinen rakennetun ympäristön tietojärjestelmä`: Rakennus- ja huoneistotiedot
- `Kaavakone` → `Kansallinen rakennetun ympäristön tietojärjestelmä`: Kaavatiedot

### A13

- `Asiointi`: `Tietojärjestelmäomistaja, Konsernihallinto`
- `Diaari Julkaisu`: `Tietojärjestelmäomistaja, Konsernihallinto`
- `Korjaa kaupunki`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Palautepolku`: `Tietojärjestelmäomistaja, Konsernihallinto`
- `Reittiopas`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Reppu Koti`: `Tietojärjestelmäomistaja, Sivistys`
- `Sähköinen asiointi kaupungin verkkopalvelussa`: `Palveluomistaja, Konsernihallinto`
- `Tonttihaku`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Työtä Älylässä`: `Tietojärjestelmäomistaja, Elinvoima`
- `Vaka-Reppu Asiointi`: `Tietojärjestelmäomistaja, Sivistys`
- `Valtuustolive`: `Tietojärjestelmäomistaja, Konsernihallinto`
- `Varaamo`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`
- `Visit Älylä`: `Tietojärjestelmäomistaja, Elinvoima`
- `Vuoro`: `Tietojärjestelmäomistaja, Sivistys`
- `Älylä-botti`: `Tietojärjestelmäomistaja, Konsernihallinto`
- `Älylä.fi`: `Tietojärjestelmäomistaja, Konsernihallinto`
- `Älylän karttapalvelu`: `Tietojärjestelmäomistaja, Kaupunkiympäristö`

### A14

- `Englantikeidas` toimii alustalla `Oppimissovelluksen pilvipalvelu (Yhdysvallat)` ja käyttää aineistoa `Oppilastiedot`

### A15

- `Diaari` (tietovirta)
- `Reppu` (tietovirta)
- `Vaka-Reppu` (tietovirta)
- `Pysäköintivahti` (käyttää tietoa, lähdettä ei kuvattu)
