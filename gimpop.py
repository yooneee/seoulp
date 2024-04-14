import aiohttp
import asyncio
from aiohttp import web
import aiohttp_cors
import os
import xmltodict  # xmltodict 라이브러리 추가

async def fetch_parking_data(session, url, params):
    async with session.get(url, params=params) as response:
        if response.status == 200:
            # XML 응답을 JSON으로 변환
            text = await response.text()
            data_dict = xmltodict.parse(text)
            return json.loads(json.dumps(data_dict))  # Convert XML dict to JSON
        else:
            return {"error": "Data fetching failed", "status": response.status}

async def get_all_airport_parking(request):
    service_key = os.getenv('SERVICE_KEY')
    base_url = "http://openapi.airport.co.kr/service/rest/AirportParkingCongestion/airportParkingCongestionRT"
    num_of_rows = request.query.get('numOfRows', '10')
    page_no = request.query.get('pageNo', '1')

    async with aiohttp.ClientSession() as session:
        tasks = []
        for airport_code in AIRPORT_CODES:
            params = {
                'serviceKey': service_key,
                'schAirportCode': airport_code,
                'numOfRows': num_of_rows,
                'pageNo': page_no,
                '_type': 'xml'  # 데이터 형식을 XML로 요청 (API가 JSON을 지원하지 않는 경우)
            }
            task = fetch_parking_data(session, base_url, params)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return web.json_response(results)

app = web.Application()
cors = aiohttp_cors.setup(app, defaults={
    "https://dalyoon.com": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

# 모든 공항 주차 혼잡도 정보 라우트 설정
all_parking_resource = cors.add(app.router.add_resource("/all-airport-parking"))
cors.add(all_parking_resource.add_route("GET", get_all_airport_parking))

if __name__ == '__main__':
    web.run_app(app, port=int(os.getenv('PORT', 8000)))