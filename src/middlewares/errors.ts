import { NextFunction, Request, RequestHandler, Response } from 'express';

export const methodNotAllowedErrorHandler: RequestHandler = (req: Request, res: Response, next: NextFunction) => {
    return res.status(405).json({ errors: [{ code: 405, msg: 'Method not allowed' }] });
};