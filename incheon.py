import aiohttp
import asyncio
from aiohttp import web
import aiohttp_cors  # CORS 지원을 위한 라이브러리 추가
import os

async def fetch_parking_data(session, url, params):
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            return {"error": "Data fetching failed", "status": response.status}

async def get_parking_status(request):
    service_key = os.getenv('SERVICE_KEY_INCHEON')  # 환경 변수에서 서비스 키 가져오기
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
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

# CORS 설정 적용한 라우트 설정
resource = cors.add(app.router.add_resource("/get-parking-status"))
cors.add(resource.add_route("GET", get_parking_status))

if __name__ == '__main__':
    web.run_app(app, port=int(os.getenv('PORT', 8080)))