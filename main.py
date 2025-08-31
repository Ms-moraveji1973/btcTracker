from fastapi import FastAPI , HTTPException , status
from aiohttp import ClientSession
from database import engine , SessionLocal
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime , timedelta
from aiohttp_socks import ProxyConnector


import models
from send_message import send , client

async def check_btc():
    connector = ProxyConnector.from_url('socks5://127.0.0.1:9052')
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"
    with SessionLocal() as db :
        try :
            async with ClientSession(connector=connector) as session:
                async with session.get(url) as response:
                    data = await response.json()
                    if response.status == 200:
                        get_info = data[0]
                        crypto_name = get_info.get('name')
                        crypto_price = get_info.get('current_price')
                        last_five_minute = datetime.utcnow() - timedelta(minutes=5)
                        last_crypto = db.query(models.Crypto).filter(models.Crypto.created_at <= last_five_minute)\
                            .order_by(models.Crypto.id.desc()).first()
                        if last_crypto :
                            calculate_presentage = ((crypto_price-last_crypto.crypto_price ) / last_crypto.crypto_price) * 100
                            print(calculate_presentage)
                            if calculate_presentage > 3 :
                                print('message sended')
                                await send()
                        add_database = models.Crypto(crypto_symbol=crypto_name, crypto_price=crypto_price,created_at=datetime.utcnow())
                        db.add(add_database)
                        db.commit()
                        print('this is working')
                        print(f"{crypto_name} : {crypto_price}")
                    else :
                        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error")
        except Exception as e :
            print(f"an error occurred: {e}")


scheduler = AsyncIOScheduler()
@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.start()
    print('client connected')
    scheduler.add_job(check_btc, 'interval',minutes=1)
    scheduler.start()
    print('scheduler started')
    yield
    scheduler.shutdown()
    print('scheduler shutdown')
    await client.disconnect()
    print('client disconnected')

app = FastAPI(lifespan=lifespan)

models.Base.metadata.create_all(engine)

