import kue from 'kue';

const queue = kue.createQueue();
const jobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account',
};

const queueName = 'push_notification_code';

const job = queue.create(queueName, jobData).save((err) => {
  if (err) {
    console.error('Notification job failed:', err);
    return;
  }
  console.log(`Notification job created: ${job.id}`);
});

job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', () => {
  console.error('Notification job failed');
});
