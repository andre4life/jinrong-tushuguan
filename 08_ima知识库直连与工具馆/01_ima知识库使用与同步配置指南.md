# 01 ima 知识库使用与同步配置指南

## 1. 腾讯 ima 知识库 OpenAPI 概述

腾讯 ima 知识库是腾讯推出的大模型知识库与智能工作台。通过 OpenAPI，可实现本地金融资产、专家方法论、培训资料与云端智能知识库的双向打通：
- **Base URL**: \`https://ima.qq.com/openapi/wiki/v1\`
- **认证方式**: HTTP Header 携带 \`ima-openapi-clientid\` 与 \`ima-openapi-apikey\`。

---

## 2. 配置文件结构 (config.json)

在金融图书馆根目录或 \`D:\Hermes输出\ima接入\config.json\` 中维护凭证：

```json
{
  "client_id": "3a93bc1ccc5f54d6b1103a0ba4824f6f",
  "api_key": "fUIfBMuEGBIB8/DtJjxo2kj6Nj164RnWCMMpbuZqTdn4MlTIJc3S3T4vy9yrOkBf6+uCXYeKsw==",
  "kb_id": "gy0q242S12_lBTcUH4QADLEnE2GcM-JKps7Jv5cg75g="
}
```

- **已连接的两个云端知识库**：
  1. \`Andre的知识库\` (\`yu8CTx613whu49MQioSMN8ODW0nmMtGsmm23qs0YS2A=\`)
  2. \`ins-knowledge base\` (\`gy0q242S12_lBTcUH4QADLEnE2GcM-JKps7Jv5cg75g=\`)
