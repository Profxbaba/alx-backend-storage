// Temporary script to change the address for testing
db.school.updateMany(
    { "name": "Holberton school" },
    { $set: { "address": "Old Address" } }
);
