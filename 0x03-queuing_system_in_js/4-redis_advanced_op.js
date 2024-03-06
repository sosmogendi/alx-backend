import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();

client.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
  storeHashValues();
});

async function storeHashValues() {
  const KEY = 'HolbertonSchools';
  const keys = ['Portland', 'Seattle', 'New York', 'Bogota', 'Cali', 'Paris'];
  const values = [50, 80, 20, 20, 40, 2];

  try {
    const hmsetAsync = promisify(client.hmset).bind(client);
    await hmsetAsync(KEY, keys.reduce((acc, key, index) => ({ ...acc, [key]: values[index] }), {}));
    const hgetallAsync = promisify(client.hgetall).bind(client);
    const hash = await hgetallAsync(KEY);
    console.log(hash);
  } catch (error) {
    console.error(`Failed to store or retrieve hash values: ${error.message}`);
  }
}
