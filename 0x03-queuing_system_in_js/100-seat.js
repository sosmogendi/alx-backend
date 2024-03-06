import express from 'express';
import kue from 'kue';
import redis from 'redis';
import { promisify } from 'util';

// Redis Client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Functions for Redis
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats) : 0;
}

// Initialize available seats to 50 and enable reservation
reserveSeat(50);
let reservationEnabled = true;

// Kue Queue
const queue = kue.createQueue();

// Express Server
const app = express();
const port = 1245;

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

// Routes
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: numberOfAvailableSeats.toString() });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', (result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    let currentAvailableSeats = await getCurrentAvailableSeats();

    if (currentAvailableSeats === 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    } else {
      currentAvailableSeats--;
      await reserveSeat(currentAvailableSeats);
      if (currentAvailableSeats >= 0) {
        done();
      } else {
        done(new Error('Not enough seats available'));
      }
    }
  });
});
