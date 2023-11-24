<h1>Client-Centric Consistency Project-3</h1>
## Environment
WSL Ubuntu 20.04LTS
python 3.10.12

```
git clone https://github.com/crypto0627/client-centric-consistency.git
cd client-centric-consistency/grpc/grpc
```

## Steps
```
python3 -m pip install --upgrade pip
pip install grpcio grpcio-tools
sudo python3 -m grpc_tools.protoc -I. --python_out=.   --pyi_out=. --grpc_python_out=. ./branch.proto
```
Default input file is "input.json" in main.py.
<img width="286" alt="image" src="https://github.com/crypto0627/client-centric-consistency/assets/62930885/29b097d2-2788-4eb0-aa8f-cbba2f019b65">
<br/>
Change two of input files -->
<img width="233" alt="image" src="https://github.com/crypto0627/client-centric-consistency/assets/62930885/dc5327ed-5a02-4050-ba64-89756ab88a28">
<img width="238" alt="image" src="https://github.com/crypto0627/client-centric-consistency/assets/62930885/f854162b-5054-4164-b238-97c4e5ac707e">

## Finally Run main.py
```
sudo python3 main.py
```

## Result
- monotonic_write_input.json:<img width="326" alt="image" src="https://github.com/crypto0627/client-centric-consistency/assets/62930885/019adda4-ff8e-4596-bbe1-88c6cac7d7c0">
- read_your_writes_input.json:<img width="328" alt="image" src="https://github.com/crypto0627/client-centric-consistency/assets/62930885/5f1156df-893f-4fa4-b2d2-5702583ed9bd">
