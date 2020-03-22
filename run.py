import subprocess

for i in range(1000):
    print(i)
    processo = subprocess.call(["python scrapping2.py >> dados_mglu_13-02-2019.txt"], shell=True)
    
