import redis from 'redis';
import { promisify } from 'util';

// Create Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

// Function to handle connection errors
client.on('error', (error) => {
  console.error(`Redis client error: ${error.message}`);
});

// Function to handle successful connection
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Function to set value for a new school
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Function to display value for a school
async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(`Value for ${schoolName}: ${value}`);
  } catch (error) {
    console.error(`Failed to get value for ${schoolName}: ${error.message}`);
  }
}

// Call functions
(async () => {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
})();
