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

# Script generated for node Step Trainer Trusted
StepTrainerTrusted_node1740293577019 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_trusted", transformation_ctx="StepTrainerTrusted_node1740293577019")

# Script generated for node Accelerometer Trusted
AccelerometerTrusted_node1740293578351 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_trusted", transformation_ctx="AccelerometerTrusted_node1740293578351")

# Script generated for node SQL Query
SqlQuery7482 = '''
select a.*, t.* 
from accelerometer_trusted a 
    inner join step_trainer_trusted t 
    on a.timeStamp = t.sensorReadingTime
'''
SQLQuery_node1740293582328 = sparkSqlQuery(glueContext, query = SqlQuery7482, mapping = {"accelerometer_trusted":AccelerometerTrusted_node1740293578351, "step_trainer_trusted":StepTrainerTrusted_node1740293577019}, transformation_ctx = "SQLQuery_node1740293582328")

# Script generated for node Machine Learning Curated
EvaluateDataQuality().process_rows(frame=SQLQuery_node1740293582328, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1740292141764", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
MachineLearningCurated_node1740293712986 = glueContext.getSink(path="s3://sleepy-ninja-wgu-d609/machine_learning/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="MachineLearningCurated_node1740293712986")
MachineLearningCurated_node1740293712986.setCatalogInfo(catalogDatabase="stedi",catalogTableName="machine_learning_curated")
MachineLearningCurated_node1740293712986.setFormat("json")
MachineLearningCurated_node1740293712986.writeFrame(SQLQuery_node1740293582328)
job.commit()