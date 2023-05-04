# Wagtail public roadmap

:sparkle: View the [official Wagtail public roadmap](https://wagtail.org/roadmap/). View full [historical data in GitHub Projects](https://github.com/orgs/wagtail/projects/16).

Our public roadmap is where you can learn about what features we're working on, what stage they're in, and when we expect to bring them to you. It also covers major community or project efforts that aren’t features.

We’re planning to iterate on the format of the roadmap itself, and we see potential to engage more in discussions about the future of Wagtail. If you have feedback about this roadmap repository itself, such as how the issues are presented, let us know through [GitHub Discussions for Wagtail](https://github.com/wagtail/wagtail/discussions).

## Guide to the roadmap

Every item on the roadmap is a GitHub issue, with [labels](https://github.com/wagtail/roadmap/labels) to indicate high-level areas of focus.

### What goes on the roadmap

Only items of significant interest to the community go onto the roadmap. This definition is purposefully vague at the moment, and should be reviewed on a regular basis.

Items only go onto the roadmap once they have been considered by the core team. These items might, or might not need an RFC for implementation details before they get on the roadmap.

### Roadmap lifecycle

The roadmap is arranged on a project board to give a sense for how far out each item is on the horizon. Every project or feature is added to a particular board column according to the release in which it is expected to be done. Items spanning multiple releases / long-term architecture changes can have a dedicated column. Items without any agreed delivery mechanism go into a "Future" column. This Future column acts as a way to attract contributions and/or sponsorship on items that align with our long-term plans.

Once an item is delivered we remove it from the board - the release notes act as the record of its delivery.

### Review process

RFCs can be used for roadmap additions, so core team members and the wider community can provide feedback easily. Using an RFC isn’t mandatory as long as additions still get duly reviewed by the core team.

The core team review should include:

- Making sure the level of detail is appropriate for the roadmap.
- Assessing whether the given addition is likely to require an RFC or not.
- Sharing the proposed additions on regular core team channels.
- Discussions at one or two core team meetings to find reviewers or discuss specific points.
- Approval by enough core team members to reach a consensus.

Feedback from the wider community is also welcome as part of roadmap additions.

#### Level of detail

Proposed roadmap items should provide enough details to fill in the relevant sections of this proposed roadmap item template:

```markdown
## Summary

A short overview of the proposed work. One paragraph, tweet-sized.

## Intended Outcome

A short paragraph or list of 2-5 items detailing what will be the result of this work.

## More information

If relevant – a list of 1-3 links to related issues, pull requests, RFCs, or other documentation.
```

Usage of the template as-is isn’t mandatory. For example, if an item is already tracked by a given issue / pull request / or RFC with sufficient details – that can be used as-is.

#### Review timeline

It helps with planning of a release if roadmap items are reviewed ahead of development starting for said release. Our process should fit between a major/minor release’s first release candidate (RC) and the final release (as defined by our [release schedule](https://github.com/wagtail/wagtail/wiki/release-schedule)).

For example, if Wagtail 4.2’s first RC is released on Friday 20th Jan, and its final release is on Monday 6th Feb, roadmap additions can be reviewed for two weeks between Monday 23rd Jan and Monday 6th Feb, including potential discussions at two core team meetings. This means the RFC will spend 3 days in its "Review" stage and 10 days in "Final Comment Period".

To keep the review process fast, we recommend to:

- Avoid making more additions to a list of roadmap items proposed as an RFC after the initial RFC submissions.
- Remove proposed roadmap items which prove too complex to review with this process. They can be reviewed separately as appropriate.

### Managing the roadmap

For maintainers, here is guidance on how to manage our roadmap data:

- Always update the [wagtail.org Roadmap page](https://wagtail.org/roadmap/) after making changes in GitHub, so it reflects the latest data.
- Always use issues on the `roadmap` repository as roadmap entries. This makes for a more consistent experience for everyone (same labels, comments all in the same repository, etc.)
- Make sure all roadmap entries set a Milestone, project Status, and Start date. The milestone is used for the wagtail.org page, status for the GitHub Projects Kanban, start date for the GitHub Projects timeline / "roadmap" view.
