# Release Process

The TASS tool is currently being developed and is at a pre-1.0 stage. The
processes surrounding the tool, including this one, will be changed and
adapted as the tool is developed. Documentation will be roughly kept in
step during the pre-1.0 stage, but will not be guaranteed to be up to date
until the 1.0 period.

## Repository

The TASS app will be released on its github repository under the
"[releases](https://github.com/StatCan/tass-ssat/releases)" section.
Further down the road, a build may be pushed to the relevant StatCan
official repository.

## Steps

In order to complete a release, the following steps must be completed.
1) A git issue called "Release X.Y.Z" must be created along with a branch
related to this issue.
2) The relevant commit in the branch will be tagged "vX.Y.Z-RC1".
3) All relevant tests will be run, with their pass/fail state documented
in the issue.
4) If any bugs are found, the team will decide whether or not they are
showstoppers. If they are, the release process is aborted. A new issue with 
the bugs is created, and linked to the release issue. Start bug squashing.
Repeat step 2 onwards and increment the number of RC.
5) Rename latest commit "vX.Y.Z-RC#" to "vX.Y.Z".
6) Go to "Releases", create a new release based on tag "vX.Y.Z".
7) Merge release branch to main, close release issue.
8) Announce as needed.

This release process requires at least two team members as the branch
merge requires a reviewer, as normal. Ideally, most or even all of the
team should be involved in, or at least aware of, the release.

### Post-Release Cleanup

After the release, everyone should take some time to cleanup any orphan
branches that are leftover, update all required issues, and tidy up the
repo.
