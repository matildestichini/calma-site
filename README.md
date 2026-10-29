# Site C'alma Home Spa

Site estático (uma página), em português e inglês (botão PT/EN; `?lang=en` abre em inglês).

- `index.html` — página gerada. **Não editar à mão**: alterar `tools/` e voltar a gerar.
- `tools/servicos.py` — serviços, preços, durações e quem faz cada um (menu v13). Fonte única do menu e do planeador.
- `tools/template.html` — textos (PT e EN), estilo e funcionamento do planeador.
- `tools/build_site.py` — gera o `index.html`: `python3 tools/build_site.py`.
- Configuração (link da Fresha, WhatsApp, taxas) no bloco `CALMA` do `template.html`.
- `assets/menu-calma.pdf` — menu para descarregar.
- `assets/photos` — fotografias reais da gravação. Ver `LEIA-ME.txt`; `?fotos` mostra onde entra cada uma.

## Avaliação pós-serviço

- `avaliacao.html` — inquérito para as clientes: **calmahomespa.co.mz/avaliacao** (`?p=F|P|A|C` pré-seleciona a profissional; `?s=massagem` o serviço).
- `src/worker.js` — guarda as respostas na base D1 `calma-avaliacoes` e mostra o painel em `/respostas?chave=…` (médias por profissional, critério do prémio, exportação CSV). A chave fica fora do repositório; aqui só está o SHA-256 (`RESPOSTAS_HASH` no `wrangler.jsonc`).
