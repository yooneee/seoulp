import aiohttp
import asyncio
from aiohttp import web
import os

async def fetch_parking_data(session, url, params):
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            return {"error": "Data fetching failed", "status": response.status}

async def get_parking_status(request):
    service_key = os.getenv('SERVICE_KEY_INCHEON')
    base_url = "http://apis.data.go.kr/B551177/StatusOfParking/getTrackingParking"
    params = {
        'serviceKey': service_key,
        'numOfRows': '50',
        'pageNo': '1',
        'type': 'json'
    }

    async with aiohttp.ClientSession() as session:
        result = await fetch_parking_data(session, base_url, params)
        return web.json_response(result)

app = web.Application()
app.router.add_get('/get-parking-status', get_parking_status)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=int(os.getenv('PORT', 8080)))