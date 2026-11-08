"""Shared names and ID series for the published outputs.
ID series: U use cases, P planted gaps (puutteet), E model-internal imperfections, N noise, Q questions, A answers."""
MODEL_TITLE = 'Älylä – synteettinen kaupungin arkkitehtuurimalli'
VERSION = '1.1'
VERSION_HISTORY = [('1.1', '8.11.2026', 'Ensimmäisten testiajojen perusteella totuuskorttia tarkennettiin ja lisättiin pisteytyslomake.'),
                   ('1.0', '7.11.2026', 'Ensimmäinen julkaisu: perusversio, testiversio, totuuskortti, kysymykset, kohinaloki ja arkkitehtuuriperiaatteet.')]
PREFIX = 'alyla-arkkitehtuurimalli'
VARIANTS = {   # variant: (build file, export file, model name, start view line)
    'base': ('world.json', f'{PREFIX}-perusversio.xml', 'Älylän kaupunki - perusversio',
             'Tämä on perusversio. Siinä ei ole istutettuja puutteita eikä kohinaa.'),
    'test': ('world-test.json', f'{PREFIX}-testiversio.xml', 'Älylän kaupunki - testiversio',
             'Tämä on testiversio. Siihen on lisätty tarkoituksellisia puutteita ja kohinaa, jotka on kuvattu totuuskortissa ja kohinalokissa.'),
}
TEST = f'{PREFIX}-testiversio'
TRUTH_CARD, QUESTIONS, NOISE_LOG, SCORECARD = f'{TEST}-totuuskortti.md', f'{TEST}-kysymykset.md', f'{TEST}-kohinaloki.csv', f'{TEST}-pisteytys.md'
# Rules that apply to every answer
GLOBAL_MUST_NOT = ['Keksiä puuttuvaa tietoa, kuten omistajaa, kuvausta tai toimittajaa.',
                   'Esittää istutettua puutetta kohinana tai sivuuttaa sitä mahdollisena kohinana. Kohina ei koske istutettujen puutteiden kohteita.']
USE_CASES = {
    'U01': ('Neuvonta ja viestintä', 'Vastataan kysymyksiin arkkitehtuurista ja kerrotaan, kuka vastaa mistäkin.'),
    'U02': ('Nykytila-analyysi', 'Selvitetään nykytilan päällekkäisyyksiä, aukkoja ja riippuvuuksia.'),
    'U03': ('Tietoaukot ja ristiriidat', 'Etsitään puuttuvaa ja ristiriitaista tietoa mallista.'),
    'U04': ('Elinkaari ja tekninen velka', 'Selvitetään, mikä vanhenee ja mitä pitää uusia.'),
    'U05': ('Muutosten vaikutukset', 'Selvitetään, mihin muutos vaikuttaa ja kenelle siitä pitää kertoa.'),
}
def answer_id(qid): return 'A' + qid[1:]
