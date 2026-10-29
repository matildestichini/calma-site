// Worker do site C'alma: serve os ficheiros estáticos e recebe as avaliações pós-serviço (D1).
// /api/avaliacao (POST)  → guarda uma resposta
// /respostas?chave=…     → painel com médias por profissional e todas as respostas
// /respostas.csv?chave=… → exportação para Excel
// Datas em hora de Maputo (UTC+2).
// A chave não está no repositório: só o seu SHA-256 (RESPOSTAS_HASH).

const PROS = { F: 'Florência', P: 'Percília', A: 'Angélica', C: 'Cardósia' };
const SERVICOS = ['Massagem', 'Corpo', 'Rosto', 'Mãos e pés', 'Unhas', 'Depilação'];

const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const int15 = (v) => { const n = parseInt(v, 10); return n >= 1 && n <= 5 ? n : null; };
const pick = (v, opts) => (opts.includes(v) ? v : null);
const clip = (v, n) => (typeof v === 'string' ? v.trim().slice(0, n) : '');

async function sha256(t) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, '0')).join('');
}

async function guardar(req, env) {
  let d;
  try { d = await req.json(); } catch { return json({ ok: false, erro: 'formato' }, 400); }
  if (d.site) return json({ ok: true }); // campo-armadilha para robôs
  const geral = int15(d.geral), cuidado = int15(d.cuidado), higiene = int15(d.higiene);
  if (!geral) return json({ ok: false, erro: 'geral' }, 400);
  await env.DB.prepare(
    "INSERT INTO respostas (criado, profissional, servico, geral, pontualidade, cuidado, higiene, recomenda, comentario, nome, autoriza, origem) VALUES (datetime('now','+2 hours'),?,?,?,?,?,?,?,?,?,?,?)"
  ).bind(
    PROS[d.profissional] ? d.profissional : null,
    pick(d.servico, SERVICOS),
    geral,
    pick(d.pontualidade, ['sim', 'pouco', 'muito']),
    cuidado, higiene,
    pick(d.recomenda, ['sim', 'talvez', 'nao']),
    clip(d.comentario, 1000), clip(d.nome, 80),
    d.autoriza ? 1 : 0,
    clip(d.origem, 40)
  ).run();
  return json({ ok: true });
}

const PONT = { sim: 'À hora', pouco: 'Pouco atrasada', muito: 'Muito atrasada' };
const REC = { sim: 'Sim', talvez: 'Talvez', nao: 'Não' };

function media(rows, k) { const v = rows.map((r) => r[k]).filter((x) => x); return v.length ? v.reduce((a, b) => a + b, 0) / v.length : null; }
const f1 = (n) => (n == null ? '—' : n.toFixed(1).replace('.', ','));
const pct = (a, b) => (b ? Math.round((a / b) * 100) + '%' : '—');

function painel(rows, chave) {
  const n = rows.length;
  const notaPro = (r) => { const v = [r.geral, r.cuidado, r.higiene].filter((x) => x); return v.length ? v.reduce((a, b) => a + b, 0) / v.length : null; };
  const porPro = Object.entries(PROS).map(([k, nome]) => {
    const rr = rows.filter((r) => r.profissional === k);
    const notas = rr.map(notaPro).filter((x) => x != null);
    const m = notas.length ? notas.reduce((a, b) => a + b, 0) / notas.length : null;
    const ok = rr.length >= 10 && m != null && m >= 4;
    return `<tr><td>${nome}</td><td>${rr.length}</td><td>${f1(m)}</td><td>${rr.length < 10 ? 'Menos de 10 respostas' : ok ? 'Cumpre (≥ 4,0)' : 'Abaixo de 4,0'}</td></tr>`;
  }).join('');
  const lin = rows.map((r) => `<tr><td>${esc(r.criado.slice(0, 16).replace('T', ' '))}</td><td>${esc(PROS[r.profissional] || '—')}</td><td>${esc(r.servico || '—')}</td><td>${r.geral ?? '—'}</td><td>${esc(PONT[r.pontualidade] || '—')}</td><td>${r.cuidado ?? '—'}</td><td>${r.higiene ?? '—'}</td><td>${esc(REC[r.recomenda] || '—')}</td><td class="c">${esc(r.comentario)}</td><td>${esc(r.nome)}</td><td>${r.autoriza ? 'Sim' : 'Não'}</td></tr>`).join('');
  return `<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Avaliações · C'alma</title>
<style>:root{--a:#EEEBE4;--c:#9C5839;--o:#454127;--s:#B2C07A}*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,sans-serif;background:var(--a);color:var(--o);padding:28px 16px}main{max-width:1200px;margin:0 auto}h1{font-size:26px;margin:0 0 4px}p.s{opacity:.7;margin:0 0 22px}.k{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:26px}.k div{background:#fff;border-radius:8px;padding:16px}.k b{display:block;font-size:28px;color:var(--c)}h2{font-size:18px;margin:26px 0 10px}.t{overflow-x:auto;background:#fff;border-radius:8px}table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:9px 12px;border-bottom:1px solid #e6e2d8;vertical-align:top}th{font-weight:600;background:#f7f5f0;white-space:nowrap}td.c{min-width:240px}a.b{display:inline-block;background:var(--c);color:#fff;text-decoration:none;padding:10px 16px;border-radius:6px;margin-top:6px}</style></head><body><main>
<h1>Avaliações pós-serviço</h1><p class="s">${n} respostas · notas de 1 a 5</p>
<div class="k"><div>Satisfação geral<b>${f1(media(rows, 'geral'))}</b></div><div>Cuidado da profissional<b>${f1(media(rows, 'cuidado'))}</b></div><div>Higiene e arrumação<b>${f1(media(rows, 'higiene'))}</b></div><div>Chegou à hora<b>${pct(rows.filter((r) => r.pontualidade === 'sim').length, rows.filter((r) => r.pontualidade).length)}</b></div><div>Recomendaria<b>${pct(rows.filter((r) => r.recomenda === 'sim').length, rows.filter((r) => r.recomenda).length)}</b></div></div>
<h2>Por profissional (critério do prémio: média ≥ 4,0 com pelo menos 10 respostas)</h2><div class="t"><table><thead><tr><th>Profissional</th><th>Respostas</th><th>Média (geral, cuidado, higiene)</th><th>Prémio</th></tr></thead><tbody>${porPro}</tbody></table></div>
<h2>Todas as respostas</h2><a class="b" href="/respostas.csv?chave=${encodeURIComponent(chave)}">Descarregar para Excel (CSV)</a>
<div class="t" style="margin-top:12px"><table><thead><tr><th>Data</th><th>Profissional</th><th>Serviço</th><th>Geral</th><th>Pontualidade</th><th>Cuidado</th><th>Higiene</th><th>Recomenda</th><th>Comentário</th><th>Nome</th><th>Autoriza partilhar</th></tr></thead><tbody>${lin || '<tr><td colspan="11">Ainda não há respostas.</td></tr>'}</tbody></table></div>
</main></body></html>`;
}

function csv(rows) {
  const q = (v) => '"' + String(v ?? '').replace(/"/g, '""') + '"';
  const head = ['Data', 'Profissional', 'Serviço', 'Geral', 'Pontualidade', 'Cuidado', 'Higiene', 'Recomenda', 'Comentário', 'Nome', 'Autoriza partilhar', 'Origem'];
  const body = rows.map((r) => [r.criado, PROS[r.profissional] || '', r.servico, r.geral, PONT[r.pontualidade] || '', r.cuidado, r.higiene, REC[r.recomenda] || '', r.comentario, r.nome, r.autoriza ? 'Sim' : 'Não', r.origem].map(q).join(';'));
  return '﻿' + [head.map(q).join(';'), ...body].join('\r\n');
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === '/api/avaliacao') {
      if (req.method !== 'POST') return json({ ok: false }, 405);
      try { return await guardar(req, env); } catch (e) { return json({ ok: false, erro: 'servidor' }, 500); }
    }
    if (url.pathname === '/respostas' || url.pathname === '/respostas.csv') {
      const chave = url.searchParams.get('chave') || '';
      if (!chave || (await sha256(chave)) !== env.RESPOSTAS_HASH) {
        return new Response('Acesso reservado.', { status: 403, headers: { 'content-type': 'text/plain; charset=utf-8' } });
      }
      const { results } = await env.DB.prepare('SELECT * FROM respostas ORDER BY id DESC').all();
      if (url.pathname.endsWith('.csv')) {
        return new Response(csv(results), { headers: { 'content-type': 'text/csv; charset=utf-8', 'content-disposition': 'attachment; filename="avaliacoes-calma.csv"', 'cache-control': 'no-store' } });
      }
      return new Response(painel(results, chave), { headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' } });
    }
    return env.ASSETS.fetch(req);
  },
};
