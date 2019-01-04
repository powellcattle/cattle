import mongoengine


def global_init():
    mongoengine.register_connection(alias="core", name="cattle", host="192.168.1.130")
