# amazon-analysis
Análise de dados baseada no [dataset de vendas da Amazon](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset), com foco em redes de relacionamentos entre produtos e usuários. O principal intuito é explorar as relações dos grafos a partir das relações dos produtos e avaliações de usuários em produtos, permitindo visualizar a rede em diferentes modos, calcular métricas a partir dos dados e visualizar as distribuições de centralidade de nós. Cada produto é um nó, e uma aresta conecta produtos que foram avaliados por usuários em comum.

# Acesso à aplicação
- Hospedagem Genphi (GitHub Pages):
 [Acesse o site](https://vanessa-maria2.github.io/amazon-analysis/#)
- Hospedagem Streamlit
  [Acesse o site](https://vanessa-maria2-amazon-analysis-app-rgjlll.streamlit.app/)

# Funcionalidades
- Seleção do tipo de visualização da rede:
Permite alternar entre diferentes modos de exibição:
    - Grafo da rede
    - Maior componente conectada
    - Nós com maior grau de conexão

- Cálculo de métricas da rede:
    - Densidade da rede
    - Esparsidade da rede
    - Assortatividade
    - Coeficiente de clustering global
    - Coeficiente de clustering local
    - Componentes fracamente conectados
    - Verificação se o grafo é direcionado

- Visualização das métricas da rede
   - Matriz de adjacência
   - Diâmetro da rede
   - Periferia da rede
   - Nós periféricos 

- Manipulação interativa da visualização (via Streamlit + Pyvis):
Filtros e ajustes dinâmicos via controles physics do Pyvis, permitindo a personalização da estrutura visual da rede com os seguintes parâmetros:
    - gravitationalConstant
    - centralGravity
    - springLength
    - springConstant
    - damping
    - avoidOverlap
    - maxVelocity
    - minVelocity
    - timestep

- Visualização de centralidade dos nós:
    - Eigenvector centrality
    - Degree centrality
    - Closeness centrality
    - Betweenness centrality

# Estrutura projeto
```
├── amazon_analysis.ipynb
├── app.py
├── amazonanalysis.html
├── got.py
├── README.md
├── docs
├── lib
├── _pycache_
└── requirements.txt
```

# Como executar o projeto
1. Clone o projeto para sua máquina local.
2. Abra o projeto em uma IDE:
3. Para instalar as dependências, execute:
    ```
    pip install -r requirements.txt
    ```
4. Para rodar a aplicação, execute:
    ```
    streamlit run app.py 
    ```
