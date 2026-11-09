# devops-projektas

Mažas Flask API, su kuriuo dirbsite visą DevOps kursą. Be nustatymų naudoja SQLite failą; MySQL įjungiama nuo 18 pamokos.

## Paleidimas (Linux/WSL/Mac)

```
./run.sh
```

Atidarykite http://localhost:5000. Veikia su Python 3.9+ (`python3 --version`), joks papildomas diegimas Mac'e nereikalingas. Windows: naudokite WSL su Ubuntu (`wsl --install`), ne PowerShell. Jei `python3 -m venv` nusiskundžia (Ubuntu): `sudo apt install python3-venv`.

## Maršrutai

| Kelias | Ką daro |
|---|---|
| `GET /health` | `{"status": "ok"}`, kodas 200 |
| `GET /status` | versija, kompiuterio vardas, DB būsena |
| `GET /items` | daiktų sąrašas |
| `POST /items` | prideda daiktą: `curl -X POST -H 'Content-Type: application/json' -d '{"name":"X"}' localhost:5000/items` |
| `GET /` | paprastas puslapis |

## Testai

```
.venv/bin/pytest
```

## Nustatymai (aplinkos kintamieji)

Žr. `.env.example`. Nukopijuokite į `.env` (jis ignoruojamas Git, **niekada** jo nekelkite į GitHub).
`APP_VERSION`, `APP_COLOR` keičia puslapio juostą ir versiją.

## MySQL (nuo 18 pamokos)

Nustatykite `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (pvz. `.env`). Programa pati sukuria lentelę pagal `schema.mysql.sql` ir įkelia `seed.sql`. SQLite naudoja `schema.sqlite.sql` (skiriasi tik `AUTOINCREMENT` / `AUTO_INCREMENT`).

## Ko čia nėra

Dockerfile, docker-compose ir GitHub Actions workflow: juos susikursite patys pamokose.
