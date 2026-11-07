"""Write the truth card, the questions (without answers) and the noise log for the test version (names in labels.py)."""
import json, csv
from collections import Counter, defaultdict
from common import load, path
from labels import MODEL_TITLE, VARIANTS, TRUTH_CARD, QUESTIONS, NOISE_LOG, USE_CASES, answer_id, VERSION

W = json.load(open(path('build', 'world-planted.json'), encoding='utf-8'))
E = {e['id']: e for e in W['elements']}
plants = json.load(open(path('build', 'plants.json'), encoding='utf-8'))
ans = json.load(open(path('build', 'answers.json'), encoding='utf-8'))
noise = json.load(open(path('build', 'noise-log.json'), encoding='utf-8'))
spec = load('skeleton', 'noise.yaml')['noise']
prin = {p['key']: p for p in json.load(open(path('build', 'records.json'), encoding='utf-8'))['principles']}
EFFECT = {('N01', 'last_confirmed'): 'vahvistettu viimeksi yli kaksi vuotta sitten; vastaus voi todeta tiedon mahdollisesti vanhentuneeksi',
          ('N02', 'description'): 'kuvaus puuttuu; vastaus ei voi kertoa käyttötarkoitusta',
          ('N02', 'vendor'): 'toimittaja puuttuu; vastaus ei voi kertoa toimittajaa',
          ('N03', 'holder'): 'roolilta puuttuu henkilön nimi',
          ('N04', 'element'): 'kuvattu kahdesti; vastaus voi luetella sen kahdesti tai tunnistaa kaksoiskuvauksen',
          ('N05', 'element'): 'moduuli on kuvattu omana järjestelmänään; vastaus voi esittää sen erillisenä järjestelmänä',
          ('N06', 'relationships'): 'järjestelmällä ei ole suhteita, joten sitä ei löydä suhteita seuraamalla'}
NOISE_MEANS = {'N01': 'Vastaus voi todeta tiedon mahdollisesti vanhentuneeksi. Ei virhe.',
               'N02': 'Vastaus ei voi kertoa puuttuvaa tietoa. Ei virhe, jos vastaus ei keksi sitä.',
               'N03': 'Rooli on olemassa, mutta sen haltijaa ei tiedetä.',
               'N04': 'Vastaus voi luetella järjestelmän kahdesti; hyvä vastaus huomaa kaksoiskuvauksen.',
               'N05': 'Vastaus voi esittää moduulin erillisenä järjestelmänä.',
               'N06': 'Järjestelmä ei löydy suhteita seuraamalla; se löytyy vain nimellä tai luettelosta.'}
def code(i): return f"`{E[i]['name']}`" if i in E else i
today = W['world_today'].split('-'); today_fi = f"{int(today[2])}.{int(today[1])}.{today[0]}"
ex = next(q for q in ans['questions'] if q['id'] == 'Q02')
TEST_XML = VARIANTS['test'][1]

L = [f"# Totuuskortti: {MODEL_TITLE} (testiversio)", "",
     f"Tämä kortti kertoo, mitä testiversioon (`{TEST_XML}`, versio {VERSION}) on lisätty tarkoituksella ja mitä hyvän vastauksen pitäisi löytää.", "",
     "## Näin käytät korttia", "",
     "**Testiversio = perusversio + istutetut puutteet + kohina.**", "",
     "- **Mallin sisäinen epätäydellisyys (E)** on realistinen heikkous, joka on jo perusversiossa. Hyvä analyysi voi raportoida senkin.",
     "- **Istutettu puute (P)** on tarkoituksella lisätty aukko, ristiriita tai mahdollinen ongelma. Hyvän analyysin pitäisi huomata se.",
     "- **Kohina (N)** on tavallista epätäydellisyyttä, kuten puuttuva kuvaus. Hyvä vastaus sietää sen; se ei ole vastauksen virhe.",
     "- **Kysymys (Q)** ja sen **odotettu vastaus (A)** kuuluvat yhteen: kysymykseen Q01 vastaa A01.", "",
     "Mallin elementtien nimet, ominaisuudet ja tiedostonimet on kirjoitettu `näin`, jotta ne on helppo löytää Archista.", "",
     f"**Esimerkki.** Kysyt tekoälyltä kysymyksen {ex['id']}: \"{ex['question']}\" Vastauksen {answer_id(ex['id'])} mukaan hyvä vastaus mainitsee ainakin, että "
     f"{ex['points'][0][0].lower()}{ex['points'][0][1:]} Jos tekoäly keksii omistajan, vastaus on virheellinen.", "",
     f"Maailman päivä on {today_fi}. Käyttötapaukset (U01–U05) on kuvattu README-tiedostossa.", "",
     "**Sisältö:** 1. Mallin sisäiset epätäydellisyydet · 2. Istutetut puutteet · 3. Tarkoituksellisia erikoisuuksia · 4. Kohina · 5. Kysymykset ja vastaukset · Liitteet A–C", "",
     "## 1. Mallin sisäiset epätäydellisyydet", "", "Nämä ovat jo perusversiossa; niitä ei ole istutettu, vaan ne on laskettu mallista. Kaikki kohteet on lueteltu liitteessä A.", "",
      "| Tunnus | Epätäydellisyys | Yhteenveto |", "|---|---|---|"]
L += [f"| {b['id']} | {b['title']} | {b['summary']} |" for b in ans['baseline']] + [""]
L += ["## 2. Istutetut puutteet", "", "| Tunnus | Puute | Käyttötapaukset |", "|---|---|---|"]
L += [f"| {p['id']} | {p['title']} | {', '.join(p['use_cases'])} |" for p in plants] + [""]
for p in plants:
    pr = ', '.join(f"{int(prin[k]['id'][4:])} {prin[k]['title']}" for k in p['principles'] if k in prin)
    L += [f"### {p['id']} {p['title']}", "", f"**Mitä mallissa on:** {p['where']}", "", "**Mitä hyvä vastaus voisi sanoa:**", ""]
    L += [f"- {x}" for x in p['good_answer']] + [""]
    if pr: L += [f"**Periaate:** {pr}", ""]
L += ["## 3. Tarkoituksellisia erikoisuuksia", "", "Nämä voivat näyttää virheiltä, mutta ne ovat tarkoituksellisia.", "",
      "- Kansallisilla palveluilla sekä konserniyhtiöiden ja hyvinvointialueen järjestelmillä ei ole kaupungin omistajaa. Niillä on ulkoinen tarjoaja.",
      "- Konserniyhtiöiden ja hyvinvointialueen sisäistä rakennetta ei kuvata. Mallissa näkyvät vain niiden palvelut, järjestelmät ja yhteydet kaupunkiin.",
      "- Omistajaroolit ovat toimialatasolla, esimerkiksi `Tietojärjestelmäomistaja, Sivistys`. Henkilön nimi on roolin ominaisuudessa `holder`.",
      "- Järjestelmän vastuuyksikkö on se yksikkö, jota järjestelmä palvelee.",
      "- Noin 145 pientä järjestelmää on kuvattu kevyemmin: kuvauksena on järjestelmän tyyppi, ja toimittaja on usein pieni yritys.",
      "- Yksiköiden omat rekisterit (toimittaja \"Kaupunki (oma)\") sijaitsevat tiedostopalvelimella.",
      "- Integraatioalusta `Väylä` ja `Kansallinen tiedonvälityskerros` palvelevat järjestelmiä, joiden tietovirrat kulkevat niiden kautta. Tietovirran reitti on ominaisuudessa `via`.",
      "- Integraationäkymissä sama järjestelmä voi näkyä kahdesti, jotta kaikki tietovirrat kulkevat vasemmalta oikealle.",
      "- Säädökset perustuvat todelliseen lainsäädäntöön yleisellä tasolla, mutta eivät välttämättä heijasta oikeaa todellisuutta.", "",
      "## 4. Kohina", "", f"Kohina on levitetty malliin satunnaisesti, ja jokainen muutos on kirjattu kohinalokiin (`{NOISE_LOG}`). Kohina ei koske istutettujen puutteiden kohteita.", "",
      "| Tunnus | Kohina | Määrä | Mitä se tarkoittaa vastauksille |", "|---|---|---|---|"]
cnt = Counter(x['noise'] for x in noise)
L += [f"| {k} | {spec[k]['name']} | {cnt[k]} | {NOISE_MEANS.get(k, '')} |" for k in spec] + [""]
L += ["## 5. Kysymykset ja vastaukset", "", f"Kysymykset ilman vastauksia ovat tiedostossa `{QUESTIONS}`. Vastaukset on laskettu ennen kohinaa; kaikki vastauksiin kuuluvat kohteet on lueteltu liitteessä C.", "",
      "| Kysymys | Käyttötapaus | Istutetut puutteet |", "|---|---|---|"]
L += [f"| {q['id']} {q['question']} | {q['k']} | {', '.join(q['plants']) or '–'} |" for q in ans['questions']] + [""]
for q in ans['questions']:
    L += [f"### {q['id']} {q['question']}", "", f"*{q['k']} {USE_CASES[q['k']][0]}*", "", f"**{answer_id(q['id'])} – hyvä vastaus mainitsee ainakin:**", ""]
    L += [f"- {x}" for x in q['points']] + [""]
    if q['noise']:
        g = defaultdict(list)
        for x in q['noise']: g[x['target']].append(EFFECT.get((x['noise'], x['field']), x['noise']))
        L += ["**Testiversiossa kohina on muuttanut näitä kohteita.** Vastaus voi olla näiltä osin vajaampi, eikä sitä lasketa virheeksi:", ""]
        L += [f"- {code(t)}: {'; '.join(v)}" for t, v in sorted(g.items(), key=lambda kv: E.get(kv[0], {}).get('name', kv[0]))] + [""]
L += ["## Liite A. Mallin sisäiset epätäydellisyydet kokonaisuudessaan", ""]
for b in ans['baseline']:
    L += [f"### {b['id']} {b['title']}", ""] + ([b['note'], ""] if b['note'] else []) + [f"- {it['text']}" for it in b['items']] + [""]
L += ["## Liite B. Istutettujen puutteiden kohteet", "", "| Tunnus | Kohteet mallissa (nimi ja tunniste) |", "|---|---|"]
L += [f"| {p['id']} | {', '.join(f'{code(i)} ({i})' for i in p['elements'])} |" for p in plants] + [""]
L += ["## Liite C. Vastauksiin kuuluvat kohteet", ""]
for q in ans['questions']:
    L += [f"### {answer_id(q['id'])}", ""] + [f"- {it['text']}" for it in q['items']] + [""]
open(path('export', TRUTH_CARD), 'w', encoding='utf-8').write('\n'.join(L))

Qs = [f"# Kysymykset: {MODEL_TITLE} (testiversio)", "",
      f"Näillä kysymyksillä voi testata, miten tekoäly käyttää arkkitehtuurimallia (versio {VERSION}). Kysymykset on ryhmitelty käyttötapauksittain. "
      f"Odotetut vastaukset (A01–A{len(ans['questions']):02d}) ovat totuuskortissa (`{TRUTH_CARD}`).", ""]
cur = None
for q in ans['questions']:
    if q['k'] != cur:
        cur = q['k']; Qs += [f"## {cur} {USE_CASES[cur][0]}", "", USE_CASES[cur][1], ""]
    Qs += [f"{q['id']}. {q['question']}", ""]
open(path('export', QUESTIONS), 'w', encoding='utf-8').write('\n'.join(Qs))
with open(path('export', NOISE_LOG), 'w', encoding='utf-8', newline='') as f:
    wr = csv.writer(f, delimiter=';'); wr.writerow(['kohina', 'kuvaus', 'kohde', 'kohteen_nimi', 'kenttä', 'alkuperäinen', 'uusi'])
    for x in noise: wr.writerow([x['noise'], x['name'], x['target'], x['target_name'], x['field'], x['old'], x['new']])
print('truth card:', len(plants), 'gaps,', len(ans['baseline']), 'imperfections,', len(ans['questions']), 'questions |', len(noise), 'noise log rows')
