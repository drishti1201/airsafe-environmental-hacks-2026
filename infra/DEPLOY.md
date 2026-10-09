# Deploy the Lambda (about 20 minutes, AWS Console)

1. **Build:** `bash infra/build.sh` from the repo root, giving `build/lambda.zip`.
2. **S3 bucket** (audio): create e.g. `heat-desk-audio-<yourname>`, keep it private.
3. **DynamoDB table** (optional, visit log): name `visits`, partition key `household_id` (String), sort key `date` (String), on-demand capacity.
4. **Lambda:** create function, Python 3.12, upload `lambda.zip`. Set Handler to `handler.handler`. Set timeout to 20 s, memory 256 MB.
5. **Environment variables:** `BUCKET=<bucket>`, `TABLE=visits`. Add `POLLY_REGION=us-east-1` only if your Hindi voice is not available in your region.
6. **IAM** (Lambda's role): allow `polly:SynthesizeSpeech`, `s3:PutObject` and `s3:GetObject` on the bucket, `dynamodb:PutItem` on the table.
7. **Function URL:** Configuration -> Function URL -> create, auth type NONE (hackathon demo only), and enable **CORS** there (allow origin `*`, methods GET and POST, header `content-type`).
8. **Test in the browser:** `<function-url>?mitanin=M01&demo=hot` should return JSON with a ranked list and an `audio_url`.

Notes
- Polly: `Kajal` (hi-IN, neural) is the default; the code falls back to `Aditi` (standard). If both fail, check voice availability in your region and set `POLLY_REGION`.
- Auth NONE means anyone with the URL can call it. Fine for synthetic data; say so in the README and delete the URL after judging.
- `demo=hot` uses a simulated forecast and is labelled `"forecast_source": "simulated"`. Say "simulated hot day" in the video. Without it, the live Open-Meteo forecast is used.
