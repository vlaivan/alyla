# Älylä – synteettinen kaupungin arkkitehtuurimalli

Älylän kaupunki on kuvitteellinen, noin 69 000 asukkaan kaupunki Älymaan maakunnassa. Tässä repositoryssa on kaupungin kokonaisarkkitehtuurimalli, jonka avulla voidaan testata tekoälyn käyttöä kokonaisarkkitehtuurityössä. Malli on luotu niin laajaksi, että sitä voi käyttää realistisena testiaineistona, ja siihen on lisätty tunnettuja puutteita, joiden avulla vastausten laatua voi arvioida.

Kaikki nimet ja sisältö ovat kuvitteellisia. Säädökset perustuvat todelliseen lainsäädäntöön yleisellä tasolla, mutta eivät välttämättä heijasta oikeaa todellisuutta. Versio 1.1. Maailman päivä on 1.11.2026.

## Mallin variantit ja tiedostot

| Tiedosto | Sisältö |
|---|---|
| `export/alyla-arkkitehtuurimalli-perusversio.xml` | Perusversio: realistinen malli ilman istutettuja puutteita ja kohinaa. Lähtökohta esittelyihin ja omiin kokeiluihin. |
| `export/alyla-arkkitehtuurimalli-testiversio.xml` | Testiversio: perusversio, istutetut puutteet ja kohina. Käytetään vastausten arviointiin. |
| `export/alyla-arkkitehtuurimalli-testiversio-kohinaloki.csv` | Jokainen kohinan tekemä muutos. |
| `export/alyla-arkkitehtuurimalli-testiversio-kysymykset.md` | Kysymyksiä mallin testaamiseen, ilman vastauksia. |
| `export/alyla-arkkitehtuurimalli-testiversio-totuuskortti.md` | Totuuskortti, eli mitä testiversioon on lisätty ja mitä hyvän vastauksen pitäisi löytää. |
| `export/alyla-arkkitehtuurimalli-testiversio-pisteytys.md` | Pisteytyslomake yhden testiajon arviointiin. |
| `export/records/` | Mallin ulkopuoliset tietueet. Mallia voi laajentaa erilaisilla tietueilla, kuten päätöksillä tai asiakirjoilla. Nyt mukana on 20 arkkitehtuuriperiaatetta kuudella alueella (`periaatteet/`). |

Mallit ovat standardinmukaisia ArchiMate 3.2 -malleja Open Groupin mallinvaihtomuodossa (Model Exchange File Format), joten ne voi avata Archissa ja muissa muotoa tukevissa työkaluissa. Archissa mallit avataan näin: File → Import → Open Exchange XML Model. Kummankin mallin aloitusnäkymä kertoo, mistä variantista on kyse.

## Mallin sisältö

| Elementtityyppi | Perusversio | Testiversio |
|---|---|---|
| Tavoitteet | 12 | 12 |
| Säädökset ja kansalliset vaatimukset | 30 | 30 |
| Kyvykkyydet | 85 | 85 |
| Toimijat | 111 | 111 |
| Roolit | 15 | 15 |
| Palvelut | 114 | 114 |
| Prosessit | 148 | 148 |
| Tietoaineistot | 82 | 82 |
| Tietojärjestelmät | 282 | 290 |
| Ohjelmistot | 37 | 37 |
| Teknologia-alustat | 37 | 38 |
| Sijainnit | 9 | 9 |
| Suhteet | 2369 | 2389 |

Organisaatio kattaa neljä toimialaa (Konsernihallinto, Elinvoima, Kaupunkiympäristö, Sivistys), konserniyhtiöt mustina laatikoina, Älymaan hyvinvointialueen ja kansalliset viranomaiset. Tietojärjestelmistä noin puolet on yksiköiden pieniä järjestelmiä, jotka on kuvattu kevyemmin.

Näkymät: 01. Karttanäkymät (yksi näkymä kutakin elementtityyppiä kohden), 02. Kerrosnäkymät (toimialoittain yksi näkymä kustakin prosessista toimijoista sijainteihin) ja 03. Integraationäkymät (yksiköittäin tietojärjestelmien tietovirrat).

## Tunnisteet

| Tunnus | Merkitys |
|---|---|
| U01… | Käyttötapaus |
| E01… | Mallin sisäinen epätäydellisyys (on jo perusversiossa) |
| P01… | Istutettu puute |
| N01… | Kohina |
| Q01… | Kysymys |
| A01… | Kysymyksen odotettu vastaus |

## Käyttötapaukset

Testiaineisto on rakennettu viiden käyttötapauksen ympärille. Kuhunkin liittyy kolme kysymystä.

| Tunnus | Käyttötapaus | Mitä tehdään |
|---|---|---|
| U01 | Neuvonta ja viestintä | Vastataan kysymyksiin arkkitehtuurista ja kerrotaan, kuka vastaa mistäkin. |
| U02 | Nykytila-analyysi | Selvitetään nykytilan päällekkäisyyksiä, aukkoja ja riippuvuuksia. |
| U03 | Tietoaukot ja ristiriidat | Etsitään puuttuvaa ja ristiriitaista tietoa mallista. |
| U04 | Elinkaari ja tekninen velka | Selvitetään, mikä vanhenee ja mitä pitää uusia. |
| U05 | Muutosten vaikutukset | Selvitetään, mihin muutos vaikuttaa ja kenelle siitä pitää kertoa. |

## Istutetut puutteet

Testiversioon on istutettu 12 puutetta: aukkoja, ristiriitoja ja mahdollisia ongelmia. Yksityiskohdat ja odotetut vastaukset ovat totuuskortissa.

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

Lisäksi totuuskortissa on 7 mallin sisäistä epätäydellisyyttä (E), jotka ovat jo perusversiossa, ja 15 kysymystä (Q) odotettuine vastauksineen (A).

## Kohina

Kohina on realistista epätäydellisyyttä, joka on levitetty testiversioon satunnaisesti. Se ei koske istutettujen puutteiden kohteita.

| Tunnus | Kohina | Määrä |
|---|---|---|
| N01 | Vahvistamatta yli kaksi vuotta | 180 |
| N02 | Puuttuva kuvaus tai toimittaja | 25 |
| N03 | Roolin haltija puuttuu | 1 |
| N04 | Pienjärjestelmä kuvattu kahdesti | 3 |
| N05 | Moduuli kuvattu omana järjestelmänä | 2 |
| N06 | Irrallinen järjestelmä ilman suhteita | 6 |

## Mallin generoinnissa käytetyt työkalut

| Polku | Sisältö |
|---|---|
| `metamodel.yaml` | Metamalli: mitä malliin saa kuulua. Kentät englanniksi, sisältö suomeksi. |
| `skeleton/` | Käsin suunniteltu lähdeaineisto: organisaatio, palvelut, prosessit, kyvykkyydet, tavoitteet, säädökset, tietoaineistot, tietojärjestelmät, teknologia, periaatteet, istutetut puutteet ja kohina. |
| `pipeline/` | Generointi, validointi ja vienti. |
| `state/` | Pysyvät tunnisteet (`ids.yaml`). Generoitu, mutta versionhallinnassa, jotta elementin tunniste säilyy, vaikka malli generoidaan uudelleen. |
| `world.yaml` | Siemenluku ja maailman päivä. |
| `export/` | Valmiit mallit ja niiden oheistiedostot. |
| `build/` | Välivaiheet (ei versionhallinnassa). |

## Mallin generointi

Tarvitaan Python 3.10 tai uudempi ja PyYAML (`pip install -r requirements.txt`). Koko malli generoidaan komennolla:

```
python pipeline/build.py
```

Vaiheet: perusversio (generate) → periaatteet (records) → istutetut puutteet (plant) → kohina (noise) → odotetut vastaukset (answers) → validointi (validate) → Archi-viennit (export_mef) → totuuskortti (truthcard) → tämä README (readme). Sama siemenluku tuottaa aina saman mallin.

## Mallin muuttaminen

- Muutokset tehdään `skeleton/`-kansion tiedostoihin, ei Archissa näkymiin. Näkymät ja viennit tuotetaan uudelleen joka kerta.
- Satunnaiset arvot, kuten päivämäärät, lasketaan kullekin kohteelle erikseen. Yhden kohteen muuttaminen ei siksi muuta muiden kohteiden arvoja.
- Uudet elementtityypit ja ominaisuuksien arvot lisätään ensin metamalliin. Sen jälkeen validointi hyväksyy ne.
- Validointi tarkistaa molemmat variantit. Istutetut poikkeamat on kuvattu `skeleton/plants.yaml`-tiedostossa.

## Versiohistoria

| Versio | Päivämäärä | Muutokset |
|---|---|---|
| 1.1 | 8.11.2026 | Ensimmäisten testiajojen perusteella totuuskorttia tarkennettiin ja lisättiin pisteytyslomake. |
| 1.0 | 7.11.2026 | Ensimmäinen julkaisu: perusversio, testiversio, totuuskortti, kysymykset, kohinaloki ja arkkitehtuuriperiaatteet. |

## Jatkokehitysmahdollisuuksia

Malli on rakennettu niin, että sitä voi laajentaa ilman, että nykyinen sisältö muuttuu. Tunnisteet säilyvät, ja uusi aineisto liitetään olemassa oleviin elementteihin. Mallia voi laajentaa esimerkiksi seuraavilla:

- Arkkitehtuuripäätökset ja poikkeamat periaatteista.
- Kehittämiskohteet, kuten hankkeet ja hankinnat, sekä niiden vaikutukset malliin.
- Asiakirjat, kuten strategiat, suunnitelmat ja ote tietojärjestelmärekisteristä.
- Näihin liittyvät uudet puutteet, kohina ja kysymykset.
- Ajassa tapahtuvat muutokset, kuten uudet hankkeet tai lakimuutokset, muutoksiin reagoivien käyttötapausten kokeiluun.
- Konserniyhtiöiden sisäinen rakenne tai uudet toimialat, jos mallista halutaan laajempi.
- Tekoälyn lukuyhteys malliin, esimerkiksi MCP-työkalut.

## Lisenssi

Katso [LICENSE](LICENSE).
