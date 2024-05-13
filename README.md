# aws-llm-apigateway
Call all LLM on AWS using the OpenAI format API

在AWS美西2区域

1. Bedrock 开启 claude 的访问权限  https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
2. Sagemaker 部署Mistral 7B模型 https://github.com/heisenbergye/aws-llm-apigateway/blob/main/vllm_mistral_7B_deploy_V9.ipynb
3. 准备 AKSK 赋予 Bedrock-runtime 和 Sagemaker-runtime的访问权限
4. 在 Sagemaker Notebook下载demo 的 repo

```
git clone https://github.com/heisenbergye/aws-llm-apigateway.git
cd aws-llm-apigateway/
```
部署步骤：
1. 替换  docker-compose.yml 中的 AK/SK
```
   - AWS_ACCESS_KEY_ID=<AK>
   - AWS_SECRET_ACCESS_KEY=<SK>
```
2. 替换 litellm_config.yaml 中的 model_list
```
  - model_name: mistral7b
    litellm_params:
      model: sagemaker/mistral7b-2024-04-23-10-33-56-031
      aws_region_name: "us-west-2"
      tpm: 1024
```
3. 部署网关
```
docker-compose up -d
```

chat
```
curl --location 'http://0.0.0.0:4000/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer sk-1234' \
--data ' {
"model": "claude3-sonnet",
"temperature": 0.1,
"max_tokens": 1000,
"messages": [
{
"role": "user",
"content": "Tell me something about large language models."
}
]
}'
```

embedding
```
curl --location 'http://0.0.0.0:4000/embeddings' \
--header 'Authorization: Bearer sk-1234' \
--header 'Content-Type: application/json' \
--data '{"input": ["Academia.edu uses"], "model": "cohere", "encoding_format": "base64"}'
```
