import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

// Utils ====================================================

const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

// Function to get an item by ID
function getItemById(id) {
  return listProducts.find((item) => item.itemId === id);
}

// Redis ====================================================

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

client.on('error', (error) => {
  console.log(`Redis client error: ${error.message}`);
});

// Function to reserve stock by item ID
function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock);
}

// Function to get current reserved stock by item ID
async function getCurrentReservedStockById(itemId) {
  try {
    const stock = await getAsync(`item.${itemId}`);
    return stock ? parseInt(stock) : null;
  } catch (error) {
    console.log(`Error retrieving stock for item ${itemId}: ${error.message}`);
    throw error;
  }
}

// Express ==================================================

const app = express();
const port = 1245;

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

// Routes ===================================================

const notFound = { status: 'Product not found' };
const noStock = { status: 'Not enough stock available' };

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json(notFound);
    return;
  }

  try {
    const currentStock = await getCurrentReservedStockById(itemId);
    const stock = currentStock !== null ? currentStock : item.initialAvailableQuantity;
    item.currentQuantity = stock;
    res.json(item);
  } catch (error) {
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = Number(req.params.itemId);
  const item = getItemById(itemId);

  if (!item) {
    res.json(notFound);
    return;
  }

  let currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock === null) currentStock = item.initialAvailableQuantity;

  if (currentStock <= 0) {
    res.json(noStock);
    return;
  }

  reserveStockById(itemId, currentStock - 1);
  res.json({ status: 'Reservation confirmed', itemId });
});
