# Gera index.html a partir de tools/servicos.py (PT e EN na mesma página).
# Uso: python3 tools/build_site.py
import json, os, html
from servicos import CATS, PROS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

def t(pt, en, tag='span'):
    """Texto nas duas línguas; o CSS mostra só a língua ativa."""
    return f'<{tag} class="pt">{pt}</{tag}><{tag} class="en" lang="en">{en}</{tag}>'

def mzn(v): return f'<span data-p="{v}">' + f'{v:,}'.replace(',', '.') + '</span>'

def dur(m, en=False):
    if m < 60: return f'{m} min'
    h, r = divmod(m, 60)
    return f'{h} h' + (f' {r}' if r else '') if not en else (f'{h} h' + (f' {r}' if r else ''))

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
WA_ICON = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3C9.1 3 3.5 8.6 3.5 15.5c0 2.4.7 4.6 1.8 6.5L3 29l7.2-2.2c1.8 1 3.9 1.6 6 1.6 6.9 0 12.3-5.6 12.3-12.5C28.5 8.6 22.9 3 16 3zm0 23.1c-1.9 0-3.7-.5-5.3-1.5l-.4-.2-4.3 1.3 1.3-4.2-.2-.4c-1.1-1.7-1.7-3.7-1.7-5.7 0-5.7 4.6-10.3 10.3-10.3s10.6 4.6 10.6 10.3S22 26.1 16 26.1zm5.8-7.7c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.6 8.6 0 0 1-2.5-1.6 9.6 9.6 0 0 1-1.8-2.2c-.2-.3 0-.5.1-.6l.4-.5.3-.4c.1-.1.1-.3 0-.4-.1-.2-.7-1.7-1-2.3-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.1.2 2.1 3.2 5.1 4.4.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.5-.1 1.7-.7 1.9-1.3.2-.6.2-1.1.2-1.2-.1-.2-.3-.3-.6-.4z"/></svg>'
WA = 'https://wa.me/258853299721'

def ph(src, alt_pt, alt_en, cap, cls='ph'):
    return (f'<figure class="{cls}"><img src="assets/photos/{src}" data-alt-pt="{E(alt_pt)}" data-alt-en="{E(alt_en)}" alt="{E(alt_pt)}" '
            f'loading="lazy" onerror="this.remove()"><figcaption>{E(cap)}</figcaption></figure>')

def price_rows(it):
    rows = []
    for oid, d, p in it['opts']:
        if it.get('unit') == 'nail':
            lab = t('por unha', 'per nail')
        elif it.get('addon'):
            lab = f'+{d} min'
        else:
            lab = dur(d)
        rows.append(f'<li><span>{lab}</span><i></i><b>{mzn(p)}</b></li>')
    return '<ul class="rows">' + ''.join(rows) + '</ul>'

def menu_panels():
    out = []
    for c in CATS:
        if c['id'] == 'extras':
            continue
        body = []
        if c.get('gel'):
            cards = [i for i in c['itens'] if i.get('card')]
            gel = [i for i in c['itens'] if not i.get('unit') and not i.get('card')]
            for i in cards:
                body.append(f'<div class="item"><h3>{t(*i["nome"])}</h3><p>{t(*i["desc"])}</p>{price_rows(i)}'
                            f'<a class="btn btn-line sm" href="#marcar" data-pick="{i["opts"][0][0]}">{t("Marcar","Book")}</a></div>')
            art = [i for i in c['itens'] if i.get('unit')]
            def cell(code):
                it = next(i for i in gel if i['id'] == code); oid, d, p = it['opts'][0]
                return f'<td><b>{mzn(p)}</b><small>{dur(d)}</small></td>'
            body.append(
                '<div class="gel-wrap"><table class="gel"><thead><tr><th></th>'
                f'<th>{t("Overlay","Overlay")}</th><th>{t("Alongamento","Extensions")}</th><th>{t("Manutenção","Infill")}</th></tr></thead><tbody>'
                f'<tr><th>Builder gel</th>{cell("bg-nat")}{cell("bg-alo")}{cell("bg-man")}</tr>'
                f'<tr><th>Polygel</th>{cell("pg-nat")}{cell("pg-alo")}{cell("pg-man")}</tr></tbody></table>'
                f'<p class="note">{t("Overlay: uma ou duas camadas de gel sobre a unha natural, para a reforçar. Manutenção: aproveita a base e repõe o gel onde a unha cresceu, até 4 semanas depois da aplicação.","Overlay: one or two layers of gel over the natural nail to strengthen it. Infill: keeps the base and refills the gel where the nail has grown, up to 4 weeks after application.")}</p>'
                f'<ul class="rows solo"><li><span>{t("Soft gel com tips","Soft gel tips")} · {dur(100)}</span><i></i><b>2.300</b></li></ul>'
                f'<a class="btn btn-solid sm" href="#marcar" data-pick="bg-nat">{t("Marcar","Book")}</a></div>')
            body.append(f'<div class="item"><h3>{t("Nail art","Nail art")} <span class="tag">{t("por unha","per nail")}</span></h3>'
                        '<ul class="rows">' + ''.join(f'<li><span>{t(*i["nome"])}</span><i></i><b>{mzn(i["opts"][0][2])}</b></li>' for i in art) +
                        f'</ul><p class="note">{t("Sobre gelish ou gel. Feita pela Angélica.","On gel polish or gel nails. Done by Angélica.")}</p></div>')
            ex = next(x for x in CATS if x['id'] == 'extras')
            body.append(f'<div class="item"><h3>{t(*ex["nome"])}</h3><p>{t(*ex["intro"])}</p>'
                        '<ul class="rows">' + ''.join(f'<li><span>{t(*i["nome"])} · +{i["opts"][0][1]} min</span><i></i><b>{mzn(i["opts"][0][2])}</b></li>' for i in ex['itens']) +
                        '</ul></div>')
            items = '<div class="items gel-items">' + ''.join(body) + '</div>'
        elif c.get('wax'):
            items = ('<div class="item wide"><ul class="rows wax">' +
                     ''.join(f'<li><span>{t(*i["nome"])} <small>{dur(i["opts"][0][1])}</small></span><i></i><b>{mzn(i["opts"][0][2])}</b></li>' for i in c['itens']) +
                     f'</ul><a class="btn btn-solid sm" href="#marcar" data-pick="d-mp">{t("Marcar","Book")}</a>'
                     f'<p class="note">{t("A depilação está disponível nos dias da Cardósia; noutros dias, confirmamos a disponibilidade.","Waxing is available on Cardósia’s working days; on other days, we will confirm availability.")}</p></div>')
            items = '<div class="items">' + items + '</div>'
        else:
            for i in c['itens']:
                tag = ''
                if i.get('pro') == 2: tag = f' <span class="tag">{t("2 profissionais","2 therapists")}</span>'
                note = f'<p class="note">{t(*i["note"])}</p>' if i.get('note') else ''
                desc = f'<p>{t(*i["desc"])}</p>' if i.get('desc') else ''
                body.append(f'<div class="item"><h3>{t(*i["nome"])}{tag}</h3>{desc}{price_rows(i)}{note}'
                            f'<a class="btn btn-line sm" href="#marcar" data-pick="{(i["opts"][1] if len(i["opts"])==3 else i["opts"][0])[0]}">{t("Marcar","Book")}</a></div>')
            items = '<div class="items">' + ''.join(body) + '</div>'
        hidden = '' if c['id'] == 'massagens' else ' hidden'
        out.append(f'<div class="panel" id="{c["id"]}" role="tabpanel" aria-labelledby="t-{c["id"]}"{hidden}>'
                   f'<h3 class="panel-title">{t(*c["nome"])}</h3><p class="panel-intro">{t(*c["intro"])}</p>{items}</div>')
    return '\n'.join(out)

def tabs():
    out = []
    first = True
    for c in CATS:
        if c['id'] == 'extras': continue
        mins = min(o[2] for i in c['itens'] for o in i['opts'] if not i.get('unit'))
        out.append(f'<button class="tab" role="tab" id="t-{c["id"]}" aria-controls="{c["id"]}" aria-selected="{"true" if first else "false"}">'
                   f'{t(*c["nome"])}<small>{t("desde","from")} {mzn(mins)}</small></button>')
        first = False
    return ''.join(out)

def planner_data():
    data = []
    for c in CATS:
        g = {'cat': list(c['nome']), 'itens': []}
        for i in c['itens']:
            for oid, d, p in i['opts']:
                nm_pt, nm_en = i['nome']
                if len(i['opts']) > 1:
                    nm_pt += ' · ' + dur(d); nm_en += ' · ' + dur(d)
                g['itens'].append({'id': oid, 'n': [nm_pt, nm_en], 'b': list(i['nome']), 'p': p, 'd': d, 'who': i.get('who'),
                                   'pro': i.get('pro', 1), 'unit': i.get('unit'), 'addon': bool(i.get('addon'))})
        data.append(g)
    return data

def team():
    out = []
    for k in ['F', 'P', 'A', 'C']:
        p = PROS[k]; n = p['nome']; slug = __import__('unicodedata').normalize('NFKD', n.lower()).encode('ascii', 'ignore').decode()
        chips_pt, chips_en = p['chips']
        chips = ''.join(f'<li>{t(a, b)}</li>' for a, b in zip(chips_pt, chips_en))
        out.append(f'<article class="person">{ph("equipa-" + slug + ".jpg", n + ", profissional da C’alma", n + ", C’alma therapist", "retrato da " + n + " de farda, 4:5")}'
                   f'<div class="person-copy"><span class="role">{t(*p["role"])}</span><h3>{n}</h3><p>{t(*p["bio"])}</p>'
                   f'<ul class="chips">{chips}</ul><a class="arrow" href="#marcar" data-pro="{k}">{t("Marcar com a " + n, "Book with " + n)} {ARROW}</a></div></article>')
    return ''.join(out)

TEMPLATE = open(os.path.join(ROOT, 'tools', 'template.html'), encoding='utf-8').read()
page = (TEMPLATE
        .replace('{{TABS}}', tabs())
        .replace('{{PANELS}}', menu_panels())
        .replace('{{TEAM}}', team())
        .replace('{{SERVICOS_JSON}}', json.dumps(planner_data(), ensure_ascii=False))
        .replace('{{PROS_JSON}}', json.dumps({k: v['nome'] for k, v in PROS.items()}, ensure_ascii=False))
        .replace('{{ARROW}}', ARROW).replace('{{WA_ICON}}', WA_ICON).replace('{{WA}}', WA))
import re
page = re.sub(r'\{\{T:(.*?)\|(.*?)\}\}', lambda m: t(m.group(1), m.group(2)), page, flags=re.S)
page = re.sub(r'\{\{PH:(.*?)\|(.*?)\|(.*?)\|(.*?)(?:\|(.*?))?\}\}', lambda m: ph(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or 'ph'), page)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(page)
print('index.html gerado:', len(page), 'bytes')
