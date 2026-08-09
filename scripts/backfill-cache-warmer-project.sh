#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"

project_owner="${PROJECT_OWNER:-ORESoftware}"
project_number="${PROJECT_NUMBER:-1}"
project_status="${PROJECT_STATUS:-Backlog}"

if (($# == 0)); then
  set -- \
    "https://github.com/ORESoftware/.github/issues/1" \
    "https://github.com/ORESoftware/k8s-cluster/issues/961"
fi

project_query='query($login:String!,$number:Int!){user(login:$login){projectV2(number:$number){id title fields(first:100){nodes{... on ProjectV2SingleSelectField{id name options{id name}}}}}}}'
project_json="$(gh api graphql -f query="$project_query" -F login="$project_owner" -F number="$project_number")"
project_id="$(jq -er '.data.user.projectV2.id' <<<"$project_json")"
project_title="$(jq -er '.data.user.projectV2.title' <<<"$project_json")"
status_field_id="$(jq -er --arg field Status '.data.user.projectV2.fields.nodes[] | select(.name == $field) | .id' <<<"$project_json")"
status_option_id="$(jq -er --arg status "$project_status" '.data.user.projectV2.fields.nodes[] | select(.name == "Status") | .options[] | select(.name == $status) | .id' <<<"$project_json")"

printf 'Project: %s #%s (%s)\n' "$project_owner" "$project_number" "$project_title"

for issue_url in "$@"; do
  if [[ ! "$issue_url" =~ ^https://github\.com/([^/]+)/([^/]+)/issues/([0-9]+)$ ]]; then
    printf 'Unsupported issue URL: %s\n' "$issue_url" >&2
    exit 2
  fi

  repo="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
  issue_number="${BASH_REMATCH[3]}"
  content_id="$(gh api "repos/${repo}/issues/${issue_number}" --jq .node_id)"

  existing_query='query($content:ID!){node(id:$content){... on Issue{projectItems(first:100){nodes{id project{id}}}}}}'
  existing_json="$(gh api graphql -f query="$existing_query" -F content="$content_id")"
  item_id="$(jq -r --arg project "$project_id" '.data.node.projectItems.nodes[] | select(.project.id == $project) | .id' <<<"$existing_json" | head -n1)"

  if [[ -z "$item_id" ]]; then
    add_mutation='mutation($project:ID!,$content:ID!){addProjectV2ItemById(input:{projectId:$project,contentId:$content}){item{id}}}'
    item_id="$(gh api graphql -f query="$add_mutation" -F project="$project_id" -F content="$content_id" --jq '.data.addProjectV2ItemById.item.id')"
    printf 'Added %s\n' "$issue_url"
  else
    printf 'Already present: %s\n' "$issue_url"
  fi

  status_mutation='mutation($project:ID!,$item:ID!,$field:ID!,$option:String!){updateProjectV2ItemFieldValue(input:{projectId:$project,itemId:$item,fieldId:$field,value:{singleSelectOptionId:$option}}){projectV2Item{id}}}'
  gh api graphql -f query="$status_mutation" -F project="$project_id" -F item="$item_id" -F field="$status_field_id" -F option="$status_option_id" >/dev/null
  printf 'Set %s -> %s\n' "$issue_url" "$project_status"
done
