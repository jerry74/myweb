# Trip Itinerary Maintenance Skill Design

## Goal

Create a low-friction workflow for maintaining the `20260530` Okinawa itinerary without hand-editing PWA code. The itinerary content should live in one YAML source, generate a human-readable Markdown file during daily edits, and update PWA data only when the user explicitly publishes.

## Source Files

- Source of truth: `data/trips/20260530-okinawa.yaml`
- Daily output: `trips/20260530-okinawa.md`
- PWA output: `20260530/data.generated.json`
- Build script: `scripts/build-trip.py`
- Skill: `.codex/skills/trip-itinerary-maintainer/SKILL.md`

## Workflow

Daily edit mode updates YAML and regenerates Markdown only. This keeps frequent itinerary adjustments out of the deployed PWA data until the user is ready.

Publish mode regenerates both Markdown and `20260530/data.generated.json`, then bumps the PWA cache version if the generated data changed.

## PWA Integration

`20260530/app.js` keeps its bundled data as a fallback, but loads `data.generated.json` at startup when available. This lets the site keep rendering offline or if the JSON fetch fails, while making generated data the normal production path.

## Validation

The travel PWA verification script checks that `20260530/data.generated.json` exists, contains trip days, has the expected trip id, and is included in the service worker cache asset list.

## Success Criteria

1. The user can ask Codex to update itinerary content without manually editing YAML.
2. Daily edits update `data/trips/20260530-okinawa.yaml` and `trips/20260530-okinawa.md`.
3. Publishing updates `20260530/data.generated.json`.
4. PWA rendering uses generated data when available.
5. The dedicated skill documents the correct edit and publish workflows.
