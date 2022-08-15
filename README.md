# TrackingAnalyzer
# Create the initial database and associated tables: only first time
    cmd prompt go in project folder util and from models.py, run create_database_tables() function
# Initial database and tables are created using fleet.csv and track.csv


-------------------------------------------  not in code yet      --------------------------------------------

#for later development:
    Able to add different accounts for organization [*** users of same organization will share same database]
    each organization: Create users page with authentication [*** provide forms to create user based on .org]
        [*** provide authentication and permissions to different user: define rules]
        Administrator account:
            users with authenticated permissions will be able to add and update table database [organization level]
            add new queries[Natural language] with their sql commands to their organization database
            add regular users permissions
        Regular User account:
            run queries to check different track and fleet status [TrackAnalyzer]
            raise requests to add more queries [support/contact/help]
            users can download both csvs
    
        Add invoicing:sales,expense and total related pages and database tables
            
        
        
         