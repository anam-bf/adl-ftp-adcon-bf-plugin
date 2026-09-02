# ADL ADCON FTP Burkina Faso Plugin

A **decoder plugin** for the [ADL FTP Plugin](https://github.com/wmo-raf/adl-ftp-plugin):
lets an ADL FTP/SFTP connection decode the daily, tab-separated observation
export files the ADCON addVANTAGE server of Burkina Faso's ANAM pushes to an
FTP server. It adds the *ADCON FTP Burkina Faso* entry to the FTP connection's
Decoder list and nothing else — hosts, credentials and station links are the
FTP plugin's.

**Operator guide:** [docs/guide.md](docs/guide.md) — the file format, how to
configure the FTP connection and station links for it, collection behaviour,
diagnostics, troubleshooting and the current **compatibility status** (read
it: this release does not work with FTP plugin 0.2.0 or later). The guide is
also published on the central ADL documentation site.

## Development setup

The plugin runs inside the ADL core image, which must already contain the
ADL FTP Plugin. Build the `adl:latest` image from the
[ADL core repository](https://github.com/wmo-raf/adl) with the FTP plugin in
its `plugins.toml`, then:

```bash
git clone https://github.com/anam-bf/adl-ftp-adcon-bf-plugin.git
cd adl-ftp-adcon-bf-plugin
cp .env.sample .env        # set PLUGIN_BUILD_UID=$(id -u), PLUGIN_BUILD_GID=$(id -g), ADL_DB_PASSWORD
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up
docker compose -f docker-compose.dev.yml exec adl adl createsuperuser
```

The admin is served by the bundled nginx proxy on `ADL_WEB_PROXY_PORT`
(default 80). The plugin source is bind-mounted, so code changes reload the
dev server. If the build fails with `pull access denied` for `adl:latest`,
prefix the build with `DOCKER_BUILDKIT=0`.

See [CONTRIBUTING.md](CONTRIBUTING.md) — a change to the decoder's file
format or to any admin surface must update the guide in the same PR.
