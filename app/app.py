import datetime

import fastapi
from models import Session, Advertisement
import schema
from lifespan import lifespan
from depencies import SessionDependency
from crud import add_item, get_item
from fastapi import Query

app = fastapi.FastAPI(
    title="Advertisement API",
    version='0.0.1',
    description='some api',
    lifespan=lifespan
)

@app.get('/v1/advertisement/{advertisement_id}/', response_model=schema.GetAdvertisementResponse)
async def get_advertisement(session: SessionDependency, advertisement_id: int):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    return advertisement.dict

@app.get('/v1/advertisement/', response_model=list[schema.GetAdvertisementResponse])
async def search_advertisement(session: SessionDependency, title: str = Query(None),
                               author: str = Query(None), price: float = Query(None)):
    query = session.query(Advertisement)
    if title:
        query = query.filter(Advertisement.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Advertisement.author.ilike(f"%{author}%"))
    if price:
        query = query.filter(Advertisement.price.ilike(f"%{price}%"))
    advertisements = await query.all()
    return [advertisement.dict() for advertisement in advertisements]


@app.post('/v1/advertisement/', response_model=schema.CreateAdvertisementResponse,
          summary="Create new advertisement item")
async def create_advertisement(advertisement_json: schema.CreateAdvertisementRequest, session: SessionDependency):
    advertisement = Advertisement(**advertisement_json.dict())
    advertisement = await add_item(session, advertisement)
    return {'id': advertisement.id}


@app.patch('/v1/advertisement/{advertisement_id}/',
           response_model=schema.UpdateAdvertisementResponse,
         )
async def update_advertisement(advertisement_json: schema.UpdateAdvertisementRequest, session: SessionDependency, advertisement_id: int):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    advertisement_dict = advertisement_json.dict(exclude_unset=True)
    for field, valued in advertisement_dict.items():
        setattr(advertisement, field, valued)
    advertisement = await add_item(session, advertisement)
    return advertisement.dict


@app.delete('/v1/advertisement/{advertisement_id}/', response_model=schema.OkResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    await session.delete(advertisement)
    await session.commit()
    return {'status': 'ok'}
