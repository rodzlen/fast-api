from fastapi import FastAPI, Depends

app = FastAPI()
DATA = {1:{'id': 1, 'name':"a", "price":2}, 2:{"id":2, "name":"b","price":2}}

def get_data():
    return DATA

@app.post('/items')
def get_item( items : dict = Depends(get_data)):
    return items

@app.post('/items/{item_id}')
def get_item(item_id : int, data : dict = Depends(get_data)):
    item = data.get(item_id)
    return item