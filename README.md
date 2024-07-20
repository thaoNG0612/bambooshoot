# bambooshoot
Em là búp măng non, em lớn lên trong nhiều ý tưởng...

# Installation 
- Clone repo
- Cài python virtualenv cho project
- Mở cmd tại vị trí của project => active venv của project
  
  ![image](https://github.com/user-attachments/assets/d0b75edb-23cf-4396-9733-9b70373e5eac) =>  ![image](https://github.com/user-attachments/assets/de89694b-e148-4956-ac54-60ac79cc18fb)


- Install các thư viện: `time`, `web3`, `schedule` bằng `pip install`
- Run `python app.py`


![image](https://github.com/user-attachments/assets/a56e9ee6-cedb-4992-a069-a30a49bd7bc5)



# Feature: 
- Check balance BNB, QFS trong wallet
- Check price của QFS cứ mỗi 2s
- Submit transaction lên [Pancakeswap](https://pancakeswap.finance/swap?outputCurrency=0xab737e248D3c088bdF093e0a28171CE35920F91b&chainId=56) để swap từ BNB qua QFS
  
# Test result: 
## Success to watch token's price directly from Pancakeswap
## Success to swap QFS from BNB
[Test transaction URL](https://bscscan.com/tx/0xd019810eeddd9f9fb78b2a454d765a58cc06dcbbdf192a32b51b694a0953033d)
![image](https://github.com/user-attachments/assets/27e24778-2df8-45e6-a4dd-4d4d64540ce3)

![image](https://github.com/user-attachments/assets/9de88179-eecf-43ed-97e4-3f9c654ba6a0)

# Next step:
## Define the logic to decide buy&sell
