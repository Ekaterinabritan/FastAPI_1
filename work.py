from random import choice
from fastapi import FastAPI, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int = Field(default=None)
    title: str = Field(min_length=2, max_length=50)
    description: str = Field(max_length=200)
    status: str


items = []
for i in range(1, 21):
    item = Item(id=i,
                title=f'Заголовок{i}',
                description='Описание',
                status=f'{choice(["задача", "выполнено", "готово"])}')
    items.append(item)

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/')
async def root():
    return {'message': ' Item'}


@app.get('/items/', response_class=HTMLResponse)
async def get_tasks(request: Request):
    return templates.TemplateResponse('file.html', {'request': request, 'items': items, 'title': 'Item'})


@app.get('/items/{item_id}', response_model=Item)
async def get_item(item_id: int = Path(..., ge=1, le=len(items))):
    for item in items:
        if item.id == item_id:
            return task


@app.post('/items/', response_model=Item)
async def create_item(new_item: Item):
    new_item.id = len(items) + 1
    items.append(new_item)
    return new_item


@app.put('/items/{item_id}', response_model=Item)
async def update_item(new_item: Item, item_id: int = Path(..., ge=1, le=len(items))):
    for idx, item in enumerate(items):
        if item.id == item_id:
            new_item.id = item_id
            items[idx] = new_item
            return new_item


@app.delete('/items/{item_id}')
async def delete_item(item_id: int = Path(..., ge=1, le=len(items))):
    items.pop(item_id - 1)
    return {'message': f'item with id {item_id} was deleted'}


if __name__ == '__main__':
    uvicorn.run('work:app', host='127.0.0.1', port=8000, reload=True)