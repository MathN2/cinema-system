CREATE DATABASE IF NOT EXISTS cinema;
USE cinema;

CREATE TABLE IF NOT EXISTS filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    duracao TIME NOT NULL,
    dias_disponiveis JSON
);

CREATE TABLE IF NOT EXISTS filme_dias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filme_id INT NOT NULL,
    weekday TINYINT NOT NULL,

    FOREIGN KEY (filme_id) REFERENCES filmes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT,
    linhas INT DEFAULT 5,
    colunas INT DEFAULT 5,
    capacidade INT GENERATED ALWAYS AS (linhas * colunas) STORED
);

CREATE TABLE IF NOT EXISTS sessoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filme_id INT,
    sala_id INT,
    data_hora DATETIME,
    assentos JSON,

    FOREIGN KEY (filme_id) REFERENCES filmes(id) ON DELETE CASCADE,
    FOREIGN KEY (sala_id) REFERENCES salas(id) ON DELETE CASCADE
);