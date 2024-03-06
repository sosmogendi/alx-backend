import redis from 'redis';
import { promisify } from 'util';

// Create Redis client
const subscriber = redis.createClient();

// Promisify the subscriber methods
const subscribeAsync = promisify(subscriber.subscribe).bind(subscriber);
const unsubscribeAsync = promisify(subscriber.unsubscribe).bind(subscriber);
const quitAsync = promisify(subscriber.quit).bind(subscriber);

// Function to handle connection errors
subscriber.on('error', (error) => {
  console.error(`Redis client not connected to the server: ${error.message}`);
});

// Function to handle successful connection
subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
  startSubscription();
});

async function startSubscription() {
  const CHANNEL = 'holberton school channel';

  try {
    await subscribeAsync(CHANNEL);
    subscriber.on('message', async (channel, message) => {
      if (channel === CHANNEL) console.log(message);
      if (message === 'KILL_SERVER') {
        await unsubscribeAsync(CHANNEL);
        await quitAsync();
      }
    });
  } catch (error) {
    console.error(`Failed to subscribe: ${error.message}`);
    await quitAsync();
  }
}
