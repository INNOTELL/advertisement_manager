from nicegui import ui, app
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import uuid

# Inject Tailwind CDN once
ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')

# ===== Models =====
class AdvertIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=80)
    image_url: Optional[str] = None

class AdvertOut(AdvertIn):
    id: str

# ===== In-memory DB =====
DB: Dict[str, AdvertOut] = {}

def ghsc(amount: float) -> str:
    return f"GHS {amount:,.2f}"

# ===== REST API (FastAPI via NiceGUI) =====
@app.post('/api/adverts', response_model=AdvertOut)
def create_advert(ad: AdvertIn):
    advert_id = str(uuid.uuid4())
    out = AdvertOut(id=advert_id, **ad.dict())
    DB[advert_id] = out
    return out

@app.get('/api/adverts', response_model=List[AdvertOut])
def list_adverts():
    return list(DB.values())

@app.get('/api/adverts/{advert_id}', response_model=AdvertOut)
def get_advert(advert_id: str):
    if advert_id not in DB:
        raise HTTPException(status_code=404, detail='Advert not found')
    return DB[advert_id]

@app.put('/api/adverts/{advert_id}', response_model=AdvertOut)
def update_advert(advert_id: str, ad: AdvertIn):
    if advert_id not in DB:
        raise HTTPException(status_code=404, detail='Advert not found')
    updated = AdvertOut(id=advert_id, **ad.dict())
    DB[advert_id] = updated
    return updated

@app.delete('/api/adverts/{advert_id}')
def delete_advert(advert_id: str):
    if advert_id not in DB:
        raise HTTPException(status_code=404, detail='Advert not found')
    del DB[advert_id]
    return {'ok': True}

# ===== Demo seed =====
def seed():
    items = [
        AdvertIn(title='iPhone 13', description='Clean, slightly used', price=3500, category='Electronics',
                 image_url='https://cdn.pixabay.com/photo/2022/10/03/20/01/iphone-13-pro-max-7496758_960_720.jpg'),
        AdvertIn(title='Office furniture set', description='Ergonomic, adjustable lumbar support', price=650, category='Furniture',
                 image_url='https://cdn.alittledelightful.com/wp-content/uploads/2025/04/luxury-office-design.jpeg'),
        AdvertIn(title='2-Bed Apartment', description='Adenta – newly painted, gated', price=3500, category='Real Estate',
                 image_url='https://cf.bstatic.com/xdata/images/hotel/max1024x768/678821115.jpg?k=0a3e051bb43246c7a6b14138fcff77d5b1ab2d7b24956e0a1fdd004492e42638&o=&hp=1'),
        AdvertIn(title='Dell laptop', description='Brand new – core i5', price=3500, category='Electronics',
                 image_url='https://cdn.mos.cms.futurecdn.net/ScV86zVws5qDnowbP7KsWA.jpg'),
        AdvertIn(title='Cats', description='New fresh cat', price=3400, category='Animals',
                 image_url='https://www.vets4pets.com/siteassets/species/cat/two-cats-on-wall-in-sun.jpg'),   
        AdvertIn(title='Makeup', description='Santa Maria– Full set, nude', price=300, category='Cosmetics',
                 image_url='https://img.freepik.com/free-photo/close-up-collection-make-up-beauty-products_23-2148620012.jpg?semt=ais_hybrid&w=740&q=80'),
        AdvertIn(title='Duplex building', description='East Legon – newly painted, gated, to let', price=15000, category='Real Estate',
                 image_url='https://5.imimg.com/data5/SELLER/Default/2021/1/SY/PN/MU/33343279/duplex-modern-house-design.JPG'),   
        AdvertIn(title='Rice cooker', description='Lapaz – brand new,', price=350, category='Electronics',
                 image_url='https://gh.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/00/7961642/1.jpg?5175'),
        AdvertIn(title='Porche SUV', description='Awoshie – brand new, eng-V8', price=50000, category='Vehicles',
                 image_url='https://hips.hearstapps.com/hmg-prod/images/2025-porsche-cayenne-gts-124-68504e2bdc20b.jpg?crop=0.665xw:0.561xh;0.172xw,0.332xh&resize=1200:*'),
        AdvertIn(title='Comfy Couch', description='Adenta – Four sides, brown', price=3500, category='Furniture',
                 image_url='https://www.vigfurniture.com/media/wysiwyg/vig-1-new_[Yolonda].jpg'),                                                   
    ]
    for s in items:
        create_advert(s)
seed()

# ===== Pages (keep names & routes) =====
from components.header import show_header
from pages.home import show_home_page
from pages.add_event import show_add_event_page
from pages.edit_event import show_edit_event_page
from pages.view_event import show_view_event_page

@ui.page('/')
def index():
    show_header()
    show_home_page()

@ui.page('/add_event')
def add_page():
    show_header()
    show_add_event_page()

@ui.page('/edit_event')
def edit_page():
    show_header()
    show_edit_event_page()

@ui.page('/view_event')
def view_page():
    show_header()
    show_view_event_page()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(reload=True)
