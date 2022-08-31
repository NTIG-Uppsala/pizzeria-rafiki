# pizzeria-rafiki
![Site deployer](https://github.com/NTIG-Uppsala/pizzeria-rafiki/actions/workflows/deployment.yml/badge.svg)


## [Länk till live sida](https://ntig-uppsala.github.io/pizzeria-rafiki/)

## Github Workflows
Efter en ändring av koden så körs en [Github Workflow](https://github.com/NTIG-Uppsala/pizzeria-rafiki/tree/main/.github/workflows/deployment.yml). Den validerar koden, testar koden och sedan uppdaterar den publicerade sidan ifall valideringen och testerna gått igenom. Samt testar ifall den publicerade sidan fungerar som den ska.

Nedan finns steg för steg hur det fungerar:
### Steg 1. Valideringen
En [github action](https://github.com/linus-jansson/html5validator-action) validerar alla CSS- och HTML-filer i mappen `src/` och sedan avslutar med ett *pass* eller *fail*.

### Steg 2. Testning
Sidan startas lokalt på githubs servrar.

För att testa hemsidan används biblioteket Selenium kombinerat med pythons inbyggda bibliotek `unittest`. Selenium laddar in hemsidan på den lokala servern (se `src/tests/test_website.py` för innehållet av skriptet) och kör tester av innehållet på hemsidan i form av *unit tests*.

Pythonskriptet returnerar om testerna har gått igenom med ett *fail* eller *pass*.

### Steg 3. Publicering av hemsidan
För att den nya sidan ska publiceras måste `Steg 1` och `Steg 2` passera. Om testerna godkänns körs sista [*Actionen*](https://github.com/linus-jansson/github-pages-deploy-action) som tar all källkod i `src/` och skapar en ny branch `gh-pages` (om den inte finns).

När Github känner av att `gh-pages` branchen uppdateras startar den en publicering av den nya hemsidan.
### Steg 4. Testa att hemsidan är publicerad
När hemsidan har publicerats i `steg 3` körs samma tester som på `steg 2` på den publicerade hemsidan. Detta för att se att den lyckades publicera och att allt innehåll finns med.

### Uppdatera & Ladda ner dependencies lokalt
Skulle det installeras nya biliotek, alternativt att befintliga bibliotek uppdateras behöver `tests_requirements.txt` uppdateras. Detta gör man lättast genom att använda [pipreqs](https://pypi.org/project/pipreqs/) för att generera en fil med de bibliotek och versionsnummer som behövs.

För att installera de biblioteken som krävs skriver man `python -m pip install -r tests_requirements.txt`  