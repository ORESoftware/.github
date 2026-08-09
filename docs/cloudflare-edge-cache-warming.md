# Centralized Cloudflare edge cache warming

**Status:** proposed / provider benchmark required  
**Scope:** approximately 20–30 ORESoftware-owned domains  
**Portfolio epic:** [ORESoftware/.github#1](https://github.com/ORESoftware/.github/issues/1)  
**Cluster implementation:** [ORESoftware/k8s-cluster#961](https://github.com/ORESoftware/k8s-cluster/issues/961)  
**Linear mirror:** [DEN-2156](https://linear.app/denman/issue/DEN-2156/infra-centralize-multi-domain-cloudflare-edge-cache-warming)

## Decision summary

Build one provider-neutral, centrally managed cache-warming service for ORESoftware's Cloudflare-fronted public sites.

The service will use:

- one reviewed portfolio manifest for all domains;
- one deployment and observability surface;
- one centrally owned account and credential set per selected provider, never one account per domain;
- bounded regional requests that measure the Cloudflare data centers actually reached;
- deployment/purge-triggered warming plus a conservative periodic safety run;
- a benchmark that compares direct regional compute, Bright Data, Decodo, ScraperAPI, ScrapingBee, Zyte, and Oxylabs before a long-term purchase.

Bright Data is a candidate, not a predetermined winner. For ORESoftware-owned public pages, direct regional runners or ordinary datacenter proxies should be tested before residential networks, browser rendering, CAPTCHA solving, or extraction products.

## Non-negotiable request policy

### Denied hosts

Never perform DNS resolution or an HTTP request for a hostname whose normalized left-most label is exactly:

- `api`
- `app`
- `www`

Apply this policy:

1. while validating the manifest;
2. before every dispatch;
3. after every DNS resolution;
4. after every redirect;
5. before any retry.

An apex redirect to `www` is a failed eligibility check, not a redirect to follow. The domain must be made apex-canonical or an explicitly approved non-denied content hostname must be selected.

The apex hostname is the only implicit target. Every other hostname requires an explicit allow-list entry.

### Allowed traffic

Only anonymous, public, idempotent HTTP(S) requests are allowed.

- Use `GET` for actual warming and verification.
- `HEAD` may be used for diagnostics, but it is not the primary warm path.
- Do not send cookies, authorization headers, credentials, signed URLs, form data, or mutations.
- Do not visit login, account, admin, checkout, personalized, application, or API routes.
- Do not crawl arbitrary subdomains or third-party resources.
- Reject nonstandard ports unless explicitly reviewed.
- Reject loopback, private, link-local, multicast, and other non-public destinations before connection and after every redirect/DNS change.

## Cloudflare behavior the design must respect

1. Cloudflare caches eligible static file extensions by default; HTML and JSON are not cached by default. Public HTML warming therefore requires a reviewed Cache Rule or safe origin policy.
2. Cloudflare caches a resource only in the data center that serves the request. Regional traffic gives measured regional coverage; it does not prove that every Cloudflare point of presence is warm.
3. A first eligible request commonly fills the cache and a later sequential request verifies it. Record `CF-Cache-Status`, `Age`, and the colo suffix in `CF-Ray` for both passes.
4. Treat `DYNAMIC` as not eligible at request time. Treat `BYPASS` as eligible at request time but rejected at response time because of origin headers or another cacheability condition. Do not retry either indefinitely.
5. Evaluate Tiered Cache before paying for broad external warm traffic. Tiered Cache reduces origin fan-out and is available on all current Cloudflare plans; topology options vary by plan.
6. Evaluate Cache Reserve/Smart Shield and plan-eligible URL prefetching separately. They may reduce, but do not automatically eliminate, the need for targeted warming.
7. Never remove privacy-sensitive cache headers or cookie behavior merely to improve the cache-hit ratio.

## Proposed architecture

### Components

1. **`edge-preloader` Rust CLI/service**
   - provider-neutral transport interface;
   - manifest validation;
   - bounded sitemap/seed discovery;
   - URL normalization and deduplication;
   - warm and sequential verify commands;
   - dry-run and cost-estimate commands;
   - structured JSON report and Prometheus/OpenTelemetry telemetry.

2. **Portfolio manifest**
   - versioned in Git;
   - no credentials;
   - supports at least 30 domains without code changes;
   - explicit paths, optional same-host sitemaps, hard discovery limits, region selection, and per-domain budgets.

3. **Kubernetes deployment**
   - container image;
   - `Job` for manual or deployment-triggered runs;
   - `CronJob` for the bounded safety run;
   - ExternalSecret/Secret references;
   - global pause switch and provider circuit breaker.

4. **Optional GitHub Actions diagnostics**
   - validation and dry-run only by default;
   - manual one-domain probe;
   - no long-running portfolio schedule in Actions when the cluster is available.

### Example manifest

```yaml
version: 1

defaults:
  regions: [us-east, us-west, south-america, europe, asia-pacific]
  max_urls_per_domain: 100
  max_redirects: 3
  max_retries: 2
  timeout_seconds: 20
  verification_sample_percent: 10
  max_response_bytes: 10485760
  daily_request_budget: 10000
  monthly_spend_budget_usd: 100

policy:
  deny_first_labels: [api, app, www]
  allow_schemes: [https]
  allow_ports: [443]

domains:
  - host: example.com
    enabled: true
    seeds: ["/"]
    sitemaps:
      - "https://example.com/sitemap.xml"
    include_paths: ["/**"]
    exclude_paths:
      - "/login/**"
      - "/account/**"
      - "/admin/**"
      - "/checkout/**"
    cache_html_expected: false
```

## Warm/verify execution flow

For each enabled domain:

1. Normalize the hostname, paths, IDN representation, trailing dots, ports, and query policy.
2. Verify authoritative DNS, Cloudflare proxying, public IP resolution, TLS, canonical redirects, origin cache headers, and cache eligibility.
3. Load only configured seeds and same-host sitemap URLs.
4. Canonicalize and deduplicate discovered URLs; strip fragments; allow query strings only when explicitly approved because they can create separate cache keys.
5. Reapply host, path, IP, port, and scheme policy immediately before dispatch.
6. Send a bounded first-pass `GET` from the requested region.
7. Send a sequential verification `GET` for critical URLs and the configured sample; do not issue a thundering herd for one cache key.
8. Record requested region, observed Cloudflare colo, redirect chain, HTTP status, `CF-Cache-Status`, `Age`, cache headers, latency, bytes, retries, provider, and cost estimate.
9. Continue with the rest of the fleet when one domain fails, while returning an aggregate run status.

## Provider benchmark

Benchmark 3–5 representative domains from 4–6 regions before selecting a paid default.

### Candidate order

1. Direct regional compute or synthetic probes.
2. Bright Data datacenter proxy network.
3. Decodo datacenter proxies.
4. ScraperAPI or ScrapingBee managed request APIs.
5. Zyte or Oxylabs when support, success rate, or geographic coverage justifies the extra platform cost.
6. Residential, mobile, browser, or unlocker products only after ordinary datacenter access is proven insufficient.

### Required measurements

- requested geography versus observed `CF-Ray` colo;
- first-pass and verification-pass cache outcome;
- success rate, latency, and geographic fidelity;
- billed requests and bytes;
- minimum commitment, overage behavior, and hard spend controls;
- account/zone reuse across all domains;
- API simplicity, auditability, credential rotation, and terms for traffic to owned sites.

Maintain a dated cost model. Vendor prices and plan capabilities must be rechecked when the provider decision is made rather than treated as permanent architecture facts.

Bright Data's current datacenter PAYG page advertises bandwidth billing and supports country targeting through zone credentials. This is appropriate for the pilot, but the pilot must still prove that the observed Cloudflare colos and cost are better than direct regional runners.

## Scheduling strategy

Initial production policy:

- run on deployment or targeted purge for affected domains;
- support a manual one-domain/one-region probe;
- run one conservative weekly bounded portfolio safety job;
- tune per-domain schedules from observed traffic, TTLs, evictions, and cache analytics.

Do not begin with a full portfolio run every 12 hours. That cadence is an upper-bound configuration example, not the default operating decision.

## Security and cost controls

- Store provider and Cloudflare credentials only in the cluster secret-management path.
- Use a read-only Cloudflare token for inventory/preflight where possible.
- Use a separate least-privilege token for any targeted purge integration.
- Never place credentials in Git, issue bodies, Linear, logs, metrics, reports, images, or command history.
- Enforce global and per-domain limits for URLs, redirects, retries, concurrency, response size, decompressed size, bytes, requests, duration, and spend.
- Redact cookies, authorization headers, query secrets, signed URLs, and provider credentials.
- Include dry-run validation and a pre-run cost estimate.
- Alert on attempted denied-host traffic, budget breach, no successful regions, or sustained verification failure.

## Observability

Emit structured logs, a machine-readable run report, and metrics for:

- attempts, successes, and failures by domain/provider/requested region;
- observed Cloudflare colo coverage;
- cache status distribution;
- verification success rate;
- latency and bytes transferred;
- estimated and actual provider spend;
- skipped URLs and exclusion reasons;
- DNS, TLS, sitemap, redirect, cacheability, and provider errors.

Dashboard the portfolio and retain a per-run artifact suitable for before/after comparison.

## Rollout

1. Inventory all candidate domains and record current DNS, proxy status, canonical redirects, sitemaps, cache rules, cache-hit ratio, cold TTFB, and origin requests.
2. Run the provider benchmark and publish the provider/cost decision.
3. Pilot two or three domains.
4. Expand to ten domains only after exclusion tests, spend caps, and cache verification pass.
5. Expand to the complete fleet.
6. Revisit regions and frequency from observed user distribution and Cloudflare analytics.

## Acceptance criteria

- [ ] One centrally managed provider account/credential set supports the fleet, or the selected direct-regional design documents why no proxy account is needed.
- [ ] A versioned manifest supports at least 30 domains without code changes.
- [ ] `api.*`, `app.*`, and `www.*` are rejected during configuration, DNS/dispatch, redirect handling, and retry handling.
- [ ] Unit, property, integration, and end-to-end tests prove an allowed apex cannot reach a denied hostname or private address.
- [ ] Every target has a recorded Cloudflare proxy/cacheability audit.
- [ ] HTML warming is not reported successful unless the page is deliberately eligible for caching.
- [ ] Requested region and observed Cloudflare colo are recorded without claiming universal PoP coverage.
- [ ] Cacheable pilot URLs show the expected sequential verification result; `DYNAMIC` and `BYPASS` produce actionable findings.
- [ ] One failed domain or provider endpoint does not abort the fleet run.
- [ ] Request, byte, duration, retry, redirect, concurrency, response-size, and spend caps are enforced.
- [ ] No secrets or private/personalized content appear in source, logs, reports, workflow output, issues, or container images.
- [ ] Before/after evidence includes cache-hit ratio, cold TTFB, origin-request volume, failure rate, and provider spend.
- [ ] The runbook covers onboarding/removing a domain, provider changes, credential rotation, pausing, cache-status debugging, and budget alerts.

## Primary references

- [Cloudflare default cache behavior](https://developers.cloudflare.com/cache/concepts/default-cache-behavior/)
- [Cloudflare cache responses](https://developers.cloudflare.com/cache/concepts/cache-responses/)
- [Cloudflare Tiered Cache](https://developers.cloudflare.com/cache/how-to/tiered-cache/)
- [Cloudflare Cache Reserve](https://developers.cloudflare.com/cache/advanced-configuration/cache-reserve/)
- [Bright Data geolocation targeting](https://docs.brightdata.com/api-reference/proxy/geolocation-targeting)
- [Bright Data datacenter pricing](https://brightdata.com/pricing/proxy-network/datacenter-proxies)
- [Squarespace with Cloudflare](https://support.squarespace.com/hc/en-us/articles/213469948-Using-Cloudflare-with-Squarespace)
