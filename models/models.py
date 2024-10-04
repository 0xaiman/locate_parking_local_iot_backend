

def create_tables(connection):
    create_table_queries =[
        """
        CREATE TABLE IF NOT EXISTS parking_area (
            area_id SERIAL PRIMARY KEY,
            area_name VARCHAR(255) NOT NULL,
            description TEXT
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS parking_bay (
            bay_id SERIAL PRIMARY KEY,
            bay_name VARCHAR(50) NOT NULL,
            time TIMESTAMPTZ NOT NULL,
            device_name VARCHAR(50),
            occupancy_bay VARCHAR(20) DEFAULT FALSE,
            license_plate VARCHAR(50) ,
            vehicle_type VARCHAR(50),
            vehicle_color VARCHAR(20),
            vehicle_brand VARCHAR(50),
            img_path VARCHAR(255) DEFAULT NULL
            );
        """,
        """
            CREATE TABLE IF NOT EXISTS logs (
            log_id SERIAL PRIMARY KEY,
            logs VARCHAR(255) NOT NULL
            );
        """
    ]

    cursor = connection.cursor()

    for query in create_table_queries:
        cursor.execute(query)
    connection.commit()
    cursor.close()
