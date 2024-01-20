echo "Keys that will expire in 5 days"

gcloud asset search-all-resources \
    --scope="organizations/1012116149117" \
    --query="createTime > 2024-01-19" \
    --asset-types="iam.googleapis.com/ServiceAccountKey" \
    --order-by="createTime" --format="json" | tee /tmp/gcloud_output.json

jq '. | length' /tmp/gcloud_output.json

echo "Keys that have expired (over 5 days old)"

gcloud asset search-all-resources \
    --scope="organizations/1012116149117" \
    --query="createTime < 2024-01-16" \
    --asset-types="iam.googleapis.com/ServiceAccountKey" \
    --order-by="createTime" --format="json" | tee /tmp/gcloud_output.json

jq '. | length' /tmp/gcloud_output.json
