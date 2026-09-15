# Native clone and fork pipeline validation

Validated on 15 September 2026. This is a diagnostic POC, not a production secret-handling example.

## Configuration

- Upstream: `ansibleautomates/oss-native-clone-lab`.
- Contributor: `Ompragash/oss-native-clone-lab`, branch `contributor/change-code-and-yaml`.
- [PR 1](https://github.com/ansibleautomates/oss-native-clone-lab/pull/1) targets upstream `main`.
- Remote Unified pipeline: `oss_native_clone`, file `.harness/pipeline.yaml`. The file omits pipeline name and identifier; these are supplied when registering it in Harness.
- PR trigger: `oss_native_clone_pr`, `pipelineBranchName: main`, opened/synchronize/reopened events, target branch `main`.
- Trigger passes the PR number as `inputs.code_ref` with type `pull-request`, and the webhook head SHA as `inputs.expected_head`.
- Native clone enabled, merge strategy, credential persistence and submodules disabled, cache disabled. No manual checkout script.
- Upstream definition/code revision during these tests: `d386af84046ea1f6194c51ea6f0bb90b705f91e9`.

## Completed tests

| Test | Observed result | Execution |
| --- | --- | --- |
| Fork changes code and replaces the pipeline marker command with `exit 77` | Success. Native clone fetched PR 1 head `b6c34b8bb02bc4ed68e1ea4105382c14dce86aef`. Application marker was `FORK_CODE_V1`; two tests passed. Executed command remained `UPSTREAM_MAIN_PLAN_EXECUTED`. | [PR opened run](https://unifiedpipeline.harness.io/ng/account/MGY3MmJmM2ItNTY5Ny00Yj/all/orgs/default/projects/chef_oss_pov/pipelines/oss_native_clone/deployments/RLg2BA5wQSa7uG3af1o0Sg/pipeline) |
| Fork updates code and replaces its YAML with an unterminated `pipeline: [` | Success. Native clone fetched new PR head `9e99f1246b45ac862b61b5150918c9f4f552ef68`. Application marker was `FORK_CODE_V2`; two tests passed. Executed command remained `UPSTREAM_MAIN_PLAN_EXECUTED`. | [PR synchronize run](https://unifiedpipeline.harness.io/ng/account/MGY3MmJmM2ItNTY5Ny00Yj/all/orgs/default/projects/chef_oss_pov/pipelines/oss_native_clone/deployments/VjF3G2b8RT68dIOqENTjMw/pipeline) |
| Manual baseline, definition and code from main | Success. `UPSTREAM_MAIN_PLAN_EXECUTED`, `UPSTREAM_CODE`, one test passed. | [Baseline](https://unifiedpipeline.harness.io/ng/account/MGY3MmJmM2ItNTY5Ny00Yj/all/orgs/default/projects/chef_oss_pov/pipelines/oss_native_clone/deployments/BKDmDdb_TVukPuHKoGTKDQ/pipeline) |
| Manual selection of definition-control branch, code still from main | Success. `UPSTREAM_ALTERNATE_PLAN_EXECUTED`, `UPSTREAM_CODE`, one test passed. Execution metadata records definition branch `definition-control`. | [Alternate definition](https://unifiedpipeline.harness.io/ng/account/MGY3MmJmM2ItNTY5Ny00Yj/all/orgs/default/projects/chef_oss_pov/pipelines/oss_native_clone/deployments/yr6XqLxYSkq3wKrncmXHiA/pipeline) |

The first two runs came from real signed GitHub webhook events. The last two were manual MCP controls. Both PR clone logs show `git fetch origin refs/pull/1/head` followed by a merge of the expected contributor SHA. These merges fast-forwarded because the tested upstream base was an ancestor of each head.

## Secret result

The trusted upstream definition deliberately supplies a synthetic canary through a Harness secret expression. Contributor-controlled application code reported `canary_readable_by_contributor_code: true` in both PR runs. Only booleans were logged, never the secret value. This proves that trusted pipeline sourcing does not automatically withhold a secret explicitly supplied to fork code.

## Interpretation and limits

The configured trigger uses upstream main for the execution plan while native cloning includes the PR changes. The fork YAML is checked out as a file, but is not parsed as the plan. This is not a universal rule that every Unified execution always uses main; the alternate-branch control demonstrates that selection matters.

The `cloned_yaml_contains_fork_override` diagnostic is not reliable evidence on its own: its search string also appears inside the upstream inspection script. The conclusions above instead use the exact checked-out SHAs, clone logs, Git file contents at those SHAs, application markers and executed commands. The invalid YAML control provides an additional check.

Two initial manual attempts failed before cloning because the MCP run input serialized an object as a branch name. They are excluded from the four completed controls: `oLZWg6yrTOGRAFeAwSXmtA` and `WFNUBXafTwalWkTHn1tIgA`. Retrying manual controls with scalar `code_ref: main` succeeded. The PR trigger's structured PR input worked without that correction.

This test does not validate runner credential isolation, approvals, OPA enforcement, public log access, independent contributor Harness accounts, or runtime license protection. Do not use real confidential secrets in this diagnostic pipeline. The earlier isolated-worker POC addresses protected downloads separately.

Publishing this report advances main after the tested revisions. The execution links and SHAs above describe the historical test inputs.
