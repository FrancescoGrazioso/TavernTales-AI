
```
  _______                      _______    _                         _____ 
 |__   __|                    |__   __|  | |                  /\   |_   _|
    | | __ ___   _____ _ __ _ __ | | __ _| | ___  ___ ______ /  \    | |  
    | |/ _` \ \ / / _ \ '__| '_ \| |/ _` | |/ _ \/ __|______/ /\ \   | |  
    | | (_| |\ V /  __/ |  | | | | | (_| | |  __/\__ \     / ____ \ _| |_ 
    |_|\__,_| \_/ \___|_|  |_| |_|_|\__,_|_|\___||___/    /_/    \_\_____|
                                                            
```

# TavernTales‑AI 🎲🧙‍♂️
*A Multiplayer D&D‑style campaign platform powered by an AI Dungeon Master*

![Python](https://img.shields.io/badge/python-3.12+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![License](https://img.shields.io/badge/license-MIT-blue)

> **TavernTales‑AI** lets a party of players connect, roll dice, and role‑play
> richly narrated adventures orchestrated by a Large Language Model (Google Gemini).  
> Think **AI Dungeon Master** meets virtual tabletop. ✨

- [Features](#features)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
- [Development workflow](#development-workflow)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Features 🚀

| Status | Module | Description |
| ------ | ------ | ----------- |
| ✅ | **Users & Auth** | JWT login / signup, password recovery |
| ✅ | **Characters** | Full D&D 5e character sheet CRUD |
| ✅ | **Party & Sessions** | Invite codes, lifecycle management |
| ✅ | **WebSockets & Chat** | Real-time chat + message history persisted |
| 🚧 | **AI Dungeon Master** | Gemini integration, context management |
| 🚧 | **Dice & Rules Engine** | SRD‑accurate dice roller + rule validator |
| ⏳ | **Content Moderation** | Automatic toxicity detection & session lockdown |
| ⏳ | **Admin Dashboard** | Live metrics, cost tracking, role‑based access |

Legend: ✅ done 🚧 in progress ⏳ planned

---

## Tech stack 🛠

| Layer | Tech |
| ----- | ---- |
| **Runtime** | Python 3.12, Django 4.2, Channels 4, Daphne |
| **Database** | PostgreSQL 15 |
| **Realtime** | Redis 7 (pub/sub) + Channels-Redis |
| **AI** | Google Gemini API |
| **DevOps** | GitHub Actions, Fly.io |
| **Observability** | Prometheus, Grafana, Loki |
| **Testing** | pytest, pytest‑django, Locust |

---

## Getting started 🐉

```bash
# clone & cd
git clone git@github.com:your‑org/taverntales‑ai.git
cd taverntales‑ai

# Python env
python3.12 -m venv .venv
source .venv/bin/activate

# install deps
pip install -r requirements.txt

# env vars
cp .env.example .env
# edit DB creds, Gemini key …

# migrate & run (ASGI server)
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/admin> to create users, or use the auth API.

### WebSocket test 🗨️

```bash
wscat -c ws://127.0.0.1:8000/ws/session/1/
```

(Requires a valid session & party membership.)

---

## Development workflow 🧰

| Command | Purpose |
| ------- | ------- |
| `pytest -q` | run unit & integration tests |
| `black . && ruff check .` | linting |
| `pip‑compile` | update lockfiles |

Pre‑commit hooks enforce formatting (`black`, `isort`, `ruff`) and tests.

---

## Roadmap 🗺

| Milestone | Target |
| --------- | ------ |
| **M1** | AI chat MVP (Gemini context, dice roller) |
| **M2** | Content moderation + SRD rule validator |
| **Beta** | Public lobby, persistent campaigns, load test 10 k WS |
| **1.0** | Front‑end launch, export/share adventures |

See the project board for granular issues.

---

## Contributing 🤝

1. Fork the repo and create a feature branch (`git checkout -b feat/my‑feature`).
2. Write tests and ensure `pytest` passes.
3. Run `ruff` & `black`.
4. Submit a pull request with a clear description.

All contributions are welcome—code, docs, bug reports, and spell‑checks!

---

## License 📝

Distributed under the **MIT License**.  

MIT License

Copyright (c) [2025] [Francesco Grazioso]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Credits 🙌

* Core devs: Francesco Grazioso
* SRD 5.1 content © Wizards of the Coast (Open Game License 1.0a)
* This project uses the Google Gemini API (© Google LLM)

*Roll high and have fun!* 🎲
