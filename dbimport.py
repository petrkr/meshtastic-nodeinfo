#!/usr/bin/env python3

from peewee import *
import json

db = SqliteDatabase('nodes.db')

infojson = open('info.json')
json_data = json.load(infojson)

class BaseModel(Model):
    class Meta:
        database = db

class Node(BaseModel):
    id = CharField(primary_key=True)
    num = IntegerField(null=True)
    snr = FloatField(null=True)
    hopsAway = IntegerField()
    lastHeard = IntegerField(null=True)

class User(BaseModel):
    node_id = ForeignKeyField(Node, backref='user', primary_key=True)
    id = CharField()
    longName = CharField()
    shortName = CharField()
    macaddr = CharField(null=True)
    hwModel = CharField()
    role = CharField(null=True)

class Position(BaseModel):
    node_id = ForeignKeyField(Node, backref='position', primary_key=True)
    altitude = IntegerField(null=True)
    time = IntegerField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)

class DeviceMetrics(BaseModel):
    node_id = ForeignKeyField(Node, backref='devicemetrics', primary_key=True)
    batteryLevel = IntegerField(null=True)
    channelUtilization = FloatField(null=True)
    airUtilTx = FloatField()
    uptimeSeconds = IntegerField(null=True)

class Metadata(BaseModel):
    owner = CharField()
    firmwareVersion = CharField()
    deviceStateVersion = IntegerField()
    canShutdown = BooleanField()
    hasWifi = BooleanField()
    hasBluetooth = BooleanField()
    positionFlags = IntegerField()
    hwModel = CharField()
    hasEthernet = BooleanField()
    role = CharField()
    hasRemoteHardware = BooleanField()


def insert_or_update_metadata(owner, metadata):
    data = metadata
    data["owner"] = owner

    metadata, created = Metadata.get_or_create(owner=data["owner"],
                                               defaults=data)
    if not created:
        for attr, val in data.items():
            setattr(metadata, attr, val)
        metadata.save()


def insert_or_update_node_data(data):
    for key, value in data.items():
        print(f"Processing node {key}")
        user_data = value["user"]
        position_data = value["position"] if "position" in value else None
        device_metrics_data = value["deviceMetrics"] if "deviceMetrics" in value else None
        if "role" not in user_data:
            user_data["role"] = "CLIENT"

        node, created = Node.get_or_create(
            id=key, num=value["num"],
            defaults={"lastHeard": value["lastHeard"] if "lastHeard" in value else None,
                      "snr": value["snr"] if "snr" in value else None,
                      "hopsAway": value["hopsAway"] if "hopsAway" in value else None})
        if not created:
            setattr(node, "lastHeard", value["lastHeard"] if "lastHeard" in value else None)
            setattr(node, "snr", value["snr"] if "snr" in value else None)
            setattr(node, "hopsAway", value["hopsAway"] if "hopsAway" in value else None)
            node.save()

        user, created = User.get_or_create(id=user_data["id"],
                                           node_id=node,
                                           defaults=user_data)
        if not created:
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        if position_data:
            position, created = Position.get_or_create(node_id=node,
                                                    defaults=position_data)
            if not created:
                for attr, val in position_data.items():
                    setattr(position, attr, val)
                position.save()


        if device_metrics_data:
            devMetrics, created = DeviceMetrics.get_or_create(node_id=node,
                                                            defaults=device_metrics_data)
            if not created:
                for attr, val in device_metrics_data.items():
                    setattr(devMetrics, attr, val)
                devMetrics.save()

def main():
    db.connect()
    db.create_tables([Node, User, Position, DeviceMetrics, Metadata])

    insert_or_update_metadata(json_data['owner'], json_data['metadata'])
    insert_or_update_node_data(json_data['nodes'])

    db.close()

if __name__ == '__main__':
    main()
