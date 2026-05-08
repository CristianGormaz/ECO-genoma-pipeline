#!/usr/bin/env bash
set -u

policy_doc="docs/architecture/eco-real-data-activation-rollback-policy.md"
policy_key="eco-real-data-activation-rollback-policy"
results_dir="results"
timestamp="$(date -u +"%Y%m%dT%H%M%SZ")"
out_file="${results_dir}/smoke-${policy_key}-${timestamp}.log"
mkdir -p "${results_dir}"

status="pass"
checks=(
  "Cambiar estado a bloqueado o needs_review."
  "Detener cualquier siguiente paso de ingestión, análisis real o automatización."
  "Requerir nueva revisión antes de cualquier reactivación."
)

{
  echo "timestamp=${timestamp}"
  echo "policy_doc=${policy_doc}"
  echo "smoke_test=${policy_key}"
  for check in "${checks[@]}"; do
    if rg -Fq "${check}" "${policy_doc}"; then
      echo "check=pass text=${check}"
    else
      echo "check=fail text=${check}"
      status="fail"
    fi
  done
  echo "status=${status}"
} > "${out_file}"

if [ "${status}" = "pass" ]; then
  echo "PASS ${out_file}"
  exit 0
fi

echo "FAIL ${out_file}"
exit 1
