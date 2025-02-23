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

# Script generated for node Accelerometer Landing
AccelerometerLanding_node1740285986403 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_landing", transformation_ctx="AccelerometerLanding_node1740285986403")

# Script generated for node Customer Trusted
CustomerTrusted_node1740286529718 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_trusted", transformation_ctx="CustomerTrusted_node1740286529718")

# Script generated for node Join
Join_node1740286422415 = Join.apply(frame1=AccelerometerLanding_node1740285986403, frame2=CustomerTrusted_node1740286529718, keys1=["user"], keys2=["email"], transformation_ctx="Join_node1740286422415")

# Script generated for node SQL Query
SqlQuery7806 = '''
select user, timestamp, x, y, z
from myDataSource
'''
SQLQuery_node1740287197007 = sparkSqlQuery(glueContext, query = SqlQuery7806, mapping = {"myDataSource":Join_node1740286422415}, transformation_ctx = "SQLQuery_node1740287197007")

# Script generated for node Drop Fields
DropFields_node1740288061212 = DropFields.apply(frame=SQLQuery_node1740287197007, paths=["customername", "email", "phone", "birthday", "serialnumber", "registrationdate", "lastupdatedate", "sharewithresearchasofdate", "sharewithpublicasofdate", "sharewithfriendsasofdate"], transformation_ctx="DropFields_node1740288061212")

# Script generated for node Accelerometer Trusted
EvaluateDataQuality().process_rows(frame=DropFields_node1740288061212, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1740285902714", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AccelerometerTrusted_node1740286612186 = glueContext.getSink(path="s3://sleepy-ninja-wgu-d609/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AccelerometerTrusted_node1740286612186")
AccelerometerTrusted_node1740286612186.setCatalogInfo(catalogDatabase="stedi",catalogTableName="accelerometer_trusted")
AccelerometerTrusted_node1740286612186.setFormat("json")
AccelerometerTrusted_node1740286612186.writeFrame(DropFields_node1740288061212)
job.commit()