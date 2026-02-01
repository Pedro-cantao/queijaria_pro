-- ddl_pcp.sql
-- Criação das tabelas principais da Queijaria Pro

CREATE TABLE produtos (
    produto_id SERIAL PRIMARY KEY,
    produto_codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(100),
    unidade_base VARCHAR(10)
);

CREATE TABLE receitas (
    receita_id SERIAL PRIMARY KEY,
    produto_id INT REFERENCES produtos(produto_id),
    descricao TEXT,
    rendimento_unidade NUMERIC
);

CREATE TABLE receita_itens (
    item_id SERIAL PRIMARY KEY,
    receita_id INT REFERENCES receitas(receita_id),
    item_codigo VARCHAR(50),
    tipo_item VARCHAR(50),
    descricao_item TEXT,
    quantidade_por_unidade NUMERIC,
    unidade_medida VARCHAR(10),
    observacao TEXT
);

CREATE TABLE estoque (
    estoque_id SERIAL PRIMARY KEY,
    item_codigo VARCHAR(50),
    tipo_item VARCHAR(50),
    lote VARCHAR(50),
    quantidade NUMERIC,
    unidade VARCHAR(10),
    localizacao TEXT,
    data_entrada TIMESTAMP DEFAULT now()
);

CREATE TABLE capacidade_maquina (
    maquina_id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT,
    capacidade_hora NUMERIC
);

CREATE TABLE turnos (
    turno_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL,
    inicio TIME,
    fim TIME
);

CREATE TABLE ordens_producao (
    op_id SERIAL PRIMARY KEY,
    numero_op VARCHAR(50) UNIQUE NOT NULL,
    produto_id INT REFERENCES produtos(produto_id),
    receita_id INT REFERENCES receitas(receita_id),
    unidades_planejadas NUMERIC,
    volume_planejado NUMERIC,
    inicio_planejado TIMESTAMP,
    fim_planejado TIMESTAMP,
    inicio_real TIMESTAMP,
    fim_real TIMESTAMP,
    operador VARCHAR(100),
    linha_equipamento VARCHAR(100),
    status VARCHAR(50)
);

CREATE TABLE insumos_consumo (
    consumo_id SERIAL PRIMARY KEY,
    op_id INT REFERENCES ordens_producao(op_id),
    item_codigo VARCHAR(50),
    quantidade NUMERIC,
    unidade_medida VARCHAR(10),
    custo_unitario NUMERIC,
    custo_total NUMERIC
);
