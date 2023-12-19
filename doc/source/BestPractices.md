# Best Practices

The following are best practices agreed upon by the team working on this
project to ease collaboration and diminish errors. Our best practices are
always open to discussion.

If you decide to not follow these practices, please ensure that your
contributions are indistinguishable from contributions created following
the practices. If there is a reason to diverge from the practices in
a specific case, please ensure you mention to the team in the appropriate
area (issue/pull request comment, email, others as appropriate).

## Coding Style

We will follow PEP-8 and use Flake8 for evaluation/enforcement.

## Tabs vs Spaces

Spaces win.

## Text Editors/IDEs

Feel free to use your favourite tools as long as they produce properly
encoded plain text files.

## Branch Naming

Branches will follow the naming scheme "type-number-summary". Ex:
feature-2-click_action.

The accepted types for now are:
- feature
- doc
- bugfix

Other types can be added as time goes on.

The summary should be a brief explanation of what the branch does, in one
to three words, separated by underscores.

## Merging

The main branch must never be pushed to. All changes must be performed in
a suitably name branch linked to an issue. When changes are ready to be
pushed to main, a pull request is created, reviewed, corrected as needed,
approved, and merged.

When approving merge requests, the reviewer must review changes, run
tests, and pass the code through flake8. Any problems can be returned to
the proposer of the change for rectification.

Currently, merge requests must be reviewed and approved by at least
1 person. As the team grows, the number of reviewers should be increased
as appropriate.
