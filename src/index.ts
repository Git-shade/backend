// imports
import express from 'express';
import dotenv from 'dotenv';
import { methodNotAllowedErrorHandler } from "./middlewares/errors";

// controllers
import clone from './controllers/clone';

// initializers
dotenv.config();

const app = express();
const router = express.Router();
const port = process.env.PORT || 3001;

// routes
app.get('/', clone, router.all('/',methodNotAllowedErrorHandler))

// starting server
app.listen(port, () => {
  console.log(`[server]: Server is running at http://localhost:${port}`);
});