# Completed Project for WGU D609 Data Analytics at Scale

This repository contains my completed work for Udacity WGU D609 Data Analytics at Scale.  It is a fork of [this repository](https://github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises) which was provided in the course materials.  The table below summarizes and documents the steps I took to complete the final project.  It includes notes and links to the final project deliverables, which are uploaded to the [/project/completed_work](/project/completed_work/) folder.  The details in the table below contain the information required to replicate my work for validation purposes which should verify that it meets the project rubric specified in the course.

## Table of Contents

|  | Step | Description / Details | Files / Artifacts |
|--|------------------------|------|----------------|
| 1. | Setup  | Run a series of commands on AWS Cloudshell to create an S3 bucket, and configure AWS Glue to connect to S3. The input and output from the AWS Cloudshell terminal was saved as a text file. | [Cloudshell_Commands_and_Output.txt](/project/completed_work/Cloudshell_Commands_and_Outputs.txt) | 
| 2. | Create Database | Open Glue Studio, select Data Catalog, create database named "stedi". | None (completed in web console)
| 3. | Create customer_landing | Create table in Data Catalog, using string and big int data types.  Save the SQL DDL. | [customer_landing.sql](/project/completed_work/customer_landing.sql) |
| 4. | Verify customer_landing | Run the following query in AWS Athena: ```SELECT * FROM customer_landing``` Capture a screenshot showing that the table contains 956 rows and has multiple rows where the shareWithResearchAsOfDate is blank. | [customer_landing.png](/project/completed_work/customer_landing.png) |
| 5. | Create accelerometer_landing | Create table in Data Catalog, using string and big int data types. Save the SQL DDL. | [accelerometer_landing.sql](/project/completed_work/accelerometer_landing.sql) |
| 6. | Verify accelerometer_landing | Run the following query in AWS Athena: ```SELECT * FROM accelerometer_landing``` Capture a screenshot showing that the table contains 81,273 rows. | [accelerometer_landing.png](/project/completed_work/accelerometer_landing.png) |
| 7. | Create step_trainer_landing | Create table in Data Catalog, using string and big int data types. Save the SQL DDL. | [step_trainer_landing.sql](/project/completed_work/step_trainer_landing.sql) |
| 8. | Verify step_trainer_landing | Run the following query in AWS Athena: ```SELECT * FROM step_trainer_landing``` Capture a screenshot showing that the table contains 28,680 rows. | [step_trainer_landing.png](/project/completed_work/step_trainer_landing.png) |
| 9. | Load customer_trusted | Create AWS Glue job to load data from customer_landing to customer_trusted table. The job includes a node called "Share with Research" that includes the following where clause in the SQL: ```where shareWithResearchAsOfDate is not null```.  This node drops rows that do not have data in the sharedWithResearchAsOfDate column.  It is implemented as a Transform SQL Query as recommended by the project rubric. The option to dynamically infer and update schema was enabled by selecting the following Data Catalog update option for the final step: ***Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions.*** The job code was saved and exported as a Python file. | [customer_landing_to_trusted.py](/project/completed_work/customer_landing_to_trusted.py) [glue_job_customer_landing_to_trusted.png](/project/completed_work/glue_job_customer_landing_to_trusted.png) |
| 10. | Verify customer_trusted | Run the following query in AWS Athena: ```SELECT * FROM customer_trusted``` Capture a screenshot showing that the table contains 482 rows. Verify that none of the rows have blank values in the shareWithResearchAsOfDate column. | [customer_trusted.png](/project/completed_work/customer_trusted.png) |
| 11. | Load accelerometer_trusted | Create AWS Glue job that joins accelerometer_landing with customer_trusted by email address. The job loads accelerometer_trusted using only the fields from accelerometer_landing. The option to dynamically infer and update schema was enabled by selecting the following Data Catalog update option for the final step: ***Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions.*** The job code was saved and exported as a Python file. | [accelerometer_landing_to_trusted.py](/project/completed_work/accelerometer_landing_to_trusted.py) [glue_job_accelerometer_landing_to_trusted.png](/project/completed_work/glue_job_accelerometer_landing_to_trusted.png) |
| 12. | Verify accelerometer_trusted | Run the following query in AWS Athena: ```SELECT * FROM accelerometer_trusted``` Capture a screenshot showing that the table contains 40,981 rows. | [accelerometer_trusted.png](/project/completed_work/accelerometer_trusted.png) |
| 13. | Load customer_curated | Create AWS Glue job that joins customer_trusted with accelerometer_trusted by email without generating duplicate values. The job loads customer_curated using only fields from customer_trusted. The option to dynamically infer and update schema was enabled by selecting the following Data Catalog update option for the final step: ***Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions.*** The job code was saved and exported as a Python file. | [customer_trusted_to_curated.py](/project/completed_work/customer_trusted_to_curated.py) [glue_job_customer_trusted_to_curated.png](/project/completed_work/glue_job_customer_trusted_to_curated.png) | 
| 14. | Verify customer_curated | Run the following query in AWS Athena: ```SELECT * FROM customer_curated``` Capture a screenshot showing that the table contains 482 rows. | [customer_curated.png](/project/completed_work/customer_curated.png) |
| 15. | Create step_trainer_trusted | Create AWS Glue job that joins step_trainer_landing with customer_curated on serialnumber. The job loads step_trainer_trusted using only fields from step_trainer_landing. The option to dynamically infer and update schema was enabled by selecting the following Data Catalog update option for the final step: ***Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions.*** The job code was saved and exported as a Python file. | [step_trainer_trusted.py](/project/completed_work/step_trainer_trusted.py) [glue_job_step_trainer_trusted.png](/project/completed_work/glue_job_step_trainer_trusted.png) |
| 16. | Verify step_trainer_trusted | Run the following query in AWS Athena: ```SELECT * FROM step_trainer_trusted``` Capture a screenshot showing that the table contains 14,460 rows. | [step_trainer_trusted.png](/project/completed_work/step_trainer_trusted.png) |
| 17. | Create machine_learning_curated | Create AWS Glue job that joins step_trainer_trusted to accelerometer_trusted on timestamp and sensorReadingTime.  The job loads all columns from both tables into machine_learning_curated. The option to dynamically infer and update schema was enabled by selecting the following Data Catalog update option for the final step: ***Create a table in the Data Catalog and on subsequent runs, update the schema and add new partitions.*** The job code was saved and exported as a Python file. | [machine_learning_curated.py](/project/completed_work/machine_learning_curated.py) [glue_job_machine_learning_curated.png](/project/completed_work/glue_job_machine_learning_curated.png) |
| 18. | Verify machine_learning_curated | Run the following query in AWS Athena: ```SELECT * FROM machine_learning_curated``` Capture a screenshot showing that the table contains 43,681 rows. | [machine_learning_curated.png](/project/completed_work/machine_learning_curated.png) |


## Disclaimer
The original version of this README document contains several notes from prior revisions to the project.  Those notes are unchanged and are preserved in their original form below.  Other README pages in other folder of the repository also contain similar historical information.  No changes or deletions were made to those files.

My project work is contained in the files and folders that are linked in the table above.  The original version of this README document appears below.



# Original README Document


# Purpose of This Repo

This repo is meant to be used to keep things organized during content development and act as the source of truth for all projects and exercises related to this course.

## Folder Structure

### Lesson Folder

This repo contains a folder for each `lesson` and one `project` folder.

Example
```
lesson-1-hello
lesson-2-world
lesson-3-foo
lesson-4-bar
project
```

Each `lesson` folder is named using the naming convention of `lesson-#-name-of-lesson`.

Example
```
lesson-1-hello
```

Four lesson folders have been provided as a template; However, you may need to add more or possibly use less than four depending on what is needed.

If you require an additional lesson folder, you can make a copy of the folder and paste it into the root directory.

### Exercises Folder

Each `lesson` folder contains an `exercises` folder. This `exercises` folder should contain all files and instructions necessary for the exercises along with the solution. The solutions for these exercises will be shared with students. See the `README` in the `exercises` folder for information about folder structure.

### Project Folder

The `project` folder should contain all files and instructions necessary for setup. If possible, a set of instructions should be provided for both Udacity workspaces and a way to work locally (for both MacOS and Windows OS). At a minimum, one set of instructions should be provided. A `README` template has been provided in the project folder. This template layout should be used to write your README.
