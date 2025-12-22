# API

## Public Endpoints

- `POST /api/v1/scan` — upload a file. Parameters: `mode` (`sync`|`async`), `explain` (bool). Returns job id or result.
- `GET /api/v1/scan/{scan_id}` — retrieve scan result.
- `GET /api/v1/jobs/{job_id}` — check async job status.
- `POST /api/v1/scan/hash` — retrieve previous scan by SHA256.

## Admin Endpoints (API key required via `X-API-Key` header)

- `GET /api/v1/admin/scans` — list recent scans.
- `GET /api/v1/admin/models` — list models.
- `POST /api/v1/admin/models/activate/{model_version}` — activate version.
- `GET /metrics` — Prometheus metrics.
- `GET /health` — health check.

### Curl Examples

```bash
curl -X POST -F "file=@sample.bin" http://localhost:8000/api/v1/scan
curl http://localhost:8000/api/v1/scan/<scan_id>
curl -H "X-API-Key: $API_KEY" http://localhost:8000/api/v1/admin/scans
```
