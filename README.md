The netdb project. Requires mongodb and flask.

Required indices:

```
db.device.createIndex({"id": 1}, { unique: true })
db.igp.createIndex({"set_id":1,"category": 1}, {unique: true})
db.interface.createIndex({"set_id": 1, "category": 1, "element_id": 1}, {unique: true})
db.firewall.createIndex({"set_id": 1, "category": 1, "family": 1, "element_id": 1}, {unique: true})
db.bgp.createIndex({"set_id": 1, "category": 1, "family": 1, "element_id": 1}, {unique: true})
db.policy.createIndex({"set_id": 1, "category": 1, "family": 1, "element_id": 1}, {unique: true})
```
