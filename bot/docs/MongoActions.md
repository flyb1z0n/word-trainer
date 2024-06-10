## Connect to mongo

```sh
docker exec -it bot-mongodb-1 mongosh wt_db
```

## Show all messages
```mongo
db.tg_messages.find()
```

## Show non mine messages
```mongo
db.tg_messages.find({ "from.username": { $ne: 'flyb1z0n' } })
```

