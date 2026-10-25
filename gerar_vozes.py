# Gera os áudios da voz do Antônio para o painel de apuração.
# Uso:  pip install edge-tts   &&   python gerar_vozes.py
# Cria a pasta "vozes" com os MP3 e o arquivo vozes.zip (é o zip que deve ser enviado).
import asyncio, os, zipfile, edge_tts

VOZ, RITMO = "pt-BR-AntonioNeural", "+6%"
U = ["zero","um","dois","três","quatro","cinco","seis","sete","oito","nove","dez","onze","doze","treze",
     "quatorze","quinze","dezesseis","dezessete","dezoito","dezenove"]
D = {2:"vinte",3:"trinta",4:"quarenta",5:"cinquenta",6:"sessenta",7:"setenta",8:"oitenta",9:"noventa"}

def num(n):
    if n < 20: return U[n]
    d, u = divmod(n, 10)
    return D[d] if u == 0 else D[d] + " e " + U[u]

CLIPS = {"urnas_apuradas":"Urnas apuradas", "lula":"Lula", "flavio_bolsonaro":"Flávio Bolsonaro",
         "por_cento":"por cento", "virgula":"vírgula", "teste":"Teste de voz"}
for i in range(100):
    CLIPS["n%d" % i] = num(i)

async def main():
    os.makedirs("vozes", exist_ok=True)
    sem = asyncio.Semaphore(4)
    async def um(nome, txt):
        async with sem:
            for t in range(4):
                try:
                    await edge_tts.Communicate(txt, VOZ, rate=RITMO).save("vozes/%s.mp3" % nome)
                    return
                except Exception as e:
                    await asyncio.sleep(1 + t)
            print("FALHOU:", nome)
    await asyncio.gather(*[um(k, v) for k, v in CLIPS.items()])
    with zipfile.ZipFile("vozes.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for k in CLIPS:
            p = "vozes/%s.mp3" % k
            if os.path.exists(p): z.write(p, k + ".mp3")
    print("Pronto: %d arquivos em vozes.zip" % len(os.listdir("vozes")))

asyncio.run(main())
