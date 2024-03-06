import redis from 'redis';

// Create Redis client
const client = redis.createClient();

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
  client.set(schoolName, value, (error, reply) => {
    if (error) {
      console.error(`Failed to set value for ${schoolName}: ${error.message}`);
    } else {
      console.log(`Successfully set value for ${schoolName}`);
    }
  });
}

// Function to display value for a school
function displaySchoolValue(schoolName) {
  client.get(schoolName, (error, reply) => {
    if (error) {
      console.error(`Failed to get value for ${schoolName}: ${error.message}`);
    } else {
      console.log(`Value for ${schoolName}: ${reply}`);
    }
  });
}

// Call functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
