# Advertisement Management Platform (Part 1)

Python + NiceGUI app implementing a simple advertisement CRUD:

## Features
- Frontend pages:
  - Home (list/grid, search, category filter, delete with confirm)
  - Add Advert
  - Edit Advert
  - View Advert
- Backend API (in-memory for Part 1):
  - POST /api/adverts
  - GET /api/adverts
  - GET /api/adverts/{id}
  - PUT /api/adverts/{id}
  - DELETE /api/adverts/{id}
- Tailwind CSS via CDN
- Responsive UI (mobile & desktop)

## Run
```bash
pip install -r requirements.txt
python main.py
```

Open [http://localhost:8080](http://localhost:8080)

## Architecture

```mermaid
flowchart LR
  A[Browser UI<br/>NiceGUI pages] -->|fetch JSON| B[FastAPI app<br/>(from nicegui import app)]
  subgraph Frontend
    A
  end
  subgraph Backend
    B --> C[CRUD Handlers<br/>Pydantic validate]
    C --> D[(In-memory DB<br/>Dict[str, AdvertOut])]
  end
  E[Tailwind via CDN] -. styling .- A
```

## Frontend Deep Dive
- Pages: `home`, `add_event`, `edit_event`, `view_event` under `pages/` and `show_header` in `components/`.
- Data fetching: `ui.run_javascript('fetch(...)')` to call API; render with NiceGUI components.
- State/URL: search and category filters sync with URL (`/?q=&cat=`); navigation via `ui.navigate.to(...)`.
- Updates: use `@ui.refreshable` sections and call `.refresh()` after create/update/delete.

## Backend Deep Dive
- App: `from nicegui import ui, app` (FastAPI instance is `app`).
- Models: `AdvertIn` (input), `AdvertOut` (output with `id`). Pydantic enforces validation.
- Storage: `DB: Dict[str, AdvertOut]` (resets on restart). Seeded with 3 demo adverts.
- Endpoints: `POST/GET/GET{id}/PUT/DELETE` under `/api/adverts` with 404 on missing IDs.

## Recreate Steps (Team Split)

Backend
- Define Pydantic models and in-memory `DB`.
- Wire endpoints on `app` with response models and 404 handling.
- Seed demo data and ensure deterministic JSON shapes.

Frontend
- Add Tailwind in head: `ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')`.
- Implement pages with forms and grid; call API via `fetch` from `ui.run_javascript`.
- Keep filters in URL, and use `@ui.refreshable` for reactive reloads.

## Part 2: Database Migration Plan

Goal: swap in-memory dict for a real DB (e.g., SQLite) without changing the API contract.

Recommended Stack
- Option A: SQLModel (clean Pydantic + SQLAlchemy hybrid)
- Option B: SQLAlchemy + Pydantic schemas (classic split)

Schema
- Table: `adverts`
  - `id: UUID` (string/UUID primary key)
  - `title: str(120)`, `description: text`, `price: numeric(10,2)`, `category: str(80)`, `image_url: str|null`

Steps
1) Add deps: `sqlmodel` or `sqlalchemy` (and `psycopg2`/`sqlite` driver as needed).
2) Create engine and session maker; call `SQLModel.metadata.create_all(engine)` on startup.
3) Define ORM model; keep separate Pydantic `AdvertIn`/`AdvertOut` for API.
4) Replace CRUD functions to use a DB session (commit/refresh) and map ORM↔Pydantic.
5) Update seeding to insert rows if table empty.
6) Keep endpoints, URLs, and JSON shapes identical to avoid frontend changes.

Example (SQLModel sketch)
```python
from sqlmodel import SQLModel, Field, Session, create_engine, select

class Advert(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    description: str
    price: float
    category: str
    image_url: str | None = None

engine = create_engine('sqlite:///db.sqlite3')
SQLModel.metadata.create_all(engine)

def create(ad_in: AdvertIn) -> AdvertOut:
    with Session(engine) as s:
        obj = Advert(id=str(uuid.uuid4()), **ad_in.dict())
        s.add(obj); s.commit(); s.refresh(obj)
        return AdvertOut(**obj.dict())
```

Testing (CLI)
- Create: `curl -X POST http://localhost:8080/api/adverts -H "Content-Type: application/json" -d '{"title":"Bike","description":"MTB","price":800,"category":"Vehicles"}'`
- List: `curl http://localhost:8080/api/adverts`
- Get: `curl http://localhost:8080/api/adverts/<id>`
- Update: `curl -X PUT http://localhost:8080/api/adverts/<id> -H "Content-Type: application/json" -d '{...}'`
- Delete: `curl -X DELETE http://localhost:8080/api/adverts/<id>`
