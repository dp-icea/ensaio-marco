# MOCK DECEA

Nesse repositório existe um mock de como utilizar os recursos para o ensaio de março do BR-UTM

Na pasta "desconflito", o arquivo app.py contém a lógica para interagir com o DSS para:
 - Consulta de restrições
 - Consulta de outras intenções de operação
 - Criação da própria intenção de operação
 - Criação da ISA para prover Tracking

O mock consiste em pegar os dados de um voo, presente na pasta flight_data, desconflitar a rota no DSS, e prover os dados de tracking desse mock de voo

# Getting Started

## Iniciar os recursos do DSS e mock_dss com o comando

``` make run_test ```

## Criar a OIR desconflitada, e a ISA para Tracking

``` python desconflito/app.py ```

O que será realizado:
 - criado um volume com base nos dados do voo (Dados do voo mockados, conforme arquivo desconflito/flight_mock)
 - consulta de restrições no volume
    - caso exista alguma restrição, será lançada uma exceção, por simplicidade do código. É esperado que os provedores consigam replanejar seu volume 4D para desconflitar com a restrição
- consulta de outras OIRs no volume
    - caso exista alguma OIR, será lançada uma exceção, por simplicidade do código. É esperado que os provedores consigam replanejar seu volume 4D para desconflitar com a OIR
- criação da própria OIR
- criação da ISA para prover tracking para esse voo

## Implementações a cargo do provedor

Espera-se que o provedor implemente os endpoints previstos para o desconflito estratégico e para o Tracking. Nesse teste, esses endpoint não foram implementados