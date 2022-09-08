# pizzeria-rafiki
![Site deployer](https://github.com/NTIG-Uppsala/pizzeria-rafiki/actions/workflows/deployment.yml/badge.svg)


## [Länk till live sida](https://ntig-uppsala.github.io/pizzeria-rafiki/)

## GitHub Workflows
Efter en ändring av koden körs en [GitHub Workflow](https://github.com/NTIG-Uppsala/pizzeria-rafiki/tree/main/.github/workflows/deployment.yml). Den validerar koden, testar koden och uppdaterar den publicerade sidan ifall valideringen och testerna gått igenom samt testar ifall den publicerade sidan fungerar som den ska.

Nedan finns steg för steg hur det fungerar:
### Steg 1. Validering
En [GitHub action](https://github.com/linus-jansson/html5validator-action) validerar alla CSS- och HTML-filer i mappen `src/` och avslutar sedan med ett *pass* eller *fail*.

### Steg 2. Testning
Sidan startas lokalt på GitHub's servrar.

För att testa hemsidan används biblioteket Selenium kombinerat med Python's inbyggda bibliotek `unittest`. Selenium laddar in hemsidan på den lokala servern (se `{REPO_DIR}/tests/test_website.py` för innehållet av skriptet) och kör tester av innehållet på hemsidan i form av *unit tests*.

Pythonskriptet returnerar om testerna har gått igenom med ett *fail* eller *pass*.

### Steg 3. Publicering av hemsidan
För att den nya sidan ska publiceras måste `Steg 1` och `Steg 2` passera. Om testerna godkänns körs den sista [*action*](https://github.com/linus-jansson/github-pages-deploy-action) som tar all källkod i `src/` och skapar en ny *branch* `gh-pages` (om branchen inte redan finns).

När GitHub känner av att `gh-pages` branchen uppdateras startar den en publicering av den nya hemsidan.
### Steg 4. Testa att hemsidan är publicerad
När hemsidan har publicerats i `steg 3` körs samma tester som i `steg 2` på den publicerade hemsidan. Detta för att se att den lyckades publicera och att allt innehåll finns med.

### Uppdatera och Ladda ner dependencies lokalt
Skulle det installeras nya bibliotek, alternativt att befintliga bibliotek uppdateras behöver `tests_requirements.txt` uppdateras. Detta gör man lättast genom att använda [pipreqs](https://pypi.org/project/pipreqs/) för att generera en fil med de bibliotek och versionsnummer som behövs.

För att installera de bibliotek som krävs skriver man `python -m pip install -r tests_requirements.txt`.

### Testa lokalt
Kör tester lokalt genom att navigera till `{REPO_DIR}/tests/` i terminalen och köra `test_website.py` med Python (för att testerna ska kunna köras krävs att du har `firefox` installerat).

## Utvecklingsmiljö
Utdrag från `tests_requirements.txt`:
```
selenium==4.4.3
webdriver_manager==3.8.3
```

## Kodningsstandard
- Fyra mellanrum per tab
- Bara gemener för *element och attributes* i HTML
- Skriv all CSS i ett eget stylesheetdokument
- Variabelnamn:
    - snake_case ( *eg hello_world_test_variabel* )
- Klassnamn:
    - pascal case ( *eg HelloWorldTestClass* )
- CSS klass och IDn:
    - pascal case ( *eg HelloWorldTestClass* )

## Programmeringsspråk
#### GitHub
- Markdown filer
- YAML för GitHub workflows
#### Hemsida
- Frontend:
    - Html, css
#### Tester
- Python

## Definition of Done 
- 50% > av närvarande måste godkänna och förstå
- Koden incheckad och klar på GitHub
- Kommentarer klara
- Dokumentation
- Tester klara och koden klarar testerna
- Redo för presentation
- En färdig produkt:
    - Det ska funka.
    - Inga felmeddelanden.
    - Inga kompileringsfel.
    - användbart gränssnitt.

