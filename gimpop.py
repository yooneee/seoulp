import aiohttp
import asyncio
from aiohttp import web
import aiohttp_cors
import os
import xmltodict  # XML을 JSON 형식으로 변환하기 위해 필요

async def fetch_parking_data(session, url, params):
    async with session.get(url, params=params) as response:
        if response.status == 200:
            text = await response.text()
            data = xmltodict.parse(text)
            return data
        else:
            return {"error": "Data fetching failed", "status": response.status}

async def get_airport_parking(request):
    service_key = os.getenv('SERVICE_KEY_GIMPOPARK')
    base_url = "http://openapi.airport.co.kr/service/rest/AirportParkingCongestion/airportParkingCongestionRT"
    params = {
        'serviceKey': service_key,
        'schAirportCode': 'GMP',
        'numOfRows': '10',
        'pageNo': '1',
        '_type': 'json'
    }

    async with aiohttp.ClientSession() as session:
        result = await fetch_parking_data(session, base_url, params)
        return web.json_response(result)

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

resource = cors.add(app.router.add_resource("/gimpo-parking"))
cors.add(resource.add_route("GET", get_airport_parking))

if __name__ == '__main__':
    web.run_app(app, port=int(os.getenv('PORT', 8000)))