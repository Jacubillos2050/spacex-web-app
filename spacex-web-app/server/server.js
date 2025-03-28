const express = require('express');
const AWS = require('aws-sdk');
const path = require('path');
const app = express();

// Configurar credenciales y región de AWS desde variables de entorno
AWS.config.update({
  region: process.env.AWS_REGION,
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
});

const dynamodb = new AWS.DynamoDB.DocumentClient();

// Servir archivos estáticos del frontend (React build)
app.use(express.static(path.join(__dirname, '../client/build')));

// Endpoint para obtener todos los lanzamientos
app.get('/api/launches', async (req, res) => {
  const params = {
    TableName: 'SpaceXLaunches'
  };
  try {
    const data = await dynamodb.scan(params).promise();
    res.json(data.Items);
  } catch (err) {
    console.error('Error al consultar DynamoDB:', err);
    res.status(500).json({ error: 'Error al obtener datos' });
  }
});

// Ruta catch-all para servir la app React
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../client/build/index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});