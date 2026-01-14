# Documentação de Arquitetura

O projeto segue uma estrutura modular inspirada em Clean Architecture:

- **src/api**: Pontos de entrada e tratamento de requisições.
- **src/core**: Configurações globais e instâncias compartilhadas (BD, log).
- **src/models**: Estruturas de dados e entidades ORM.
- **src/repository**: Abstração da camada de persistência e implementações.
- **src/services**: Lógica de negócio e orquestrações.
- **src/scraper**: Pipeline de extração de dados externos.
