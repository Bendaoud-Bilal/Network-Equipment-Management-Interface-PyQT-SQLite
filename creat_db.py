import sqlite3

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect("database.db")
c = conn.cursor()

# Create tables
c.execute(
    """
    CREATE TABLE IF NOT EXISTS wilaya (
        code_wilaya INTEGER PRIMARY KEY,
        wilaya_name VARCHAR(100) NOT NULL
    );
"""
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS equipment_type (
        code_type INTEGER PRIMARY KEY,
        type_name VARCHAR(150) NOT NULL
    );
"""
)

c.execute(
    """
    CREATE TABLE IF NOT EXISTS equipment (
        id_equipment INTEGER PRIMARY KEY,
        description VARCHAR(1000),
        address_IPV4_decimal VARCHAR(20),
        address_IPV4_binary VARCHAR(40),
        address_IPV6_decimal VARCHAR(40),
        address_IPV6_binary VARCHAR(140),
        start_serving_date TIMESTAMP,
        code_wil INTEGER,
        code_t INTEGER,
        FOREIGN KEY (code_wil) REFERENCES wilaya (code_wilaya),
        FOREIGN KEY (code_t) REFERENCES equipment_type (code_type)
    );
"""
)

# Populate Wilayas (Algerian provinces)
wilayas = [
    (1, "Adrar"),
    (2, "Chlef"),
    (3, "Laghouat"),
    (4, "Oum El Bouaghi"),
    (5, "Batna"),
    (6, "Béjaïa"),
    (7, "Biskra"),
    (8, "Béchar"),
    (9, "Blida"),
    (10, "Bouira"),
    (11, "Tamanrasset"),
    (12, "Tébessa"),
    (13, "Tlemcen"),
    (14, "Tiaret"),
    (15, "Tizi Ouzou"),
    (16, "Alger"),
    (17, "Djelfa"),
    (18, "Jijel"),
    (19, "Sétif"),
    (20, "Saïda"),
    (21, "Skikda"),
    (22, "Sidi Bel Abbès"),
    (23, "Annaba"),
    (24, "Guelma"),
    (25, "Constantine"),
    (26, "Médéa"),
    (27, "Mostaganem"),
    (28, "M'Sila"),
    (29, "Mascara"),
    (30, "Ouargla"),
    (31, "Oran"),
    (32, "El Bayadh"),
    (33, "Illizi"),
    (34, "Bordj Bou Arréridj"),
    (35, "Boumerdès"),
    (36, "El Tarf"),
    (37, "Tindouf"),
    (38, "Tissemsilt"),
    (39, "El Oued"),
    (40, "Khenchela"),
    (41, "Souk Ahras"),
    (42, "Tipaza"),
    (43, "Mila"),
    (44, "Aïn Defla"),
    (45, "Naâma"),
    (46, "Aïn Témouchent"),
    (47, "Ghardaïa"),
    (48, "Relizane"),
    (49, "Timimoun"),
    (50, "Bordj Badji Mokhtar"),
    (51, "Ouled Djellal"),
    (52, "Béni Abbès"),
    (53, "In Salah"),
    (54, "In Guezzam"),
    (55, "Touggourt"),
    (56, "Djanet"),
    (57, "El M'Ghair"),
    (58, "El Menia"),
]

c.executemany("INSERT OR IGNORE INTO wilaya VALUES (?, ?)", wilayas)

# Populate Equipment Types (Algerie Telecom specific)
equipment_types = [
    (1, "Optical Line Terminal (OLT)"),
    (2, "Optical Network Unit (ONU)"),
    (3, "DSL Access Multiplexer (DSLAM)"),
    (4, "Core Router"),
    (5, "Edge Router"),
    (6, "Mobile Switching Center (MSC)"),
    (7, "Base Transceiver Station (BTS)"),
    (8, "Fiber Distribution Hub"),
    (9, "Network Switch"),
    (10, "VoIP Gateway"),
]

c.executemany("INSERT OR IGNORE INTO equipment_type VALUES (?, ?)", equipment_types)

# Add Sample Equipment
equipment = [
    (
        "Algiers Central OLT",
        "192.168.1.1",
        "11000000.10101000.00000001.00000001",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "00100000000000010000101110000011100001011010001100000000000000000000000000000000100010100010111000000011011100000111001100110100",
        "2023-01-15 08:00:00",
        16,
        1,
    ),
    (
        "Oran Core Router",
        "10.0.0.1",
        "00001010.00000000.00000000.00000001",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7335",
        "00100000000000010000101110000011100001011010001100000000000000000000000000000000100010100010111000000011011100000111001100110101",
        "2022-11-01 14:30:00",
        31,
        4,
    ),
    (
        "Constantine DSLAM",
        "172.16.0.5",
        "10101100.00010000.00000000.00000101",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7336",
        "00100000000000010000101110000011100001011010001100000000000000000000000000000000100010100010111000000011011100000111001100110110",
        "2023-03-22 10:15:00",
        25,
        3,
    ),
]

c.executemany(
    """
    INSERT INTO equipment 
    (description, address_IPV4_decimal, address_IPV4_binary,
     address_IPV6_decimal, address_IPV6_binary, start_serving_date,
     code_wil, code_t)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
    equipment,
)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created and populated successfully!")
print("Added:")
print(f"- {len(wilayas)} Algerian wilayas")
print(f"- {len(equipment_types)} equipment types")
print(f"- {len(equipment)} sample equipment entries")
