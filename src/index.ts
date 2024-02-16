import { Request, Response } from "express";

const express = require('express');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const port = process.env.PORT;


app.get('/',(request:Request,response:Response) => {
  response.send('Hello From GitShade');
})

app.listen(port, () => {
  console.log(`[server]: Server is running at http://localhost:${port}`);
});