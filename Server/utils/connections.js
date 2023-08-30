const path = require('path');
const dotenv = require("dotenv");
const { Pool } = require("pg");

const envFilePath = path.join(__dirname, '../../envs/.node_env');

dotenv.config({path:envFilePath})

console.log('PD DATA',process.env.PGUSER,process.env.PGHOST,process.env.PGDATABASE,process.env.PGPASSWORD, process.env.PGPORT);
 
const connectDb = async () => {
    try {
        const pool = new Pool({
            user: process.env.PGUSER,
            host: process.env.PGHOST,
            database: process.env.PGDATABASE,
            password: process.env.PGPASSWORD,
            port: process.env.PGPORT,
        });
 
        await pool.connect()
        const res = await pool.query('SELECT * FROM chat_room')
        console.log(res)
        await pool.end()
    } catch (error) {
        console.log(error)
    }
}
 
module.exports = { connectDb };