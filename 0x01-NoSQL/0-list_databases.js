// my comment

const { MongoClient } = require('mongodb');

async function main() {
    const uri = 'mongodb://localhost:27017';
    const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });

    try {
        await client.connect();
        const adminDb = client.db('admin').admin();

        const databasesList = await adminDb.listDatabases();

        console.log("MongoDB server version:", await adminDb.serverStatus().then(({version}) => version));
        console 2024
