use lambda_runtime::{service_fn, Error, LambdaEvent};
use aws_sdk_s3::Client;
use serde_json::json;
use aws_lambda_events::encodings::Body;
use aws_lambda_events::event::apigw::ApiGatewayProxyResponse;

#[tokio::main]
async fn main() -> Result<(), Error> {
    let func = service_fn(handler);
    lambda_runtime::run(func).await?;
    Ok(())
}

async fn handler(_event: LambdaEvent<serde_json::Value>) -> Result<ApiGatewayProxyResponse, Error> {
    let config = aws_config::defaults(aws_config::BehaviorVersion::latest()).load().await;
    let client = Client::new(&config);

    let bucket = std::env::var("BUCKET_NAME").expect("BUCKET_NAME must be set");
    let resp = client.list_objects_v2().bucket(&bucket).send().await?;

    let files: Vec<String> = resp.contents
        .unwrap_or_default()
        .iter()
        .filter_map(|obj| obj.key().map(ToString::to_string))
        .collect();

    Ok(ApiGatewayProxyResponse {
        status_code: 200,
        body: Some(Body::Text(json!(files).to_string())),
        ..Default::default()
    })
}
