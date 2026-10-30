# Gera assets/menu-calma.html (menu em A4, 2 páginas) a partir de tools/servicos.py.
# PDF: abrir no Chromium e imprimir (ou playwright page.pdf com preferCSSPageSize).
# Uso: python3 tools/build_menu.py
import os, html
from servicos import CATS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
def mzn(v): return f'{v:,}'.replace(',', '.')
def dur(m):
    if m < 60: return f'{m} min'
    h, r = divmod(m, 60); return f'{h} h' + (f' {r}' if r else '')

def line(name, meta, price, cls='ln'):
    return f'<div class="{cls}"><span class="nm">{name}</span>{f"<small>{meta}</small>" if meta else ""}<i></i><b>{mzn(price)}</b></div>'

def item(i, desc=True):
    nome = E(i['nome'][0]); d = E((i.get('desc') or ('', ''))[0]) if desc else ''
    if len(i['opts']) > 1:
        rows = ''.join(f'<div class="ln sub"><small>{dur(m)}</small><i></i><b>{mzn(p)}</b></div>' for _, m, p in i['opts'])
        return f'<div class="it"><div class="nm solo">{nome}</div>{f"<p>{d}</p>" if d else ""}{rows}</div>'
    _, m, p = i['opts'][0]
    meta = 'por unha' if i.get('unit') == 'nail' else (f'+{m} min' if i.get('addon') else dur(m))
    return f'<div class="it">{line(nome, meta, p)}{f"<p>{d}</p>" if d else ""}</div>'

def sec(title, intro, body):
    return f'<section><h2>{E(title)}</h2><p class="intro">{E(intro)}</p>{body}</section>'

by = {c['id']: c for c in CATS}
gel = by['gel']
cards = [i for i in gel['itens'] if i.get('card')]
cards = sorted(cards, key=lambda i: 0 if i['id'].startswith('v') else 1)
gels = {i['id']: i for i in gel['itens'] if not i.get('card') and not i.get('unit')}
art = [i for i in gel['itens'] if i.get('unit')]

def gcell(k):
    _, m, p = gels[k]['opts'][0]
    return f'<td><b>{mzn(p)}</b><small>{dur(m)}</small></td>'
geltab = ('<table class="gel"><thead><tr><th></th><th>Overlay</th><th>Alongamento</th><th>Manutenção</th></tr></thead><tbody>'
          f'<tr><th>Builder gel</th>{gcell("bg-nat")}{gcell("bg-alo")}{gcell("bg-man")}</tr>'
          f'<tr><th>Polygel</th>{gcell("pg-nat")}{gcell("pg-alo")}{gcell("pg-man")}</tr></tbody></table>'
          + item(gels['sg'], desc=False))

c1 = (sec('Massagens', by['massagens']['intro'][0], ''.join(item(i) for i in by['massagens']['itens']))
      + sec('Corpo', by['corpo']['intro'][0], ''.join(item(i) for i in by['corpo']['itens'])))
c2 = (sec('Rosto', 'Cuidados de rosto com limpeza, massagem e hidratação.', ''.join(item(i) for i in by['rosto']['itens']))
      + sec('Mãos e pés', 'Cuidado de mãos e pés, com material higienizado em cada visita.', ''.join(item(i) for i in by['maos']['itens']))
      + sec('Unhas', 'O gelish inclui a manicure ou a pedicure. O verniz normal junta-se a outro serviço.', ''.join(item(i, desc=False) for i in cards)))
c3 = (sec('Gel', 'Mãos, com manicure incluída. Overlay: gel sobre a unha natural, para a reforçar. Alongamento com tip ou molde. Manutenção: aproveita a base e repõe o gel onde a unha cresceu, até 4 semanas depois da aplicação.', geltab)
      + sec('Nail art', 'Por unha, sobre gelish ou gel.', ''.join(item(i) for i in art))
      + sec('Complementos', by['extras']['intro'][0], ''.join(item(i) for i in by['extras']['itens'])))
wax = ''.join(item(i, desc=False) for i in by['depilacao']['itens']) + '<p>Rosto completo: buço, queixo, maxilar e pescoço. Sem sobrancelhas.</p>'
info = ('<div class="box"><h3>Como funciona</h3>'
        '<p><b>Deslocação.</b> Zona 1: incluída em visitas a partir de 2.500 MZN; abaixo deste valor, 300 MZN. Zona 2: 500 MZN. Zona 3: 700 MZN, com mínimo de 60 min de serviço. Confirmamos sempre a zona e o valor total antes de marcar.</p>'
        '<p class="z"><b>Zona 1</b> Baixa, Alto Maé, Polana Cimento, Sommerschield, Coop, Malhangalene, Malanga, Munhuana, Mafalala, Maxaquene A e B.</p>'
        '<p class="z"><b>Zona 2</b> Maxaquene C e D, Urbanização, Polana Caniço, Aeroporto, Mavalane, FPLM, Ferroviário, Chamanculo, Xipamanine, Unidade 7, Hulene A.</p>'
        '<p class="z"><b>Zona 3</b> Costa do Sol, Triunfo, Laulane, Mahotas, Hulene B, Albazine, Magoanine, Malhazine. Zimpeto, conforme a localização.</p>'
        '<p class="z">Matola, KaTembe e KaNyaka ainda não fazem parte da área de atendimento.</p>'
        '<p><b>Valor mínimo</b> por visita: 1.000 MZN em serviços.</p>'
        '<p><b>Pagamento</b> no fim, por POS, M-Pesa ou transferência. Não aceitamos numerário.</p>'
        '<p><b>Sinal de 30%</b> nas reservas com mais de 2 h, na massagem a quatro mãos e para duas ou mais clientes ao mesmo tempo.</p>'
        '<p><b>Cancelamento</b> sem custo até 12 h antes (24 h nas reservas com sinal) ou até às 20h do dia anterior, no caso das marcações da manhã.</p>'
        '<p><b>Horário:</b> todos os dias, das 6h às 20h. Primeira marcação às 6h30. A profissional chega 10 min antes para preparar o espaço; o tempo indicado é o do serviço.</p></div>')
c4 = sec('Depilação com cera', by['depilacao']['intro'][0], wax) + info

CSS = '''@font-face{font-family:BM;src:url(fonts/BlackMango-Regular.ttf)}
@font-face{font-family:Jost;src:url(fonts/jost-latin-400-normal.woff2);font-weight:400}
@font-face{font-family:Jost;src:url(fonts/jost-latin-400-italic.woff2);font-weight:400;font-style:italic}
@font-face{font-family:Jost;src:url(fonts/jost-latin-500-normal.woff2);font-weight:500}
@page{size:A4;margin:0}*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Jost,sans-serif;color:#454127;font-size:8.6pt;line-height:1.4;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.pg{width:210mm;height:297mm;padding:14mm 15mm 10mm;background:#F3F1EC;display:flex;flex-direction:column;break-after:page;position:relative}
.top{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;margin-bottom:7mm}
.top img{height:15mm}
.top h1{font-family:BM;font-weight:400;font-size:27pt;color:#9C5839;letter-spacing:.01em}
.top .r{text-align:right;font-size:8.4pt;line-height:1.45;align-self:start;padding-top:3mm}
.top .r small{display:block;margin-top:3mm;font-size:7.6pt;opacity:.85}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:0 10mm;flex:1;margin-bottom:7mm}
section{margin-bottom:6mm}
h2{font-family:BM;font-weight:400;font-size:17pt;color:#9C5839;padding-bottom:1.6mm;border-bottom:.8px solid #9C5839;margin-bottom:2mm}
.intro{font-style:italic;font-size:7.8pt;opacity:.8;margin-bottom:3mm}
.it{margin-bottom:1.9mm}.it p{font-size:7.6pt;opacity:.8;margin-top:.4mm}
.ln{display:flex;align-items:baseline;gap:1.6mm}
.ln .nm,.nm.solo{font-weight:500;font-size:9pt}
.ln small{font-size:7.6pt;opacity:.7}
.ln i{flex:1;border-bottom:.9px dotted rgba(69,65,39,.45);transform:translateY(-1.2mm)}
.ln b{font-weight:400;color:#9C5839;font-size:9.4pt}
.sub{padding-left:2.5mm;margin-top:.6mm}
table.gel{width:100%;border-collapse:collapse;margin:1mm 0 3mm;font-size:8pt}
table.gel th{font-weight:500;text-align:left;padding:1.4mm 1mm}
table.gel thead th{font-size:7.6pt;text-align:center}
table.gel td{text-align:center;padding:1.6mm 1mm;border-top:.6px solid rgba(69,65,39,.15)}
table.gel tbody th{border-top:.6px solid rgba(69,65,39,.15)}
table.gel td b{display:block;font-weight:400;color:#9C5839;font-size:9pt}table.gel td small{font-size:7pt;opacity:.7}
.box{background:#fff;border-radius:3mm;padding:4mm 5mm}.box h3{font-family:BM;font-weight:400;font-size:13pt;margin-bottom:2mm}
.box p{font-size:7.4pt;margin-bottom:1.3mm}.box p.z{font-size:7.2pt;padding-left:3mm;margin-bottom:1.1mm}.box p.z b{color:#9C5839;margin-right:1mm}.box b{font-weight:500}
.foot{text-align:center;font-size:7.6pt;opacity:.75;letter-spacing:.02em}'''

top = ('<div class="top"><img src="logos/horizontal-chestnut.png" alt="C\'alma Home Spa"><h1>Menu</h1>'
       '<div class="r">Bem-estar ao domicílio em Maputo<br>Todos os dias, 06:00–20:00<small>Preços em MZN</small></div></div>')
foot = '<div class="foot">calmahomespa.co.mz · WhatsApp +258 85 329 9721 · @calmahomespa.mz</div>'
page = (f'<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>Menu C\'alma</title><style>{CSS}</style></head><body>'
        f'<div class="pg">{top}<div class="cols"><div>{c1}</div><div>{c2}</div></div>{foot}</div>'
        f'<div class="pg">{top}<div class="cols"><div>{c3}</div><div>{c4}</div></div>{foot}</div></body></html>')
open(os.path.join(ROOT, 'assets', 'menu-calma.html'), 'w', encoding='utf-8').write(page)
print('assets/menu-calma.html gerado')
