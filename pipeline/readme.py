"""Write README.md for the repository from the same data as the model (counts, use cases, gaps, noise)."""
import json
from collections import Counter
from common import load, path
from labels import VERSION, VERSION_HISTORY, MODEL_TITLE, VARIANTS, TRUTH_CARD, QUESTIONS, NOISE_LOG, SCORECARD, USE_CASES

base = json.load(open(path('build', 'world.json'), encoding='utf-8'))
test = json.load(open(path('build', 'world-test.json'), encoding='utf-8'))
plants = json.load(open(path('build', 'plants.json'), encoding='utf-8'))
ans = json.load(open(path('build', 'answers.json'), encoding='utf-8'))
noise = json.load(open(path('build', 'noise-log.json'), encoding='utf-8'))
spec = load('skeleton', 'noise.yaml')['noise']
rec = json.load(open(path('build', 'records.json'), encoding='utf-8'))
TYPES = [('Goal', 'Tavoitteet'), ('Constraint', 'Säädökset ja kansalliset vaatimukset'), ('Capability', 'Kyvykkyydet'), ('BusinessActor', 'Toimijat'),
         ('BusinessRole', 'Roolit'), ('BusinessService', 'Palvelut'), ('BusinessProcess', 'Prosessit'), ('DataObject', 'Tietoaineistot'),
         ('ApplicationComponent', 'Tietojärjestelmät'), ('SystemSoftware', 'Ohjelmistot'), ('Node', 'Teknologia-alustat'), ('Location', 'Sijainnit')]
bc, tc = Counter(e['type'] for e in base['elements']), Counter(e['type'] for e in test['elements'])
d = base['world_today'].split('-'); today = f"{int(d[2])}.{int(d[1])}.{d[0]}"
BASE_XML, TEST_XML = VARIANTS['base'][1], VARIANTS['test'][1]
L = [f"# {MODEL_TITLE}", "",
     "Älylän kaupunki on kuvitteellinen, noin 69 000 asukkaan kaupunki Älymaan maakunnassa. Tässä repositoryssa on kaupungin kokonaisarkkitehtuurimalli, "
     "jonka avulla voidaan testata tekoälyn käyttöä kokonaisarkkitehtuurityössä. Malli on luotu niin laajaksi, että sitä voi käyttää realistisena testiaineistona, "
     "ja siihen on lisätty tunnettuja puutteita, joiden avulla vastausten laatua voi arvioida.", "",
     "Kaikki nimet ja sisältö ovat kuvitteellisia. Säädökset perustuvat todelliseen lainsäädäntöön yleisellä tasolla, mutta eivät välttämättä heijasta oikeaa todellisuutta. "
     f"Versio {VERSION}. Maailman päivä on {today}.", "",
     "## Mallin variantit ja tiedostot", "", "| Tiedosto | Sisältö |", "|---|---|",
     f"| `export/{BASE_XML}` | Perusversio: realistinen malli ilman istutettuja puutteita ja kohinaa. Lähtökohta esittelyihin ja omiin kokeiluihin. |",
     f"| `export/{TEST_XML}` | Testiversio: perusversio, istutetut puutteet ja kohina. Käytetään vastausten arviointiin. |",
     f"| `export/{NOISE_LOG}` | Jokainen kohinan tekemä muutos. |",
     f"| `export/{QUESTIONS}` | Kysymyksiä mallin testaamiseen, ilman vastauksia. |",
     f"| `export/{TRUTH_CARD}` | Totuuskortti, eli mitä testiversioon on lisätty ja mitä hyvän vastauksen pitäisi löytää. |",
     f"| `export/{SCORECARD}` | Pisteytyslomake yhden testiajon arviointiin. |",
     f"| `export/records/` | Mallin ulkopuoliset tietueet. Mallia voi laajentaa erilaisilla tietueilla, kuten päätöksillä tai asiakirjoilla. Nyt mukana on {len(rec['principles'])} arkkitehtuuriperiaatetta kuudella alueella (`periaatteet/`). |", "",
     "Mallit ovat standardinmukaisia ArchiMate 3.2 -malleja Open Groupin mallinvaihtomuodossa (Model Exchange File Format), joten ne voi avata Archissa ja muissa muotoa tukevissa työkaluissa. Archissa mallit avataan näin: File → Import → Open Exchange XML Model. Kummankin mallin aloitusnäkymä kertoo, mistä variantista on kyse.", "",
     "## Mallin sisältö", "", "| Elementtityyppi | Perusversio | Testiversio |", "|---|---|---|"]
L += [f"| {fi} | {bc[t]} | {tc[t]} |" for t, fi in TYPES]
L += [f"| Suhteet | {len(base['relationships'])} | {len(test['relationships'])} |", "",
      "Organisaatio kattaa neljä toimialaa (Konsernihallinto, Elinvoima, Kaupunkiympäristö, Sivistys), konserniyhtiöt mustina laatikoina, Älymaan hyvinvointialueen ja kansalliset viranomaiset. "
      "Tietojärjestelmistä noin puolet on yksiköiden pieniä järjestelmiä, jotka on kuvattu kevyemmin.", "",
      "Näkymät: 01. Karttanäkymät (yksi näkymä kutakin elementtityyppiä kohden), 02. Kerrosnäkymät (toimialoittain yksi näkymä kustakin prosessista toimijoista sijainteihin) "
      "ja 03. Integraationäkymät (yksiköittäin tietojärjestelmien tietovirrat).", "",
      "## Tunnisteet", "", "| Tunnus | Merkitys |", "|---|---|",
      "| U01… | Käyttötapaus |", "| E01… | Mallin sisäinen epätäydellisyys (on jo perusversiossa) |", "| P01… | Istutettu puute |",
      "| N01… | Kohina |", "| Q01… | Kysymys |", "| A01… | Kysymyksen odotettu vastaus |", "",
      "## Käyttötapaukset", "", "Testiaineisto on rakennettu viiden käyttötapauksen ympärille. Kuhunkin liittyy kolme kysymystä.", "",
      "| Tunnus | Käyttötapaus | Mitä tehdään |", "|---|---|---|"]
L += [f"| {k} | {n} | {d_} |" for k, (n, d_) in USE_CASES.items()]
L += ["", "## Istutetut puutteet", "", f"Testiversioon on istutettu {len(plants)} puutetta: aukkoja, ristiriitoja ja mahdollisia ongelmia. Yksityiskohdat ja odotetut vastaukset ovat totuuskortissa.", "",
      "| Tunnus | Puute | Käyttötapaukset |", "|---|---|---|"]
L += [f"| {p['id']} | {p['title']} | {', '.join(p['use_cases'])} |" for p in plants]
L += ["", f"Lisäksi totuuskortissa on {len(ans['baseline'])} mallin sisäistä epätäydellisyyttä (E), jotka ovat jo perusversiossa, ja {len(ans['questions'])} kysymystä (Q) odotettuine vastauksineen (A).", "",
      "## Kohina", "", "Kohina on realistista epätäydellisyyttä, joka on levitetty testiversioon satunnaisesti. Se ei koske istutettujen puutteiden kohteita.", "",
      "| Tunnus | Kohina | Määrä |", "|---|---|---|"]
cnt = Counter(x['noise'] for x in noise)
L += [f"| {k} | {spec[k]['name']} | {cnt[k]} |" for k in spec]
L += ["", "## Mallin generoinnissa käytetyt työkalut", "",
      "| Polku | Sisältö |", "|---|---|",
      "| `metamodel.yaml` | Metamalli: mitä malliin saa kuulua. Kentät englanniksi, sisältö suomeksi. |",
      "| `skeleton/` | Käsin suunniteltu lähdeaineisto: organisaatio, palvelut, prosessit, kyvykkyydet, tavoitteet, säädökset, tietoaineistot, tietojärjestelmät, teknologia, periaatteet, istutetut puutteet ja kohina. |",
      "| `pipeline/` | Generointi, validointi ja vienti. |",
      "| `state/` | Pysyvät tunnisteet (`ids.yaml`). Generoitu, mutta versionhallinnassa, jotta elementin tunniste säilyy, vaikka malli generoidaan uudelleen. |",
      "| `world.yaml` | Siemenluku ja maailman päivä. |",
      "| `export/` | Valmiit mallit ja niiden oheistiedostot. |",
      "| `build/` | Välivaiheet (ei versionhallinnassa). |", "",
      "## Mallin generointi", "",
      "Tarvitaan Python 3.10 tai uudempi ja PyYAML (`pip install -r requirements.txt`). Koko malli generoidaan komennolla:", "",
      "```", "python pipeline/build.py", "```", "",
      "Vaiheet: perusversio (generate) → periaatteet (records) → istutetut puutteet (plant) → kohina (noise) → odotetut vastaukset (answers) → validointi (validate) "
      "→ Archi-viennit (export_mef) → totuuskortti (truthcard) → tämä README (readme). Sama siemenluku tuottaa aina saman mallin.", "",
      "## Mallin muuttaminen", "",
      "- Muutokset tehdään `skeleton/`-kansion tiedostoihin, ei Archissa näkymiin. Näkymät ja viennit tuotetaan uudelleen joka kerta.",
      "- Satunnaiset arvot, kuten päivämäärät, lasketaan kullekin kohteelle erikseen. Yhden kohteen muuttaminen ei siksi muuta muiden kohteiden arvoja.",
      "- Uudet elementtityypit ja ominaisuuksien arvot lisätään ensin metamalliin. Sen jälkeen validointi hyväksyy ne.",
      "- Validointi tarkistaa molemmat variantit. Istutetut poikkeamat on kuvattu `skeleton/plants.yaml`-tiedostossa.", "",
      "## Versiohistoria", "", "| Versio | Päivämäärä | Muutokset |", "|---|---|---|"] + [f"| {v} | {d} | {t} |" for v, d, t in VERSION_HISTORY] + ["",
      "## Jatkokehitysmahdollisuuksia", "",
      "Malli on rakennettu niin, että sitä voi laajentaa ilman, että nykyinen sisältö muuttuu. Tunnisteet säilyvät, ja uusi aineisto liitetään olemassa oleviin elementteihin. Mallia voi laajentaa esimerkiksi seuraavilla:", "",
      "- Arkkitehtuuripäätökset ja poikkeamat periaatteista.",
      "- Kehittämiskohteet, kuten hankkeet ja hankinnat, sekä niiden vaikutukset malliin.",
      "- Asiakirjat, kuten strategiat, suunnitelmat ja ote tietojärjestelmärekisteristä.",
      "- Näihin liittyvät uudet puutteet, kohina ja kysymykset.",
      "- Ajassa tapahtuvat muutokset, kuten uudet hankkeet tai lakimuutokset, muutoksiin reagoivien käyttötapausten kokeiluun.",
      "- Konserniyhtiöiden sisäinen rakenne tai uudet toimialat, jos mallista halutaan laajempi.",
      "- Tekoälyn lukuyhteys malliin, esimerkiksi MCP-työkalut.", "",
      "## Lisenssi", "", "Katso [LICENSE](LICENSE)."]
open(path('README.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('README.md written')
