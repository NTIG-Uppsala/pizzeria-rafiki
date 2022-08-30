# pizzeria-rafiki
![Site deployer](https://github.com/NTIG-Uppsala/pizzeria-rafiki/actions/workflows/deployment.yml/badge.svg)

## Testing
Unittests används för att testa hemsidan, dess tillgänglighet och delar av hemsidan såsom innehållet. Skripten i `src/tests/` installerar automatiskt den senaste chrome drivern som behövs för att kunna simulera en webläsare. För att installerar man de dependencies som behövs så behöver man `python 3.10+` och sedan installera genom att köra `python -m pip install -r tests_requirements.txt`.

Testerna kan även köras som github action för att automatisera körninge. [Se här för mer info](https://github.com/NTIG-Uppsala/pizzeria-rafiki/tree/main/.github/workflows)

## Uppdatera dependencies
Skulle det installera nya biliotek eller något behöver uppdateras så kan man använda [pipreqs](https://pypi.org/project/pipreqs/) för att generera en dependencies fil med de bibliotek som användas i skriptet.

## HTML validering
En [github action](https://github.com/linus-jansson/html5validator-action) validerar koden vid varje push & pull-request

## Website deployment
Hemsidan deployas med hjälp av [en action](https://github.com/linus-jansson/github-pages-deploy-action). Om någon action misslyckas kommer inte senaste versionen av sidan publiceras.