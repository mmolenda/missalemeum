## Problem
The workflow was failing because it tried to request a review from the PR author (mmolenda). GitHub's API doesn't allow this—you cannot request a review from yourself on a pull request you created.

Error: `Review cannot be requested from pull request author.`

## Solution
Removed the `reviewers` section from the `create-pull-request` action. The PR will still be created successfully without attempting to assign a self-review.

## Changes
- Removed lines 49-50 (`reviewers: mmolenda`) from `.github/workflows/update-divinum-officium-submodule.yml`