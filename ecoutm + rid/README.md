# MOCK DECEA

Nesse repositório existe um mock de como utilizar os recursos para o ensaio de março do BR-UTM

Na pasta raiz, o arquivo app.py contém a lógica para interagir com o ECO-UTM e com o DSS

O mock consiste em pegar os dados de um voo, presente na pasta flight_data, solicitar o espaço aéreo no SARPAS, e prover os dados de tracking desse mock de voo

# Getting Started

## Iniciar os recursos do DSS e mock_dss com o comando

``` make run_test ```

## Inserir os dados do flight_data no mock_uss_ridsp (Remote ID service provider)

``` python app.py ```

Nesse momento, será feita uma requisição de voo no ECO-UTM, e depois injetado os dados no mock_uss_ridsp

O voo terá inicio em 90 segundos após a requisição

## Iniciar o visualizador

Para executar o BFF do visualizador

``` python front/bff.py & ```

Para abrir o visualizador, basta abrir o arquivo front/viwer.html em algum navegador
