# Revenue Evidence Snapshot - 2026-06-21T19:25:35+00:00

- Revenue readiness: `blocked`
- Can explain non-payment from analytics: `False`
- External action state: `unverified`
- Allowed external action count: `None`
- Blockers: primary_offer_public_deployment_drift, no_local_funnel_events

## Public Storefront
- 200 <https://igorganapolsky.github.io/> ok=True
- 200 <https://igorganapolsky.github.io/openclaw-agent-safety-diagnostic.html> ok=True
- 200 <https://igorganapolsky.github.io/openclaw-agent-safety-sample.html> ok=True
- 200 <https://igorganapolsky.github.io/openclaw-computer-use-troubleshooting.html> ok=True
- 200 <https://igorganapolsky.github.io/openclaw-mac-ai-workstation-setup/troubleshooting.html> ok=True
- 200 <https://igorganapolsky.github.io/openclaw-mac-ai-workstation-setup/computer-use-plugin-unavailable.html> ok=True
- 200 <https://igorganapolsky.github.io/resumeos/> ok=True
- 200 <https://igorganapolsky.github.io/applyops/> ok=True
- 200 <https://igorganapolsky.github.io/ralph-resume-os/> ok=True
- 200 <https://igorganapolsky.github.io/api/products.json> ok=True
- 200 <https://igorganapolsky.github.io/thanks/> ok=True

## Checkout Links
- 200 <https://buy.stripe.com/00w14neyUcXA5pL5e33sI0e?client_reference_id=api_agent_safety_diagnostic&utm_source=products_api&utm_medium=catalog&utm_campaign=openclaw_agent_safety> ok=True
- 200 <https://buy.stripe.com/5kQ9ATduQcXA5pL35V3sI0R?client_reference_id=api_stripe_connect_diagnostic&utm_source=products_api&utm_medium=catalog&utm_campaign=stripe_connect_audit> ok=True
- 200 <https://buy.stripe.com/3cIaEX1M80aO9G1fSH3sI2N?client_reference_id=api_truth_snapshot&utm_source=products_api&utm_medium=catalog&utm_campaign=resumeos_launch> ok=True
- 200 <https://buy.stripe.com/3cI3cvgH26zccSd7mb3sI2O?client_reference_id=api_resume_os_pro&utm_source=products_api&utm_medium=catalog&utm_campaign=resumeos_launch> ok=True
- 200 <https://buy.stripe.com/9B600j4YkcXAcSdayn3sI2P?client_reference_id=api_done_for_you_sprint&utm_source=products_api&utm_medium=catalog&utm_campaign=resumeos_launch> ok=True

## Funnel Experiment Deployment
- Local implemented experiments: `sample_to_checkout_bridge, clarify_diagnostic_scope_and_deliverables, capture_diagnostic_checkout_objections`
- Public deployed experiments: `sample_to_checkout_bridge, clarify_diagnostic_scope_and_deliverables, capture_diagnostic_checkout_objections`
- `capture_diagnostic_checkout_objections`: deployed=`True` status=`200` missing=`none` <https://igorganapolsky.github.io/openclaw-agent-safety-diagnostic.html>
- `clarify_diagnostic_scope_and_deliverables`: deployed=`True` status=`200` missing=`none` <https://igorganapolsky.github.io/openclaw-agent-safety-diagnostic.html>
- `sample_to_checkout_bridge`: deployed=`True` status=`200` missing=`none` <https://igorganapolsky.github.io/openclaw-agent-safety-sample.html>
- `tighten_openclaw_entrypoint_message`: deployed=`False` status=`200` missing=`unapproved external side effect, logged-in production browser` <https://igorganapolsky.github.io/>

## Public Primary Offer Deployment
- All Stripe Connect primary-offer surfaces deployed: `False`
- Deployed surfaces: `products_json, schema_json, llms_txt, well_known_llms_txt`
- `llms_txt`: deployed=`True` status=`200` missing=`none` <https://igorganapolsky.github.io/llms.txt>
- `products_json`: deployed=`True` status=`200` missing=`none` <https://igorganapolsky.github.io/api/products.json>
- `root`: deployed=`False` status=`200` missing=`Stripe Connect marketplace payment bugs are expensive to debug after launch.` <https://igorganapolsky.github.io/>
- `schema_json`: deployed=`True` status=`200` missing=`none` <https://igorganapolsky.github.io/api/schema.json>
- `well_known_llms_txt`: deployed=`True` status=`200` missing=`none` <https://igorganapolsky.github.io/.well-known/llms.txt>

## Analytics
- Plausible readback configured: `True`
- Plausible API readback ok: `True`
- Plausible API status: `200`
- Plausible API diagnosis: `ok`
- Conversion diagnosis: `insufficient_evidence`
- Site id present: `True`
- Token present: `True`
- Plausible v2 query status: `200`
- Plausible v1 aggregate status: `200`
- Plausible v1 sites status: `200`
- Plausible 7d visitors: `43`
- Plausible 7d visits: `43`
- Plausible 7d pageviews: `45`
- Plausible 7d bounce rate: `33`
- Plausible 7d range: `2026-06-14T00:00:00-04:00` to `2026-06-20T23:59:59-04:00`

### Top Pages
- `/`: visitors `16`, pageviews `19`, bounce `62`
- `/openclaw-mac-ai-workstation-setup/computer-use-plugin-unavailable.html`: visitors `12`, pageviews `11`, bounce `27`
- `/openclaw-mac-ai-workstation-setup/troubleshooting.html`: visitors `12`, pageviews `11`, bounce `9`
- `/applyops/`: visitors `2`, pageviews `2`, bounce `0`
- `/openclaw-mac-ai-workstation-setup/`: visitors `1`, pageviews `1`, bounce `0`
- `/openclaw-mac-ai-workstation-setup/codex-computer-use-intel-mac.html`: visitors `1`, pageviews `1`, bounce `0`

### Top Sources
- `Direct / None`: visitors `30`, visits `30`, bounce `47`
- `Google`: visitors `6`, visits `6`, bounce `0`
- `GitHub`: visitors `5`, visits `5`, bounce `0`
- `DuckDuckGo`: visitors `2`, visits `2`, bounce `0`

### Top Events
- `pageview`: events `45`, visitors `41`
- `offer_objection_click`: events `41`, visitors `29`

## Conversion Diagnosis
- Likely primary issue: `insufficient_evidence`
- Findings: `traffic_without_checkout_intent`
- Checkout click events 7d: `0`
- Checkout abandon reason events 7d: `0`
- Lead click events 7d: `0`
- Visitors 7d: `43`
- Sitewide bounce 7d: `33`
- Top-page bounce: `62`

## Recommended Next Experiment
- Implemented experiments: `sample_to_checkout_bridge, clarify_diagnostic_scope_and_deliverables, capture_diagnostic_checkout_objections`
- Public deployed experiments: `sample_to_checkout_bridge, clarify_diagnostic_scope_and_deliverables, capture_diagnostic_checkout_objections`
- Experiment: `publish_stripe_connect_primary_offer_surfaces`
- Why: The Stripe Connect primary offer exists locally or in catalog files, but it is not proven across the public root, product catalog, Schema.org, and LLM index surfaces.
- Success metric: `public_primary_offer.all_deployed=true and all required Stripe Connect markers present on public URLs`
- Safe action: Publish owned GitHub Pages surfaces only; do not spend Connects or post externally.

## External Action Gates
- Business date: `2026-06-21`
- Controller: `reports/revenue_controls/latest_no_connect_revenue_controller.json` exists=`False`
- State: `unverified`
- Allowed actions: `None`
- Blocked actions: `None`
- Connect spend allowed: `None`
- External side effects observed: `None`
- Submitted or spent Connects: `None`
- Money-truth artifacts complete: `False`
- Required artifacts:
  - `operator_close_packet`: exists=`False` path=`reports/gtm/2026-06-21-money-today/operator-close-packet.md`
  - `revenue_evidence_snapshot`: exists=`False` path=`reports/gtm/2026-06-21-revenue-evidence.md`
  - `stripe_truth_readback`: exists=`False` path=`reports/gtm/2026-06-21-stripe-truth-readback.md`

## Local Funnel Events
- Events: `0`
- Latest timestamp: `None`

### Local Checkout Abandon Reasons
- By reason: `none recorded`

## Payment Truth
- Stripe revenue is not inferred from local files. Use the Stripe connector/export and attach object IDs.
