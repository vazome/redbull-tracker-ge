import boto3
import json


def lambda_handler(event, context):
    pipeline_name = "redbull-tracker-ge_bot_pipeline"
    client = boto3.client("codepipeline")

    response = client.list_pipeline_executions(pipelineName=pipeline_name, maxResults=1)
    executions = (
        response["pipelineExecutionSummaries"][0]
        if response["pipelineExecutionSummaries"]
        else None
    )

    if executions:
        status = {
            "pipelineName": pipeline_name,
            "status": executions["status"],
            "lastExecutionId": executions["pipelineExecutionId"],
        }
    else:
        status = {"pipelineName": pipeline_name, "status": "No executions found"}

    return {
        "statusCode": 200,
        "body": json.dumps(status),
        "headers": {"Content-Type": "application/json"},
    }
