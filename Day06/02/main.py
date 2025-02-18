from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket('/ws')
async def websocket_endpoint(websocket : WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f'서버응답 : {data}')
    except WebSocketDisconnect:
        print("클라이언트가 연결을 종료")
    except Exception as e:
        print(f"오류 발생: {e}")