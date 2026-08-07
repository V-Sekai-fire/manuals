---
title: "RFD 0061: Run services as systemd podman quadlets on Fedora 44 instead of Harvester HCI"
state: published
scope: deployment target for fabric runtime services
---

## Decision

Services run as systemd podman quadlets directly on Fedora 44 hosts,
not inside VMs on a Harvester HCI cluster. The superseded Harvester
plan wraps a full virtualization tier — hypervisor, VM lifecycle,
qcow2 pipeline — around the same podman quadlets that already drive
the workloads. Fedora 44 runs those quadlets under systemd without
that tier. Each service deploys as an OCI container image launched by
a quadlet `.container` unit, with `.network` and `.volume` units
alongside, copied into `~/.config/containers/systemd`. OpenTofu in the
`infra` repo provisions the Fedora 44 hosts and delivers the quadlet
units, in place of baking and booting qcow2 images. This decision
supersedes the earlier Harvester HCI record; Fly.io stays off the
table from that record, and Harvester HCI joins it.

## References

- Full drivers, considered options, consequences, and confirmation:
  `DETAILS.md`
- Original record:
  `decisions/20260613-quadlets-on-fedora-44-instead-of-harvester.md`
- Infra repo: [infra](https://github.com/v-sekai-multiplayer-fabric/infra)

## Related

- `rfd/0056-systemd-quadlet-verification-queue`: the verification
  smokes that already run as a quadlet queue on the same convention.
