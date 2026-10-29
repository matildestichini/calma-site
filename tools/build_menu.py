# Gera assets/menu-calma.html a partir de tools/servicos.py; o PDF faz-se com Chromium (ver README).
# Uso: python3 tools/build_menu.py
import os, html
from servicos import CATS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
def mzn(v): return f'{v:,}'.replace(',', '.')
def dur(m):
    if m < 60: return f'{m} min'
    h, r = divmod(m, 60); return f'{h} h' + (f' {r}' if r else '')

def item(i):
    out = []
    nome, desc = i['nome'][0], (i.get('desc') or ('', ''))[0]
    if len(i['opts']) > 1:
        out.append(f'<div class="it"><div class="nm">{E(nome)}</div>')
        if desc: out.append(f'<div class="ds">{E(desc)}</div>')
        for _, d, p in i['opts']:
            out.append(f'<div class="ln sub"><span>{dur(d)}</span><b>{mzn(p)}</b></div>')
        out.append('</div>')
    else:
        _, d, p = i['opts'][0]
        lab = 'por unha' if i.get('unit') == 'nail' else (f'+{d} min' if i.get('addon') else dur(d))
        out.append(f'<div class="it"><div class="ln"><span class="nm">{E(nome)} <small>{lab}</small></span><b>{mzn(p)}</b></div>')
        if desc and not i.get('unit'): out.append(f'<div class="ds">{E(desc)}</div>')
        out.append('</div>')
    return ''.join(out)

def cat(c, itens=None, intro=None):
    its = itens if itens is not None else c['itens']
    return (f'<section><h2>{E(c["nome"][0])}</h2><p class="in">{E(intro or c["intro"][0])}</p>'
            + ''.join(item(i) for i in its) + '</section>')

by = {c['id']: c for c in CATS}
gel = by['gel']
cards = [i for i in gel['itens'] if i.get('card')]
gels = [i for i in gel['itens'] if not i.get('card') and not i.get('unit')]
art = [i for i in gel['itens'] if i.get('unit')]

p1 = cat(by['massagens']) + cat(by['corpo']) + cat(by['rosto']) + cat(by['maos'])
p2 = (cat(gel, cards, 'O gelish inclui a manicure ou a pedicure. O verniz normal junta-se a outro serviço.')
      + cat({'nome': ('Gel', 'Gel'), 'intro': ('', '')}, gels, 'Overlay: gel sobre a unha natural. Alongamento com tip ou molde. Manutenção: aproveita a base e repõe o gel onde a unha cresceu, até 4 semanas depois.')
      + cat({'nome': ('Nail art', 'Nail art'), 'intro': ('', '')}, art, 'Por unha, sobre gelish ou gel.')
      + cat(by['extras']) + cat(by['depilacao']))

CSS = '''@font-face{font-family:BM;src:url(fonts/BlackMango-Bold.ttf)}
@page{size:A4;margin:0}*{box-sizing:border-box;margin:0}body{font-family:Jost,'Helvetica Neue',Arial,sans-serif;color:#454127;font-size:10.6pt;line-height:1.4}
.pg{width:210mm;height:297mm;padding:13mm 14mm 11mm;display:flex;flex-direction:column;background:#EEEBE4;break-after:page}
.top{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2px solid #9C5839;padding-bottom:6px;margin-bottom:10px}
.top img{height:30px}.top .r{text-align:right;font-size:8pt;opacity:.8}
.cols{column-count:2;column-gap:9mm;flex:1}
section{break-inside:avoid-column;margin-bottom:14px}
h2{font-family:BM;font-size:19pt;color:#9C5839;margin-bottom:1px;font-weight:700}
.in{font-size:9.4pt;opacity:.7;margin-bottom:7px}
.it{margin-bottom:8px;break-inside:avoid}.nm{font-weight:500}.nm small{font-weight:400;opacity:.65;font-size:9pt}
.ln{display:flex;justify-content:space-between;gap:8px}.ln b{font-weight:500;color:#9C5839}.sub{padding-left:8px}
.ds{font-size:9.2pt;opacity:.72}
.foot{font-size:7.6pt;text-align:center;opacity:.75;border-top:1px solid rgba(69,65,39,.2);padding-top:6px}'''

top = ('<div class="top"><img src="logos/horizontal-chestnut.png" alt="C\'alma Home Spa">'
       '<div class="r">Bem-estar ao domicílio em Maputo · Todos os dias, 06:00–20:00<br>Preços em MZN, por pessoa</div></div>')
foot1 = '<div class="foot">Deslocação: Zona 1, 300 MZN, incluída a partir de 2.500 MZN · Zona 2, 500 MZN · Zona 3, 700 MZN · Mínimo por visita: 1.000 MZN em serviços</div>'
foot2 = '<div class="foot">calmahomespa.co.mz · WhatsApp +258 85 329 9721 · @calmahomespa.mz · Pagamento por POS, M-Pesa ou transferência</div>'
page = (f'<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>Menu C\'alma</title>'
        '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&display=swap" rel="stylesheet">'
        f'<style>{CSS}</style></head><body>'
        f'<div class="pg">{top}<div class="cols">{p1}</div>{foot1}</div>'
        f'<div class="pg">{top}<div class="cols">{p2}</div>{foot2}</div></body></html>')
open(os.path.join(ROOT, 'assets', 'menu-calma.html'), 'w', encoding='utf-8').write(page)
print('assets/menu-calma.html gerado')
