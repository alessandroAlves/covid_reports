# covid_reports
Projeto para geração de relatórios em csv sobre a pandemia de covid 19.

Os relatórios gerados são no formato csv separados por "|" e possuem as seguintes informações:

**Relatório diário**
- País
- Código do país
- Estado
- Casos confirmados
- Quantidade de mortes
- Quantidade de recuperados
- Quantidade de casos ativos
- Data de referência

**Relatório semanal**
- País
- Código do país
- Estado
- Casos confirmados
- Quantidade de mortes
- Quantidade de recuperados
- Quantidade de casos ativos
- Média de Casos confirmados
- Média de mortes
- Média de recuperados
- Média de casos ativos
- Mínimo de Casos confirmados
- Mínimo de mortes
- Mínimo de recuperados
- Mínimo de casos ativos
- Máximo de Casos confirmados
- Máximo de mortes
- Máximo de recuperados
- Máximo de casos ativos      
- Semana de referência

Ambos os relatórios usam a data de execução para buscar os dados do último mês. 
**Ex.:** Relatório executado no dia 01/04/2021 trará os dados consolidaddos do mês de Março.
---

## Dependências 

* Python 3.x -> Disponível em [python.org](http://www.python.org/getit/).
* Pandas 1.0.5
* Requests 2.24.0
---

## Execução
Para geração dos relatórios execute o script covid_report.py com os seguintes parâmetros:

Obs.: Os argumentos são posicionais e precisam estar nessa ordem. 

* diretorio : Diretório de destino do arquivo csv, sem o nome do arquivo, pois o mesmo é gerado dinâmicamente.
* formato : Formato de geração dos dados, por dia ou semana. Use "D" ou "d" para o formato diário e "S" ou "s" para o formato semanal.

#### Exemplo

O comando abaixo irá gerar no diretório /tmp um report com os dados diários.
```python
python3 covid_report /tmp d 
```    
---