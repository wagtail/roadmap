# Wagtail public roadmap

:sparkle: View the [official Wagtail public roadmap](https://wagtail.org/roadmap/).

---

Our public roadmap is where you can learn about what features we're working on, what stage they're in, and when we expect to bring them to you. It also covers major community or project efforts that aren’t features.

## What goes on the roadmap

Only items of significant interest to the community go onto the roadmap. Inclusion is based on judgement by the core team rather than a fixed checklist. These items might, or might not need an [RFC](https://github.com/wagtail/rfcs) for implementation details before they get on the roadmap.

### Roadmap reports

Every item on the roadmap is a GitHub issue, with [labels](https://github.com/wagtail/roadmap/labels) to indicate high-level areas of focus. Some of the labels have special meanings:

- [needs contributions](https://github.com/wagtail/roadmap/issues?q=sort%3Aupdated-desc+is%3Aopen+label%3A%22needs+contributions%22): there is a particular dependency on more contributors getting involved.
- [needs sponsorship](https://github.com/wagtail/roadmap/issues?q=sort%3Aupdated-desc+is%3Aopen+label%3A%22needs+sponsorship%22): this item is dependent on a [feature sponsorship](https://wagtail.org/sponsor/)
- [sponsored](https://github.com/wagtail/roadmap/issues?q=sort%3Aupdated-desc+is%3Aopen+label%3Asponsored): this item is going ahead thanks to a feature sponsor (thank you!)

We also have reports in GitHub Projects:

- [Roadmap items per release](https://github.com/orgs/wagtail/projects/16/insights/1)
- [Sponsored features per release](https://github.com/orgs/wagtail/projects/16/insights/3)

View [full data in GitHub Projects](https://github.com/orgs/wagtail/projects/16) to see previous roadmap items.

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
- Approval by enough core team members.

Feedback from the wider community is also welcome as part of roadmap additions.

For roadmap updates in bulk, use the [roadmap-specific RFC template](rfc-template.md). For context, see [past roadmap-focused RFCs](https://github.com/wagtail/rfcs/pulls?q=is%3Apr+label%3Aroadmap) and the [Wagtail release schedule](https://github.com/wagtail/wagtail/wiki/Release-schedule).

#### Level of detail

Roadmap items should have titles accessible to stakeholders without technical expertise a lot of context on how Wagtail works.

Proposed roadmap items should provide enough details to fill in the relevant sections of our [roadmap item template](item-template.md).

Usage of the template is encouraged but isn’t mandatory. For example, if an item is already tracked by a given issue / pull request / or RFC with sufficient details – that can be used as-is.

#### Review timeline

It helps with planning of a release if roadmap items are reviewed ahead of development starting for said release. Our process should fit between a major/minor release’s first release candidate (RC) and the final release (as defined by our [release schedule](https://github.com/wagtail/wagtail/wiki/release-schedule)).

For example, if Wagtail 4.2’s first RC is released on Friday 20th Jan, and its final release is on Monday 6th Feb, roadmap additions can be reviewed for two weeks between Monday 23rd Jan and Monday 6th Feb, including potential discussions at two core team meetings. This means the RFC will spend 3 days in its "Review" stage and 10 days in "Final Comment Period".

To keep the review process fast, we recommend to:

- Avoid making more additions to a list of roadmap items proposed as an RFC after the initial RFC submissions.
- Remove proposed roadmap items which prove too complex to review with this process. They can be reviewed separately as appropriate.

### Managing the roadmap

We’re planning to iterate on the format of the roadmap itself, and we see potential to engage more in discussions about the future of Wagtail. If you have feedback about this roadmap repository itself, such as how the issues are presented, let us know through [GitHub Discussions for Wagtail](https://github.com/wagtail/wagtail/discussions).

For maintainers, here is guidance on how to manage our roadmap data:

- Use [this secret issue creation link](https://github.com/wagtail/roadmap/issues/new/choose?template=blank) to add new items. Issue creation is enabled but configured to direct users to other channels.
- Always update the [wagtail.org Roadmap page](https://wagtail.org/roadmap/) after making changes in GitHub, so it reflects the latest data.
- Always use issues on the `roadmap` repository as roadmap entries. This makes for a more consistent experience for everyone (same labels, comments all in the same repository, etc.)
- Make sure all roadmap entries set all metadata defined in [roadmap item template](item-template.md), and a Start Date. The milestone is used for the wagtail.org page, status for the GitHub Projects Kanban, start date for the GitHub Projects timeline / "roadmap" view.
- In comments, encourage brevity, questions and feedback on the roadmap items, progress updates. Extended discussions and offers to contribute are best kept to GitHub Discussions or other appropriate channels.
