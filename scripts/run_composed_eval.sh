#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scripts/run_composed_eval.sh <path-to-domain-skill-repo> <main|reference|regression> [scenario ...] [-- tessl eval run args...]

Runs a domain skill's hosted eval suite with BOTH the domain skill and java-functional-style as
the injected context. This is the composition check from docs/agents/ownership-boundaries.md:

  domain skill alone (published) <= domain skill + java-functional-style (with-context)

The domain repository is a checkout of java-streams-skill or java-optionals-skill. Its suite
directory (evals/, evals-reference/, evals-regression/) is passed to `tessl eval run` as the
scenarios source, and a temporary plugin that bundles both skills is passed as --context.

Only the with-context variant runs (--skip-baseline): the baseline for this check is the domain
skill's own published result, not a no-context run.

Examples:
  scripts/run_composed_eval.sh ../java-streams-skill main
  scripts/run_composed_eval.sh ../java-optionals-skill reference 02-lazy-upsert 26-review-eager-fallback-regression
  scripts/run_composed_eval.sh ../java-streams-skill main -- --label "composition check" --runs 2
USAGE
}

if [[ $# -lt 2 ]]; then
  usage >&2
  exit 2
fi

domain_repo="$(cd "$1" && pwd)"
suite="$2"
shift 2

case "$suite" in
  main) source_dir="evals" ;;
  reference) source_dir="evals-reference" ;;
  regression) source_dir="evals-regression" ;;
  -h|--help|help) usage; exit 0 ;;
  *) echo "Unknown suite: $suite" >&2; usage >&2; exit 2 ;;
esac

scenarios=()
extra_args=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --) shift; extra_args=("$@"); break ;;
    *) scenarios+=("$1"); shift ;;
  esac
done

if ! command -v tessl >/dev/null 2>&1; then
  echo "tessl CLI is required to run hosted evals." >&2
  exit 127
fi

repo_root="$(git rev-parse --show-toplevel)"
domain_manifest="$domain_repo/.tessl-plugin/plugin.json"
if [[ ! -f "$domain_manifest" ]]; then
  echo "Not a Tessl plugin checkout: $domain_repo" >&2
  exit 1
fi
domain_skill_dir="$(find "$domain_repo/skills" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
if [[ -z "$domain_skill_dir" ]]; then
  echo "No skill directory under $domain_repo/skills" >&2
  exit 1
fi
domain_skill="$(basename "$domain_skill_dir")"
suite_path="$domain_repo/$source_dir"
if [[ ! -d "$suite_path" ]]; then
  echo "Missing suite directory: $suite_path" >&2
  exit 1
fi

# Everything Tessl reads must sit inside this repository, because `tessl eval run` resolves the
# Tessl project from the scenarios path. The staging directory is gitignored.
tmp_dir="$(mktemp -d "$repo_root/.tessl-composition.XXXXXX")"
trap 'rm -rf "$tmp_dir"' EXIT

composed="$tmp_dir/composed-plugin"
mkdir -p "$composed/.tessl-plugin" "$composed/skills" "$composed/rules"
cp -a "$domain_skill_dir" "$composed/skills/$domain_skill"
cp -a "$repo_root/skills/java-functional-style" "$composed/skills/java-functional-style"
cp -a "$repo_root/rules/." "$composed/rules/"
cat > "$composed/.tessl-plugin/plugin.json" <<JSON
{
  "name": "martinfrancois/composition-check",
  "version": "0.0.0",
  "description": "Temporary composed context: $domain_skill plus java-functional-style. Never published.",
  "private": true
}
JSON

scenario_source="$tmp_dir/scenarios"
mkdir -p "$scenario_source"
if [[ "${#scenarios[@]}" -eq 0 ]]; then
  for scenario in "$suite_path"/*/; do
    cp -a "$scenario" "$scenario_source/"
  done
else
  for scenario in "${scenarios[@]}"; do
    if [[ ! -d "$suite_path/$scenario" ]]; then
      echo "Unknown $suite scenario in $domain_repo: $scenario" >&2
      exit 1
    fi
    cp -a "$suite_path/$scenario" "$scenario_source/"
  done
fi

echo "Composition check: $domain_skill + java-functional-style"
echo "Domain repo:   $domain_repo ($(git -C "$domain_repo" rev-parse --short HEAD))"
echo "Companion:     $(git -C "$repo_root" rev-parse --short HEAD)"
echo "Suite:         $suite ($source_dir)"
echo "Scenarios:"
find "$scenario_source" -mindepth 1 -maxdepth 1 -type d -printf '  %f\n' | sort
echo "Variant:       with-context only"

(
  cd "$repo_root"
  tessl eval run --context "$composed" --skip-baseline --force "${extra_args[@]}" "$scenario_source"
)
