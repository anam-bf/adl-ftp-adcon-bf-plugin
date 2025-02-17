from adl.core.registries import Plugin


class PluginNamePlugin(Plugin):
    type = "adl_ftp_adcon_bf_plugin"
    label = "adl-ftp-adcon-bf-plugin"

    def get_urls(self):
        return []

    def get_data(self):
        return []
