# Site C'alma Home Spa

Site estático (uma página), em português e inglês (botão PT/EN; `?lang=en` abre em inglês).

- `index.html` — página gerada. **Não editar à mão**: alterar `tools/` e voltar a gerar.
- `tools/servicos.py` — serviços, preços, durações e quem faz cada um (menu v13). Fonte única do menu e do planeador.
- `tools/template.html` — textos (PT e EN), estilo e funcionamento do planeador.
- `tools/build_site.py` — gera o `index.html`: `python3 tools/build_site.py`.
- Configuração (link da Fresha, WhatsApp, taxas) no bloco `CALMA` do `template.html`.
- `assets/menu-calma.pdf` — menu para descarregar.
- `assets/photos` — fotografias reais da gravação. Ver `LEIA-ME.txt`; `?fotos` mostra onde entra cada uma.
