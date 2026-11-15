# AGENTS.md

Guide for agents (and humans) working in this repository.

## What this repo is

The Home Assistant configuration for a single house — a **YAML-first**
configuration, not a Python project. There is no application to build, no test
suite and no dependency manager. Every change here is a change to a live home:
lights, heating, an alarm system, cameras and notifications to real phones.

Home Assistant itself runs as `homeassistant-0` in the `homeassistant`
namespace of the `raspberry01` Kubernetes cluster. This repo is the source of
truth for its `/config` directory.

`README.md` is the user-facing description (feature list + hardware
inventory). Keep it in sync when a change adds or removes a visible feature or
a piece of hardware.

## Layout

```
configuration.yaml            Root config; wires everything together via !include
secrets.yaml                  Secrets (untracked, local only)
hass_sa.json                  Google service account (untracked, local only)
ui-lovelace.yaml              The whole dashboard, YAML mode
deploy-kubernetes.sh          Deploy: tars the config into the running pod
www/                          Statically served files (floorplan.png, layout-card.js)
configuration/
  automation/*.yaml           Automations, one file per feature/area
  script/*.yaml               Scripts, one file per script
  template.yaml               Template sensors/binary sensors (modern style)
  sensor.yaml                 Platform sensors (legacy style: rest, derivative, integration)
  binary_sensor.yaml          Platform binary sensors (trend, group)
  input_boolean.yaml          Helpers …
  input_select.yaml
  input_number.yaml
  input_datetime.yaml
  scene.yaml                  Scenes
  alert.yaml                  Alerts
  group.yaml                  Groups
  person.yaml                 Persons
  customize.yaml              Per-entity overrides
  customize_glob.yaml         Glob overrides (device_class/icon by name pattern)
  google_assistant.yaml       Which entities are exposed to Google, and their Dutch names
custom_components/            Old copies of custom integrations — no longer deployed (see below)
custom_components_sources/    Upstream git clones of those integrations (untracked)
.history/                     Editor local history — ignore it entirely, never edit
```

### How the includes work

- `automation: !include_dir_merge_list configuration/automation/` — every file
  is a **YAML list** of automations, merged into one list. File names are free
  form; group by feature or area (`livinglights.yaml`, `doorbell.yaml`,
  `washing_machine.yaml`).
- `script: !include_dir_named configuration/script/` — the **file name becomes
  the entity id**: `configuration/script/cast_dashboard_office.yaml` →
  `script.cast_dashboard_office`. Each file is a single script mapping
  (`alias:` + `sequence:`), not a list. Renaming a file renames the entity, so
  grep for the old `script.<name>` first.
- Everything else is a plain `!include` of one file.

## Conventions

### Automations

- Every automation has a stable `id:` in `snake_case` **and** a quoted
  `alias:`. The `id` is what traces, the UI and `automation.trigger` hang on —
  changing it loses the trace history, so treat it as permanent.
  (Historically added in "Give all automations an ID to be able to use
  traces"; a handful of files still lack one — add it when you touch them.)
- Prefer the **modern syntax** in new and edited code:
  - `- trigger: state` inside `trigger:`, not `- platform: state`
  - `- action: light.turn_off` + `target: {entity_id: …}`, not `service:` +
    top-level `entity_id:`
  Older files still use the legacy form. That is fine — do **not** mass-migrate
  them; migrate only what you are already editing, in the same commit as a real
  change.
- With more than one trigger that needs distinct handling, give triggers an
  `id:` and branch on `trigger.id` in conditions/templates (see
  `at_the_table.yaml`, `livinglights.yaml`).
- Add `alias:` to an individual condition or action step when its intent is not
  obvious from the YAML (`alias: TV is on`, `alias: Turn on movie scene`).
- Set `mode:` deliberately when the default `single` is wrong: `restart` for
  notification flows that may re-fire (`doorbell.yaml`), `parallel` + `max:`
  for per-person automations (`at_the_table.yaml`).
- `continue_on_error: true` on steps that are nice-to-have and must not abort
  the rest (snapshots, stopping media on a device that may be off).
- Wrap side-effect-free work that must happen simultaneously in `parallel:`
  rather than serialising it — a doorbell press should not wait for a snapshot.

### Templates

- Always give filters a default: `| float(0)`, `| int(0)`, `states('…') |
  float(0.0)`. Entities are `unknown`/`unavailable` on restart and after
  integration hiccups, and an undefaulted template floods the log.
- Guard availability explicitly where it matters: `availability: "{{
  has_value('sensor.ups_load') }}"`, or a trigger-based template sensor with
  `not_to: [unavailable, unknown]` to latch the last good value (see the
  External IP sensor in `template.yaml`).
- Give template entities a `unique_id:` when they should be editable/renameable
  in the UI.

### Naming and language

- **Entity ids, automation ids, aliases, comments and commit messages:
  English.** Area first, then what it measures:
  `sensor.living_illuminance`, `binary_sensor.hallway_gf_motion`,
  `switch.small_office`.
- **Anything a human reads in the house: Dutch.** Notification titles and
  bodies, helper `name:`s, dashboard card titles, Google Assistant names and
  rooms, alert messages, TTS.
- Some legacy entities carry Dutch ids (`binary_sensor.voordeur_opening`,
  `media_player.werkkamer`). Leave them; renaming ripples through automations,
  the dashboard and the recorder database.

### Comments

Comments explain **why**, especially hardware quirks that are invisible in the
YAML and would otherwise be "cleaned up" by the next reader. Examples worth
imitating:

```yaml
# Live image: the Hub fetches it once the receiver is ready, so it is
# always current. Do not add a query string, that disables the URL
# signing of Home Assistant and the Hub gets a 401.
```

```yaml
# The SNZB-01P (Small Office Button) has no event entity in ZHA, it only
# fires zha_event. A short press sends 'toggle' (double press 'on', long 'off').
```

Wrap them at ~78 characters.

### Secrets

- Anything private goes through `!secret`: coordinates, URLs, database URL,
  tokens, chat ids, user ids, file paths under the media folder, entity
  pictures.
- `secrets.yaml`, `hass_sa.json` and `www/` are **not tracked** by git but
  **are** deployed. Never print their contents into a commit, a comment or a
  dashboard, and never introduce a literal token/coordinate into a tracked
  file.
- `.gitignore` is an allow-list (`/*` then `!…`). A new top-level file is
  invisible to git until it is explicitly un-ignored, so check `git status`
  after adding one.

### Dashboard (`ui-lovelace.yaml`)

One file, `mode: yaml`, so a change is live on reload without touching the UI
editor. Views have a `path:` that automations and cast scripts reference by
name (`dashboard`, `kids-dashboard`, `solar-energy`) — renaming a path breaks
`cast.show_lovelace_view` calls in `configuration/script/cast_*.yaml`. Prefer
`tile` cards with `features:` for controls and `entities` cards with `type:
divider` for grouped read-outs, matching what is already there.

### Custom components

Custom integrations are installed and updated through the built-in
Marketplace (formerly HACS) in Home Assistant itself, which writes them to
`/config/custom_components/` on the pod. They are **not** deployed from this
repo anymore: `deploy-kubernetes.sh` deliberately leaves `custom_components/`
out, so it can't overwrite the Marketplace-managed versions with stale copies.

Installed via the Marketplace: `gree` (RobHofmann/HomeAssistant-GreeClimateComponent),
`homewizard_climate` (dennis1804/homewizard-climate-hass), `nefiteasy`
(ksya/ha-nefiteasy). The local `custom_components/` and
`custom_components_sources/` directories are leftovers from the old
copy-and-upload workflow and are untracked in git.

## Workflows

**Validate.** There is no linter or CI in this repo. Validation is Home
Assistant itself: Developer Tools → YAML → *Check configuration*, or
`hass --script check_config` inside the pod. At minimum, confirm a file still
parses as YAML and that every `entity_id` you introduce actually exists (grep
the repo, or check Developer Tools → States) — a typo'd entity fails silently
at runtime.

**Deploy.** `./deploy-kubernetes.sh` — switches to the `raspberry01` context
and tars `configuration.yaml secrets.yaml hass_sa.json ui-lovelace.yaml www/
configuration/` into `/config` of the running pod. It does
not reload or restart anything; after it, reload the relevant domain
(automations/scripts/template) or restart Home Assistant. Running it pushes
live changes to a real house — **only run it when asked to.**

**Commit.** Short imperative English subject lines describing the behaviour
change, no prefixes or issue numbers: "Add button for turning on/off the small
office", "Fix race condition in doorbell snapshot on Nest Hub's", "Stop casting
dashboard when turned off". One logical change per commit. Only commit when
asked.

## Things to avoid

- Editing `.history/` or `.idea/` — editor artefacts, not configuration.
- Bulk reformatting or migrating legacy YAML syntax "while you are in there".
- Removing a comment that documents a hardware quirk or a race condition.
- Deleting an automation `id:` or renaming a script file without grepping for
  references.
- Inventing entity ids. If you cannot verify an entity exists, say so instead
  of guessing at a plausible name.
- Leaving commented-out YAML behind as a way of "keeping" a draft.
