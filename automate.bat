@echo off
"C:\Users\Ron\AppData\Local\Programs\Python\Python311\python.exe" ./run.py -p 5000
pause
@echo on
curl http://localhost:5000/mine
curl -X POST -H "Content-Type: application/json" -d '{"sender": "address1", "recipient": "address2", "amount": 5}' http://localhost:5000/transactions/new
curl http://localhost:5000/chain
curl -X POST -H "Content-Type: application/json" -d '{"nodes": ["http://localhost:5001"]}' http://localhost:5000/nodes/register
curl http://localhost:5000/nodes/resolve
python blockchain.py -p 5000
python blockchain.py -p 5001
python blockchain.py -p 5002
curl -X POST -H "Content-Type: application/json" -d '{"nodes": ["http://localhost:5001"]}' http://localhost:5000/nodes/register
