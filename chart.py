import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from database import SessionLocal
import models

def chart():
    with SessionLocal() as db:
        try:
            thirty_minutes_ago = datetime.utcnow() - timedelta(minutes=30)
            prices_data = db.query(models.Crypto).filter(
                models.Crypto.created_at >= thirty_minutes_ago
            ).order_by(models.Crypto.created_at.asc()).all()

            if not prices_data:
                print("there are no items")
                return

            created_at = [p.created_at for p in prices_data]
            price = [p.crypto_price for p in prices_data]

            fig, ax = plt.subplots(figsize=(15,9))
            ax.plot(created_at, price,color='black',marker='o',linestyle='-',label='btc-price')
            ax.set_title('btc price chart')
            ax.set_xlabel('time')
            ax.set_ylabel('price')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.grid(True)
            ax.legend()
            file_path = "chart.png"
            fig.savefig(file_path, format='png')
            plt.close(fig)
            print(f"chart saved : {file_path}")
        except Exception as error:
            print(error)

chart()