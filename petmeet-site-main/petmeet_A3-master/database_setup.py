import sqlite3

# Database initialization
conn = sqlite3.connect('app_pet_meet.db', check_same_thread=False)
cursor = conn.cursor()

# Criação das tabelas se elas não existirem
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuario (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Email TEXT NOT NULL,
        Senha TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pet (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Especie TEXT NOT NULL,
        Raca TEXT,
        Genero TEXT,       
        DataNascimento DATE,
        Cor TEXT,
        Peso REAL,
        Imagem TEXT,  -- Campo para armazenar o endereço da imagem
        Notas TEXT,
        Vacinacao TEXT,
        Medicamentos TEXT,
        UltimaConsulta DATE,
        Veterinario TEXT,
        HistoricoSaude TEXT,
        Alimentacao TEXT,
        Comportamento TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS PetUsuario (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PetID INTEGER,
        UsuarioID INTEGER,
        FOREIGN KEY (PetID) REFERENCES Pet(ID),
        FOREIGN KEY (UsuarioID) REFERENCES Usuario(ID)
    )
''')

conn.commit()
conn.close()
