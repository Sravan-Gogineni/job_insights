def gold_layer_etl():
    import pandas as pd
    import psycopg2
    from psycopg2 import sql, OperationalError

    def check_postgres_connection(host, dbname, user, password, port=5444):
        """Check PostgreSQL connection."""
        connection = None
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

        # Read CSV into DataFrame
        df = pd.read_csv(csv_file_path)

        # Create temporary table
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

        # Insert data into TempJobPostings
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

        # Insert into DimCompany
        cursor.execute("""
        INSERT INTO DimCompany (CompanyName, CompanyOverviewLink, CompanyReviewCount)
        SELECT DISTINCT company, companyOverviewLink, companyReviewCount FROM TempJobPostings
        ON CONFLICT (CompanyName) DO NOTHING;
        """)

        # Insert into DimLocation
        cursor.execute("""
        INSERT INTO DimLocation (City, State, ZipCode, Country)
        SELECT DISTINCT COALESCE(jobLocationCity, 'OTHER') AS City,
                        COALESCE(jobLocationState, 'OTHER') AS State,
                        COALESCE(zipcode, 'UNKNOWN')AS ZipCode,
                        'United States' AS Country FROM TempJobPostings
        ON CONFLICT (City, State) DO NOTHING;
        """)

        # Insert into DimJobType
        cursor.execute("""
        INSERT INTO DimJobType (JobTypeName)
        SELECT DISTINCT job_type FROM TempJobPostings
        ON CONFLICT (JobTypeName) DO NOTHING;
        """)

        # Insert into DimBenefits
        cursor.execute("""
        INSERT INTO DimBenefits (BenefitDescription)
        SELECT DISTINCT LOWER(TRIM(benefits_offered)) as benefitdescription 
        FROM TempJobPostings
        WHERE benefits_offered IS NOT NULL
        ON CONFLICT (BenefitDescription) DO NOTHING;
        """)

        # Insert into FactJobPostings without benefits
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

       # Create FactJobBenefits table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS FactJobBenefits (
           JobPostingID INT,
           BenefitID INT,
           PRIMARY KEY (JobPostingID, BenefitID),
           FOREIGN KEY (JobPostingID) REFERENCES FactJobPostings(JobPostingID),
           FOREIGN KEY (BenefitID) REFERENCES DimBenefits(BenefitID)
        );
        """)

       # Insert into FactJobBenefits for many-to-many relationship
        cursor.execute("""
        INSERT INTO FactJobBenefits (JobPostingID, BenefitID)
        SELECT DISTINCT f.JobPostingID,
            b.BenefitID
        FROM FactJobPostings f
        JOIN TempJobPostings t ON f.JobTitle = t.displayTitle 
        AND f.PostedDate = t.converted_datetime::DATE
        CROSS JOIN LATERAL unnest(string_to_array(t.benefits_offered, ',')) AS benefit(name)
        JOIN DimBenefits b ON LOWER(TRIM(benefit.name)) = b.BenefitDescription
        ON CONFLICT (JobPostingID, BenefitID) DO NOTHING;  
        """)
       # Drop temporary table after use
        drop_temp_table_query = "DROP TABLE IF EXISTS TempJobPostings;"
        cursor.execute(drop_temp_table_query)

        conn.commit()
       
        cursor.close()
        conn.close()

    host = "73.167.111.240"  
    dbname = "postgres"  
    user = "postgres" 
    password = "Ch0wd@ry" 
    port = 5444  

    check_postgres_connection(host=host, dbname=dbname, user=user, password=password)

    CSV_FILE_PATH = '/home/ubuntu/airflow/downloaded_files/cleaned_job_file.csv'

    insert_data_to_postgres(csv_file_path=CSV_FILE_PATH,
                             host=host,
                             dbname=dbname,
                             user=user,
                             password=password)
    
    print("Data inserted successfully.")

