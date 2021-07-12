#import packages
from typing import Type
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)
print(type(spark))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configure MLflow Experiment
mlflow_experiment_id = 866112

# Including MLflow
import mlflow
import mlflow.spark

import os
print("MLflow Version: %s" % mlflow.__version__)

#MLflow Version: 0.8.2

#df = spark.sql("select Type_code, Type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest from SAMPLE")
#df = spark.createDataFrame(["SAMPLE"])
#df = spark.read.load("C:/Users/sneha/OneDrive/Desktop/Snehal/Masters_Study/Study-SEM2/CaseStudy_Pwc/SAMPLE.csv", format="csv")

df = spark.read.csv("C:/Users/sneha/OneDrive/Desktop/Snehal/Masters_Study/Study-SEM2/CaseStudy_Pwc/python_scripts/12_07_2021_SAMPLE.csv", inferSchema=True, header=True)


#print(df.head())

df.show(5)
df.printSchema()

#RULE BASED MODELS
# Calculate the differences between originating and destination balances
df = df.withColumn("orgDiff", df.oldbalanceOrg - df.newbalanceOrg).withColumn("destDiff", df.newbalanceDest - df.oldbalanceDest)

# Create temporary view
df.createOrReplaceTempView("financials")

df.show()

from pyspark.sql import functions as F

# Rules to Identify Known Fraud-based
df = df.withColumn("label", 
                   F.when(
                     (
                       (df.oldbalanceOrg <= 50000) & (df.Type == "TRANSFER" ) & (df.oldbalanceDest <= 105)) | 
                       (
                         (df.oldbalanceOrg > 50000) & (df.newbalanceOrg <= 12) | (df.oldbalanceDest <= 105)) | 
                           (
                             (df.oldbalanceOrg > 50000) & (df.newbalanceOrg > 12) & (df.amount > 1160000)
                           ), 1
                   ).otherwise(0))

# Calculate proportions
fraud_cases = df.filter(df.label == 1).count()
total_cases = df.count()
fraud_pct = 1.*fraud_cases/total_cases

# Provide quick statistics
print("Based on these rules, we have flagged %s (%s) fraud cases out of a total of %s cases." % (fraud_cases, fraud_pct, total_cases))

# #Export labelled data
# df.to_csv('LabelledData.csv')

# Create temporary view to review data
df.createOrReplaceTempView("financials_labeled")

df.show(30)

#DECISION TREES
# Initially split our dataset between training and test datasets
(train, test) = df.randomSplit([0.75, 0.25], seed=12345)

# Cache the training and test datasets
train.cache()
test.cache()

# Print out dataset counts
print("Total rows: %s, Training rows: %s, Test rows: %s" % (df.count(), train.count(), test.count()))

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier

#Encodes a string column of labels to a column of label indices
indexer = StringIndexer(inputCol = "Type", outputCol = "typeIndexed")

# VectorAssembler is a transformer that combines a given list of columns into a single vector column
va = VectorAssembler(inputCols = ["typeIndexed", "amount", "oldbalanceOrg", "newbalanceOrg", "oldbalanceDest", "newbalanceDest" ], outputCol = "features")

# Using the DecisionTree classifier model
dt = DecisionTreeClassifier(labelCol = "label", featuresCol = "features", seed = 54321, maxDepth = 5)

# Create our pipeline stages
pipeline = Pipeline(stages=[indexer, va, dt])

dt_model = pipeline.fit(train)
#dt_model.show()
print(dt_model.stages[-1].toDebugString)

predictions = dt_model.transform(test)
print(predictions.show())

from pyspark.ml.evaluation import MulticlassClassificationEvaluator
evaluator = MulticlassClassificationEvaluator(labelCol="isFraud", predictionCol="prediction",metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g " % (1.0 - accuracy))
print("Accuracy = %g " % accuracy)