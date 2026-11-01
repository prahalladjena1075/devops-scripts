# DevOps Scripts

## Application Health Checker

Checks whether an application is UP or DOWN using the HTTP status code.

### Usage
```bash
python health_checker.py http://localhost:4499        # check once
python health_checker.py http://localhost:4499 10     # check every 10 seconds
```

### Rules
- Status 200 to 399: UP
- Status 400 or above, no connection, or timeout: DOWN
- Each result is printed and saved in `health.log`
- Exit code is 0 for UP and 1 for DOWN
