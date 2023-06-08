'''


THE QUESTION: SHOULD WE INVEST IN BITCOIN OR NOT?
        
	
'''

# The main libraries.
import websocket, json
import pandas as pd 
import dateutil.parser
from datetime import timedelta

# Create the variables
time_processes = {}
time_candlesticks = []
cur_tick = None #current tick
pre_tick = None #previos tick

# Connection with websocket
socket = 'wss://ws-feed.exchange.coinbase.com'
def on_open(ws):
	print("Connection is opened")
	subscribe_msg = {
		"type": "subscribe",
		"channels": [
			{
			"name": "ticker",
			"product_ids": [
				"BTC-USD"
				]
			}
		]
	}

# Pull data from ws
	ws.send(json.dumps(subscribe_msg))

''' This will send the Json look like: {'type': 'ticker', 'sequence': 61479485394, 'product_id': 'BTC-USD', 'price': '26467.94', 'open_24h': '26804.58', 
                                        'volume_24h': '13627.16644495', 'low_24h': '26121.06', 'high_24h': '26981.69', 'volume_30d': '321185.94195378', 
                                        'best_bid': '26467.94', 'best_bid_size': '0.04562289', 'best_ask': '26469.84', 'best_ask_size': '0.27667000', 
                                        'side': 'sell', 'time': '2023-06-08T07:41:47.893326Z', 'trade_id': 537108931, 'last_size': '0.01215711'}
This will change in one minute
'''

def on_message(ws, message):
	global cur_tick, pre_tick

	pre_tick = cur_tick
	cur_tick = json.loads(message)

	print("=== Received Tick ===")
	print(f"{cur_tick['price']} @ {cur_tick['time']}")

# Candlestick Data Processing
    # Format the time style
	tick_datetime_object = dateutil.parser.parse(cur_tick['time'])
	timenow = tick_datetime_object + timedelta(hours=8)
	tick_dt = timenow.strftime("%m/%d/%Y %H:%M")
	print(tick_datetime_object.minute)
	print(tick_dt)

    # Create Candlesticks
	if not tick_dt in time_processes:
		print("This is a new candlestick")
		time_processes[tick_dt] = True

		if len(time_candlesticks) > 0:
			time_candlesticks[-1]['close'] = pre_tick['price']

		time_candlesticks.append({
			'minute': tick_dt, 
			'open': cur_tick['price'],
			'high': cur_tick['price'],
			'low': cur_tick['price']
			})
    # Save the Candlestick data to csv file
		df = pd.DataFrame(time_candlesticks[:-1])
		df.to_csv("bitcoin_data_tut.csv")
		
    # Update the current candlestick data
	if len(time_candlesticks) > 0:
		current_candlestick = time_candlesticks[-1]
		if cur_tick['price'] > current_candlestick['high']:
			current_candlestick['high'] = cur_tick['price']
		if cur_tick['price'] < current_candlestick['low']:
			current_candlestick['low'] = cur_tick['price']
			
		print("== Candlesticks ==")
		for candlestick in time_candlesticks:
			print(candlestick)
			
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()