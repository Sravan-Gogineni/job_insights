def gold_layer_etl():
    import pandas as pd
    import psycopg2
    from psycopg2 import sql, OperationalError
    from dotenv import load_dotenv
    import os
    
    load_dotenv
    def check_postgres_connection(host, dbname, user, password, port=5444):
        """Check PostgreSQL connection."""
        try:
            connection = psycopg2.connect(
                host=host,
                dbname=dbname,
                user=user,
                password=password,
                port=port  
            )
            print("Connection successful")
            
            cursor = connection.cursor()
            cursor.execute("SELECT 1;")
            
        except OperationalError as e:
            print(f"Connection failed: {e}")
        
        finally:
            if connection:
                cursor.close()
                connection.close()

    def insert_data_to_postgres(csv_file_path, host, dbname, user, password, port=5444):
        """Insert data from CSV to PostgreSQL star schema."""
      
        conn = psycopg2.connect(host=host, database=dbname, user=user, password=password, port=port)
        cursor = conn.cursor()

     
        df = pd.read_csv(csv_file_path)

        create_temp_table_query = """
        CREATE TEMP TABLE TempJobPostings (
            company VARCHAR(255),
            companyOverviewLink VARCHAR(5000),
            companyRating NUMERIC(5, 2),
            companyReviewCount NUMERIC,
            displayTitle VARCHAR(255),
            extractedSalary_type VARCHAR(50),
            feedId NUMERIC,
            jobDescription TEXT,
            jobLocationCity VARCHAR(100),
            jobLocationState VARCHAR(100),
            normTitle VARCHAR(100),
            snippet TEXT,
            thirdPartyApplyUrl VARCHAR(5000),
            title VARCHAR(255),
            converted_datetime TIMESTAMP,
            zipcode VARCHAR(10),
            jobLocationState_full VARCHAR(100),
            job_type VARCHAR(50),
            average_expected_salary NUMERIC(15),
            benefits_offered TEXT
        );
        """
        cursor.execute(create_temp_table_query)

       
        for index, row in df.iterrows():
        
            row_data = tuple(None if pd.isna(val) else val for val in row)
        
            cursor.execute(sql.SQL("""
                INSERT INTO TempJobPostings (company, companyOverviewLink, companyRating, companyReviewCount,
                                            displayTitle, extractedSalary_type, feedId, jobDescription,
                                            jobLocationCity, jobLocationState, normTitle, snippet,
                                            thirdPartyApplyUrl, title, converted_datetime, zipcode,
                                            jobLocationState_full, job_type, average_expected_salary,
                                            benefits_offered)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """), row_data)

        
        cursor.execute("""
        INSERT INTO DimCompany (CompanyName, CompanyOverviewLink, CompanyReviewCount)
        SELECT DISTINCT company, companyOverviewLink, companyReviewCount FROM TempJobPostings
        ON CONFLICT (CompanyName) DO NOTHING;
        """)

        
        cursor.execute("""
        INSERT INTO DimLocation (City, State, ZipCode,Country)
        SELECT DISTINCT jobLocationCity AS City,
                        COALESCE(jobLocationState, 'Texas') AS State,
                        zipcode AS ZipCode,
                        'United States' AS Country FROM TEMPJobPostings
        ON CONFLICT (City, State) DO NOTHING;
        """)

        
        cursor.execute("""
        INSERT INTO DimJobType (JobTypeName)
        SELECT DISTINCT job_type FROM TempJobPostings
        ON CONFLICT (JobTypeName) DO NOTHING;
        """)
        
        cursor.execute("""
        INSERT INTO DimBenefits (BenefitDescription)
        SELECT DISTINCT LOWER(TRIM(benefits_offered)) as benefitdescription 
        FROM TempJobPostings
        WHERE benefits_offered IS NOT NULL
        ON CONFLICT (BenefitDescription) DO NOTHING;
        """)

       
        cursor.execute("""
        INSERT INTO FactJobPostings (CompanyID, JobTitle, JobTypeID, LocationID,
                             PostedDate, ConvertedDateTime,
                             Salary, CompanyRating)
        SELECT 
            c.CompanyID,
            t.displayTitle,
            j.JobTypeID,
            l.LocationID,
            t.converted_datetime::DATE,
            t.converted_datetime,
            t.average_expected_salary,
            t.companyRating
        FROM TempJobPostings t
        JOIN DimCompany c ON t.company = c.CompanyName
        JOIN DimLocation l ON t.jobLocationCity = l.City AND t.jobLocationState = l.State AND t.zipcode = l.ZipCode
        JOIN DimJobType j ON t.job_type = j.JobTypeName;
        """)

        
        drop_temp_table_query = "DROP TABLE IF EXISTS TempJobPostings;"
        cursor.execute(drop_temp_table_query)
        

        
        conn.commit()
        
        cursor.close()
        conn.close()

    
    host = "73.167.111.240"  
    dbname = "postgres"  
    user = "postgres" 
    password = os.getenv('POSTGRES_PASSWORD')
    port = 5444  

    
    check_postgres_connection(host=host, dbname=dbname, user=user, password=password)

    
    CSV_FILE_PATH = '/home/ubuntu/airflow/downloaded_files/cleaned_job_file.csv'

    
    insert_data_to_postgres(csv_file_path=CSV_FILE_PATH,
                             host=host,
                             dbname=dbname,
                             user=user,
                             password=password)
    
    print("Data inserted successfully.")

gold_layer_etl()
