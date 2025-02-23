import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Customer Curated
CustomerCurated_node1740291423103 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_curated", transformation_ctx="CustomerCurated_node1740291423103")

# Script generated for node Step Trainer Landing
StepTrainerLanding_node1740291373653 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_landing", transformation_ctx="StepTrainerLanding_node1740291373653")

# Script generated for node SQL Query
SqlQuery7855 = '''
select step_trainer_landing.* 
from step_trainer_landing inner join customer_curated
on step_trainer_landing.serialnumber = customer_curated.serialnumber
'''
SQLQuery_node1740291463315 = sparkSqlQuery(glueContext, query = SqlQuery7855, mapping = {"step_trainer_landing":StepTrainerLanding_node1740291373653, "customer_curated":CustomerCurated_node1740291423103}, transformation_ctx = "SQLQuery_node1740291463315")

# Script generated for node Step Trainer Trusted
EvaluateDataQuality().process_rows(frame=SQLQuery_node1740291463315, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1740291115934", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
StepTrainerTrusted_node1740291835703 = glueContext.getSink(path="s3://sleepy-ninja-wgu-d609/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="StepTrainerTrusted_node1740291835703")
StepTrainerTrusted_node1740291835703.setCatalogInfo(catalogDatabase="stedi",catalogTableName="step_trainer_trusted")
StepTrainerTrusted_node1740291835703.setFormat("json")
StepTrainerTrusted_node1740291835703.writeFrame(SQLQuery_node1740291463315)
job.commit()