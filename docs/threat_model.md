# Threat Model

- **Assets**: model artifacts, scan results, database records, and service availability.
- **Adversaries**: attackers attempting to bypass detection, exfiltrate scan data, or overload the service.
- **Threats**: malicious files crafted to crash parsers, unauthorized access to admin endpoints, and poisoning via untrusted datasets.
- **Controls**:
  - Input validation and size limits (20 MB default).
  - API key protection for admin routes.
  - Structured logging and metrics for anomaly detection.
  - Default behavior avoids storing raw files, keeping only hashes and metadata.
  - Graceful fallbacks when specialized parsers are unavailable.
