import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

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

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1740289665244 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_trusted", transformation_ctx="AccelerometerTrusted_node1740289665244")

# Script generated for node Customer Trusted
CustomerTrusted_node1740289656905 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="CustomerTrusted_node1740289656905")

# Script generated for node Join
Join_node1740289797911 = Join.apply(frame1=CustomerTrusted_node1740289656905, frame2=AccelerometerTrusted_node1740289665244, keys1=["email"], keys2=["user"], transformation_ctx="Join_node1740289797911")

# Script generated for node Drop Fields
DropFields_node1740289829405 = DropFields.apply(frame=Join_node1740289797911, paths=["user", "timestamp", "x", "y", "z"], transformation_ctx="DropFields_node1740289829405")

# Script generated for node Drop Duplicates
DropDuplicates_node1740290689862 =  DynamicFrame.fromDF(DropFields_node1740289829405.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1740290689862")

# Script generated for node Customer Curated
EvaluateDataQuality().process_rows(frame=DropDuplicates_node1740290689862, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1740288213868", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
CustomerCurated_node1740289923703 = glueContext.getSink(path="s3://sleepy-ninja-wgu-d609/customer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="CustomerCurated_node1740289923703")
CustomerCurated_node1740289923703.setCatalogInfo(catalogDatabase="stedi",catalogTableName="customer_curated")
CustomerCurated_node1740289923703.setFormat("json")
CustomerCurated_node1740289923703.writeFrame(DropDuplicates_node1740290689862)
job.commit()